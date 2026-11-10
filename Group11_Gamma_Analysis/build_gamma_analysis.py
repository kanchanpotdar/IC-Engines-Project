"""Group 11 Chemkin NASA-7 mixture Cp, Cv, gamma post-processing.
Run: python build_gamma_analysis.py
Requires: Python standard library and matplotlib. Does not modify source XLSM.
"""
import csv, math, re, zipfile, io, contextlib, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path('/mnt/data'); OUT=BASE/'Group11_Gamma_Analysis';OUT.mkdir(exist_ok=True)
THERMOZIP=BASE/'Isooctane_nHeptane_Ethanol_Methanol(1).zip'
XLSM=BASE/'Book1(1).xlsm'
R=8.31446261815324 # J mol-1 K-1
with zipfile.ZipFile(THERMOZIP) as z:
    therm=z.read('Isooctane_nHeptane_Ethanol_Methanol/therm.dat').decode('latin1').splitlines()

def floats15(line):
    # Chemkin NASA-7 coefficients use five 15-character fields per line, 4 lines/species
    return [float(line[i:i+15].strip().replace('D','E')) for i in range(0,75,15) if line[i:i+15].strip()]

species={};invalid=[]
i=2
while i<len(therm):
    if therm[i].strip().upper()=='END':break
    if not therm[i].strip():i+=1;continue
    if i+3>=len(therm):break
    head=therm[i]; name=head[:18].strip().split()[0].lower()
    try:
        tmin=float(head[45:55]); tmax=float(head[55:65]); tmid=float(head[65:75]);
        a=floats15(therm[i+1])+floats15(therm[i+2])+floats15(therm[i+3]);
        if len(a)!=14:raise ValueError(f'expected 14 NASA coefficients, got {len(a)}')
        species[name]={'tmin':tmin,'tmax':tmax,'tmid':tmid,'high':a[:7],'low':a[7:]}
    except Exception as e:invalid.append((name,str(e)))
    i+=4

def cp_species(sp,T):
    dat=species[sp]; a=dat['low'] if T<=dat['tmid'] else dat['high']
    return R*(a[0]+a[1]*T+a[2]*T*T+a[3]*T**3+a[4]*T**4)

# Use existing standard-library XLSM extraction, without invoking its analysis at import
script=(BASE/'group11_analysis.py').read_text()
start=script.index('def read_sheet_from_xlsm(')
end=script.index('\ndef save_csv(',start)
namespace={'Path':Path,'ZipFile':zipfile.ZipFile,'ET':__import__('xml.etree.ElementTree',fromlist=['ElementTree']),
'MAIN':'{http://schemas.openxmlformats.org/spreadsheetml/2006/main}',
'OD':'{http://schemas.openxmlformats.org/officeDocument/2006/relationships}',
'PK':'{http://schemas.openxmlformats.org/package/2006/relationships}'}
exec(script[start:end],namespace)
read=namespace['read_sheet_from_xlsm']

def write_csv(p,data,cols):
    with open(p,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(data)

infile=BASE/'Group11_Python_Analysis/group11_150_cases.csv'
with infile.open(newline='') as f: study=list(csv.DictReader(f))
runs={int(x['run']):x for x in study}
# Workbook has baseline + 150 sweeps, Run#2 ... #151
book_sheets={}
with zipfile.ZipFile(XLSM) as z:
    from xml.etree import ElementTree as ET
    root=ET.fromstring(z.read('xl/workbook.xml'));nm='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    for el in root.findall('.//'+nm+'sheet'):
        found=re.search(r'Run#(\d+)$',el.get('name',''))
        if found and 'soln_no_1_' in el.get('name',''):book_sheets[int(found.group(1))]=el.get('name')

sample=[];records=[];quality=[];minT=1e8;maxT=0
all_comp=set();seen_thermo=set();missing_seen=set()
for run in sorted(runs):
    if run not in book_sheets:
        quality.append({'run':run,'issue':'missing run sheet'});continue
    d=read(XLSM,book_sheets[run]);hdr=d[0]
    for zone in ['Unburned_Zone','Burned_Zone','Zone_Avg']:
        tx=next((j for j,k in enumerate(hdr) if isinstance(k,str) and k.strip().startswith('Temperature_'+zone+'_')),None)
        cx=next((j for j,k in enumerate(hdr) if isinstance(k,str) and k.strip().startswith('Crank_rotation_angle_'+zone+'_')),None)
        # Zone average crank angle may use an alternative name
        if cx is None:cx=next((j for j,k in enumerate(hdr) if isinstance(k,str) and 'Crank_rotation_angle' in k and ('_Zone_Avg_' in k or zone=='Zone_Avg')),None)
        inds=[]
        for j,k in enumerate(hdr):
            if not isinstance(k,str):continue
            m=re.match(r'\s*Mole_fraction_(.+?)_'+re.escape(zone)+r'_Run#',k)
            if m:inds.append((j,m.group(1).lower()))
        if tx is None or not inds:quality.append({'run':run,'issue':f'missing temperature/species for {zone}'});continue
        for row_idx,row in enumerate(d[1:],start=2):
            try:
                T=float(row[tx]);
                if not math.isfinite(T) or T<=0:continue
                ca=float(row[cx]) if cx is not None and cx<len(row) and isinstance(row[cx],(float,int)) else None
                comp={sp:float(row[j]) for j,sp in inds if j<len(row) and isinstance(row[j],(float,int)) and float(row[j])>0}
            except (ValueError,IndexError,TypeError):continue
            total=sum(comp.values())
            if total<0.98 or total>1.02:
                quality.append({'run':run,'issue':f'{zone} row {row_idx}: mole fraction sum {total:.5g}'});continue
            missing=[sp for sp,v in comp.items() if sp not in species]
            if missing:
                missing_seen.update(missing);quality.append({'run':run,'issue':f'{zone} row {row_idx}: thermo missing {missing}'});continue
            # If any species is outside NASA temperature fit, preserve provenance and flag it
            invalid_range=[sp for sp,v in comp.items() if T<species[sp]['tmin'] or T>species[sp]['tmax']]
            if invalid_range:
                quality.append({'run':run,'issue':f'{zone} row {row_idx}: T={T:g} K outside thermodynamic range for {invalid_range[:4]}'});continue
            cp=sum(v*cp_species(sp,T) for sp,v in comp.items())/total
            cv=cp-R
            if cv<=0 or not math.isfinite(cv):quality.append({'run':run,'issue':f'{zone} row {row_idx}: non-positive Cv'});continue
            record={'run':run,'zone':zone,'point_index':row_idx-1,'crank_angle_deg':ca,'temperature_K':T,'mole_fraction_sum':total,
                    'Cp_J_per_mol_K':cp,'Cv_J_per_mol_K':cv,'gamma':cp/cv}
            records.append(record)
            minT=min(minT,T);maxT=max(maxT,T)
            all_comp.update(comp);seen_thermo.update(comp)

cols=list(records[0]) if records else []
write_csv(OUT/'gamma_all_states.csv',records,cols)
summary=[]
for run in sorted(runs):
    base=runs[run]
    item={'run':run,'rpm':float(base['rpm']),'start_angle_deg':float(base['start_angle_deg']), 'burn_duration_deg':float(base['burn_duration_deg'])}
    for zone in ['Unburned_Zone','Burned_Zone','Zone_Avg']:
        arr=[r for r in records if r['run']==run and r['zone']==zone]
        item[zone+'_n_states']=len(arr)
        item[zone+'_initial_gamma']=arr[0]['gamma'] if arr else None
        item[zone+'_final_gamma']=arr[-1]['gamma'] if arr else None
        item[zone+'_initial_T_K']=arr[0]['temperature_K'] if arr else None
        item[zone+'_final_T_K']=arr[-1]['temperature_K'] if arr else None
        item[zone+'_min_gamma']=min((r['gamma'] for r in arr),default=None)
        item[zone+'_max_gamma']=max((r['gamma'] for r in arr),default=None)
    summary.append(item)
write_csv(OUT/'gamma_150_run_summary.csv',summary,list(summary[0]))
write_csv(OUT/'gamma_quality_issues.csv',quality,['run','issue'])

# Representative case: max torque and min SFC, Run identified from optimization output
byrun={r['run']:r for r in records}
with (BASE/'Group11_Python_Analysis/group11_optima.csv').open(newline='') as f:opt=list(csv.DictReader(f))
rep=int(float(next(x['run'] for x in opt if x['objective']=='Max torque')))
fig,ax=plt.subplots(figsize=(8,5))
for zone in ['Unburned_Zone','Burned_Zone','Zone_Avg']:
    sub=[r for r in records if r['run']==rep and r['zone']==zone and r['crank_angle_deg'] is not None]
    if sub:ax.plot([r['crank_angle_deg'] for r in sub],[r['gamma'] for r in sub],label=zone.replace('_',' '))
ax.set(xlabel='Crank angle (degrees)',ylabel=r'Mixture specific-heat ratio $\gamma=C_p/C_v$',title=f'Chemkin NASA-7 mixture gamma — Run #{rep}')
ax.grid(alpha=0.25);ax.legend();fig.tight_layout();fig.savefig(OUT/'gamma_vs_crank_angle_representative.png',dpi=200);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,5))
for zone in ['Unburned_Zone','Burned_Zone','Zone_Avg']:
    sub=[r for r in records if r['run']==rep and r['zone']==zone]
    if sub:ax.scatter([r['temperature_K'] for r in sub],[r['gamma'] for r in sub],s=14,label=zone.replace('_',' '),alpha=.65)
ax.set(xlabel='Gas temperature (K)',ylabel=r'Mixture $\gamma$',title=f'Mixture gamma vs temperature — Run #{rep}')
ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/'gamma_vs_temperature_representative.png',dpi=200);plt.close(fig)

# Air-standard constant gamma Otto sensitivity is explicitly NOT an engine thermodynamic prediction
eta=[{'gamma_assumed':round(1.25+0.01*k,2),'otto_efficiency_percent':100*(1-12**(-(round(1.25+0.01*k,2)-1)))} for k in range(16)]
write_csv(OUT/'otto_constant_gamma_sensitivity.csv',eta,list(eta[0]))
fig,ax=plt.subplots(figsize=(7,4.5));ax.plot([x['gamma_assumed'] for x in eta],[x['otto_efficiency_percent'] for x in eta],marker='o');ax.axvline(1.4,linestyle='--',label='Conventional air-standard gamma = 1.4');ax.set(xlabel='Assumed constant gamma',ylabel='Ideal Otto efficiency (%)',title='Constant-gamma Otto cycle sensitivity (r = 12)');ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'otto_gamma_sensitivity.png',dpi=200);plt.close(fig)

# make file straightforward and audit-ready
countbyzone={z:sum(1 for r in records if r['zone']==z) for z in ['Unburned_Zone','Burned_Zone','Zone_Avg']}
text=f'''Group 11 — Ethanol SI engine: calculated mixture Cp, Cv and gamma

Inputs:
- Book1(1).xlsm: Chemkin time-series temperatures and species MOLE fractions (Run #2 through Run #151)
- Isooctane_nHeptane_Ethanol_Methanol(1).zip / therm.dat: NASA-7 high/low temperature coefficients
- group11_150_cases.csv: parameters of the 150 factorial runs

Method:
NASA-7 Cp/R = a1 + a2*T + a3*T**2 + a4*T**3 + a5*T**4
Cp_mix = sum_i[(X_i/sum_j X_j)*Cp_i(T)] [J/(mol K)]
Cv_mix = Cp_mix - R_u; gamma = Cp_mix/Cv_mix; R_u = {R:.12g} J/(mol K).
Applies only to ideal-gas mixtures. Uses the appropriate high/low NASA-7 polynomial by temperature.
For every time sample with a valid mole-fraction sum and within all active species' fitted temperature ranges, calculate all three values.

Record counts:
- Thermodynamic species parsed: {len(species)}; parse errors: {len(invalid)}
- Study runs: {len(runs)}; time-state records accepted: {len(records)}
- Records by zone: {countbyzone}
- Accepted temperature range: {minT:.3f}–{maxT:.3f} K
- Unique species used in accepted gas mixtures: {len(seen_thermo)}
- Data-quality flag rows: {len(quality)}; see gamma_quality_issues.csv
- Species lacking thermo coefficients, if any: {sorted(missing_seen)}
- Representative optimized case: Run #{rep} (maximum torque on sampled grid).

Files:
- gamma_all_states.csv: row-by-row Cp/Cv/gamma and time/crank angle for every usable state
- gamma_150_run_summary.csv: initial/final/min/max gamma for each zone and each run
- gamma_quality_issues.csv: excluded states and reasons
- gamma_vs_crank_angle_representative.png, gamma_vs_temperature_representative.png
- otto_constant_gamma_sensitivity.csv, otto_gamma_sensitivity.png
- build_gamma_analysis.py: complete reproducible source code

Interpretation and limitations:
1. Mixture gamma varies with both temperature and species composition; it is not one fixed ethanol-engine gamma.
2. Different zones' mole-fraction compositions are processed separately, and zone-average calculations are based on Chemkin's exported zone-average state.
3. Initial time-series points need not coincide with start of intake/compression for another engine; study exact crank angles.
4. Standard Otto efficiency with r=12 and gamma=1.4 = {100*(1-12**(-0.4)):.4f}%. This is the conventional CONSTANT-specific-heat air-standard benchmark.
5. Do not substitute variable-gamma values into the constant-gamma Otto formula as if that produced a variable-specific-heat Otto cycle. Such a cycle must use the temperature-dependent internal energy and isentropic relations.
6. These outputs are post-processing of already exported Chemkin results, not new Chemkin simulations.
7. Failure diagnostics and convergence are not established by successful spreadsheet extraction alone.
'''
(OUT/'README.txt').write_text(text)
(OUT/'build_gamma_analysis.py').write_text(Path(__file__).read_text())
print(text)
