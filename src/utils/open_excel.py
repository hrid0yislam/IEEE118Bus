#!/usr/bin/env python3
"""
Open Excel File Utility

This script opens Excel files using the default application.
Usage: python open_excel.py [filename]
If no filename is provided, it will open the Comparissons.xlsx file.
"""

import os
import sys
import subprocess
import platform

def open_file(file_path):
    """Open a file with the default application based on the operating system."""
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file_path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(file_path)
        else:  # Linux
            subprocess.call(('xdg-open', file_path))
        print(f"Successfully opened {file_path}")
        return True
    except Exception as e:
        print(f"Error opening file: {e}")
        return False

def main():
    """Main function to handle opening Excel files."""
    # Get the absolute path to the repository root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    # Default Excel file
    default_excel = os.path.join(repo_root, 'data', 'profiles', 'Comparissons.xlsx')
    
    # Check if a filename was provided as an argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        # Check if the file exists in the current directory
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            # Check if the file exists in the data/profiles directory
            profiles_path = os.path.join(repo_root, 'data', 'profiles', filename)
            if os.path.exists(profiles_path):
                file_path = profiles_path
            else:
                print(f"Error: File '{filename}' not found.")
                print(f"Checking for Excel files in the repository...")
                
                # Search for Excel files in the repository
                excel_files = []
                for root, dirs, files in os.walk(repo_root):
                    for file in files:
                        if file.endswith(('.xlsx', '.xls')):
                            excel_files.append(os.path.join(root, file))
                
                if excel_files:
                    print("\nAvailable Excel files:")
                    for i, file in enumerate(excel_files, 1):
                        rel_path = os.path.relpath(file, repo_root)
                        print(f"{i}. {rel_path}")
                    
                    try:
                        choice = int(input("\nEnter the number of the file you want to open (or 0 to exit): "))
                        if 1 <= choice <= len(excel_files):
                            file_path = excel_files[choice-1]
                        else:
                            print("Exiting...")
                            return
                    except ValueError:
                        print("Invalid input. Exiting...")
                        return
                else:
                    print("No Excel files found in the repository.")
                    return
    else:
        # Use the default Excel file
        if os.path.exists(default_excel):
            file_path = default_excel
        else:
            print(f"Error: Default Excel file not found at {default_excel}")
            return
    
    # Open the file
    open_file(file_path)

if __name__ == "__main__":
    main() 