# IEEE 118-Bus System Repository Organization

This document outlines the proposed organization structure for the IEEE 118-Bus System repository to make it more professional and easier to navigate.

## Proposed Directory Structure

```
IEEE118Bus/
├── README.md                      # Main repository documentation
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
│
├── data/                          # All input data files
│   ├── dss/                       # OpenDSS model files
│   │   ├── master_file.dss        # Main OpenDSS file
│   │   ├── lines.dss              # Line definitions
│   │   ├── transformers.dss       # Transformer definitions
│   │   ├── generators.dss         # Generator definitions
│   │   ├── loads.dss              # Load definitions
│   │   ├── shunts.dss             # Shunt definitions
│   │   └── sw_shunts.dss          # Switched shunts definitions
│   │
│   ├── modified/                  # Modified OpenDSS files
│   │   ├── master_file_fixed.dss  # Fixed master file
│   │   ├── generators_fixed.dss   # Fixed generators file
│   │   └── simplified_circuit.dss # Simplified circuit
│   │
│   └── profiles/                  # Time series profiles
│       └── hourly_load_profile.csv # Hourly load profile
│
├── src/                           # Source code
│   ├── utils/                     # Utility functions
│   │   ├── opendss_utils.py       # OpenDSS utility functions
│   │   └── visualization_utils.py # Visualization utility functions
│   │
│   ├── analysis/                  # Analysis scripts
│   │   ├── voltage_analysis.py    # Voltage analysis
│   │   ├── loss_analysis.py       # Loss analysis
│   │   └── critical_buses.py      # Critical bus identification
│   │
│   ├── simulation/                # Simulation scripts
│   │   ├── run_opendss.py         # Main OpenDSS runner
│   │   ├── time_series.py         # Time series simulation
│   │   └── convergence_fix.py     # Convergence fixing script
│   │
│   └── visualization/             # Visualization scripts
│       ├── voltage_viz.py         # Voltage visualization
│       ├── loss_viz.py            # Loss visualization
│       └── network_viz.py         # Network visualization
│
├── docs/                          # Documentation
│   ├── reports/                   # Markdown reports
│   │   ├── voltage_analysis.md    # Voltage analysis report
│   │   ├── loss_analysis.md       # Loss analysis report
│   │   └── time_series.md         # Time series analysis report
│   │
│   └── latex/                     # LaTeX documents
│       ├── main_report.tex        # Main report
│       └── figures/               # Figures for LaTeX
│
└── results/                       # Simulation results
    ├── figures/                   # Generated figures
    │   ├── voltage/               # Voltage-related figures
    │   ├── losses/                # Loss-related figures
    │   └── time_series/           # Time series figures
    │
    ├── data/                      # Generated data
    │   ├── voltage_results.csv    # Voltage results
    │   └── loss_results.csv       # Loss results
    │
    └── logs/                      # Simulation logs
        └── simulation.log         # Main simulation log
```

## Duplicate Files to Remove

The following duplicate files should be removed:

1. `generators.dss.bak` - Backup of generators.dss
2. Multiple visualization scripts with similar functionality:
   - `simple_loss_viz.py`, `ascii_loss_viz.py`, `basic_loss_viz.py` - Consolidate into a single script
   - `voltage_loss_viz.py`, `voltage_loss_viz_fixed.py` - Keep only the fixed version
3. Multiple time series scripts:
   - `simple_time_series.py`, `simplified_time_series.py`, `fixed_time_series.py`, `robust_time_series.py`, `stabilized_time_series.py` - Keep only the most robust version
4. Duplicate figures in root and thesis_figures directories
5. Duplicate analysis text files

## Implementation Plan

1. Create the directory structure
2. Move files to appropriate directories
3. Remove duplicate files
4. Update import paths in Python scripts
5. Update README.md with the new structure

## Benefits of New Structure

1. **Clarity**: Clear separation of data, code, documentation, and results
2. **Maintainability**: Easier to find and update specific components
3. **Professionalism**: Standard project structure that follows best practices
4. **Scalability**: Easy to add new components without cluttering the repository
5. **Collaboration**: Easier for others to understand and contribute to the project 