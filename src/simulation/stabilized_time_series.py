import opendssdirect as dss
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
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

def initialize_stabilized_circuit():
    """Initialize the circuit with voltage stabilization measures"""
    print_section("INITIALIZING STABILIZED CIRCUIT")
    
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            print("ERROR: Failed to start OpenDSS engine")
            return False
        
        # Clear and create circuit
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 pu=1.0 angle=0 bus1=89_clinchrv')
        
        # Set voltage bases
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        dss.Text.Command('redirect confirm_kv_bases.dss')
        
        # Set very relaxed solution parameters
        dss.Text.Command('set algorithm=NEWTON')
        dss.Text.Command('set maxcontroliter=1000')
        dss.Text.Command('set maxiterations=1000')
        dss.Text.Command('set tolerance=0.1')
        dss.Text.Command('set controlmode=OFF')
        
        print("Circuit initialized with relaxed settings")
        
        # First add only the swing bus generator with controlled voltage
        print("\nAdding swing bus generator...")
        dss.Text.Command('New Generator.SwingGen bus1=89_clinchrv phases=3 kV=138.0 kW=607000.0 model=3 Vpu=1.0 maxkvar=300000.0 minkvar=-210000.0')
        
        # Solve with just the swing bus
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with only swing bus generator did not converge")
            return False
        
        print("Circuit with swing bus generator converged")
        
        # Now add other generators with controlled voltages
        print("\nAdding other generators...")
        dss.Text.Command('redirect generators_fixed.dss')
        
        # Solve with all generators
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with all generators did not converge")
            return False
        
        print("Circuit with all generators converged")
        
        # Add lines
        print("\nAdding lines...")
        dss.Text.Command('redirect lines.dss')
        
        # Solve with generators and lines
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with generators and lines did not converge")
            return False
        
        print("Circuit with generators and lines converged")
        
        # Add transformers
        print("\nAdding transformers...")
        dss.Text.Command('redirect transformers.dss')
        
        # Solve with generators, lines, and transformers
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with generators, lines, and transformers did not converge")
            return False
        
        print("Circuit with generators, lines, and transformers converged")
        
        # Add shunts for voltage support
        print("\nAdding shunts...")
        dss.Text.Command('redirect shunts.dss')
        dss.Text.Command('redirect sw_shunts.dss')
        
        # Solve with all components except loads
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with all components except loads did not converge")
            return False
        
        print("Circuit with all components except loads converged")
        
        # Add loads at very reduced level (1%)
        print("\nAdding loads at 1% level...")
        dss.Text.Command('redirect loads.dss')
        
        # Scale all loads to 1%
        dss.Text.Command('BatchEdit Load..* kW=0.01')
        dss.Text.Command('BatchEdit Load..* kvar=0.01')
        
        # Solve with all components at 1% load
        dss.Solution.Solve()
        if not dss.Solution.Converged():
            print("ERROR: Circuit with all components at 1% load did not converge")
            return False
        
        print("Circuit with all components at 1% load converged")
        
        # Get initial metrics
        metrics = get_system_metrics()
        if metrics:
            print("\nInitial System Metrics (1% load):")
            print(f"  Active Losses: {metrics['active_loss_mw']:.2f} MW")
            print(f"  Reactive Losses: {metrics['reactive_loss_mvar']:.2f} MVAR")
            print(f"  Voltage Range: {metrics['min_voltage']:.3f} - {metrics['max_voltage']:.3f} pu")
            print(f"  Average Voltage: {metrics['avg_voltage']:.3f} pu")
        
        return True
    
    except Exception as e:
        print(f"ERROR initializing circuit: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")
        return False

def scale_loads_safely(multiplier):
    """Scale all loads with proper error handling"""
    print(f"\nScaling all loads to {multiplier*100:.0f}%...")
    try:
        # Use BatchEdit for efficiency
        dss.Text.Command(f'BatchEdit Load..* kW={multiplier}')
        dss.Text.Command(f'BatchEdit Load..* kvar={multiplier}')
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
        print(f"  Solution attempt {i+1}: {options['algorithm']}, tol={options['tolerance']}")
        
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
    # Scale these down to a maximum that works for the system
    # For example, if the system only converges up to 60%, scale all values by 0.6
    max_load_factor = 0.4  # Adjusted based on diagnostic results
    
    base_load_multipliers = [
        0.65, 0.60, 0.58, 0.56, 0.55, 0.57,  # Hours 0-5
        0.62, 0.72, 0.85, 0.95, 0.98, 1.00,  # Hours 6-11
        0.99, 0.97, 0.95, 0.93, 0.94, 0.98,  # Hours 12-17
        1.00, 0.97, 0.92, 0.85, 0.75, 0.68   # Hours 18-23
    ]
    
    # Scale the multipliers
    load_multipliers = [m * max_load_factor for m in base_load_multipliers]
    
    # Store results
    results = []
    
    # Run simulation for each hour
    for hour, multiplier in enumerate(load_multipliers):
        print_section(f"HOUR {hour:02d}:00 (LOAD: {multiplier:.2%})")
        
        # Scale loads
        if not scale_loads_safely(multiplier):
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
            
            # Print key metrics
            print("\nSystem Metrics:")
            print(f"  Active Losses: {metrics['active_loss_mw']:.2f} MW")
            print(f"  Reactive Losses: {metrics['reactive_loss_mvar']:.2f} MVAR")
            print(f"  Voltage Range: {metrics['min_voltage']:.3f} - {metrics['max_voltage']:.3f} pu")
            print(f"  Average Voltage: {metrics['avg_voltage']:.3f} pu")
    
    # Create visualizations if we have results
    if results:
        create_visualizations(results)
        save_results_to_file(results, max_load_factor)
        return True
    else:
        print("\nNo results to save")
        return False

def create_visualizations(results):
    """Create visualizations of the results"""
    print_section("CREATING VISUALIZATIONS")
    
    # Extract data for plotting
    hours = [r['hour'] for r in results]
    active_losses = [r['active_loss_mw'] for r in results]
    reactive_losses = [r['reactive_loss_mvar'] for r in results]
    min_voltages = [r['min_voltage'] for r in results]
    max_voltages = [r['max_voltage'] for r in results]
    avg_voltages = [r['avg_voltage'] for r in results]
    load_multipliers = [r['multiplier'] for r in results]
    
    # Create figure with subplots
    plt.figure(figsize=(12, 15))
    
    # Plot 1: Load Profile
    plt.subplot(3, 1, 1)
    plt.plot(hours, load_multipliers, 'b-', linewidth=2, marker='o')
    plt.fill_between(hours, load_multipliers, alpha=0.2)
    plt.title('24-Hour Load Profile', fontsize=14, pad=20)
    plt.xlabel('Hour of Day')
    plt.ylabel('Load Multiplier (p.u.)')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Voltage Profile
    plt.subplot(3, 1, 2)
    plt.plot(hours, min_voltages, 'r-', label='Minimum', marker='v')
    plt.plot(hours, max_voltages, 'g-', label='Maximum', marker='^')
    plt.plot(hours, avg_voltages, 'b--', label='Average', marker='o')
    plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
    plt.axhline(y=1.05, color='g', linestyle='--', label='Upper Limit')
    plt.title('System Voltage Profile', fontsize=14, pad=20)
    plt.xlabel('Hour of Day')
    plt.ylabel('Voltage (p.u.)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 3: System Losses
    plt.subplot(3, 1, 3)
    plt.plot(hours, active_losses, 'b-', label='Active (MW)', marker='o')
    plt.plot(hours, reactive_losses, 'r--', label='Reactive (MVAR)', marker='s')
    plt.title('System Losses Over Time', fontsize=14, pad=20)
    plt.xlabel('Hour of Day')
    plt.ylabel('Power Loss')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('simulation_results/time_series_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create a second figure: Load vs Losses
    plt.figure(figsize=(10, 8))
    plt.scatter(load_multipliers, active_losses, label='Active Losses', alpha=0.7, s=100)
    
    # Add trend line
    z = np.polyfit(load_multipliers, active_losses, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(load_multipliers), max(load_multipliers), 100)
    plt.plot(x_trend, p(x_trend), "r--", alpha=0.8, label='Quadratic Trend')
    
    plt.title('Load vs Losses Relationship', fontsize=14, pad=20)
    plt.xlabel('Load Multiplier (p.u.)')
    plt.ylabel('Active Losses (MW)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the figure
    plt.savefig('simulation_results/load_vs_losses.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations saved to simulation_results directory")

def save_results_to_file(results, max_load_factor):
    """Save results to text file"""
    print_section("SAVING RESULTS")
    
    with open('simulation_results/time_series_results.txt', 'w') as f:
        f.write("Time Series Simulation Results\n")
        f.write("============================\n\n")
        
        f.write(f"Note: All loads were scaled by a maximum factor of {max_load_factor:.2f} for convergence.\n\n")
        
        # Write hourly results
        f.write("Hourly Results:\n")
        f.write("--------------\n")
        for r in results:
            f.write(f"Hour {r['hour']:02d}:00 (Load: {r['multiplier']:.2%})\n")
            f.write(f"  Active Losses: {r['active_loss_mw']:.2f} MW\n")
            f.write(f"  Reactive Losses: {r['reactive_loss_mvar']:.2f} MVAR\n")
            f.write(f"  Voltage Range: {r['min_voltage']:.3f} - {r['max_voltage']:.3f} pu\n")
            f.write(f"  Average Voltage: {r['avg_voltage']:.3f} pu\n\n")
        
        # Write summary statistics
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
        
        # Write quadratic relationship
        f.write("\nLoad-Loss Relationship:\n")
        f.write("---------------------\n")
        f.write("The relationship between load level and losses follows a quadratic pattern:\n")
        
        if results:
            load_multipliers = [r['multiplier'] for r in results]
            active_losses = [r['active_loss_mw'] for r in results]
            
            z = np.polyfit(load_multipliers, active_losses, 2)
            f.write(f"Losses(MW) = {z[0]:.2f} × Load² + {z[1]:.2f} × Load + {z[2]:.2f}\n")
            
            # Calculate R-squared
            p = np.poly1d(z)
            predicted = [p(m) for m in load_multipliers]
            ss_total = sum((l - np.mean(active_losses))**2 for l in active_losses)
            ss_residual = sum((l - p(m))**2 for l, m in zip(active_losses, load_multipliers))
            r_squared = 1 - (ss_residual / ss_total)
            
            f.write(f"R² = {r_squared:.4f}\n")
    
    print("Results saved to simulation_results/time_series_results.txt")

def main():
    try:
        # Fix the swing bus
        generators_file = fix_swing_bus()
        if not generators_file:
            print("Failed to fix or verify swing bus")
            return
        
        # Initialize the circuit with voltage stabilization
        if not initialize_stabilized_circuit():
            print("Failed to initialize stabilized circuit")
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