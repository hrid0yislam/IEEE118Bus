import os
import shutil

# Create directory structure
def create_directories():
    directories = [
        # Main directories
        'src',
        'data',
        'docs',
        'results',
        
        # Source code subdirectories
        'src/simulation',
        'src/visualization',
        'src/diagnostics',
        'src/utilities',
        
        # DSS files
        'src/dss_files',
        'src/dss_files/base',
        'src/dss_files/modified',
        
        # Data directories
        'data/input',
        'data/output',
        
        # Results directories
        'results/figures',
        'results/reports',
        'results/time_series',
        
        # Documentation
        'docs/latex',
        'docs/markdown'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

# File categorization
def organize_files():
    # Define file mappings
    file_mappings = {
        # Simulation scripts
        'src/simulation': [
            'stabilized_time_series.py',
            'fixed_time_series.py',
            'simplified_time_series.py',
            'robust_time_series.py',
            'simple_time_series.py',
            'time_series_simulation.py'
        ],
        
        # Visualization scripts
        'src/visualization': [
            'network_visualization.py',
            'network_visualization_fixed.py',
            'voltage_visualization.py',
            'voltage_profile_visualization.py',
            'visualize_time_series.py',
            'simple_visualization.py',
            'loss_visualization.py',
            'simple_loss_viz.py',
            'voltage_loss_viz.py',
            'voltage_loss_viz_fixed.py',
            'voltage_loss_analysis.py',
            'loss_relationship_viz.py',
            'voltage_improvement_viz.py',
            'critical_bus_improvement.py',
            'critical_buses.py',
            'plot_losses.py',
            'ascii_loss_viz.py',
            'basic_loss_viz.py'
        ],
        
        # Diagnostic scripts
        'src/diagnostics': [
            'diagnose_convergence.py',
            'check_convergence.py',
            'voltage_stabilized_simulation.py',
            'fix_swing_bus.py',
            'fix_generators.py',
            'get_base_losses.py',
            'test_opendss.py',
            'check_opendss.py',
            'test_voltage_read.py'
        ],
        
        # Utility scripts
        'src/utilities': [
            'read_excel.py',
            'run_opendss.py',
            'hello.py'
        ],
        
        # Base DSS files
        'src/dss_files/base': [
            'master_file.dss',
            'generators.dss',
            'lines.dss',
            'transformers.dss',
            'loads.dss',
            'shunts.dss',
            'sw_shunts.dss',
            'dc_and_facts_equiv_elements.dss',
            'confirm_kv_bases.dss',
            'generators_as_vsrcs.dss'
        ],
        
        # Modified DSS files
        'src/dss_files/modified': [
            'generators_fixed.dss',
            'master_file_fixed.dss',
            'generators.dss.bak',
            'voltage_stabilized_circuit.dss',
            'simplified_circuit.dss'
        ],
        
        # Input data
        'data/input': [
            'hourly_load_profile.csv',
            'Comparissons.xlsx'
        ],
        
        # Output data
        'data/output': [
            'ieee118bus_VLN_Node.txt',
            'ieee118bus_Power_elem_MVA.txt',
            'ieee118bus_Losses.txt'
        ],
        
        # Result figures
        'results/figures': [
            'time_series_results.png',
            'simple_loss_analysis.png',
            'loss_analysis.png',
            'loss_relationship.png',
            'critical_buses_analysis.png',
            'power_loss_analysis.png',
            'basic_voltage_loss.png',
            'critical_bus_improvement.png',
            'voltage_profile.png',
            'network_voltage_loss.png',
            'system_losses.png',
            'reactive_compensation.png',
            'regional_losses.png',
            'major_line_losses.png',
            'voltage_improvement_trajectory.png',
            'voltage_loss_relationship.png',
            'loss_density.png',
            'loss_by_voltage.png',
            'voltage_profile_analysis.png',
            'time_series_visualization.png',
            'regional_voltage_patterns.png',
            'load_vs_losses.png',
            'network_topology.png',
            'error_analysis.png',
            'power_comparison.png'
        ],
        
        # Result reports
        'results/reports': [
            'time_series_results.txt',
            'simple_loss_summary.txt',
            'simulation_results.txt',
            'loss_summary.txt',
            'critical_buses_analysis.txt',
            'power_loss_summary.txt',
            'voltage_loss_analysis.txt',
            'network_analysis.txt',
            'critical_bus_analysis.txt',
            'voltage_summary.txt',
            'network_statistics.txt',
            'statistics.txt',
            'hourly_results.csv',
            'simulation.log'
        ],
        
        # LaTeX documents
        'docs/latex': [
            'ieee118_bus_report.tex',
            'generator_analysis.tex',
            'snapshot_powerflow.tex',
            'voltage_profile_analysis.tex',
            'baseline_analysis_report.tex',
            'opendss_python_implementation.tex',
            'voltage_loss_analysis.tex',
            'loss_analysis.tex',
            'smart_inverter_plan.tex',
            'time_series_explanation.tex',
            'simplified_time_series_analysis.tex',
            'test_compile.tex',
            'time_series_report.tex',
            'ieee118_bus_report.pdf',
            'generator_analysis.pdf',
            'snapshot_powerflow.pdf',
            'opendss_python_implementation.pdf'
        ],
        
        # Markdown documents
        'docs/markdown': [
            'README.md',
            'time_series_solution.md',
            'loss_explanation.md',
            'opendss_explanation.md',
            'time_series_analysis.md',
            'voltage_profile_report.md',
            'loss_analysis_report.md',
            'voltage_loss_report.md',
            'voltage_violation_analysis.md',
            'smart_inverter_implementation.md',
            'thesis_report.md'
        ]
    }
    
    # Copy files to their destinations
    for dest_dir, files in file_mappings.items():
        for file in files:
            if os.path.exists(file):
                try:
                    shutil.copy2(file, os.path.join(dest_dir, file))
                    print(f"Copied {file} to {dest_dir}")
                except Exception as e:
                    print(f"Error copying {file}: {str(e)}")
            else:
                print(f"Warning: File {file} not found")

# Move existing directories
def move_existing_directories():
    dir_mappings = {
        'simulation_results': 'results/time_series',
        'thesis_figures': 'results/figures/thesis',
        'latex_report': 'docs/latex/reports',
        'xlsx_files': 'data/input/xlsx'
    }
    
    for src_dir, dest_dir in dir_mappings.items():
        if os.path.exists(src_dir) and os.path.isdir(src_dir):
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copy contents instead of moving the directory
            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
                d = os.path.join(dest_dir, item)
                try:
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                        print(f"Copied directory {s} to {d}")
                    else:
                        shutil.copy2(s, d)
                        print(f"Copied file {s} to {d}")
                except Exception as e:
                    print(f"Error copying {s}: {str(e)}")

# Create requirements.txt in the root directory
def create_requirements():
    if os.path.exists('requirements.txt'):
        shutil.copy2('requirements.txt', 'requirements.txt.bak')
        print("Backed up existing requirements.txt")
    
    with open('requirements.txt', 'w') as f:
        f.write("""# IEEE 118-Bus System Analysis Requirements
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
opendssdirect.py>=0.8.4
pandas>=2.0.0
networkx>=3.1
""")
    print("Created requirements.txt")

# Main function
def main():
    print("Starting file organization...")
    create_directories()
    organize_files()
    move_existing_directories()
    create_requirements()
    print("\nFile organization complete!")
    print("\nNOTE: Original files have not been deleted. After verifying the organization,")
    print("you may want to clean up the root directory by removing the original files.")

if __name__ == "__main__":
    main() 