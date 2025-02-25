#!/usr/bin/env python3
"""
Final Remaining Cleanup Script for IEEE 118-Bus System Repository

This script handles the remaining files in the root directory.
"""

import os
import shutil
import sys
from pathlib import Path

def move_remaining_files():
    """Move remaining files to their appropriate directories."""
    # Dictionary mapping files to destination directories
    file_mappings = {
        # Documentation - Markdown reports
        "loss_analysis_report.md": "docs/reports/",
        "smart_inverter_implementation.md": "docs/reports/",
        "voltage_loss_report.md": "docs/reports/",
        "opendss_explanation.md": "docs/reports/",
        "voltage_violation_analysis.md": "docs/reports/",
        "voltage_profile_report.md": "docs/reports/",
        "time_series_solution.md": "docs/reports/",
        "time_series_analysis.md": "docs/reports/",
        
        # Documentation - LaTeX
        "simplified_time_series_analysis.tex": "docs/latex/",
        "time_series_explanation.tex": "docs/latex/",
        "time_series_report.tex": "docs/latex/",
    }
    
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
            
            # Remove the original file
            os.remove(source)
            print(f"Removed original: {source}")
        else:
            print(f"Warning: Source file not found: {source}")

def move_organization_scripts():
    """Move organization scripts to the scripts directory."""
    # List of organization scripts
    organization_scripts = [
        "organize_repository.py",
        "complete_organization.py",
        "final_cleanup.py",
        "REPOSITORY_ORGANIZATION.md",
        "final_remaining_cleanup.py"
    ]
    
    # Create scripts directory
    os.makedirs("scripts", exist_ok=True)
    
    # Move organization scripts
    for script in organization_scripts:
        if os.path.exists(script):
            dest_path = os.path.join("scripts", script)
            shutil.copy2(script, dest_path)
            print(f"Moved organization script: {script} -> {dest_path}")
            
            # Don't remove the current script until it's done executing
            if script != "final_remaining_cleanup.py":
                os.remove(script)
                print(f"Removed original: {script}")

def main():
    """Main function to perform final remaining cleanup."""
    print("Starting final remaining cleanup...")
    
    # Move remaining files
    move_remaining_files()
    
    # Move organization scripts
    move_organization_scripts()
    
    # Check if there are any remaining files in the root directory
    remaining_files = [f for f in os.listdir(".") if os.path.isfile(f) and 
                      f not in [".gitignore", "README.md", "requirements.txt", "final_remaining_cleanup.py"]]
    
    if remaining_files:
        print("\nRemaining files in root directory:")
        for file in remaining_files:
            print(f"  - {file}")
        print("\nConsider manually moving these files to appropriate directories.")
    else:
        print("\nAll files have been organized successfully!")
    
    print("\nFinal remaining cleanup complete!")
    print("The repository is now organized according to the structure defined in scripts/REPOSITORY_ORGANIZATION.md.")
    print("\nNote: You can safely delete this script (final_remaining_cleanup.py) after it finishes executing.")

if __name__ == "__main__":
    main() 