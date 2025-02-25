#!/usr/bin/env python3
"""
IEEE 118-Bus System Repository Organization Script

This script organizes the repository according to the structure defined in REPOSITORY_ORGANIZATION.md.
It creates the necessary directories, moves files to appropriate locations, and removes duplicates.
"""

import os
import shutil
import sys
from pathlib import Path

def create_directory_structure():
    """Create the directory structure for the repository."""
    directories = [
        "data/dss",
        "data/modified",
        "data/profiles",
        "src/utils",
        "src/analysis",
        "src/simulation",
        "src/visualization",
        "docs/reports",
        "docs/latex/figures",
        "results/figures/voltage",
        "results/figures/losses",
        "results/figures/time_series",
        "results/data",
        "results/logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def move_files():
    """Move files to their appropriate directories."""
    # Dictionary mapping file patterns to destination directories
    file_mappings = {
        # OpenDSS model files
        "master_file.dss": "data/dss/",
        "lines.dss": "data/dss/",
        "transformers.dss": "data/dss/",
        "generators.dss": "data/dss/",
        "loads.dss": "data/dss/",
        "shunts.dss": "data/dss/",
        "sw_shunts.dss": "data/dss/",
        "dc_and_facts_equiv_elements.dss": "data/dss/",
        "confirm_kv_bases.dss": "data/dss/",
        
        # Modified OpenDSS files
        "master_file_fixed.dss": "data/modified/",
        "generators_fixed.dss": "data/modified/",
        "simplified_circuit.dss": "data/modified/",
        "voltage_stabilized_circuit.dss": "data/modified/",
        "generators_as_vsrcs.dss": "data/modified/",
        
        # Profiles
        "hourly_load_profile.csv": "data/profiles/",
        
        # Utility scripts
        "check_opendss.py": "src/utils/",
        "test_opendss.py": "src/utils/",
        "read_excel.py": "src/utils/",
        
        # Analysis scripts
        "voltage_loss_analysis.py": "src/analysis/",
        "critical_buses.py": "src/analysis/",
        "fix_generators.py": "src/analysis/",
        "fix_swing_bus.py": "src/analysis/",
        "check_convergence.py": "src/analysis/",
        "get_base_losses.py": "src/analysis/",
        
        # Simulation scripts
        "run_opendss.py": "src/simulation/",
        "stabilized_time_series.py": "src/simulation/time_series.py",  # Rename to time_series.py
        "voltage_stabilized_simulation.py": "src/simulation/convergence_fix.py",  # Rename to convergence_fix.py
        
        # Visualization scripts
        "voltage_visualization.py": "src/visualization/voltage_viz.py",  # Rename to voltage_viz.py
        "loss_visualization.py": "src/visualization/loss_viz.py",  # Rename to loss_viz.py
        "network_visualization_fixed.py": "src/visualization/network_viz.py",  # Rename to network_viz.py
        "visualize_time_series.py": "src/visualization/time_series_viz.py",  # Add time_series_viz.py
        
        # Documentation - Markdown reports
        "voltage_profile_report.md": "docs/reports/",
        "loss_analysis_report.md": "docs/reports/",
        "time_series_analysis.md": "docs/reports/",
        "voltage_loss_report.md": "docs/reports/",
        "voltage_violation_analysis.md": "docs/reports/",
        "smart_inverter_implementation.md": "docs/reports/",
        "opendss_explanation.md": "docs/reports/",
        "time_series_solution.md": "docs/reports/",
        
        # Documentation - LaTeX
        "ieee118_bus_report.tex": "docs/latex/main_report.tex",  # Rename to main_report.tex
        "voltage_profile_analysis.tex": "docs/latex/",
        "loss_analysis.tex": "docs/latex/",
        "voltage_loss_analysis.tex": "docs/latex/",
        "time_series_report.tex": "docs/latex/",
        "simplified_time_series_analysis.tex": "docs/latex/",
        "time_series_explanation.tex": "docs/latex/",
        "baseline_analysis_report.tex": "docs/latex/",
        "opendss_python_implementation.tex": "docs/latex/",
        "snapshot_powerflow.tex": "docs/latex/",
        "generator_analysis.tex": "docs/latex/",
        
        # Results - Figures
        "voltage_profile_analysis.png": "results/figures/voltage/",
        "critical_buses_analysis.png": "results/figures/voltage/",
        "critical_bus_improvement.png": "results/figures/voltage/",
        "basic_voltage_loss.png": "results/figures/voltage/",
        "voltage_improvement_trajectory.png": "results/figures/voltage/",
        "regional_voltage_patterns.png": "results/figures/voltage/",
        
        "loss_analysis.png": "results/figures/losses/",
        "loss_relationship.png": "results/figures/losses/",
        "power_loss_analysis.png": "results/figures/losses/",
        "simple_loss_analysis.png": "results/figures/losses/",
        "voltage_loss_analysis.png": "results/figures/losses/",
        "loss_density.png": "results/figures/losses/",
        "loss_by_voltage.png": "results/figures/losses/",
        "voltage_loss_relationship.png": "results/figures/losses/",
        "system_losses.png": "results/figures/losses/",
        "reactive_compensation.png": "results/figures/losses/",
        "regional_losses.png": "results/figures/losses/",
        "major_line_losses.png": "results/figures/losses/",
        "load_vs_losses.png": "results/figures/losses/",
        
        "time_series_results.png": "results/figures/time_series/",
        "time_series_visualization.png": "results/figures/time_series/",
        
        # Results - Data
        "critical_buses_analysis.txt": "results/data/",
        "voltage_loss_analysis.txt": "results/data/",
        "loss_summary.txt": "results/data/",
        "power_loss_summary.txt": "results/data/",
        "simple_loss_summary.txt": "results/data/",
        "simulation_results.txt": "results/data/",
        "hourly_results.csv": "results/data/",
        
        # Results - Logs
        "simulation.log": "results/logs/",
        "ieee118_bus_report.log": "results/logs/"
    }
    
    # Files to delete (duplicates)
    files_to_delete = [
        "generators.dss.bak",
        "simple_loss_viz.py",
        "ascii_loss_viz.py",
        "basic_loss_viz.py",
        "voltage_loss_viz.py",  # Keep only voltage_loss_viz_fixed.py
        "simple_time_series.py",
        "simplified_time_series.py",
        "fixed_time_series.py",
        "robust_time_series.py",  # Keep only stabilized_time_series.py
        "create_folders.py",
        "create_folders.sh",
        "move_files.py",
        "organize.py",
        "organize.sh",
        "organize_files.py",
        "FOLDER_STRUCTURE.md"  # Replaced by REPOSITORY_ORGANIZATION.md
    ]
    
    # Move files according to the mappings
    for source, destination in file_mappings.items():
        if os.path.exists(source):
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # If destination is a directory, keep the original filename
            if destination.endswith("/"):
                dest_path = os.path.join(destination, os.path.basename(source))
            else:
                dest_path = destination
            
            # Move the file
            shutil.copy2(source, dest_path)
            print(f"Moved: {source} -> {dest_path}")
        else:
            print(f"Warning: Source file not found: {source}")
    
    # Delete duplicate files
    for file_to_delete in files_to_delete:
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            print(f"Deleted: {file_to_delete}")
        else:
            print(f"Warning: File to delete not found: {file_to_delete}")

def update_readme():
    """Update README.md with the new repository structure."""
    readme_content = """# IEEE 118-Bus System

This repository contains the IEEE 118-bus system model implemented in OpenDSS, along with analysis scripts, simulation tools, and documentation.

## Repository Structure

- `data/`: Input data files
  - `dss/`: OpenDSS model files
  - `modified/`: Modified OpenDSS files
  - `profiles/`: Time series profiles

- `src/`: Source code
  - `utils/`: Utility functions
  - `analysis/`: Analysis scripts
  - `simulation/`: Simulation scripts
  - `visualization/`: Visualization scripts

- `docs/`: Documentation
  - `reports/`: Markdown reports
  - `latex/`: LaTeX documents

- `results/`: Simulation results
  - `figures/`: Generated figures
  - `data/`: Generated data
  - `logs/`: Simulation logs

## Getting Started

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the OpenDSS simulation:
   ```
   python src/simulation/run_opendss.py
   ```

3. Analyze the results:
   ```
   python src/analysis/voltage_analysis.py
   ```

4. Visualize the results:
   ```
   python src/visualization/voltage_viz.py
   ```

## Documentation

For detailed documentation, please refer to the files in the `docs/` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("Updated README.md with the new repository structure")

def main():
    """Main function to organize the repository."""
    print("Starting repository organization...")
    
    # Create the directory structure
    create_directory_structure()
    
    # Move files to appropriate directories
    move_files()
    
    # Update README.md
    update_readme()
    
    print("\nRepository organization complete!")
    print("Please review the changes and make any necessary adjustments.")
    print("Note: You may need to update import paths in Python scripts manually.")

if __name__ == "__main__":
    main() 