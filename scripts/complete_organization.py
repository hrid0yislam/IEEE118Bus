#!/usr/bin/env python3
"""
Complete Organization Script for IEEE 118-Bus System Repository

This script completes the organization by moving remaining files to their appropriate locations.
"""

import os
import shutil
import sys
from pathlib import Path

def move_remaining_files():
    """Move remaining files to their appropriate directories."""
    # Dictionary mapping file patterns to destination directories
    file_mappings = {
        # Data files
        "ieee118bus_Power_elem_MVA.txt": "data/profiles/",
        
        # Modified OpenDSS files (still in root)
        "voltage_stabilized_circuit.dss": "data/modified/",
        
        # Analysis scripts
        "voltage_loss_analysis.py": "src/analysis/",
        "critical_bus_improvement.py": "src/analysis/",
        "voltage_improvement_viz.py": "src/analysis/",
        "simple_voltage_loss.py": "src/analysis/",
        "test_voltage_read.py": "src/analysis/",
        "plot_losses.py": "src/analysis/",
        "loss_relationship_viz.py": "src/analysis/",
        
        # Visualization scripts
        "voltage_loss_viz_fixed.py": "src/visualization/voltage_loss_viz.py",  # Rename
        "voltage_profile_visualization.py": "src/visualization/voltage_profile_viz.py",  # Rename
        "simple_visualization.py": "src/visualization/simple_viz.py",  # Rename
        
        # Documentation - Markdown reports
        "loss_explanation.md": "docs/reports/",
        "thesis_report.md": "docs/reports/",
        
        # Documentation - LaTeX
        "test_compile.tex": "docs/latex/",
        
        # Results - Figures
        "voltage_profile_analysis.png": "results/figures/voltage/",
        "critical_buses_analysis.png": "results/figures/voltage/",
        "critical_bus_improvement.png": "results/figures/voltage/",
        "basic_voltage_loss.png": "results/figures/voltage/",
        
        "loss_analysis.png": "results/figures/losses/",
        "loss_relationship.png": "results/figures/losses/",
        "power_loss_analysis.png": "results/figures/losses/",
        "simple_loss_analysis.png": "results/figures/losses/",
        
        "time_series_results.png": "results/figures/time_series/",
        
        # Results - Data
        "critical_buses_analysis.txt": "results/data/",
        "voltage_loss_analysis.txt": "results/data/",
        "loss_summary.txt": "results/data/",
        "power_loss_summary.txt": "results/data/",
        "simple_loss_summary.txt": "results/data/",
        "simulation_results.txt": "results/data/",
        
        # Results - Logs
        "ieee118_bus_report.log": "results/logs/",
        "ieee118_bus_report.aux": "results/logs/",
        "ieee118_bus_report.out": "results/logs/",
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

def move_existing_directories():
    """Move contents of existing directories to the new structure."""
    directory_mappings = {
        "thesis_figures": "results/figures",
        "latex_report": "docs/latex",
        "simulation_results": "results/data",
        "xlsx_files": "data/profiles"
    }
    
    for source_dir, dest_dir in directory_mappings.items():
        if os.path.exists(source_dir) and os.path.isdir(source_dir):
            # Get all files in the source directory
            files = os.listdir(source_dir)
            
            for file in files:
                source_path = os.path.join(source_dir, file)
                
                # Determine the appropriate destination subdirectory
                if dest_dir == "results/figures":
                    if "voltage" in file.lower() or "bus" in file.lower() or "profile" in file.lower():
                        dest_subdir = os.path.join(dest_dir, "voltage")
                    elif "loss" in file.lower() or "power" in file.lower():
                        dest_subdir = os.path.join(dest_dir, "losses")
                    elif "time" in file.lower() or "series" in file.lower():
                        dest_subdir = os.path.join(dest_dir, "time_series")
                    else:
                        dest_subdir = dest_dir
                else:
                    dest_subdir = dest_dir
                
                # Create destination directory if it doesn't exist
                os.makedirs(dest_subdir, exist_ok=True)
                
                # Destination path
                dest_path = os.path.join(dest_subdir, file)
                
                # Copy the file
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, dest_path)
                    print(f"Moved: {source_path} -> {dest_path}")
            
            # Remove the original directory after all files have been copied
            shutil.rmtree(source_dir)
            print(f"Removed original directory: {source_dir}")
        else:
            print(f"Warning: Source directory not found: {source_dir}")

def clean_up_duplicates():
    """Clean up any remaining duplicate files."""
    # PDF files that should be moved to docs/latex
    pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        dest_path = os.path.join("docs/latex", pdf_file)
        if os.path.exists(pdf_file):
            shutil.copy2(pdf_file, dest_path)
            os.remove(pdf_file)
            print(f"Moved PDF: {pdf_file} -> {dest_path}")
    
    # Check for any remaining Python scripts in the root directory
    py_files = [f for f in os.listdir(".") if f.endswith(".py") and f not in ["organize_repository.py", "complete_organization.py"]]
    if py_files:
        print("\nRemaining Python scripts in root directory:")
        for py_file in py_files:
            print(f"  - {py_file}")
        print("\nConsider manually moving these files to appropriate directories.")
    
    # Check for any remaining DSS files in the root directory
    dss_files = [f for f in os.listdir(".") if f.endswith(".dss")]
    if dss_files:
        print("\nRemaining DSS files in root directory:")
        for dss_file in dss_files:
            print(f"  - {dss_file}")
        print("\nConsider manually moving these files to appropriate directories.")

def main():
    """Main function to complete the repository organization."""
    print("Starting completion of repository organization...")
    
    # Move remaining files
    move_remaining_files()
    
    # Move contents of existing directories
    move_existing_directories()
    
    # Clean up duplicates
    clean_up_duplicates()
    
    print("\nRepository organization completion finished!")
    print("Please review the changes and make any necessary adjustments.")

if __name__ == "__main__":
    main() 