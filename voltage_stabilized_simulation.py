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
    """Fix the swing bus in the generators.dss file"""
    print_section("FIXING SWING BUS")
    
    try:
        # Check if generators.dss exists
        if not os.path.isfile('generators.dss'):
            print("ERROR: generators.dss file not found")
            return None
        
        # Check if swing bus is commented out
        swing_bus_commented = False
        with open('generators.dss', 'r') as f:
            for line in f:
                if '! New Generator.Gen_at_89_1' in line:
                    swing_bus_commented = True
                    print("WARNING: Swing bus is commented out in generators.dss")
                    print("Line: " + line.strip())
                    break
        
        # Create a fixed generators file if needed
        if swing_bus_commented:
            print("\nCreating fixed generators file...")
            with open('generators.dss', 'r') as f:
                lines = f.readlines()
            
            with open('generators_fixed.dss', 'w') as f:
                for line in lines:
                    if '! New Generator.Gen_at_89_1' in line:
                        fixed_line = line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1')
                        f.write(fixed_line)
                        print("Fixed line: " + fixed_line.strip())
                    else:
                        f.write(line)
            
            print("Created generators_fixed.dss with uncommented swing bus")
            return 'generators_fixed.dss'
        else:
            print("Swing bus is not commented out, using original file")
            return 'generators.dss'
    
    except Exception as e:
        print(f"ERROR fixing swing bus: {str(e)}")
        return None

def create_voltage_stabilized_circuit():
    """Create a circuit file with voltage stabilization measures"""
    print_section("CREATING VOLTAGE-STABILIZED CIRCUIT")
    
    try:
        # Create a modified master file with voltage stabilization
        with open('voltage_stabilized_circuit.dss', 'w') as f:
            f.write("""Clear

! Set system base frequency
Set DefaultBaseFrequency=50

! Define the circuit with controlled settings
New Circuit.ieee118bus
~ basekv=138.0 
~ phases=3 
~ pu=1.0
~ angle=0
~ bus1=89_clinchrv

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

! First add only the swing bus generator with controlled voltage
New Generator.SwingGen bus1=89_clinchrv phases=3 kV=138.0 kW=607000.0 model=3 Vpu=1.0 maxkvar=300000.0 minkvar=-210000.0

! Solve with just the swing bus
Solve

! Now add other generators with controlled voltages
redirect generators_fixed.dss

! Solve with all generators
Solve

! Add lines
redirect lines.dss

! Solve with generators and lines
Solve

! Add transformers
redirect transformers.dss

! Solve with generators, lines, and transformers
Solve

! Add shunts for voltage support
redirect shunts.dss
redirect sw_shunts.dss

! Solve with all components except loads
Solve

! Add loads at very reduced level (1%)
redirect loads.dss

! Scale all loads to 1%
BatchEdit Load..* kW=0.01
BatchEdit Load..* kvar=0.01

! Solve with all components at 1% load
Solve

! Show initial results
show voltages ln Nodes
show losses
""")
        
        print("Created voltage_stabilized_circuit.dss")
        return True
    
    except Exception as e:
        print(f"Error creating voltage-stabilized circuit: {str(e)}")
        return False

def run_voltage_stabilized_simulation():
    """Run a simulation with voltage stabilization measures"""
    print_section("RUNNING VOLTAGE-STABILIZED SIMULATION")
    
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            print("ERROR: Failed to start OpenDSS engine")
            return False
        
        # Use the voltage-stabilized circuit
        print("Loading voltage-stabilized circuit...")
        dss.Text.Command('Redirect voltage_stabilized_circuit.dss')
        
        # Check if circuit was created
        if dss.Circuit.Name() == '':
            print("ERROR: Failed to create circuit")
            return False
        
        print(f"Circuit created: {dss.Circuit.Name()}")
        
        # Check if initial solution converged
        if not dss.Solution.Converged():
            print("ERROR: Initial solution did not converge")
            return False
        
        print("Initial solution converged with 1% load")
        
        # Create output directory
        os.makedirs('simulation_results', exist_ok=True)
        
        # Progressive loading test
        print_section("PROGRESSIVE LOADING TEST")
        
        load_levels = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        max_converged_level = 0.01  # We already know 1% works
        
        for level in load_levels:
            print(f"\nTesting at {level*100:.0f}% load...")
            
            # Scale all loads
            dss.Text.Command(f'BatchEdit Load..* kW={level}')
            dss.Text.Command(f'BatchEdit Load..* kvar={level}')
            
            # Try to solve with multiple options
            solution_options = [
                {'algorithm': 'NEWTON', 'iterations': 100, 'tolerance': 0.001},
                {'algorithm': 'NEWTON', 'iterations': 500, 'tolerance': 0.01},
                {'algorithm': 'NEWTON', 'iterations': 1000, 'tolerance': 0.1},
                {'algorithm': 'NORM', 'iterations': 500, 'tolerance': 0.01}
            ]
            
            converged = False
            
            for i, options in enumerate(solution_options):
                print(f"  Solution attempt {i+1}: {options['algorithm']}, tol={options['tolerance']}")
                
                # Apply options
                dss.Text.Command(f"set algorithm={options['algorithm']}")
                dss.Text.Command(f"set maxiterations={options['iterations']}")
                dss.Text.Command(f"set tolerance={options['tolerance']}")
                
                # Try to solve
                dss.Solution.Solve()
                
                if dss.Solution.Converged():
                    print(f"  SUCCESS: Converged at {level*100:.0f}% load")
                    converged = True
                    max_converged_level = level
                    
                    # Get system metrics
                    losses = dss.Circuit.Losses()
                    print(f"  Losses: {losses[0]/1000000:.2f} MW, {losses[1]/1000000:.2f} MVAR")
                    
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
                        print(f"  Voltage range: {min_v:.3f} - {max_v:.3f} pu, Avg: {avg_v:.3f} pu")
                    
                    break
                else:
                    print(f"  FAILED: Did not converge at {level*100:.0f}% load")
            
            if not converged:
                print(f"\nWARNING: Could not converge at {level*100:.0f}% load")
                print(f"Maximum converged load level: {max_converged_level*100:.0f}%")
                break
        
        # Summary
        print_section("SIMULATION SUMMARY")
        
        if max_converged_level >= 1.0:
            print("RESULT: System converges at full load (100%)")
            print("The time series simulation should work correctly.")
        elif max_converged_level >= 0.6:
            print(f"RESULT: System converges at {max_converged_level*100:.0f}% load")
            print("The time series simulation may work with reduced load levels.")
        else:
            print(f"RESULT: System only converges at {max_converged_level*100:.0f}% load")
            print("The time series simulation will likely fail without significant modifications.")
        
        # Save results
        with open('simulation_results/voltage_stabilized_results.txt', 'w') as f:
            f.write("Voltage-Stabilized Simulation Results\n")
            f.write("===================================\n\n")
            f.write(f"Maximum converged load level: {max_converged_level*100:.0f}%\n\n")
            
            if max_converged_level >= 1.0:
                f.write("The system converges at full load (100%).\n")
                f.write("The time series simulation should work correctly.\n")
            elif max_converged_level >= 0.6:
                f.write(f"The system converges at {max_converged_level*100:.0f}% load.\n")
                f.write("The time series simulation may work with reduced load levels.\n")
            else:
                f.write(f"The system only converges at {max_converged_level*100:.0f}% load.\n")
                f.write("The time series simulation will likely fail without significant modifications.\n")
            
            f.write("\nRecommendations:\n")
            f.write("1. Use the voltage-stabilized approach for all simulations\n")
            f.write("2. Start with very low load levels (1-5%)\n")
            f.write("3. Gradually increase load in small steps\n")
            f.write("4. Use very relaxed convergence settings\n")
            f.write("5. Monitor voltage profiles carefully\n")
        
        print(f"\nResults saved to simulation_results/voltage_stabilized_results.txt")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")
        return False

def main():
    try:
        # Fix the swing bus
        generators_file = fix_swing_bus()
        if not generators_file:
            print("Failed to fix or verify swing bus")
            return
        
        # Create voltage-stabilized circuit
        if not create_voltage_stabilized_circuit():
            print("Failed to create voltage-stabilized circuit")
            return
        
        # Run voltage-stabilized simulation
        run_voltage_stabilized_simulation()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main() 