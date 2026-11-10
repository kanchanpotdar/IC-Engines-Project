# Problem 11 Assignment Checklist

Status meanings: **Verified**, **Partially verified**, or **Missing evidence**.

| Requirement | Status | Evidence / remaining work |
|---|---|---|
| Use the SI-engine sample project | Partially verified | Packaged `.ckprj` exists; exact original sample filename is not separately present. |
| Load mechanism, thermo, and transport files | Verified | Chemkin bundle and supplied mechanism archive contain `mech.dat`, `therm.dat`, and `trans.dat`. |
| Use ethanol fuel | Verified | `project.inp` contains `c2h5oh`; Problem 11 is ethanol. |
| Use air at 21% O2 and 79% N2 | Verified | Input mole fractions correspond approximately to the requested air composition. |
| Use requested speed range | Verified | 500, 1000, 1500, 2000, 2500, 3000 RPM. |
| Use requested start-angle range | Verified | -15, -12.5, -10, -7.5, -5 degrees. |
| Use requested burn-duration range | Verified | 10, 20, 30, 40, 50 degrees. |
| Complete 150-case factorial study | Verified as exported data | 150 unique rows and 151 workbook run sheets including baseline. Solver completion is not independently proven. |
| Evaluate torque, power, and thermal efficiency | Verified | Present in analysis CSVs and plots. |
| Find maximum torque | Verified for sampled grid | Run 47: 34.9903 Nm. |
| Find maximum power | Verified for sampled grid | Run 147: 10.9907 kW. |
| Find minimum SFC | Verified for sampled grid | Run 47: 241.3150 g/kWh. |
| Establish continuous global optima | Missing evidence | Current results are discrete-grid optima. Boundary behavior requires qualification or targeted refinement. |
| Explain parameter effects from first principles | Partially verified | Plot/data basis exists; final assignment-quality discussion is not present. |
| Compare with ideal Otto cycle | Verified numerically | 62.9893% benchmark at r=12, gamma=1.4. |
| Explain Otto/Chemkin difference | Partially verified | Draft explanation exists; final wording must include finite burn duration, phasing, variable properties, and verified zero-wall-loss assumption. |
| Isolate each parameter effect | Verified as analysis outputs | 12 isolated-effect plots and corresponding CSVs are packaged. |
| Document mechanism details/source | Partially verified | 80 species/349 reactions and mechanism files are present; source attribution and citations still need final report wording. |
| Include Chemkin screenshots | Partially verified | Screenshots exist; final selection, ordering, and captions are unfinished. |
| Include group-member contributions | Missing evidence | Must be supplied by the group; do not infer this from files. |
| Prepare final report/presentation | Missing | No final report or presentation is in the folder. |
