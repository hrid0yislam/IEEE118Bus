import opendssdirect as dss

def initialize_dss():
    """Initialize OpenDSS with basic settings"""
    print("Initializing OpenDSS...")
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            raise Exception("Failed to start OpenDSS")
        
        # Clear and create circuit
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
        
        # Load components
        dss.Text.Command('Redirect generators.dss')
        dss.Text.Command('Redirect lines.dss')
        dss.Text.Command('Redirect transformers.dss')
        dss.Text.Command('Redirect loads.dss')
        dss.Text.Command('Redirect shunts.dss')
        dss.Text.Command('Redirect sw_shunts.dss')
        
        # Set solution parameters
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        dss.Text.Command('set algorithm=NCIM')
        dss.Text.Command('set maxiterations=100')
        dss.Text.Command('set tolerance=0.0001')
        
        return True
    except Exception as e:
        print(f"Initialization error: {str(e)}")
        return False

def scale_loads(multiplier):
    """Scale all loads individually"""
    try:
        # Get all loads
        dss.Circuit.SetActiveClass('Load')
        for load_name in dss.ActiveClass.AllNames():
            # Get original kW and kvar values
            dss.Circuit.SetActiveElement(f'Load.{load_name}')
            orig_kw = float(dss.Properties.Value('kW'))
            orig_kvar = float(dss.Properties.Value('kvar'))
            
            # Calculate new values
            new_kw = orig_kw * multiplier
            new_kvar = orig_kvar * multiplier
            
            # Set new values
            dss.Text.Command(f'Edit Load.{load_name} kW={new_kw:.1f} kvar={new_kvar:.1f}')
        
        return True
    except Exception as e:
        print(f"Load scaling error: {str(e)}")
        return False

def run_simulation():
    """Run time series simulation"""
    # Define load multipliers for 24 hours
    load_multipliers = [
        0.65, 0.60, 0.58, 0.56, 0.55, 0.57,  # Hours 0-5
        0.62, 0.72, 0.85, 0.95, 0.98, 1.00,  # Hours 6-11
        0.99, 0.97, 0.95, 0.93, 0.94, 0.98,  # Hours 12-17
        1.00, 0.97, 0.92, 0.85, 0.75, 0.68   # Hours 18-23
    ]
    
    # Create output file
    with open('simulation_results.txt', 'w') as f:
        f.write("Time Series Simulation Results\n")
        f.write("============================\n\n")
        
        # Run simulation for each hour
        for hour, multiplier in enumerate(load_multipliers):
            print(f"\nProcessing hour {hour:02d}:00 (Load: {multiplier:.2%})")
            f.write(f"\nHour {hour:02d}:00 (Load: {multiplier:.2%})\n")
            
            try:
                # Scale all loads
                if not scale_loads(multiplier):
                    msg = f"Failed to scale loads"
                    print(msg)
                    f.write(f"  {msg}\n")
                    continue
                
                # Solve power flow
                dss.Solution.Solve()
                
                if not dss.Solution.Converged():
                    msg = f"Solution did not converge"
                    print(msg)
                    f.write(f"  {msg}\n")
                    continue
                
                # Get losses
                losses = dss.Circuit.Losses()
                active_loss = losses[0]/1000  # Convert to MW
                reactive_loss = losses[1]/1000  # Convert to MVAR
                
                # Get voltage range
                voltages = []
                dss.Circuit.SetActiveBus("")
                for bus in dss.Circuit.AllBusNames():
                    dss.Circuit.SetActiveBus(bus)
                    v_mag = dss.Bus.puVmagAngle()[0]
                    voltages.append(v_mag)
                
                min_v = min(voltages)
                max_v = max(voltages)
                
                # Print and save results
                results = [
                    f"  Active Power Loss: {active_loss:.2f} MW",
                    f"  Reactive Power Loss: {reactive_loss:.2f} MVAR",
                    f"  Voltage Range: {min_v:.3f} - {max_v:.3f} pu"
                ]
                
                for line in results:
                    print(line)
                    f.write(line + "\n")
                
            except Exception as e:
                msg = f"Error in hour {hour}: {str(e)}"
                print(msg)
                f.write(f"  {msg}\n")

def main():
    if not initialize_dss():
        print("Failed to initialize OpenDSS")
        return
    
    print("\nStarting time series simulation...")
    run_simulation()
    print("\nSimulation completed. Results saved to 'simulation_results.txt'")

if __name__ == "__main__":
    main() 