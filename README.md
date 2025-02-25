# IEEE 118-Bus System Repository

This repository contains simulation, analysis, and visualization tools for the IEEE 118-bus power system using OpenDSS.

## Repository Structure

The repository is organized into the following directories:

```
IEEE118Bus/
├── data/
│   ├── dss/                # Original DSS files
│   ├── modified/           # Modified DSS files for convergence
│   ├── profiles/           # Load and generation profiles
│   └── results/            # Simulation result data
├── docs/
│   ├── latex/              # LaTeX documentation
│   └── reports/            # Markdown reports and documentation
├── results/
│   ├── figures/            # Generated figures and plots
│   └── tables/             # Generated tables and data summaries
├── scripts/                # Organization and utility scripts
├── src/
│   ├── analysis/           # Analysis scripts
│   ├── simulation/         # Simulation scripts
│   ├── utils/              # Utility functions
│   └── visualization/      # Visualization scripts
└── README.md               # This file
```

## Key Components

### Simulation Files

- `src/simulation/minimal_solution.py`: Creates a minimal working circuit with just the swing bus
- `src/simulation/final_solution.py`: Attempts to build a complete working circuit
- `src/simulation/progressive_loading.py`: Gradually increases load levels to find convergence limits
- `src/simulation/run_simplified_circuit.py`: Runs a simplified version of the circuit

### Analysis Files

- `src/analysis/check_convergence.py`: Checks if the circuit converges
- `src/analysis/fix_convergence.py`: Attempts to fix convergence issues
- `src/analysis/fix_generators.py`: Modifies generator settings for better convergence

### Visualization Files

- `src/visualization/voltage_visualization.py`: Visualizes voltage profiles
- `src/visualization/loss_visualization.py`: Visualizes system losses

### Documentation

- `docs/reports/`: Contains detailed reports on various aspects of the system
- `docs/latex/`: Contains LaTeX documents for academic reporting

## Convergence Issues and Solutions

The IEEE 118-bus system has inherent convergence challenges. Our investigations have found:

1. **Swing Bus Configuration**: The system requires a dedicated swing bus generator with high capacity.
2. **Solution Parameters**: Extremely relaxed convergence settings are necessary.
3. **Progressive Loading**: Gradually adding components and increasing load levels helps achieve convergence.
4. **Minimal Working Solution**: A minimal working circuit is provided in `minimal_working_circuit.dss`.

## Usage

### Setting Up the Environment

```bash
# Clone the repository
git clone https://github.com/hrid0yislam/IEEE118Bus.git
cd IEEE118Bus

# Install required packages
pip install -r requirements.txt
```

### Running the Minimal Solution

```bash
python src/simulation/minimal_solution.py
```

This creates a minimal working circuit with just the swing bus, which serves as a starting point for more complex simulations.

### Running Analysis

```bash
# Check convergence of a circuit
python src/analysis/check_convergence.py

# Fix convergence issues
python src/analysis/fix_convergence.py
```

### Visualizing Results

```bash
# Visualize voltage profiles
python src/visualization/voltage_visualization.py

# Visualize system losses
python src/visualization/loss_visualization.py
```

### Working with Excel Files

The repository includes Excel files with data and analysis results. To open these files:

```bash
# Open the default Excel file (Comparissons.xlsx)
./open_excel.sh

# Open a specific Excel file
./open_excel.sh filename.xlsx
```

If the specified file is not found, the script will list all available Excel files in the repository and allow you to choose one to open.

Alternatively, you can use the Python script directly:

```bash
python src/utils/open_excel.py [filename]
```

### GitHub Repository Management

This repository includes a helper script for managing GitHub operations:

```bash
# Show repository status
./github_helper.sh status

# Commit changes
./github_helper.sh commit "Your commit message"

# Push changes to GitHub
./github_helper.sh push

# Pull latest changes
./github_helper.sh pull

# Show commit history
./github_helper.sh log

# Show repository URL
./github_helper.sh url
```

## Key Findings

1. The IEEE 118-bus system is inherently unstable and difficult to solve with OpenDSS.
2. A dedicated swing bus generator with very high capacity is required.
3. Extremely relaxed convergence settings are necessary.
4. Progressive loading and component addition is the most effective approach.
5. The system data may contain errors or inconsistencies that affect convergence.

## Future Work

1. Verify the IEEE 118-bus system data for potential errors.
2. Implement alternative power flow solvers.
3. Develop more robust convergence strategies.
4. Extend the analysis to include time-series simulations.
5. Implement smart inverter controls for improved stability.

## Contributing

Contributions to this repository are welcome. To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or contributions, please open an issue in this repository or contact the repository owner at [GitHub](https://github.com/hrid0yislam).
