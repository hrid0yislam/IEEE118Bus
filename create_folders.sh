#!/bin/bash

# Create the directory structure
mkdir -p src/{simulation,visualization,diagnostics,utilities,dss_files/{base,modified}}
mkdir -p data/{input/xlsx,output}
mkdir -p docs/{latex/reports,markdown}
mkdir -p results/{figures/thesis,reports,time_series}

echo "Directory structure created successfully!"
echo "Please refer to FOLDER_STRUCTURE.md for details on how to organize your files." 