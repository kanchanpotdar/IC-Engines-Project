# Next Steps

## Required before final submission

1. Obtain or export the per-run Chemkin status/log evidence and verify all 150 cases completed without relevant solver errors.
2. Preserve the original Excel extraction path or document the exact extraction method used to create `group11_150_cases.csv`.
3. Qualify optimization language as “best among 150 sampled cases” unless targeted in-range refinement is performed.
4. If refinement is approved, add only cases that address the boundary optima and explain why each case is needed. Do not extrapolate outside the assignment ranges.
5. Write the first-principles discussion using the observed plots, explicitly accounting for combustion phasing, finite burn duration, engine speed, variable properties, and the zero-wall-heat-loss model assumption.
6. Select and caption the required Chemkin screenshots.
7. Add the actual contributions of all five group members.
8. Assemble the final report and presentation.

## Optional improvements

- Make the two Python scripts locally rerunnable by replacing hard-coded paths with command-line arguments.
- Add a single top-level README explaining extraction, analysis, and validation order.
- Add automated tests for CSV schema, grid completeness, units, and optimum reproduction.
- Add a solver-log parser if logs become available.

## Recommended final claims

Use “discrete-grid optimum” for the current best cases. Report the 150-case coverage, parameter levels, units, and IVC–EVO scope. Do not claim all runs converged until logs are checked, and do not call the results mathematically global without additional justification.
