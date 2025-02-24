import opendssdirect as dss
import os
import sys

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def initialize_circuit():
    """Initialize the circuit with minimal components first"""
    print_section("INITIALIZING CIRCUIT")
    
    # Start OpenDSS
    if not dss.Basic.Start(0):
        print("ERROR: Failed to start OpenDSS engine")
        return False
    
    # Clear and create empty circuit
    dss.Text.Command('Clear')
    dss.Text.Command('Set DefaultBaseFrequency=50')
    dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
    
    # Set very relaxed solution parameters
    dss.Text.Command('Set VoltageBases=[138.0]')
    dss.Text.Command('Calcv')
    dss.Text.Command('set algorithm=NEWTON')
    dss.Text.Command('set maxiterations=1000')
    dss.Text.Command('set maxcontroliter=1000')
    dss.Text.Command('set tolerance=0.1')  # Very relaxed tolerance
    
    print("Circuit initialized with relaxed settings")
    return True

def add_component_file(file_name, component_type):
    """Add components from a file with error handling"""
    print(f"\nAdding {component_type} from {file_name}...")
    try:
        dss.Text.Command(f'Redirect {file_name}')
        
        # Verify components were added
        dss.Circuit.SetActiveClass(component_type)
        count = len(dss.ActiveClass.AllNames())
        print(f"Added {count} {component_type}")
        
        # Try to solve after adding components
        dss.Text.Command('set maxiterations=100')
        dss.Text.Command('solve')
        
        if dss.Solution.Converged():
            print(f"Circuit converged after adding {component_type}")
        else:
            print(f"WARNING: Circuit did not converge after adding {component_type}")
            print(f"Continuing with relaxed settings...")
            dss.Text.Command('set maxiterations=1000')
            dss.Text.Command('set tolerance=0.1')
        
        return True
    except Exception as e:
        print(f"ERROR adding {component_type}: {str(e)}")
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

def run_simplified_simulation():
    """Run a simplified simulation with progressive loading"""
    print_section("RUNNING SIMPLIFIED SIMULATION")
    
    # Create output directory
    os.makedirs('simulation_results', exist_ok=True)
    
    # Define load levels to test
    load_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    
    # Store results
    results = []
    
    # Try each load level
    for level in load_levels:
        print_section(f"TESTING LOAD LEVEL: {level*100:.0f}%")
        
        # Scale loads
        if not scale_all_loads(level):
            print(f"Failed to scale loads to {level*100:.0f}%")
            continue
        
        # Try to solve
        if not try_solve_with_options():
            print(f"Failed to converge at {level*100:.0f}% load")
            continue
        
        # Get metrics
        metrics = get_system_metrics()
        if metrics:
            metrics['load_level'] = level
            results.append(metrics)
    
    # Save results
    if results:
        with open('simulation_results/simplified_results.txt', 'w') as f:
            f.write("Simplified Simulation Results\n")
            f.write("============================\n\n")
            
            for r in results:
                f.write(f"Load Level: {r['load_level']*100:.0f}%\n")
                f.write(f"  Active Losses: {r['active_loss_mw']:.2f} MW\n")
                f.write(f"  Reactive Losses: {r['reactive_loss_mvar']:.2f} MVAR\n")
                f.write(f"  Voltage Range: {r['min_voltage']:.3f} - {r['max_voltage']:.3f} pu\n")
                f.write(f"  Average Voltage: {r['avg_voltage']:.3f} pu\n\n")
        
        print(f"\nResults saved to simulation_results/simplified_results.txt")
        return True
    else:
        print("\nNo results to save")
        return False

def main():
    try:
        # Initialize circuit
        if not initialize_circuit():
            print("Failed to initialize circuit")
            return
        
        # Add components one by one
        print_section("ADDING COMPONENTS GRADUALLY")
        
        # First add generators (voltage sources)
        if not add_component_file('generators.dss', 'Generator'):
            print("Failed to add generators")
            return
        
        # Then add lines
        if not add_component_file('lines.dss', 'Line'):
            print("Failed to add lines")
            return
        
        # Then add transformers
        if not add_component_file('transformers.dss', 'Transformer'):
            print("Failed to add transformers")
            return
        
        # Add shunts
        if not add_component_file('shunts.dss', 'Capacitor'):
            print("Failed to add shunts")
            # Continue anyway
        
        # Finally add loads at reduced level
        if not add_component_file('loads.dss', 'Load'):
            print("Failed to add loads")
            return
        
        # Scale loads to 10% initially
        if not scale_all_loads(0.1):
            print("Failed to scale loads")
            return
        
        # Try to solve
        if not try_solve_with_options():
            print("Failed to solve even with 10% load")
            return
        
        # Run simplified simulation
        run_simplified_simulation()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")

if __name__ == "__main__":
    main() 