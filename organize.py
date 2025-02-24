import os
import shutil

# Create main directories
os.makedirs('src', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('docs', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Create subdirectories
os.makedirs('src/simulation', exist_ok=True)
os.makedirs('src/visualization', exist_ok=True)
os.makedirs('src/diagnostics', exist_ok=True)
os.makedirs('src/dss_files', exist_ok=True)
os.makedirs('data/input', exist_ok=True)
os.makedirs('data/output', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)
os.makedirs('results/reports', exist_ok=True)
os.makedirs('docs/latex', exist_ok=True)
os.makedirs('docs/markdown', exist_ok=True)

print("Created directory structure")

# Define file groups
simulation_files = [
    'stabilized_time_series.py',
    'fixed_time_series.py',
    'simplified_time_series.py',
    'robust_time_series.py',
    'simple_time_series.py'
]

visualization_files = [
    'network_visualization.py',
    'voltage_visualization.py',
    'visualize_time_series.py',
    'simple_visualization.py',
    'loss_visualization.py',
    'simple_loss_viz.py',
    'voltage_loss_viz.py',
    'voltage_loss_analysis.py'
]

diagnostic_files = [
    'diagnose_convergence.py',
    'check_convergence.py',
    'voltage_stabilized_simulation.py',
    'fix_swing_bus.py',
    'fix_generators.py',
    'test_opendss.py'
]

dss_files = [
    'master_file.dss',
    'generators.dss',
    'lines.dss',
    'transformers.dss',
    'loads.dss',
    'shunts.dss',
    'sw_shunts.dss',
    'generators_fixed.dss',
    'master_file_fixed.dss'
]

markdown_docs = [
    'README.md',
    'time_series_solution.md',
    'loss_explanation.md',
    'opendss_explanation.md',
    'time_series_analysis.md',
    'voltage_profile_report.md'
]

latex_docs = [
    'ieee118_bus_report.tex',
    'generator_analysis.tex',
    'snapshot_powerflow.tex',
    'voltage_profile_analysis.tex',
    'time_series_explanation.tex'
]

# Copy files to their destinations
def copy_files(files, destination):
    for file in files:
        if os.path.exists(file):
            try:
                shutil.copy2(file, os.path.join(destination, file))
                print(f"Copied {file} to {destination}")
            except Exception as e:
                print(f"Error copying {file}: {str(e)}")
        else:
            print(f"Warning: File {file} not found")

# Copy files to their respective directories
copy_files(simulation_files, 'src/simulation')
copy_files(visualization_files, 'src/visualization')
copy_files(diagnostic_files, 'src/diagnostics')
copy_files(dss_files, 'src/dss_files')
copy_files(markdown_docs, 'docs/markdown')
copy_files(latex_docs, 'docs/latex')

# Copy existing directories
if os.path.exists('simulation_results'):
    if not os.path.exists('results/time_series'):
        os.makedirs('results/time_series', exist_ok=True)
    for item in os.listdir('simulation_results'):
        src = os.path.join('simulation_results', item)
        dst = os.path.join('results/time_series', item)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        except Exception as e:
            print(f"Error copying {src}: {str(e)}")

if os.path.exists('thesis_figures'):
    if not os.path.exists('results/figures'):
        os.makedirs('results/figures', exist_ok=True)
    for item in os.listdir('thesis_figures'):
        src = os.path.join('thesis_figures', item)
        dst = os.path.join('results/figures', item)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
        except Exception as e:
            print(f"Error copying {src}: {str(e)}")

print("\nFile organization complete!")
print("\nNOTE: Original files have not been deleted. After verifying the organization,")
print("you may want to clean up the root directory by removing the original files.") 