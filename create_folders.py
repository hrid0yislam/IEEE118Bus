import os

# Define the directory structure
directories = [
    # Source code directories
    'src/simulation',
    'src/visualization',
    'src/diagnostics',
    'src/utilities',
    'src/dss_files/base',
    'src/dss_files/modified',
    
    # Data directories
    'data/input/xlsx',
    'data/output',
    
    # Documentation directories
    'docs/latex/reports',
    'docs/markdown',
    
    # Results directories
    'results/figures/thesis',
    'results/reports',
    'results/time_series'
]

# Create the directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("\nDirectory structure created successfully!")
print("Please refer to FOLDER_STRUCTURE.md for details on how to organize your files.") 