# Group 11 — Ethanol SI Engine: Python Analysis

## Data and methods
Source: Chemkin-provided endpoint performance results for 150 factorial cases (Run #2 to Run #151; Run #1 is an excluded baseline).
Chemkin outputs used: IVC–EVO torque, power, specific fuel consumption, thermal efficiency.
Unit conversions are already reflected in the input data (Nm, kW, g/kWh, %).
The ideal Otto benchmark assumes compression ratio r=12 and **constant γ=1.4 for air**.
γ=1.4 is NOT substituted into the Chemkin simulation data and does NOT imply that Chemkin used constant heat capacities.

## Grid-search optima

| Objective | Value | RPM | Start angle (°CA) | Burn duration (°CA) | Run |
|---|---:|---:|---:|---:|---:|
| Maximum torque | 34.9903 Nm | 1000 | -5 | 10 | 47 |
| Maximum power | 10.9907 kW | 3000 | -5 | 10 | 147 |
| Minimum SFC | 241.3150 g/kWh | 1000 | -5 | 10 | 47 |
| Maximum thermal efficiency | 53.7968 % | 1000 | -5 | 10 | 47 |

## Otto efficiency comparison
Ideal Otto: **62.9893%** (r=12, γ=1.4).
Best simulated efficiency: **53.7968%**.
Absolute difference: **9.1925 percentage points**.

## Isolated-effect plot reference cases
- Engine speed study: start angle = −10°CA and burn duration = 30°CA.
- Start angle study: speed = 1500 RPM and burn duration = 30°CA.
- Burn duration study: speed = 1500 RPM and start angle = −10°CA.

## Plot guide
- 12 isolated-effect plots: 3 varied parameters × 4 performance metrics.
- 24 heatmaps: 6 RPM levels × 4 metrics; all 25 start-angle/burn-duration combinations at each RPM.
- 4 speed-sweep comparison plots at fixed duration 30°CA.
- 1 direct Otto-vs-Chemkin efficiency comparison and 1 Otto gamma sensitivity plot.

## Technical interpretation (subject to solver-log validation)
- Combustion timing controls where heat is released relative to top dead center and therefore changes expansion work.
- Burn duration modifies the heat-release phasing. Shorter duration is not automatically optimal at every timing setting.
- Power reflects torque multiplied by angular speed; comparing these outputs provides a consistency check.
- Fuel consumption and thermal efficiency are linked by fuel heating value and work output.
- The ideal air-standard Otto comparison neglects heat losses and finite-duration combustion; realistic gas-specific heats vary with temperature.

## Important limitations
- The numerical best cases are optima among **150 discrete grid points**, not proven continuous global optima.
- The workbook alone cannot establish that all Chemkin solver runs converged: verify run logs/status before final submission.
- Results are from the Chemkin **IVC–EVO** window (indicated performance), not necessarily brake output.
- Additional mechanisms, experimental error bars, and optimizer convergence claims are not supported by these data.
- Input file used here is pre-cleaned; original worksheet extraction script should be kept as provenance.

## How to rerun
Install numpy and matplotlib, then run `python analyze_group11.py` from this folder.
Generated outputs appear in `results/` and `plots/`.
No simulation rerun is necessary: this script post-processes previously exported Chemkin data.
