#!/usr/bin/env python3
"""
Final Cleanup Script for IEEE 118-Bus System Repository

This script handles the remaining files in the root directory.
"""

import os
import shutil
import sys
from pathlib import Path

def move_remaining_python_files():
    """Move remaining Python files to their appropriate directories."""
    # Dictionary mapping Python files to destination directories
    py_file_mappings = {
        # Utils
        "test_opendss.py": "src/utils/",
        "read_excel.py": "src/utils/",
        "check_opendss.py": "src/utils/",
        
        # Analysis
        "fix_generators.py": "src/analysis/",
        "fix_swing_bus.py": "src/analysis/",
        "check_convergence.py": "src/analysis/",
        "get_base_losses.py": "src/analysis/",
        "critical_buses.py": "src/analysis/",
        
        # Simulation
        "run_opendss.py": "src/simulation/",
        "stabilized_time_series.py": "src/simulation/",
        "voltage_stabilized_simulation.py": "src/simulation/",
        
        # Visualization
        "voltage_visualization.py": "src/visualization/",
        "loss_visualization.py": "src/visualization/",
        "network_visualization_fixed.py": "src/visualization/",
        "visualize_time_series.py": "src/visualization/",
    }
    
    # Move files according to the mappings
    for source, destination in py_file_mappings.items():
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
            
            # Remove the original file
            os.remove(source)
            print(f"Removed original: {source}")
        else:
            print(f"Warning: Source file not found: {source}")

def move_remaining_dss_files():
    """Move remaining DSS files to their appropriate directories."""
    # Dictionary mapping DSS files to destination directories
    dss_file_mappings = {
        # Original DSS files
        "generators.dss": "data/dss/",
        "lines.dss": "data/dss/",
        "transformers.dss": "data/dss/",
        "loads.dss": "data/dss/",
        "shunts.dss": "data/dss/",
        "sw_shunts.dss": "data/dss/",
        "confirm_kv_bases.dss": "data/dss/",
        "dc_and_facts_equiv_elements.dss": "data/dss/",
        "master_file.dss": "data/dss/",
        
        # Modified DSS files
        "generators_fixed.dss": "data/modified/",
        "generators_as_vsrcs.dss": "data/modified/",
        "master_file_fixed.dss": "data/modified/",
        "simplified_circuit.dss": "data/modified/",
    }
    
    # Move files according to the mappings
    for source, destination in dss_file_mappings.items():
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
            
            # Remove the original file
            os.remove(source)
            print(f"Removed original: {source}")
        else:
            print(f"Warning: Source file not found: {source}")

def clean_up_organization_scripts():
    """Clean up the organization scripts."""
    # List of organization scripts to move to a new 'scripts' directory
    organization_scripts = [
        "organize_repository.py",
        "complete_organization.py",
        "final_cleanup.py",
        "REPOSITORY_ORGANIZATION.md"
    ]
    
    # Create scripts directory
    os.makedirs("scripts", exist_ok=True)
    
    # Move organization scripts
    for script in organization_scripts:
        if os.path.exists(script):
            dest_path = os.path.join("scripts", script)
            shutil.copy2(script, dest_path)
            print(f"Moved organization script: {script} -> {dest_path}")

def main():
    """Main function to perform final cleanup."""
    print("Starting final cleanup...")
    
    # Move remaining Python files
    move_remaining_python_files()
    
    # Move remaining DSS files
    move_remaining_dss_files()
    
    # Clean up organization scripts
    clean_up_organization_scripts()
    
    # Check if there are any remaining files in the root directory
    remaining_files = [f for f in os.listdir(".") if os.path.isfile(f) and 
                      f not in [".gitignore", "README.md", "requirements.txt"]]
    
    if remaining_files:
        print("\nRemaining files in root directory:")
        for file in remaining_files:
            print(f"  - {file}")
        print("\nConsider manually moving these files to appropriate directories.")
    else:
        print("\nAll files have been organized successfully!")
    
    print("\nFinal cleanup complete!")
    print("The repository is now organized according to the structure defined in REPOSITORY_ORGANIZATION.md.")

if __name__ == "__main__":
    main() 