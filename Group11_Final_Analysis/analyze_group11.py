#!/usr/bin/env python3
"""Reproducible Chemkin Group 11 full-factorial post-processing.

Usage:
    python analyze_group11.py [path/to/group11_150_cases.csv]
Produces results/ plots/ in same directory as this script.
All Chemkin outputs come from original 150-case parameter study. Gamma=1.4
is used ONLY in ideal constant-specific-heat Otto efficiency benchmark.
"""
from pathlib import Path
import csv, math, sys, textwrap, json, statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'data'/'group11_150_cases.csv'
OUT = HERE/'results'; PLOTS = HERE/'plots'
OUT.mkdir(exist_ok=True); PLOTS.mkdir(exist_ok=True)
R = 12.0; GAMMA = 1.4
OTTO = 100*(1-1/R**(GAMMA-1))
COLS=['run','rpm','start_angle_deg','burn_duration_deg','torque_Nm','power_kW','sfc_g_per_kWh','thermal_efficiency_pct']
with SOURCE.open(newline='',encoding='utf-8-sig') as f:
    reader=csv.DictReader(f)
    assert all(k in reader.fieldnames for k in COLS),reader.fieldnames
    D=[]
    for row in reader:
        item={k:float(row[k]) for k in COLS}
        if not all(math.isfinite(v) for v in item.values()):
            raise ValueError('Non-finite value in row '+str(row))
        item['run']=int(item['run']);D.append(item)
assert len(D)==150, f'Expected 150 rows, got {len(D)}'
SPEEDS=sorted(set(r['rpm'] for r in D)); ANGLES=sorted(set(r['start_angle_deg'] for r in D)); DURATIONS=sorted(set(r['burn_duration_deg'] for r in D))
assert (len(SPEEDS),len(ANGLES),len(DURATIONS))==(6,5,5)
keys=[(d['rpm'],d['start_angle_deg'],d['burn_duration_deg']) for d in D]
assert len(set(keys))==150,'duplicate input combinations'
assert all(d['sfc_g_per_kWh']>0 and d['power_kW']>0 for d in D)

# Verification of output consistency, not independent solver convergence check.
for d in D:
    predicted=d['torque_Nm']*2*math.pi*d['rpm']/60/1000
    d['power_vs_torque_relative_error_pct']=100*(d['power_kW']-predicted)/predicted

best={
  'Maximum torque':max(D,key=lambda d:d['torque_Nm']),
  'Maximum power':max(D,key=lambda d:d['power_kW']),
  'Minimum SFC':min(D,key=lambda d:d['sfc_g_per_kWh']),
  'Maximum thermal efficiency':max(D,key=lambda d:d['thermal_efficiency_pct'])
}

def write_csv(path,rows,cols):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

write_csv(OUT/'cleaned_150_cases.csv',D,COLS+['power_vs_torque_relative_error_pct'])
write_csv(OUT/'optimal_cases.csv',[{'objective':k,**v} for k,v in best.items()],['objective']+COLS)

METRICS=[('torque_Nm','Torque','Nm'),('power_kW','Power','kW'),('sfc_g_per_kWh','Specific fuel consumption','g/kWh'),('thermal_efficiency_pct','Thermal efficiency','%')]
PARAMS=[('rpm','Engine speed','RPM'),('start_angle_deg','Start of combustion','°CA'),('burn_duration_deg','Burn duration','°CA')]
# Isolated-effect profiles at reproducible common reference settings (present in grid).
SLICES={
  'rpm': {'start_angle_deg':-10.0,'burn_duration_deg':30.0},
  'start_angle_deg': {'rpm':1500.0,'burn_duration_deg':30.0},
  'burn_duration_deg': {'rpm':1500.0,'start_angle_deg':-10.0},
}
figures=[]
plt.rcParams.update({'font.size':10, 'axes.spines.top':False,'axes.spines.right':False})
for x,name,unit in PARAMS:
    frozen=SLICES[x]
    rows=sorted([d for d in D if all(d[k]==v for k,v in frozen.items())], key=lambda d:d[x])
    write_csv(OUT/f'isolated_{x}.csv',rows,COLS)
    assert len(rows)==(6 if x=='rpm' else 5)
    for y,ylab,yunit in METRICS:
        fig,ax=plt.subplots(figsize=(7.8,4.8))
        ax.plot([d[x] for d in rows],[d[y] for d in rows],'-o',linewidth=2,markersize=6)
        ax.set_xlabel(f'{name} ({unit})');ax.set_ylabel(f'{ylab} ({yunit})')
        fixedtxt='; '.join(k.replace('_deg','').replace('_',' ')+' = '+str(int(v) if float(v).is_integer() else v) for k,v in frozen.items())
        ax.set_title(f'{ylab} versus {name}\nOther inputs fixed: {fixedtxt}',fontsize=11)
        ax.grid(alpha=0.24)
        path=PLOTS/f'isolated_{x}_vs_{y}.png';fig.tight_layout();fig.savefig(path,dpi=180);plt.close(fig)
        figures.append(path.name)

# Full-grid heatmaps: one map per output for each speed (24 graphs), no interpolation.
for rpm in SPEEDS:
    for metric,label,unit in METRICS:
        arr=np.array([[next(d[metric] for d in D if d['rpm']==rpm and d['start_angle_deg']==angle and d['burn_duration_deg']==duration)
                       for duration in DURATIONS] for angle in ANGLES])
        fig,ax=plt.subplots(figsize=(7.2,4.8))
        img=ax.imshow(arr,origin='lower',aspect='auto',cmap='viridis')
        ax.set_xticks(range(len(DURATIONS)),[f'{x:g}' for x in DURATIONS]);ax.set_yticks(range(len(ANGLES)),[f'{x:g}' for x in ANGLES])
        ax.set_xlabel('Burn duration (°CA)');ax.set_ylabel('Combustion start (°CA)')
        ax.set_title(f'{label} at {rpm:g} RPM')
        fig.colorbar(img,ax=ax,label=f'{label} ({unit})',shrink=.83)
        fig.tight_layout();path=PLOTS/f'heatmap_{int(rpm)}rpm_{metric}.png';fig.savefig(path,dpi=160);plt.close(fig);figures.append(path.name)

# Multi-line maps: variation with speed for each combustion start at fixed burn duration=30
for metric,label,unit in METRICS:
    fig,ax=plt.subplots(figsize=(8,5))
    for angle in ANGLES:
        rows=sorted([d for d in D if d['start_angle_deg']==angle and d['burn_duration_deg']==30],key=lambda d:d['rpm'])
        ax.plot([d['rpm'] for d in rows],[d[metric] for d in rows],marker='o',label=f'{angle:g}°')
    ax.set(xlabel='Engine speed (RPM)',ylabel=f'{label} ({unit})',title=f'{label} vs speed at burn duration 30°CA')
    ax.grid(alpha=.25);ax.legend(title='Combustion start',fontsize=8)
    fig.tight_layout();path=PLOTS/f'speed_sweep_by_start_{metric}.png';fig.savefig(path,dpi=180);plt.close(fig);figures.append(path.name)

# Otto comparison for optimal-efficiency run
fig,ax=plt.subplots(figsize=(6.8,4.7))
actual=best['Maximum thermal efficiency']['thermal_efficiency_pct']
ax.bar(['Ideal Otto\n(r=12, γ=1.4)','Best Chemkin\n(grid case)'],[OTTO,actual],width=.55)
for i,v in enumerate([OTTO,actual]):ax.text(i,v+0.5,f'{v:.2f}%',ha='center',fontsize=11)
ax.set_ylabel('Thermal efficiency (%)');ax.set_ylim(0,max(OTTO,actual)*1.18)
ax.set_title('Air-standard Otto benchmark vs simulated IVC–EVO efficiency')
fig.tight_layout();path=PLOTS/'otto_vs_chemkin_efficiency.png';fig.savefig(path,dpi=180);plt.close(fig);figures.append(path.name)

# Sensitivity comparison, marked theoretical scenarios, not fitted to Chemkin engine.
gammas=[1.30,1.35,1.40]
write_csv(OUT/'otto_gamma_sensitivity.csv',[{'compression_ratio':R,'gamma':g,'ideal_otto_efficiency_pct':100*(1-R**(1-g))} for g in gammas],['compression_ratio','gamma','ideal_otto_efficiency_pct'])
fig,ax=plt.subplots(figsize=(6.8,4.6))
gg=np.linspace(1.25,1.45,100)
ax.plot(gg,[100*(1-R**(1-g)) for g in gg],linewidth=2)
ax.axvline(1.4,ls='--',alpha=.7);ax.scatter([1.4],[OTTO]);ax.annotate(f'γ=1.4: {OTTO:.2f}%',(1.4,OTTO),xytext=(1.31,OTTO+3),arrowprops={'arrowstyle':'->'})
ax.set(xlabel='Assumed constant γ',ylabel='Ideal Otto efficiency (%)',title='Sensitivity of air-standard Otto efficiency (r=12)')
ax.grid(alpha=.25);fig.tight_layout();path=PLOTS/'otto_gamma_sensitivity.png';fig.savefig(path,dpi=180);plt.close(fig);figures.append(path.name)

# Machine readable QA
qa={
 'source':str(SOURCE.name),'n_cases':len(D),'n_unique_combinations':len(set(keys)),
 'parameter_levels':{'rpm':SPEEDS,'start_angle_deg':ANGLES,'burn_duration_deg':DURATIONS},
 'max_absolute_power_torque_error_pct':max(abs(d['power_vs_torque_relative_error_pct']) for d in D),
 'all_sfc_and_power_positive':True,
 'observed_metric_ranges':{m:[min(d[m] for d in D),max(d[m] for d in D)] for m,_,_ in METRICS},
 'compression_ratio':R,'gamma_otto_assumption':GAMMA,'ideal_otto_efficiency_pct':OTTO,
 'max_simulated_efficiency_pct':actual,'otto_minus_max_chemkin_percentage_points':OTTO-actual,
 'solver_convergence_verified':False,
 'interpretation':'150-case discrete-grid optima, NOT mathematically guaranteed global optima; source solver logs require separate review.'
}
(OUT/'quality_checks.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False),encoding='utf-8')

summary=['# Group 11 — Ethanol SI Engine: Python Analysis','',
 '## Data and methods',
 'Source: Chemkin-provided endpoint performance results for 150 factorial cases (Run #2 to Run #151; Run #1 is an excluded baseline).',
 'Chemkin outputs used: IVC–EVO torque, power, specific fuel consumption, thermal efficiency.',
 'Unit conversions are already reflected in the input data (Nm, kW, g/kWh, %).',
 'The ideal Otto benchmark assumes compression ratio r=12 and **constant γ=1.4 for air**.',
 'γ=1.4 is NOT substituted into the Chemkin simulation data and does NOT imply that Chemkin used constant heat capacities.',
 '', '## Grid-search optima','',
 '| Objective | Value | RPM | Start angle (°CA) | Burn duration (°CA) | Run |',
 '|---|---:|---:|---:|---:|---:|']
for obj,b in best.items():
    k={'Maximum torque':('torque_Nm','Nm'),'Maximum power':('power_kW','kW'),'Minimum SFC':('sfc_g_per_kWh','g/kWh'),'Maximum thermal efficiency':('thermal_efficiency_pct','%')}[obj]
    summary.append(f'| {obj} | {b[k[0]]:.4f} {k[1]} | {b["rpm"]:g} | {b["start_angle_deg"]:g} | {b["burn_duration_deg"]:g} | {b["run"]} |')
summary += ['','## Otto efficiency comparison',f'Ideal Otto: **{OTTO:.4f}%** (r=12, γ=1.4).',f'Best simulated efficiency: **{actual:.4f}%**.',f'Absolute difference: **{OTTO-actual:.4f} percentage points**.',
 '', '## Isolated-effect plot reference cases',
 '- Engine speed study: start angle = −10°CA and burn duration = 30°CA.',
 '- Start angle study: speed = 1500 RPM and burn duration = 30°CA.',
 '- Burn duration study: speed = 1500 RPM and start angle = −10°CA.',
 '', '## Plot guide',
 '- 12 isolated-effect plots: 3 varied parameters × 4 performance metrics.',
 '- 24 heatmaps: 6 RPM levels × 4 metrics; all 25 start-angle/burn-duration combinations at each RPM.',
 '- 4 speed-sweep comparison plots at fixed duration 30°CA.',
 '- 1 direct Otto-vs-Chemkin efficiency comparison and 1 Otto gamma sensitivity plot.',
 '', '## Technical interpretation (subject to solver-log validation)',
 '- Combustion timing controls where heat is released relative to top dead center and therefore changes expansion work.',
 '- Burn duration modifies the heat-release phasing. Shorter duration is not automatically optimal at every timing setting.',
 '- Power reflects torque multiplied by angular speed; comparing these outputs provides a consistency check.',
 '- Fuel consumption and thermal efficiency are linked by fuel heating value and work output.',
 '- The ideal air-standard Otto comparison neglects heat losses and finite-duration combustion; realistic gas-specific heats vary with temperature.',
 '', '## Important limitations',
 '- The numerical best cases are optima among **150 discrete grid points**, not proven continuous global optima.',
 '- The workbook alone cannot establish that all Chemkin solver runs converged: verify run logs/status before final submission.',
 '- Results are from the Chemkin **IVC–EVO** window (indicated performance), not necessarily brake output.',
 '- Additional mechanisms, experimental error bars, and optimizer convergence claims are not supported by these data.',
 '- Input file used here is pre-cleaned; original worksheet extraction script should be kept as provenance.',
 '', '## How to rerun',
 'Install numpy and matplotlib, then run `python analyze_group11.py` from this folder.',
 'Generated outputs appear in `results/` and `plots/`.',
 'No simulation rerun is necessary: this script post-processes previously exported Chemkin data.',
 '']
(HERE/'README.md').write_text('\n'.join(summary),encoding='utf-8')
print(f'Generated {len(figures)} plots, {len(D)} cases, Otto={OTTO:.3f}%')
print('Optima:', [(k,v['run'],v['rpm'],v['start_angle_deg'],v['burn_duration_deg']) for k,v in best.items()])
