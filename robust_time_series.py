import opendssdirect as dss
import os
import sys
import time

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def fix_swing_bus():
    """Create a fixed version of the generators file with swing bus uncommented"""
    print_section("FIXING SWING BUS")
    
    try:
        # Read the generators file
        with open('generators.dss', 'r') as f:
            lines = f.readlines()
        
        # Create a fixed version
        fixed_lines = []
        fixed_swing = False
        
        for line in lines:
            # Check if this is the commented swing bus line
            if '! New Generator.Gen_at_89_1' in line:
                # Uncomment the line
                fixed_line = line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1')
                fixed_lines.append(fixed_line)
                fixed_swing = True
                print(f"Fixed swing bus line: {line.strip()} -> {fixed_line.strip()}")
            else:
                fixed_lines.append(line)
        
        if fixed_swing:
            # Write the fixed file
            with open('generators_fixed.dss', 'w') as f:
                f.writelines(fixed_lines)
            print("Created generators_fixed.dss with uncommented swing bus")
            return True
        else:
            print("Could not find commented swing bus line")
            return False
    
    except Exception as e:
        print(f"Error fixing swing bus: {str(e)}")
        return False

def create_simplified_circuit():
    """Create a simplified circuit file for better convergence"""
    print_section("CREATING SIMPLIFIED CIRCUIT")
    
    try:
        # Create a simplified master file
        with open('simplified_circuit.dss', 'w') as f:
            f.write("""Clear

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
""")
        
        print("Created simplified_circuit.dss")
        return True
    
    except Exception as e:
        print(f"Error creating simplified circuit: {str(e)}")
        return False

def initialize_dss():
    """Initialize OpenDSS with the simplified circuit"""
    print_section("INITIALIZING OPENDSS")
    
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            print("ERROR: Failed to start OpenDSS engine")
            return False
        
        # Use the simplified circuit
        print("Loading simplified circuit...")
        dss.Text.Command('Redirect simplified_circuit.dss')
        
        # Check if circuit was created
        if dss.Circuit.Name() == '':
            print("ERROR: Failed to create circuit")
            return False
        
        print(f"Circuit created: {dss.Circuit.Name()}")
        
        # Try to solve with very relaxed settings
        print("\nAttempting initial solution...")
        dss.Text.Command('set algorithm=NEWTON')
        dss.Text.Command('set maxiterations=2000')
        dss.Text.Command('set tolerance=0.1')
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("Initial solution converged!")
        else:
            print("WARNING: Initial solution did not converge")
            print("Continuing anyway with reduced load...")
            
            # Try with reduced load
            print("\nTrying with reduced load (10%)...")
            dss.Text.Command('redirect loads.dss')
            scale_all_loads(0.1)
            dss.Solution.Solve()
            
            if dss.Solution.Converged():
                print("Solution converged with 10% load")
            else:
                print("ERROR: Could not converge even with 10% load")
                return False
        
        return True
    
    except Exception as e:
        print(f"Initialization error: {str(e)}")
        return False

def scale_all_loads(multiplier):
    """Scale all loads with proper error handling"""
    print(f"\nScaling all loads to {multiplier*100:.0f}%...")
    try:
        # Get all loads first
        load_names = []
        dss.Circuit.SetActiveClass('Load')
        for load_name in dss.ActiveClass.AllNames():
            load_names.append(load_name)
        
        print(f"Found {len(load_names)} loads to scale")
        
        # Scale each load individually
        for load_name in load_names:
            try:
                # Access load properties safely
                dss.Circuit.SetActiveElement(f'Load.{load_name}')
                
                # Get original values
                orig_kw = float(dss.Properties.Value('kW'))
                orig_kvar = float(dss.Properties.Value('kvar'))
                
                # Calculate new values
                new_kw = orig_kw * multiplier
                new_kvar = orig_kvar * multiplier
                
                # Use Edit command to modify the load
                dss.Text.Command(f'Edit Load.{load_name} kW={new_kw:.1f} kvar={new_kvar:.1f}')
            except Exception as e:
                print(f"Warning: Error scaling load {load_name}: {str(e)}")
        
        return True
    except Exception as e:
        print(f"ERROR scaling loads: {str(e)}")
        return False

def try_solve_with_options():
    """Try to solve with multiple options"""
    print("\nAttempting to solve with multiple options...")
    
    # Try different solution options
    solution_options = [
        {'algorithm': 'NEWTON', 'iterations': 100, 'tolerance': 0.001},
        {'algorithm': 'NEWTON', 'iterations': 500, 'tolerance': 0.01},
        {'algorithm': 'NEWTON', 'iterations': 1000, 'tolerance': 0.1},
        {'algorithm': 'NORM', 'iterations': 500, 'tolerance': 0.01}
    ]
    
    for i, options in enumerate(solution_options):
        print(f"\nSolution attempt {i+1}:")
        print(f"  Algorithm: {options['algorithm']}")
        print(f"  Max iterations: {options['iterations']}")
        print(f"  Tolerance: {options['tolerance']}")
        
        # Apply options
        dss.Text.Command(f"set algorithm={options['algorithm']}")
        dss.Text.Command(f"set maxiterations={options['iterations']}")
        dss.Text.Command(f"set tolerance={options['tolerance']}")
        
        # Try to solve
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("  SUCCESS: Solution converged!")
            return True
        else:
            print("  FAILED: Solution did not converge")
            error = dss.Error.Description()
            if error:
                print(f"  Error: {error}")
    
    print("\nFAILED: Could not converge with any solution options")
    return False

def get_system_metrics():
    """Get system metrics with error handling"""
    try:
        # Get losses
        losses = dss.Circuit.Losses()
        active_loss = losses[0]/1000000  # Convert to MW
        reactive_loss = losses[1]/1000000  # Convert to MVAR
        
        # Get voltage range
        voltages = []
        dss.Circuit.SetActiveBus("")
        for bus in dss.Circuit.AllBusNames():
            try:
                dss.Circuit.SetActiveBus(bus)
                v_mag = dss.Bus.puVmagAngle()[0]
                voltages.append(v_mag)
            except:
                pass
        
        if voltages:
            min_v = min(voltages)
            max_v = max(voltages)
            avg_v = sum(voltages) / len(voltages)
        else:
            min_v = max_v = avg_v = 0
        
        print("\nSystem Metrics:")
        print(f"  Active Losses: {active_loss:.2f} MW")
        print(f"  Reactive Losses: {reactive_loss:.2f} MVAR")
        print(f"  Voltage Range: {min_v:.3f} - {max_v:.3f} pu")
        print(f"  Average Voltage: {avg_v:.3f} pu")
        
        return {
            'active_loss_mw': active_loss,
            'reactive_loss_mvar': reactive_loss,
            'min_voltage': min_v,
            'max_voltage': max_v,
            'avg_voltage': avg_v
        }
    except Exception as e:
        print(f"ERROR getting metrics: {str(e)}")
        return None

def run_time_series():
    """Run time series simulation with progressive loading"""
    print_section("RUNNING TIME SERIES SIMULATION")
    
    # Create output directory
    os.makedirs('simulation_results', exist_ok=True)
    
    # Define load multipliers for 24 hours
    load_multipliers = [
        0.65, 0.60, 0.58, 0.56, 0.55, 0.57,  # Hours 0-5
        0.62, 0.72, 0.85, 0.95, 0.98, 1.00,  # Hours 6-11
        0.99, 0.97, 0.95, 0.93, 0.94, 0.98,  # Hours 12-17
        1.00, 0.97, 0.92, 0.85, 0.75, 0.68   # Hours 18-23
    ]
    
    # Store results
    results = []
    
    # Run simulation for each hour
    for hour, multiplier in enumerate(load_multipliers):
        print_section(f"HOUR {hour:02d}:00 (LOAD: {multiplier:.2%})")
        
        # Scale loads
        if not scale_all_loads(multiplier):
            print(f"Failed to scale loads for hour {hour}")
            continue
        
        # Try to solve
        if not try_solve_with_options():
            print(f"Failed to converge for hour {hour}")
            continue
        
        # Get metrics
        metrics = get_system_metrics()
        if metrics:
            metrics['hour'] = hour
            metrics['multiplier'] = multiplier
            results.append(metrics)
    
    # Save results
    if results:
        with open('simulation_results/time_series_results.txt', 'w') as f:
            f.write("Time Series Simulation Results\n")
            f.write("============================\n\n")
            
            for r in results:
                f.write(f"Hour {r['hour']:02d}:00 (Load: {r['multiplier']:.2%})\n")
                f.write(f"  Active Losses: {r['active_loss_mw']:.2f} MW\n")
                f.write(f"  Reactive Losses: {r['reactive_loss_mvar']:.2f} MVAR\n")
                f.write(f"  Voltage Range: {r['min_voltage']:.3f} - {r['max_voltage']:.3f} pu\n")
                f.write(f"  Average Voltage: {r['avg_voltage']:.3f} pu\n\n")
            
            # Write summary
            f.write("\nSummary Statistics:\n")
            f.write("------------------\n")
            
            if results:
                active_losses = [r['active_loss_mw'] for r in results]
                reactive_losses = [r['reactive_loss_mvar'] for r in results]
                min_voltages = [r['min_voltage'] for r in results]
                max_voltages = [r['max_voltage'] for r in results]
                
                f.write(f"Average active losses: {sum(active_losses)/len(active_losses):.2f} MW\n")
                f.write(f"Maximum active losses: {max(active_losses):.2f} MW\n")
                f.write(f"Minimum active losses: {min(active_losses):.2f} MW\n\n")
                
                f.write(f"Average reactive losses: {sum(reactive_losses)/len(reactive_losses):.2f} MVAR\n")
                f.write(f"Maximum reactive losses: {max(reactive_losses):.2f} MVAR\n")
                f.write(f"Minimum reactive losses: {min(reactive_losses):.2f} MVAR\n\n")
                
                f.write(f"Lowest voltage: {min(min_voltages):.3f} pu\n")
                f.write(f"Highest voltage: {max(max_voltages):.3f} pu\n")
        
        print(f"\nResults saved to simulation_results/time_series_results.txt")
        return True
    else:
        print("\nNo results to save")
        return False

def main():
    try:
        # Fix the swing bus
        if not fix_swing_bus():
            print("Failed to fix swing bus")
            return
        
        # Create simplified circuit
        if not create_simplified_circuit():
            print("Failed to create simplified circuit")
            return
        
        # Initialize OpenDSS
        if not initialize_dss():
            print("Failed to initialize OpenDSS")
            return
        
        # Run time series simulation
        run_time_series()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")

if __name__ == "__main__":
    main() 