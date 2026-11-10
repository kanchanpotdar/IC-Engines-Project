# Parametric Analysis of an Ethanol-Fuelled SI Engine

Group 11 · ME60111 Internal Combustion Engine · Department of Mechanical Engineering, IIT Kharagpur

This repository preserves the group's ANSYS Chemkin-Pro 2025 R2 project, exported results, Python post-processing, technical report, and presentation. The study varied engine speed, combustion start angle, and prescribed burn duration for an ethanol–air spark-ignition engine model. The reported outputs are **indicated simulation quantities**, not measured brake-engine performance.

**Start here:** [technical report](Group11_Report.docx) · [final presentation](presentations/Group11_Ethanol_Final_v11.pptx) · [150-case data](Group11_Final_Analysis/data/group11_150_cases.csv) · [analysis script](Group11_Final_Analysis/analyze_group11.py)

## Study at a glance

| Input | Evaluated levels |
| --- | --- |
| Engine speed | 500, 1000, 1500, 2000, 2500, 3000 RPM |
| Combustion start | −15, −12.5, −10, −7.5, −5°CA |
| Burn duration | 10, 20, 30, 40, 50°CA |

The full-factorial grid contains **6 × 5 × 5 = 150 cases**. Run #1 in the workbook is a separate baseline; the analysis uses Run #2 through Run #151. The packaged Chemkin input specifies a two-zone, prescribed-combustion SI-engine model with a Wiebe burn profile, compression ratio 12, and zero wall heat transfer. The supplied mechanism header identifies 80 species and 349 reactions.

| Objective | Best sampled result | Speed | Start | Duration |
| --- | ---: | ---: | ---: | ---: |
| Maximum indicated torque | 34.990 N·m | 1000 RPM | −5°CA | 10°CA |
| Maximum indicated power | 10.991 kW | 3000 RPM | −5°CA | 10°CA |
| Minimum indicated specific fuel consumption (ISFC) | 241.315 g/kWh | 1000 RPM | −5°CA | 10°CA |
| Maximum indicated thermal efficiency | 53.797% | 1000 RPM | −5°CA | 10°CA |

These are the **best sampled conditions**, not proven continuous or global optima. The common timing combination lies on the latest-start and shortest-duration boundaries of the evaluated grid. The report also compares the maximum simulated indicated efficiency with the ideal air-standard Otto benchmark of 62.99% at *r* = 12 and assumed constant γ = 1.4. The 9.19-percentage-point difference is a benchmark gap between different modelling assumptions; it is not an experimentally measured loss. The zero-wall-transfer model cannot use wall heat loss to explain that gap.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`Group11_Report.docx`](Group11_Report.docx) | Final technical report with Chemkin evidence, isolated trends, interaction plots, sampled optimization, and limitations. |
| [`presentations/Group11_Ethanol_Final_v11.pptx`](presentations/Group11_Ethanol_Final_v11.pptx) | Final group presentation. |
| [`chemkin/project/Group11_Ethanol_SI_Engine.ckprj`](chemkin/project/Group11_Ethanol_SI_Engine.ckprj) | Packaged Chemkin project and adjacent input, chemistry, and configuration files. |
| [`chemkin/mechanism/Isooctane_nHeptane_Ethanol_Methanol/`](chemkin/mechanism/Isooctane_nHeptane_Ethanol_Methanol/) | Supplied mechanism, thermodynamic, and transport files. |
| [`Book1.xlsm`](Book1.xlsm) | Original Chemkin spreadsheet export, including baseline and study run sheets. Contains macros; no macros were executed in this repository audit. |
| [`Group11_Final_Analysis/`](Group11_Final_Analysis/) | 150-case CSV, Python analysis script, result tables, quality checks, and generated plots. |
| [`Group11_Gamma_Analysis/`](Group11_Gamma_Analysis/) | Archived NASA-7 mixture-property post-processing code and outputs. |
| [`screenshots/`](screenshots/) | Selected genuine Chemkin setup, parameter-study, and result screenshots. |
| [`audit/`](audit/) | Dated inspection/checklist notes. These are historical snapshots and may describe work that was completed later. |
| Root ZIP files | Original supplied project, mechanism, analysis, screenshot, and XML bundles retained for provenance. |

## Reproduce the 150-case plots and tables

The analysis script reads the committed CSV and writes to `Group11_Final_Analysis/results/` and `Group11_Final_Analysis/plots/`. Use Python with NumPy and Matplotlib installed:

```bash
python Group11_Final_Analysis/analyze_group11.py
```

The script checks the 150 unique input combinations, positive power and ISFC, and the consistency of exported indicated power with torque and speed. It generates isolated-effect plots, discrete-grid heatmaps, speed sweeps, the sampled-objective table, and the ideal Otto comparison. Running it **post-processes exported data**; it does not launch Chemkin or verify that every original solver run converged. The command has been inspected from source; a fresh rerun is not required to use the committed outputs.

To inspect or adapt the original model, open the `.ckprj` in ANSYS Chemkin-Pro 2025 R2. The project was packaged on another Windows machine, so file paths inside its configuration may need relinking to the adjacent `mech.dat`, `therm.dat`, and `trans.dat` files. Chemkin itself is proprietary and is not included here.

The gamma archive contains 52,944 accepted exported time states and a post-processing script. **Its original script is not directly rerunnable from this repository:** it refers to absolute `/mnt/data` paths and to an unavailable `group11_analysis.py` workbook-extraction helper. The committed gamma CSVs and plots are archived results, not a claim that this secondary workflow has been reproduced from a clean checkout.

## Reading the results

- The [isolated speed plots](Group11_Final_Analysis/plots/isolated_rpm_vs_torque_Nm.png) hold combustion start at −10°CA and duration at 30°CA. Torque changes little over the selected slice while indicated power rises with RPM.
- The start-angle slice holds 1500 RPM and 30°CA duration. Its trend toward −15°CA is **only a fixed-slice result**.
- The duration slice holds 1500 RPM and −10°CA start. Its torque peak near 20°CA is **only a fixed-slice result**.
- The [interaction plots in the report](Group11_Report.docx) show why start angle and duration must be considered together. The −5°CA / 10°CA combination is best among sampled points even though the 30°CA-duration slice favours an earlier start.
- The [quality-check summary](Group11_Final_Analysis/results/quality_checks.json) records the data grid and explicitly marks full solver convergence as unverified.

## Limits and provenance

The 150 exported cases cover a discrete, boundary-limited grid. The model prescribes combustion, assumes zero wall heat transfer, and has no same-engine experimental validation. The supplied materials do not include a complete per-run solver-log set or the original workbook-to-CSV extraction script. Results should therefore be interpreted as Chemkin simulation outputs and post-processing of those outputs.

The course [problem statement](<Problem statements for group projects (1).pdf>), supplied reaction mechanism, and project files are retained with their original provenance. No repository-wide license or independently verified redistribution terms for the supplied mechanism were found; inclusion here does not grant additional rights to those materials.

## Group 11 contributions

| Member | Roll number | Primary contribution |
| --- | --- | --- |
| Raksha Gupta | 23ME10066 | Baseline simulation |
| Kanchan Potdar | 23ME10038 | 150-case parameter study |
| Saloni | 23ME10074 | Performance optimization and Otto comparison |
| Nagineni Lakshmipravallika | 23ME10053 | Python data analysis and visualization |
| Pranjali Khatua | 23ME10060 | Technical report and presentation |
