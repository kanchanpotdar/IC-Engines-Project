# Validation Report

Inspection date: 2026-11-09

## Verified from available artifacts

- The assignment maps Group 11 to Problem 11.
- The packaged Chemkin input uses ethanol (`c2h5oh`) with oxygen and nitrogen.
- The supplied mechanism header states 80 species and 349 reactions.
- The workbook contains 178 worksheets, including 151 run sheets: Run #1 through Run #151.
- The analysis package contains 150 optimization rows and reports 150 unique parameter combinations.
- Parameter levels are 6 RPM values, 5 start-angle values, and 5 burn-duration values.
- Reported ranges are torque 30.733–34.990 Nm, power 1.609–10.991 kW, SFC 241.315–274.740 g/kWh, and thermal efficiency 47.252–53.797%.
- The reported maximum absolute power/torque consistency error is 0.0000604%.
- The conventional Otto benchmark is 62.9893% for compression ratio 12 and constant gamma 1.4.
- The best sampled simulated efficiency is 53.7968%, a difference of 9.1925 percentage points.
- The gamma post-processing reports 52,944 accepted states, 107 parsed thermo species, 44 species used, and zero flagged quality rows.

## Reported sampled optima

| Objective | Run | RPM | Start | Duration | Result |
|---|---:|---:|---:|---:|---:|
| Maximum torque | 47 | 1000 | -5 deg | 10 deg | 34.9903 Nm |
| Maximum power | 147 | 3000 | -5 deg | 10 deg | 10.9907 kW |
| Minimum SFC | 47 | 1000 | -5 deg | 10 deg | 241.3150 g/kWh |
| Maximum thermal efficiency | 47 | 1000 | -5 deg | 10 deg | 53.7968% |

These are optima over the sampled grid, not independently demonstrated continuous global optima.

## Solver evidence limitation

The folder contains screenshots showing successful runs and a packaged project/XML output, but it does not contain a complete per-run solver log set. Therefore, all-150 convergence is not independently verified. The analysis package itself explicitly records `solver_convergence_verified: false`.

## Reproducibility limitations

- The final-analysis Python source is packaged, not loose in the project root.
- The original workbook-extraction script is not present.
- The gamma script contains hard-coded `/mnt/data` paths and references filenames not present exactly in this folder, so it is not directly rerunnable without path adaptation.
- The packaged Chemkin project is available, but the original sample project named in the assignment is not separately present under that exact filename.

## Optimization assessment

The 150 cases are a complete discrete factorial grid over the declared levels. All reported best settings occur at the start-angle and burn-duration boundaries (-5 and 10 degrees). This is evidence of a boundary optimum on the grid, but it does not prove a continuous global optimum. Additional simulations inside the allowed domain would strengthen the claim, but should be targeted and justified rather than run indiscriminately.
