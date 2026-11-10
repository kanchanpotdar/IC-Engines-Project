# Project Handoff: Group 11 Ethanol SI Engine

Inspection date: 2026-11-09

## Objective

Group 11 is assigned Problem 11: analyze an ethanol-fueled four-stroke SI engine in ANSYS Chemkin-Pro, varying engine speed, start of combustion, and burn duration, then determine torque, power, SFC, and thermal-efficiency behavior.

## Directory map

- `Problem statements for group projects (1).pdf`: assignment specification. Pages 4–5 establish that Group 11 maps to Problem 11; Problem 11 specifies ethanol and air.
- `Group11_Ethanol_SI_Engine_20261109_215921.ckzip.zip`: packaged Chemkin project, mechanism, thermodynamics, transport data, input, and XML output.
- `Isooctane_nHeptane_Ethanol_Methanol.zip`: supplied 80-species/349-reaction mechanism package.
- `Book1.xlsm`: Chemkin Excel export with 178 worksheets, including Run #1 through Run #151 and summary sheets. It contains embedded VBA; macros were not executed.
- `XMLdata_project.zip`: additional Chemkin/AURORA XML exports.
- `Group11_Final_Analysis.zip`: Python post-processing, 150-case CSV, results, and plots.
- `Group11_Gamma_Analysis.zip`: NASA-7 mixture Cp/Cv/gamma post-processing and supporting outputs.
- `group11_ethanol_results.zip`: screenshots and basic Chemkin plots.
- `gamma_all_states.csv`: loose gamma-state output, also represented in the gamma-analysis archive.

## Simulation configuration found

`project.inp` in the Chemkin bundle specifies a four-stroke, transient, single-piston SI engine with Wiebe burn profile, two active chemistry zones, ideal-gas law, compression ratio 12, bore 8.5 cm, stroke 10.82 cm, connecting-rod/crank-radius ratio 3.3, start angle -14.5 degrees, burn duration 45.6 degrees, and baseline speed 600 RPM. The reactants are `c2h5oh`, `o2`, and `n2`; the supplied mole fractions are approximately 3.3536%, 20.2957%, and 76.3506%, respectively.

The same input shows `HVAL 0.0`, `No_Gas-Velocity_Correlation`, and no wall-heat-transfer command. The zero-wall-loss conclusion should be stated as a model assumption, not as proof that every other loss mechanism is absent.

## Existing analysis

The final-analysis script checks a 6 x 5 x 5 factorial grid: 500–3000 RPM, -15 to -5 degrees start angle, and 10 to 50 degrees burn duration. It produces isolated-effect plots, 24 heatmaps, speed sweeps, optimal-case tables, quality checks, and an ideal-Otto comparison.

The gamma analysis uses NASA-7 thermodynamic coefficients to calculate mixture Cp, Cv, and gamma for 52,944 accepted states across 150 runs. Its README reports zero quality-issue rows and no missing thermo species.

## Current status

The numerical post-processing and engineering-plot stage is substantially complete. The project is not yet a fully auditable final submission because individual Chemkin solver logs are absent, the original Excel-to-150-case extraction source is absent, and no final report, presentation, or member-contribution record is present.
