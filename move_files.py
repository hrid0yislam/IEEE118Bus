import os
import shutil

# Define file mappings
file_mappings = {
    # Simulation files
    'stabilized_time_series.py': 'src/simulation/',
    'fixed_time_series.py': 'src/simulation/',
    'simplified_time_series.py': 'src/simulation/',
    'robust_time_series.py': 'src/simulation/',
    'simple_time_series.py': 'src/simulation/',
    
    # Visualization files
    'network_visualization.py': 'src/visualization/',
    'voltage_visualization.py': 'src/visualization/',
    'visualize_time_series.py': 'src/visualization/',
    'simple_visualization.py': 'src/visualization/',
    'loss_visualization.py': 'src/visualization/',
    'simple_loss_viz.py': 'src/visualization/',
    'voltage_loss_viz.py': 'src/visualization/',
    'voltage_loss_analysis.py': 'src/visualization/',
    
    # Diagnostic files
    'diagnose_convergence.py': 'src/diagnostics/',
    'check_convergence.py': 'src/diagnostics/',
    'voltage_stabilized_simulation.py': 'src/diagnostics/',
    'fix_swing_bus.py': 'src/diagnostics/',
    'fix_generators.py': 'src/diagnostics/',
    'test_opendss.py': 'src/diagnostics/',
    
    # DSS files
    'master_file.dss': 'src/dss_files/base/',
    'generators.dss': 'src/dss_files/base/',
    'lines.dss': 'src/dss_files/base/',
    'transformers.dss': 'src/dss_files/base/',
    'loads.dss': 'src/dss_files/base/',
    'shunts.dss': 'src/dss_files/base/',
    'sw_shunts.dss': 'src/dss_files/base/',
    'dc_and_facts_equiv_elements.dss': 'src/dss_files/base/',
    'confirm_kv_bases.dss': 'src/dss_files/base/',
    'generators_as_vsrcs.dss': 'src/dss_files/base/',
    
    # Modified DSS files
    'generators_fixed.dss': 'src/dss_files/modified/',
    'master_file_fixed.dss': 'src/dss_files/modified/',
    'generators.dss.bak': 'src/dss_files/modified/',
    'voltage_stabilized_circuit.dss': 'src/dss_files/modified/',
    'simplified_circuit.dss': 'src/dss_files/modified/',
    
    # Data files
    'ieee118bus_VLN_Node.txt': 'data/output/',
    'ieee118bus_Power_elem_MVA.txt': 'data/output/',
    'ieee118bus_Losses.txt': 'data/output/',
    
    # Markdown docs
    'README.md': 'docs/markdown/',
    'time_series_solution.md': 'docs/markdown/',
    'loss_explanation.md': 'docs/markdown/',
    'opendss_explanation.md': 'docs/markdown/',
    'time_series_analysis.md': 'docs/markdown/',
    'voltage_profile_report.md': 'docs/markdown/',
    'FOLDER_STRUCTURE.md': 'docs/markdown/',
    
    # LaTeX docs
    'ieee118_bus_report.tex': 'docs/latex/',
    'generator_analysis.tex': 'docs/latex/',
    'snapshot_powerflow.tex': 'docs/latex/',
    'voltage_profile_analysis.tex': 'docs/latex/',
    'time_series_explanation.tex': 'docs/latex/',
    'simplified_time_series_analysis.tex': 'docs/latex/',
    'test_compile.tex': 'docs/latex/'
}

# Create directories
for directory in set(file_mappings.values()):
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Copy files to their destinations
for file, destination in file_mappings.items():
    if os.path.exists(file):
        try:
            shutil.copy2(file, os.path.join(destination, file))
            print(f"Copied {file} to {destination}")
        except Exception as e:
            print(f"Error copying {file}: {str(e)}")
    else:
        print(f"Warning: File {file} not found")

print("\nFile organization complete!")
print("Original files have not been deleted. After verifying the organization,")
print("you may want to clean up the root directory by removing the original files.") 