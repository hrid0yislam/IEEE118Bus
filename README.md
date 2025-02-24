# Time Series Analysis of IEEE 118-Bus System

## Overview
This repository contains a comprehensive time series analysis of the IEEE 118-bus power system, focusing on voltage profiles, system losses, and load variations over a 24-hour period.

## Key Components

### 1. Load Profile Analysis
- **Peak Periods**: 11:00 and 18:00 (100% loading)
- **Minimum Load**: 04:00 (55% loading)
- **Load Variations**:
  * Morning Ramp: 05:00-11:00 (55% → 100%)
  * Evening Ramp: 16:00-18:00 (93% → 100%)
  * Night Decline: 19:00-23:00 (97% → 68%)

### 2. Voltage Profile Analysis

#### Critical Bus Voltages
| Bus | Base Voltage (pu) | Status |
|-----|------------------|---------|
| 89_CLINCHRV | 0.678 | Highest |
| 69_SPORN | 0.161 | Critical |
| 77_TURNER | 0.227 | Critical |
| 92_SALTVLLE | 0.550 | Concerning |

#### Regional Distribution
- **Northern Region**: 0.161-0.350 pu (Most critical)
- **Central Region**: 0.450-0.550 pu (Below normal)
- **Southern Region**: 0.550-0.678 pu (Best performing)

### 3. System Losses

#### Loss Components
- **Line Losses**: 76,353.20 kW (99.996%)
- **Transformer Losses**: 30.54 kW (0.004%)
- **Total Base Losses**: 76,383.74 kW

#### Loss Variation
- **Peak Hours**: ~76 MW
- **Minimum Load**: ~23 MW
- **Relationship**: Quadratic with loading (I²R losses)

## Implementation Details

### 1. Time Series Simulation
```python
# Hourly load multipliers
load_multipliers = [0.65, 0.60, 0.58, 0.56, 0.55, 0.57, 0.62, 0.72, 0.85, 
                   0.95, 0.98, 1.00, 0.99, 0.97, 0.95, 0.93, 0.94, 0.98, 
                   1.00, 0.97, 0.92, 0.85, 0.75, 0.68]
```

### 2. Analysis Parameters
- **Time Steps**: 24 hours
- **Base Voltage**: 138 kV
- **Monitoring Points**: 118 buses
- **Critical Buses**: 4 monitored locations

## Key Findings

### 1. Voltage Violations
- All buses operate below nominal voltage
- No buses within acceptable range (0.95-1.05 pu)
- Most severe violations in northern region
- Voltage variations follow load pattern

### 2. Loss Characteristics
- Quadratic relationship with loading confirmed
- Line losses dominate system losses
- Peak losses coincide with maximum loading
- Regional loss concentration in heavily loaded areas

### 3. System Performance
- **Voltage Stability**: Concerning (all buses below 0.95 pu)
- **Loss Efficiency**: Poor (high percentage of total power)
- **Regional Disparities**: Significant north-south variation

## Recommendations

### Immediate Actions (1-2 months)
1. **Voltage Support**
   - Install capacitor banks:
     * Bus 69_SPORN: 150 MVAR
     * Bus 77_TURNER: 100 MVAR
   - Adjust transformer taps
   - Implement local voltage control

2. **Loss Reduction**
   - Optimize power flow
   - Balance loading
   - Monitor critical lines

### Medium-term Solutions (3-6 months)
1. **System Upgrades**
   - Install SVCs at critical buses
   - Network reconfiguration
   - Control system improvements

2. **Monitoring Enhancement**
   - Real-time voltage monitoring
   - Loss tracking system
   - Performance metrics

### Long-term Improvements (6+ months)
1. **Infrastructure**
   - Network reinforcement
   - New transmission lines
   - Substation upgrades

2. **Smart Grid Integration**
   - Advanced control systems
   - Dynamic optimization
   - Automated responses

## Technical Implementation

### 1. Simulation Framework
```python
# Key components
- Load scaling at each hour
- Power flow solution
- Data collection
- Result analysis
```

### 2. Visualization Tools
- Load profile plots
- Voltage variation charts
- Loss analysis graphs
- Regional comparisons

### 3. Data Management
- Time series data storage
- Performance metrics
- Analysis results
- Visualization outputs

## Results Summary

### 1. Voltage Performance
- **Maximum Voltage**: 0.678 pu (Below normal)
- **Minimum Voltage**: 0.161 pu (Critical)
- **Average Voltage**: 0.419 pu (Poor)
- **Violations**: 100% of buses

### 2. Loss Analysis
- **Peak Losses**: 76.38 MW
- **Minimum Losses**: 23.06 MW
- **Average Losses**: 49.72 MW
- **Loss Factor**: 0.3048

### 3. System Metrics
- **Voltage Stability Margin**: Negative
- **Loss Percentage**: 30.48%
- **Critical Buses**: 3
- **Affected Regions**: All

## Future Work

### 1. Analysis Extensions
- Dynamic stability assessment
- Contingency analysis
- Economic impact study
- Reliability evaluation

### 2. Tool Enhancements
- Real-time monitoring
- Automated reporting
- Advanced visualization
- Predictive analytics

## Repository Structure
```
.
├── time_series_simulation.py
├── visualize_time_series.py
├── data/
│   ├── load_profiles/
│   ├── voltage_data/
│   └── loss_analysis/
├── results/
│   ├── figures/
│   └── reports/
└── docs/
```

## Usage
1. Run time series simulation
2. Generate visualizations
3. Analyze results
4. Review recommendations

## Dependencies
- Python 3.x
- NumPy
- Matplotlib
- OpenDSS
- Pandas 

# IEEE 118-Bus System Time Series Simulation

This repository contains scripts for running time series simulations on the IEEE 118-bus system using OpenDSS. The scripts address convergence issues that commonly occur with this complex system.

## Problem Overview

The IEEE 118-bus system time series simulation was failing to converge due to several issues:

1. **Missing Swing Bus**: The swing bus (Bus 89_CLINCHRV) was commented out in the generators.dss file.
2. **Voltage Instability**: The system experiences extreme voltage values during the convergence process.
3. **Convergence Settings**: The default convergence settings were too strict for this complex system.
4. **Component Loading Order**: The order in which components are loaded affects convergence.

## Solution Approach

The solution involves several key strategies:

1. **Fix the Swing Bus**: Uncomment the swing bus generator in the generators.dss file.
2. **Voltage Stabilization**: Initialize the circuit with a controlled approach to stabilize voltages.
3. **Progressive Component Loading**: Add components gradually and solve after each addition.
4. **Very Relaxed Convergence Settings**: Use relaxed tolerance and increased iterations.
5. **Load Scaling**: Start with very low load levels (1%) and gradually increase.

## Scripts

### 1. `voltage_stabilized_simulation.py`

This script diagnoses the convergence issues and determines the maximum load level at which the system can converge.

```bash
python voltage_stabilized_simulation.py
```

### 2. `stabilized_time_series.py`

This script runs a full 24-hour time series simulation using the voltage stabilization approach.

```bash
python stabilized_time_series.py
```

### 3. `fix_swing_bus.py`

This script fixes the swing bus issue by uncommenting the swing bus generator in the generators.dss file.

```bash
python fix_swing_bus.py
```

### 4. `diagnose_convergence.py`

This script diagnoses convergence issues by testing different component combinations and load levels.

```bash
python diagnose_convergence.py
```

## Key Features

1. **Robust Error Handling**: All scripts include comprehensive error handling to catch and report issues.
2. **Progressive Loading**: The scripts use a gradual approach to loading the system to ensure convergence.
3. **Multiple Solution Attempts**: The scripts try multiple solution options with different algorithms and tolerances.
4. **Detailed Reporting**: The scripts generate detailed reports and visualizations of the results.

## Results

The scripts generate the following outputs in the `simulation_results` directory:

1. **Time Series Results**: A text file with detailed results for each hour of the simulation.
2. **Visualizations**: PNG files showing the load profile, voltage profile, and system losses over time.
3. **Load-Loss Relationship**: A visualization and analysis of the quadratic relationship between load level and losses.

## Recommendations for Use

1. **Start with Diagnosis**: Run `voltage_stabilized_simulation.py` first to determine the maximum load level.
2. **Adjust Load Factor**: Modify the `max_load_factor` in `stabilized_time_series.py` based on the diagnosis.
3. **Monitor Convergence**: Watch for convergence issues during the simulation and adjust settings if needed.
4. **Check Results**: Verify that the results make sense by examining the visualizations and summary statistics.

## Requirements

- Python 3.6 or higher
- OpenDSS Direct (opendssdirect.py)
- NumPy
- Matplotlib

Install the required packages using:

```bash
pip install opendssdirect numpy matplotlib
```

## Troubleshooting

If you encounter issues:

1. **Verify OpenDSS Installation**: Make sure OpenDSS Direct is installed correctly.
2. **Check File Paths**: Ensure all required DSS files are in the correct location.
3. **Reduce Load Factor**: Try reducing the `max_load_factor` in `stabilized_time_series.py`.
4. **Increase Tolerance**: Try increasing the tolerance in the solution options.
5. **Check Swing Bus**: Verify that the swing bus is properly defined in the generators file.

## References

- IEEE 118-bus system documentation
- OpenDSS documentation
- Power system analysis techniques 

Files in the repository: [NEED TO BE DOUBLECHECKED]
- **master_file.dss**: Main DSS file that loads all other components
- **master_file_fixed.dss**: Fixed version of the master file
- **generators.dss**: Original generator definitions with commented-out swing bus
- **generators_fixed.dss**: Fixed generator definitions with uncommented swing bus
- **lines.dss**: Line definitions
- **loads.dss**: Load definitions
- **shunts.dss**: Shunt definitions
- **voltage_stabilized_circuit.dss**: Circuit with voltage stabilization measures
- **simplified_circuit.dss**: Simplified version of the circuit

### Simulation Scripts

- **stabilized_time_series.py**: Main time series simulation with voltage stabilization
- **voltage_stabilized_simulation.py**: Diagnoses convergence issues and determines maximum load level
- **fixed_time_series.py**: Fixed version of time series simulation
- **simplified_time_series.py**: Simplified version of time series simulation
- **robust_time_series.py**: Robust version of time series simulation
- **simple_time_series.py**: Simple version of time series simulation

### Diagnostic Scripts

- **diagnose_convergence.py**: Diagnoses convergence issues
- **check_convergence.py**: Checks convergence
- **fix_swing_bus.py**: Fixes swing bus issues
- **fix_generators.py**: Fixes generator issues
- **test_opendss.py**: Tests OpenDSS installation
- **check_opendss.py**: Checks OpenDSS functionality

### Visualization Scripts

- **network_visualization.py**: Network visualization
- **voltage_visualization.py**: Voltage profile visualization
- **visualize_time_series.py**: Time series visualization
- **loss_visualization.py**: Loss visualization
- **simple_loss_viz.py**: Simple loss visualization
- **voltage_loss_viz.py**: Voltage loss visualization
- **voltage_loss_analysis.py**: Voltage loss analysis

### Data Files

- **ieee118bus_VLN_Node.txt**: Voltage data
- **ieee118bus_Power_elem_MVA.txt**: Power flow data
- **ieee118bus_Losses.txt**: Loss data

### Documentation

- **time_series_solution.md**: Detailed solution for time series simulation
- **opendss_explanation.md**: Explanation of OpenDSS functionality
- **FOLDER_STRUCTURE.md**: Recommended folder structure for the repository
