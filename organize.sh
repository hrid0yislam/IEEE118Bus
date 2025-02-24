#!/bin/bash

# Create directory structure
echo "Creating directory structure..."

# Main directories
mkdir -p src/simulation
mkdir -p src/visualization
mkdir -p src/diagnostics
mkdir -p src/dss_files
mkdir -p data/input
mkdir -p data/output
mkdir -p results/figures
mkdir -p results/reports
mkdir -p results/time_series
mkdir -p docs/latex
mkdir -p docs/markdown

echo "Directory structure created."

# Copy simulation files
echo "Copying simulation files..."
cp stabilized_time_series.py src/simulation/ 2>/dev/null || echo "Warning: stabilized_time_series.py not found"
cp fixed_time_series.py src/simulation/ 2>/dev/null || echo "Warning: fixed_time_series.py not found"
cp simplified_time_series.py src/simulation/ 2>/dev/null || echo "Warning: simplified_time_series.py not found"
cp robust_time_series.py src/simulation/ 2>/dev/null || echo "Warning: robust_time_series.py not found"
cp simple_time_series.py src/simulation/ 2>/dev/null || echo "Warning: simple_time_series.py not found"

# Copy visualization files
echo "Copying visualization files..."
cp network_visualization.py src/visualization/ 2>/dev/null || echo "Warning: network_visualization.py not found"
cp voltage_visualization.py src/visualization/ 2>/dev/null || echo "Warning: voltage_visualization.py not found"
cp visualize_time_series.py src/visualization/ 2>/dev/null || echo "Warning: visualize_time_series.py not found"
cp simple_visualization.py src/visualization/ 2>/dev/null || echo "Warning: simple_visualization.py not found"
cp loss_visualization.py src/visualization/ 2>/dev/null || echo "Warning: loss_visualization.py not found"
cp simple_loss_viz.py src/visualization/ 2>/dev/null || echo "Warning: simple_loss_viz.py not found"
cp voltage_loss_viz.py src/visualization/ 2>/dev/null || echo "Warning: voltage_loss_viz.py not found"
cp voltage_loss_analysis.py src/visualization/ 2>/dev/null || echo "Warning: voltage_loss_analysis.py not found"

# Copy diagnostic files
echo "Copying diagnostic files..."
cp diagnose_convergence.py src/diagnostics/ 2>/dev/null || echo "Warning: diagnose_convergence.py not found"
cp check_convergence.py src/diagnostics/ 2>/dev/null || echo "Warning: check_convergence.py not found"
cp voltage_stabilized_simulation.py src/diagnostics/ 2>/dev/null || echo "Warning: voltage_stabilized_simulation.py not found"
cp fix_swing_bus.py src/diagnostics/ 2>/dev/null || echo "Warning: fix_swing_bus.py not found"
cp fix_generators.py src/diagnostics/ 2>/dev/null || echo "Warning: fix_generators.py not found"
cp test_opendss.py src/diagnostics/ 2>/dev/null || echo "Warning: test_opendss.py not found"

# Copy DSS files
echo "Copying DSS files..."
cp master_file.dss src/dss_files/ 2>/dev/null || echo "Warning: master_file.dss not found"
cp generators.dss src/dss_files/ 2>/dev/null || echo "Warning: generators.dss not found"
cp lines.dss src/dss_files/ 2>/dev/null || echo "Warning: lines.dss not found"
cp transformers.dss src/dss_files/ 2>/dev/null || echo "Warning: transformers.dss not found"
cp loads.dss src/dss_files/ 2>/dev/null || echo "Warning: loads.dss not found"
cp shunts.dss src/dss_files/ 2>/dev/null || echo "Warning: shunts.dss not found"
cp sw_shunts.dss src/dss_files/ 2>/dev/null || echo "Warning: sw_shunts.dss not found"
cp generators_fixed.dss src/dss_files/ 2>/dev/null || echo "Warning: generators_fixed.dss not found"
cp master_file_fixed.dss src/dss_files/ 2>/dev/null || echo "Warning: master_file_fixed.dss not found"

# Copy markdown docs
echo "Copying markdown documents..."
cp README.md docs/markdown/ 2>/dev/null || echo "Warning: README.md not found"
cp time_series_solution.md docs/markdown/ 2>/dev/null || echo "Warning: time_series_solution.md not found"
cp loss_explanation.md docs/markdown/ 2>/dev/null || echo "Warning: loss_explanation.md not found"
cp opendss_explanation.md docs/markdown/ 2>/dev/null || echo "Warning: opendss_explanation.md not found"
cp time_series_analysis.md docs/markdown/ 2>/dev/null || echo "Warning: time_series_analysis.md not found"
cp voltage_profile_report.md docs/markdown/ 2>/dev/null || echo "Warning: voltage_profile_report.md not found"

# Copy LaTeX docs
echo "Copying LaTeX documents..."
cp ieee118_bus_report.tex docs/latex/ 2>/dev/null || echo "Warning: ieee118_bus_report.tex not found"
cp generator_analysis.tex docs/latex/ 2>/dev/null || echo "Warning: generator_analysis.tex not found"
cp snapshot_powerflow.tex docs/latex/ 2>/dev/null || echo "Warning: snapshot_powerflow.tex not found"
cp voltage_profile_analysis.tex docs/latex/ 2>/dev/null || echo "Warning: voltage_profile_analysis.tex not found"
cp time_series_explanation.tex docs/latex/ 2>/dev/null || echo "Warning: time_series_explanation.tex not found"

# Copy data files
echo "Copying data files..."
cp ieee118bus_VLN_Node.txt data/output/ 2>/dev/null || echo "Warning: ieee118bus_VLN_Node.txt not found"
cp ieee118bus_Power_elem_MVA.txt data/output/ 2>/dev/null || echo "Warning: ieee118bus_Power_elem_MVA.txt not found"
cp ieee118bus_Losses.txt data/output/ 2>/dev/null || echo "Warning: ieee118bus_Losses.txt not found"

# Copy existing directories
echo "Copying existing directories..."

# Copy simulation_results
if [ -d "simulation_results" ]; then
    echo "Copying simulation_results directory..."
    cp -r simulation_results/* results/time_series/ 2>/dev/null
fi

# Copy thesis_figures
if [ -d "thesis_figures" ]; then
    echo "Copying thesis_figures directory..."
    cp -r thesis_figures/* results/figures/ 2>/dev/null
fi

# Copy latex_report
if [ -d "latex_report" ]; then
    echo "Copying latex_report directory..."
    mkdir -p docs/latex/reports
    cp -r latex_report/* docs/latex/reports/ 2>/dev/null
fi

# Copy xlsx_files
if [ -d "xlsx_files" ]; then
    echo "Copying xlsx_files directory..."
    mkdir -p data/input/xlsx
    cp -r xlsx_files/* data/input/xlsx/ 2>/dev/null
fi

echo "File organization complete!"
echo ""
echo "NOTE: Original files have not been deleted. After verifying the organization,"
echo "you may want to clean up the root directory by removing the original files." 