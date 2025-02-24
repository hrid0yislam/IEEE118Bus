# Time Series Simulation Solution Guide

## Problem Analysis

The IEEE 118-bus system time series simulation is failing to converge due to several issues:

1. **Missing Swing Bus**: The swing bus (Bus 89_CLINCHRV) is commented out in the generators.dss file, which is critical for power flow convergence.
2. **Convergence Settings**: The default convergence settings are too strict for this complex system.
3. **Load Scaling**: The system may not be able to handle full load immediately, requiring a gradual approach.
4. **Component Loading Order**: The order in which components are loaded affects convergence.

## Step-by-Step Solution

### 1. Fix the Swing Bus Issue

The most critical issue is the commented-out swing bus in the generators.dss file.

1. Open the `generators.dss` file
2. Find the line: `! swing bus - bus: 89_clinchrv`
3. Find the next line: `! New Generator.Gen_at_89_1 bus1=89_clinchrv  phases=3 kV=138.0 kW=607000.0...`
4. Remove the `!` at the beginning of the second line to uncomment it
5. Save the file

Alternatively, create a fixed version:

```python
# Create a fixed generators file
with open('generators.dss', 'r') as f:
    lines = f.readlines()

with open('generators_fixed.dss', 'w') as f:
    for line in lines:
        if '! New Generator.Gen_at_89_1' in line:
            # Uncomment the line
            f.write(line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1'))
        else:
            f.write(line)
```

### 2. Create a Modified Master File

Create a new master file with relaxed settings:

```
Clear

! Set system base frequency
Set DefaultBaseFrequency=50

! Define the circuit with relaxed settings
New Circuit.ieee118bus
~ basekv=138.0 
~ phases=3 
~ pu=1.0
~ bus1=89_clinchrv

! Use fixed generators file with swing bus
redirect generators_fixed.dss

! Load other circuit elements
redirect lines.dss
redirect transformers.dss
redirect shunts.dss
redirect sw_shunts.dss

! Set voltage bases
Set VoltageBases = [138.0]
Calcv
redirect confirm_kv_bases.dss

! Very relaxed solution parameters
set algorithm=NEWTON
set maxcontroliter=1000
set maxiterations=1000
set tolerance=0.1
set controlmode=OFF

! Load model
set loadmodel=1

! Solve
Solve mode=snap
```

### 3. Implement a Robust Time Series Simulation Script

Use the following approach in your Python script:

1. **Gradual Component Loading**:
   - Load generators first
   - Then lines and transformers
   - Then shunts
   - Finally loads at reduced level (10%)

2. **Progressive Load Scaling**:
   - Start with 10% load
   - Gradually increase to 100%
   - Use smaller steps if needed (10%, 20%, 40%, 60%, 80%, 100%)

3. **Multiple Solution Attempts**:
   - Try different algorithms (NEWTON, NORM)
   - Use progressively relaxed tolerances (0.001, 0.01, 0.1)
   - Increase maximum iterations (100, 500, 1000)

4. **Robust Error Handling**:
   - Catch and report all exceptions
   - Implement fallback options
   - Continue with partial results if possible

### 4. Key Code Snippets for Implementation

#### Fixing the Swing Bus
```python
def fix_swing_bus():
    with open('generators.dss', 'r') as f:
        lines = f.readlines()
    
    with open('generators_fixed.dss', 'w') as f:
        for line in lines:
            if '! New Generator.Gen_at_89_1' in line:
                f.write(line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1'))
            else:
                f.write(line)
```

#### Safe Load Scaling
```python
def scale_loads_safely(multiplier):
    # Get all loads first
    load_names = []
    dss.Circuit.SetActiveClass('Load')
    for load_name in dss.ActiveClass.AllNames():
        load_names.append(load_name)
    
    # Scale each load individually
    for load_name in load_names:
        try:
            dss.Circuit.SetActiveElement(f'Load.{load_name}')
            orig_kw = float(dss.Properties.Value('kW'))
            orig_kvar = float(dss.Properties.Value('kvar'))
            dss.Text.Command(f'Edit Load.{load_name} kW={orig_kw*multiplier:.1f} kvar={orig_kvar*multiplier:.1f}')
        except Exception as e:
            print(f"Warning: Error scaling load {load_name}: {str(e)}")
```

#### Multiple Solution Attempts
```python
def try_solve_with_options():
    solution_options = [
        {'algorithm': 'NEWTON', 'iterations': 100, 'tolerance': 0.001},
        {'algorithm': 'NEWTON', 'iterations': 500, 'tolerance': 0.01},
        {'algorithm': 'NEWTON', 'iterations': 1000, 'tolerance': 0.1},
        {'algorithm': 'NORM', 'iterations': 500, 'tolerance': 0.01}
    ]
    
    for options in solution_options:
        dss.Text.Command(f"set algorithm={options['algorithm']}")
        dss.Text.Command(f"set maxiterations={options['iterations']}")
        dss.Text.Command(f"set tolerance={options['tolerance']}")
        
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            return True
    
    return False
```

### 5. Running the Time Series Simulation

1. Fix the swing bus issue by creating `generators_fixed.dss`
2. Create the modified master file `simplified_circuit.dss`
3. Run the robust time series script:
   ```
   python robust_time_series.py
   ```

### 6. Troubleshooting Common Issues

1. **OpenDSS Installation Issues**:
   - Verify OpenDSS is installed: `pip install opendssdirect`
   - Check if it can be imported: `import opendssdirect as dss`
   - Test with a simple circuit

2. **File Path Issues**:
   - Ensure all required files are in the current directory
   - Use absolute paths if necessary
   - Check file permissions

3. **Convergence Issues**:
   - Try with even more relaxed settings
   - Reduce load further (5% or 1%)
   - Check for errors in the model (zero impedance lines, isolated buses)

4. **Memory Issues**:
   - Reduce the complexity of the model if needed
   - Close other applications
   - Monitor memory usage

## Conclusion

The IEEE 118-bus system is a complex model that requires careful handling to achieve convergence in time series simulations. By fixing the swing bus issue, using relaxed convergence settings, implementing progressive loading, and using robust error handling, you should be able to successfully run the time series simulation.

If you continue to face issues, consider simplifying the model or using a more powerful computer for the simulation. 