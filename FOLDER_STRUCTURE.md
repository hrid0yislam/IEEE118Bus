# Recommended Folder Structure for IEEE 118-Bus System

This document outlines a recommended folder structure for organizing the IEEE 118-Bus System project files. Following this structure will help maintain a clean and organized codebase.

## Top-Level Directories

```
IEEE118Bus/
├── src/               # Source code
├── data/              # Data files
├── docs/              # Documentation
├── results/           # Simulation results
└── requirements.txt   # Project dependencies
```

## Source Code (`src/`)

```
src/
├── simulation/        # Time series simulation scripts
├── visualization/     # Visualization scripts
├── diagnostics/       # Diagnostic and troubleshooting scripts
├── utilities/         # Utility scripts
└── dss_files/         # OpenDSS files
    ├── base/          # Original DSS files
    └── modified/      # Modified DSS files
```

### Simulation Scripts (`src/simulation/`)

- `stabilized_time_series.py` - Main time series simulation with voltage stabilization
- `fixed_time_series.py` - Fixed version of time series simulation
- `simplified_time_series.py` - Simplified version of time series simulation
- `robust_time_series.py` - Robust version of time series simulation
- `simple_time_series.py` - Simple version of time series simulation

### Visualization Scripts (`src/visualization/`)

- `network_visualization.py` - Network visualization
- `voltage_visualization.py` - Voltage profile visualization
- `visualize_time_series.py` - Time series visualization
- `loss_visualization.py` - Loss visualization
- `simple_loss_viz.py` - Simple loss visualization
- `voltage_loss_viz.py` - Voltage loss visualization
- `voltage_loss_analysis.py` - Voltage loss analysis

### Diagnostic Scripts (`src/diagnostics/`)

- `diagnose_convergence.py` - Diagnose convergence issues
- `check_convergence.py` - Check convergence
- `voltage_stabilized_simulation.py` - Voltage stabilized simulation
- `fix_swing_bus.py` - Fix swing bus issues
- `fix_generators.py` - Fix generator issues
- `test_opendss.py` - Test OpenDSS installation

### DSS Files (`src/dss_files/`)

#### Base DSS Files (`src/dss_files/base/`)

- `master_file.dss` - Main DSS file
- `generators.dss` - Generator definitions
- `lines.dss` - Line definitions
- `transformers.dss` - Transformer definitions
- `loads.dss` - Load definitions
- `shunts.dss` - Shunt definitions
- `sw_shunts.dss` - Switched shunt definitions
- `dc_and_facts_equiv_elements.dss` - DC and FACTS elements
- `confirm_kv_bases.dss` - Confirm kV bases

#### Modified DSS Files (`src/dss_files/modified/`)

- `generators_fixed.dss` - Fixed generator definitions
- `master_file_fixed.dss` - Fixed master file
- `voltage_stabilized_circuit.dss` - Voltage stabilized circuit
- `simplified_circuit.dss` - Simplified circuit

## Data Files (`data/`)

```
data/
├── input/             # Input data
│   └── xlsx/          # Excel files
└── output/            # Output data
```

### Input Data (`data/input/`)

- `hourly_load_profile.csv` - Hourly load profile
- `Comparissons.xlsx` - Comparison data

### Output Data (`data/output/`)

- `ieee118bus_VLN_Node.txt` - Voltage data
- `ieee118bus_Power_elem_MVA.txt` - Power flow data
- `ieee118bus_Losses.txt` - Loss data

## Documentation (`docs/`)

```
docs/
├── latex/             # LaTeX documents
│   └── reports/       # LaTeX reports
└── markdown/          # Markdown documents
```

### LaTeX Documents (`docs/latex/`)

- `ieee118_bus_report.tex` - IEEE 118-bus report
- `generator_analysis.tex` - Generator analysis
- `snapshot_powerflow.tex` - Snapshot power flow analysis
- `voltage_profile_analysis.tex` - Voltage profile analysis
- `time_series_explanation.tex` - Time series explanation

### Markdown Documents (`docs/markdown/`)

- `README.md` - Project README
- `time_series_solution.md` - Time series solution
- `loss_explanation.md` - Loss explanation
- `opendss_explanation.md` - OpenDSS explanation
- `time_series_analysis.md` - Time series analysis
- `voltage_profile_report.md` - Voltage profile report

## Results (`results/`)

```
results/
├── figures/           # Figures and plots
│   └── thesis/        # Thesis figures
├── reports/           # Reports
└── time_series/       # Time series results
```

### Figures (`results/figures/`)

- Various visualization outputs (PNG files)

### Reports (`results/reports/`)

- Various report files (TXT files)

### Time Series Results (`results/time_series/`)

- Time series simulation results

## How to Organize Your Files

To organize your files according to this structure, you can:

1. Create the directory structure manually:
   ```bash
   mkdir -p src/{simulation,visualization,diagnostics,utilities,dss_files/{base,modified}}
   mkdir -p data/{input/xlsx,output}
   mkdir -p docs/{latex/reports,markdown}
   mkdir -p results/{figures/thesis,reports,time_series}
   ```

2. Move files to their appropriate directories:
   ```bash
   # Example: Move simulation files
   mv stabilized_time_series.py src/simulation/
   mv fixed_time_series.py src/simulation/
   
   # Example: Move DSS files
   mv master_file.dss src/dss_files/base/
   mv generators.dss src/dss_files/base/
   
   # Example: Move documentation
   mv README.md docs/markdown/
   ```

3. Update file references if necessary to reflect the new file locations.

## Benefits of This Structure

- **Modularity**: Related files are grouped together
- **Scalability**: Easy to add new components
- **Maintainability**: Clear organization makes it easier to find and update files
- **Collaboration**: Standard structure helps team members understand the project organization 