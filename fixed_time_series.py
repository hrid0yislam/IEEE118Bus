import opendssdirect as dss
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def initialize_dss():
    """Initialize OpenDSS with settings to improve convergence"""
    print("Initializing OpenDSS...")
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            raise Exception("Failed to start OpenDSS")
        
        # Clear and create circuit FIRST
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        
        # Create circuit with very relaxed settings
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
        
        # Set very relaxed solution parameters
        print("Setting up initial solution parameters...")
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        
        # Use very relaxed settings initially
        dss.Text.Command('set algorithm=NEWTON')
        dss.Text.Command('set maxiterations=1000')
        dss.Text.Command('set maxcontroliter=1000')
        dss.Text.Command('set tolerance=0.01')
        
        # Load components gradually with stabilization between each step
        print("\nLoading circuit components gradually...")
        
        # First load generators (voltage sources)
        print("Loading generators...")
        dss.Text.Command('Redirect generators.dss')
        stabilize_system()
        
        # Then load lines
        print("Loading lines...")
        dss.Text.Command('Redirect lines.dss')
        stabilize_system()
        
        # Then load transformers
        print("Loading transformers...")
        dss.Text.Command('Redirect transformers.dss')
        stabilize_system()
        
        # Load shunts before loads
        print("Loading shunts...")
        dss.Text.Command('Redirect shunts.dss')
        dss.Text.Command('Redirect sw_shunts.dss')
        stabilize_system()
        
        # Finally load loads at reduced level
        print("Loading loads at reduced level...")
        dss.Text.Command('Redirect loads.dss')
        
        # Scale all loads to 10% initially
        scale_loads_safely(0.1)
        stabilize_system()
        
        # Gradually increase load to 100%
        print("\nGradually increasing load to 100%...")
        for load_level in [0.2, 0.4, 0.6, 0.8, 1.0]:
            print(f"Setting load to {load_level*100:.0f}%...")
            scale_loads_safely(load_level)
            if not stabilize_system():
                print(f"Could not converge at {load_level*100:.0f}% load")
                # If we can't reach 100%, but got to at least 60%, consider it good enough
                if load_level >= 0.6:
                    print("Reached at least 60% load, continuing with simulation")
                    return True
                else:
                    raise Exception(f"Could not stabilize system at {load_level*100:.0f}% load")
        
        print("Base case converged successfully at 100% load.")
        return True
    except Exception as e:
        print(f"Initialization error: {str(e)}")
        return False

def stabilize_system():
    """Try to stabilize the system with multiple solution attempts"""
    print("Attempting to stabilize system...")
    
    # Try different algorithms and settings
    solution_attempts = [
        # First try with normal settings
        {'algorithm': 'NEWTON', 'iterations': 100, 'tolerance': 0.001},
        # Then try with more relaxed settings
        {'algorithm': 'NEWTON', 'iterations': 500, 'tolerance': 0.01},
        # Try with very relaxed settings
        {'algorithm': 'NEWTON', 'iterations': 1000, 'tolerance': 0.1},
        # Try with different algorithm
        {'algorithm': 'NORM', 'iterations': 500, 'tolerance': 0.01}
    ]
    
    for i, settings in enumerate(solution_attempts):
        # Apply solution settings
        dss.Text.Command(f"set algorithm={settings['algorithm']}")
        dss.Text.Command(f"set maxiterations={settings['iterations']}")
        dss.Text.Command(f"set tolerance={settings['tolerance']}")
        
        # Try to solve
        print(f"  Attempt {i+1}: {settings['algorithm']}, tol={settings['tolerance']}")
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print(f"  System stabilized on attempt {i+1}")
            return True
    
    print("  Failed to stabilize system after all attempts")
    return False

def scale_loads_safely(multiplier):
    """Scale all loads with proper error handling"""
    try:
        # Get all loads
        load_names = []
        dss.Circuit.SetActiveClass('Load')
        for load_name in dss.ActiveClass.AllNames():
            load_names.append(load_name)
        
        # Scale each load individually
        for load_name in load_names:
            try:
                # Access load properties safely
                dss.Circuit.SetActiveElement(f'Load.{load_name}')
                
                # Get base values from model property
                base_kw = float(dss.Properties.Value('kW'))
                base_kvar = float(dss.Properties.Value('kvar'))
                
                # Calculate new values
                new_kw = base_kw * multiplier
                new_kvar = base_kvar * multiplier
                
                # Use Edit command to modify the load
                dss.Text.Command(f'Edit Load.{load_name} kW={new_kw:.1f} kvar={new_kvar:.1f}')
            except Exception as e:
                print(f"Warning: Error scaling load {load_name}: {str(e)}")
        
        return True
    except Exception as e:
        print(f"Load scaling error: {str(e)}")
        return False

def get_system_metrics():
    """Get voltage and loss metrics with error handling"""
    try:
        # Get voltages
        voltages = []
        dss.Circuit.SetActiveBus("")
        for bus in dss.Circuit.AllBusNames():
            try:
                dss.Circuit.SetActiveBus(bus)
                v_mag = dss.Bus.puVmagAngle()[0]
                voltages.append(v_mag)
            except:
                print(f"Warning: Could not get voltage for bus {bus}")
        
        # Get losses
        losses = dss.Circuit.Losses()
        
        # Calculate metrics
        if voltages:
            min_v = min(voltages)
            max_v = max(voltages)
            avg_v = sum(voltages) / len(voltages)
        else:
            min_v = max_v = avg_v = 0
        
        return {
            'min_voltage': min_v,
            'max_voltage': max_v,
            'avg_voltage': avg_v,
            'active_loss_mw': losses[0] / 1000000,
            'reactive_loss_mvar': losses[1] / 1000000
        }
    except Exception as e:
        print(f"Error getting metrics: {str(e)}")
        return None

def run_time_series():
    """Run time series simulation with improved convergence handling"""
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
        print(f"\nProcessing hour {hour:02d}:00 (Load: {multiplier:.2%})")
        
        # Scale loads safely
        if not scale_loads_safely(multiplier):
            print(f"Failed to scale loads for hour {hour}")
            continue
        
        # Try to stabilize the system
        if not stabilize_system():
            print(f"Failed to converge for hour {hour}")
            continue
        
        # Get results
        metrics = get_system_metrics()
        if metrics:
            metrics['hour'] = hour
            metrics['multiplier'] = multiplier
            results.append(metrics)
            
            # Print key metrics
            print(f"  Voltage range: {metrics['min_voltage']:.3f} - {metrics['max_voltage']:.3f} pu")
            print(f"  Losses: {metrics['active_loss_mw']:.2f} MW, {metrics['reactive_loss_mvar']:.2f} MVAR")
    
    # Create visualizations if we have results
    if results:
        create_visualizations(results)
        save_results_to_file(results)
        return True
    else:
        print("No results to visualize")
        return False

def create_visualizations(results):
    """Create visualizations of the results"""
    # Extract data for plotting
    hours = [r['hour'] for r in results]
    active_losses = [r['active_loss_mw'] for r in results]
    reactive_losses = [r['reactive_loss_mvar'] for r in results]
    min_voltages = [r['min_voltage'] for r in results]
    max_voltages = [r['max_voltage'] for r in results]
    avg_voltages = [r['avg_voltage'] for r in results]
    
    # Create figure with subplots
    plt.figure(figsize=(12, 15))
    
    # Plot 1: Losses
    plt.subplot(3, 1, 1)
    plt.plot(hours, active_losses, 'b-', label='Active (MW)', marker='o')
    plt.plot(hours, reactive_losses, 'r--', label='Reactive (MVAR)', marker='s')
    plt.title('System Losses Over 24 Hours')
    plt.xlabel('Hour')
    plt.ylabel('Power Loss')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: Voltage Profile
    plt.subplot(3, 1, 2)
    plt.plot(hours, min_voltages, 'r-', label='Minimum', marker='v')
    plt.plot(hours, max_voltages, 'g-', label='Maximum', marker='^')
    plt.plot(hours, avg_voltages, 'b--', label='Average', marker='o')
    plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
    plt.axhline(y=1.05, color='g', linestyle='--', label='Upper Limit')
    plt.title('System Voltage Profile')
    plt.xlabel('Hour')
    plt.ylabel('Voltage (pu)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 3: Load vs Losses
    plt.subplot(3, 1, 3)
    multipliers = [r['multiplier'] for r in results]
    plt.scatter(multipliers, active_losses, label='Active Losses', alpha=0.7)
    
    # Add trend line
    z = np.polyfit(multipliers, active_losses, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(multipliers), max(multipliers), 100)
    plt.plot(x_trend, p(x_trend), "r--", alpha=0.8, label='Quadratic Trend')
    
    plt.title('Load vs Losses Relationship')
    plt.xlabel('Load Multiplier')
    plt.ylabel('Active Losses (MW)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('simulation_results/time_series_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations saved to simulation_results/time_series_results.png")

def save_results_to_file(results):
    """Save results to text file"""
    with open('simulation_results/time_series_summary.txt', 'w') as f:
        f.write("Time Series Simulation Results\n")
        f.write("============================\n\n")
        
        # Write hourly results
        f.write("Hourly Results:\n")
        f.write("--------------\n")
        for r in results:
            f.write(f"Hour {r['hour']:02d}:00 (Load: {r['multiplier']:.2%})\n")
            f.write(f"  Voltage range: {r['min_voltage']:.3f} - {r['max_voltage']:.3f} pu\n")
            f.write(f"  Losses: {r['active_loss_mw']:.2f} MW, {r['reactive_loss_mvar']:.2f} MVAR\n\n")
        
        # Write summary statistics
        f.write("\nSummary Statistics:\n")
        f.write("------------------\n")
        
        # Calculate statistics
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
    
    print("Results summary saved to simulation_results/time_series_summary.txt")

def main():
    try:
        # Initialize OpenDSS
        if not initialize_dss():
            print("Failed to initialize OpenDSS")
            return
        
        print("\nStarting time series simulation...")
        run_time_series()
        
        print("\nSimulation completed.")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")

if __name__ == "__main__":
    main() 