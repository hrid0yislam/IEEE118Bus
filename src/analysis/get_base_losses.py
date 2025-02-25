import opendssdirect as dss

def get_base_case_losses():
    """Get losses for base case"""
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            raise Exception("Failed to start OpenDSS")
        
        print("Initializing OpenDSS...")
        
        # Clear and create circuit
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
        
        # Load components
        print("\nLoading circuit components...")
        dss.Text.Command('Redirect generators.dss')
        dss.Text.Command('Redirect lines.dss')
        dss.Text.Command('Redirect transformers.dss')
        dss.Text.Command('Redirect loads.dss')
        dss.Text.Command('Redirect shunts.dss')
        dss.Text.Command('Redirect sw_shunts.dss')
        
        # Set solution parameters
        print("\nSetting up solution parameters...")
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        dss.Text.Command('set algorithm=NCIM')
        dss.Text.Command('set maxiterations=100')
        dss.Text.Command('set tolerance=0.0001')
        
        # Solve power flow
        print("\nSolving power flow...")
        dss.Solution.Solve()
        
        if not dss.Solution.Converged():
            print("Solution did not converge!")
            return
        
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
        
        # Print results
        print("\nBase Case Results:")
        print(f"Active Power Loss: {active_loss:.2f} MW")
        print(f"Reactive Power Loss: {reactive_loss:.2f} MVAR")
        print(f"Voltage Range: {min_v:.3f} - {max_v:.3f} pu")
        
        # Get individual line losses
        print("\nMajor Line Losses:")
        dss.Circuit.SetActiveClass('Line')
        for line_name in dss.ActiveClass.AllNames():
            dss.Circuit.SetActiveElement(f'Line.{line_name}')
            line_losses = dss.CktElement.Losses()
            if abs(line_losses[0]) > 1000000:  # Show lines with losses > 1 MW
                print(f"{line_name}: {line_losses[0]/1000000:.2f} MW")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")

if __name__ == "__main__":
    get_base_case_losses() 