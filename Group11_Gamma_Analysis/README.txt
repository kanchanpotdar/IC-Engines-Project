Group 11 — Ethanol SI engine: calculated mixture Cp, Cv and gamma

Inputs:
- Book1(1).xlsm: Chemkin time-series temperatures and species MOLE fractions (Run #2 through Run #151)
- Isooctane_nHeptane_Ethanol_Methanol(1).zip / therm.dat: NASA-7 high/low temperature coefficients
- group11_150_cases.csv: parameters of the 150 factorial runs

Method:
NASA-7 Cp/R = a1 + a2*T + a3*T**2 + a4*T**3 + a5*T**4
Cp_mix = sum_i[(X_i/sum_j X_j)*Cp_i(T)] [J/(mol K)]
Cv_mix = Cp_mix - R_u; gamma = Cp_mix/Cv_mix; R_u = 8.31446261815 J/(mol K).
Applies only to ideal-gas mixtures. Uses the appropriate high/low NASA-7 polynomial by temperature.
For every time sample with a valid mole-fraction sum and within all active species' fitted temperature ranges, calculate all three values.

Record counts:
- Thermodynamic species parsed: 107; parse errors: 0
- Study runs: 150; time-state records accepted: 52944
- Records by zone: {'Unburned_Zone': 17648, 'Burned_Zone': 17648, 'Zone_Avg': 17648}
- Accepted temperature range: 353.000–2237.163 K
- Unique species used in accepted gas mixtures: 44
- Data-quality flag rows: 0; see gamma_quality_issues.csv
- Species lacking thermo coefficients, if any: []
- Representative optimized case: Run #47 (maximum torque on sampled grid).

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
4. Standard Otto efficiency with r=12 and gamma=1.4 = 62.9893%. This is the conventional CONSTANT-specific-heat air-standard benchmark.
5. Do not substitute variable-gamma values into the constant-gamma Otto formula as if that produced a variable-specific-heat Otto cycle. Such a cycle must use the temperature-dependent internal energy and isentropic relations.
6. These outputs are post-processing of already exported Chemkin results, not new Chemkin simulations.
7. Failure diagnostics and convergence are not established by successful spreadsheet extraction alone.
