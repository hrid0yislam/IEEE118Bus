import opendssdirect as dss
import os
import sys
import numpy as np

def execute_command(cmd, description):
    print(f"\nExecuting: {description}")
    print(f"Command: {cmd}")
    result = dss.Text.Command(cmd)
    error = dss.Error.Description()
    if error:
        print(f"Error: {error}")
        return False
    if result:
        print(f"Result: {result}")
    return True

def analyze_voltages():
    """Analyze voltage profiles for all buses"""
    voltages = {}
    
    print("\nVoltage Profile Analysis:")
    print("=" * 100)
    print(f"{'Bus Name':<20} {'Base kV':<10} {'pu Voltage':<12} {'Actual kV':<12} {'Status':<15}")
    print("-" * 100)
    
    v_min = float('inf')
    v_max = float('-inf')
    v_min_bus = ""
    v_max_bus = ""
    
    # Get all bus voltages
    dss.Circuit.SetActiveBus("")
    buses = dss.Circuit.AllBusNames()
    
    for bus in buses:
        # Set the active bus
        dss.Circuit.SetActiveBus(bus)
        
        # Get base voltage (138 kV for all buses in this case)
        base_kv = 138.0
        
        # Get voltage magnitudes
        v_mag_array = dss.Bus.VMagAngle()[::2]  # Even indices are magnitudes
        if len(v_mag_array) >= 3:  # Three-phase
            # Calculate average phase voltage magnitude in per unit
            v_mag = np.mean(v_mag_array) / (base_kv * 1000)  # Convert from V to kV
        else:  # Single-phase or two-phase
            v_mag = v_mag_array[0] / (base_kv * 1000)  # Convert from V to kV
            
        actual_kv = v_mag * base_kv
        
        # Determine voltage status
        if v_mag > 1.05:
            status = "High Voltage"
        elif v_mag < 0.95:
            status = "Low Voltage"
        else:
            status = "Normal"
            
        # Track min and max voltages
        if v_mag < v_min:
            v_min = v_mag
            v_min_bus = bus
        if v_mag > v_max:
            v_max = v_mag
            v_max_bus = bus
            
        print(f"{bus:<20} {base_kv:<10.2f} {v_mag:<12.4f} {actual_kv:<12.2f} {status:<15}")
        voltages[bus] = (v_mag, status)
    
    # Print summary statistics
    print("\nVoltage Profile Summary:")
    print("=" * 50)
    print(f"Maximum Voltage: {v_max:.4f} pu at bus {v_max_bus}")
    print(f"Minimum Voltage: {v_min:.4f} pu at bus {v_min_bus}")
    
    # Count buses in different voltage ranges
    normal_count = sum(1 for v, s in voltages.values() if s == "Normal")
    high_count = sum(1 for v, s in voltages.values() if s == "High Voltage")
    low_count = sum(1 for v, s in voltages.values() if s == "Low Voltage")
    
    total_buses = len(voltages)
    print(f"\nVoltage Range Statistics:")
    print(f"Normal Voltage Buses (0.95-1.05 pu): {normal_count} ({normal_count/total_buses*100:.1f}%)")
    print(f"High Voltage Buses (>1.05 pu): {high_count} ({high_count/total_buses*100:.1f}%)")
    print(f"Low Voltage Buses (<0.95 pu): {low_count} ({low_count/total_buses*100:.1f}%)")
    
    return voltages

def main():
    try:
        # Change to the directory containing the DSS files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"Working directory: {os.getcwd()}")

        # List all DSS files in the directory
        print("\nDSS files in directory:")
        for file in os.listdir('.'):
            if file.endswith('.dss'):
                print(f"  {file}")

        # Start OpenDSS
        if not dss.Basic.Start(0):
            raise Exception("Failed to start OpenDSS engine")

        # Clear any existing circuit
        print("\nInitializing OpenDSS...")
        if not execute_command('Clear', 'Clearing circuit'):
            raise Exception("Failed to clear circuit")

        if not execute_command('Set DefaultBaseFrequency=50', 'Setting base frequency'):
            raise Exception("Failed to set base frequency")

        # Create new circuit
        if not execute_command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv frequency=50.0', 'Creating new circuit'):
            raise Exception("Failed to create circuit")

        # Compile each component file
        components = [
            ('generators.dss', 'generators'),
            ('lines.dss', 'lines'),
            ('transformers.dss', 'transformers'),
            ('loads.dss', 'loads'),
            ('shunts.dss', 'shunts'),
            ('sw_shunts.dss', 'switched shunts')
        ]

        for file, description in components:
            if not execute_command(f'Redirect {file}', f'Loading {description}'):
                raise Exception(f"Failed to compile {file}")

        # Set voltage bases
        if not execute_command('Set VoltageBases = [138.0]', 'Setting voltage bases'):
            raise Exception("Failed to set voltage bases")

        if not execute_command('Calcv', 'Calculating voltage bases'):
            raise Exception("Failed to calculate voltage bases")

        if not execute_command('Redirect confirm_kv_bases.dss', 'Confirming voltage bases'):
            raise Exception("Failed to confirm voltage bases")

        # Set solution mode and parameters
        print("\nConfiguring solution parameters...")
        solution_params = [
            'set algorithm=NCIM',  # Newton-Raphson Current Injection Mode
            'set maxiterations=100',  # Increase maximum iterations
            'set maxcontroliter=100',  # Increase control iterations
            'set tolerance=0.0001',  # Adjust convergence tolerance
            'set controlmode=off',  # Turn off controls for initial solution
            'set loadmodel=1',  # Constant power load model
            'set voltagebases=[138.0]'  # Confirm voltage bases
        ]

        for param in solution_params:
            if not execute_command(param, f'Setting {param}'):
                raise Exception(f"Failed to set {param}")

        # Try to solve with a flat start
        if not execute_command('solve mode=direct', 'Initial direct solution'):
            print("Direct solution failed, trying with flat start...")
            if not execute_command('set loadmodel=2', 'Setting constant Z load model'):
                raise Exception("Failed to set load model")
            if not execute_command('solve mode=snap', 'Snap solution with constant Z'):
                raise Exception("Failed to solve with flat start")

        # Now try normal solution
        print("\nAttempting final solution...")
        if not execute_command('set loadmodel=1', 'Restoring constant P load model'):
            raise Exception("Failed to restore load model")
        if not execute_command('solve', 'Final solution'):
            raise Exception("Failed to solve circuit")
        
        if not dss.Solution.Converged():
            raise Exception("Circuit solution did not converge")

        # Analyze voltage profiles
        voltages = analyze_voltages()

        # Show results
        print("\nCircuit Results:")
        print("\nVoltage Report:")
        execute_command('show voltages ln nodes', 'Showing voltages')
        
        print("\nPower Flow Report:")
        execute_command('show powers mva elem', 'Showing power flow')
        
        print("\nCircuit Summary:")
        execute_command('summary', 'Showing summary')

        # Print power losses
        print("\nCircuit Losses:")
        losses = dss.Circuit.Losses()
        print(f"Total Power Losses: {losses[0]/1000:.2f} kW + j{losses[1]/1000:.2f} kVAR")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error Details: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 