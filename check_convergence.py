import opendssdirect as dss

def check_system_conditions():
    """Check and report system conditions that might cause convergence issues"""
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            raise Exception("Failed to start OpenDSS")
        
        print("Initializing OpenDSS and checking system conditions...")
        
        # Clear and create circuit FIRST before setting other parameters
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
        
        # NOW we can set solution modes and other parameters
        dss.Text.Command('Set controlmode=static')
        dss.Text.Command('Set mode=snapshot')
        
        # Load components with status checking
        print("\nChecking circuit components...")
        
        # Load and check generators
        print("\nChecking generators...")
        dss.Text.Command('Redirect generators.dss')
        dss.Circuit.SetActiveClass('Generator')
        n_gens = len(dss.ActiveClass.AllNames())
        print(f"Found {n_gens} generators")
        
        # Load and check lines
        print("\nChecking transmission lines...")
        dss.Text.Command('Redirect lines.dss')
        dss.Circuit.SetActiveClass('Line')
        n_lines = len(dss.ActiveClass.AllNames())
        print(f"Found {n_lines} lines")
        
        # Load and check transformers
        print("\nChecking transformers...")
        dss.Text.Command('Redirect transformers.dss')
        dss.Circuit.SetActiveClass('Transformer')
        n_trans = len(dss.ActiveClass.AllNames())
        print(f"Found {n_trans} transformers")
        
        # Load and check loads
        print("\nChecking loads...")
        dss.Text.Command('Redirect loads.dss')
        dss.Circuit.SetActiveClass('Load')
        n_loads = len(dss.ActiveClass.AllNames())
        total_mw = 0
        total_mvar = 0
        for load_name in dss.ActiveClass.AllNames():
            dss.Circuit.SetActiveElement(f'Load.{load_name}')
            total_mw += float(dss.Properties.Value('kW')) / 1000
            total_mvar += float(dss.Properties.Value('kvar')) / 1000
        print(f"Found {n_loads} loads")
        print(f"Total load: {total_mw:.1f} MW + j{total_mvar:.1f} MVAR")
        
        # Load remaining components
        dss.Text.Command('Redirect shunts.dss')
        dss.Text.Command('Redirect sw_shunts.dss')
        
        # Set solution parameters with better convergence properties
        print("\nSetting up solution parameters...")
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        dss.Text.Command('set algorithm=NEWTON')  # Try Newton-Raphson instead of NCIM
        dss.Text.Command('set maxiterations=500')  # Increase maximum iterations
        dss.Text.Command('set tolerance=0.001')    # Slightly relax tolerance
        
        # Try solving with progressive loading
        print("\nAttempting solution with progressive loading...")
        load_steps = [0.2, 0.4, 0.6, 0.8, 1.0]
        
        for step in load_steps:
            print(f"\nTrying {step*100:.0f}% load...")
            
            # Scale all loads
            dss.Circuit.SetActiveClass('Load')
            for load_name in dss.ActiveClass.AllNames():
                dss.Circuit.SetActiveElement(f'Load.{load_name}')
                try:
                    orig_kw = float(dss.Properties.Value('kW'))
                    orig_kvar = float(dss.Properties.Value('kvar'))
                    dss.Text.Command(f'Edit Load.{load_name} kW={orig_kw*step:.1f} kvar={orig_kvar*step:.1f}')
                except Exception as e:
                    print(f"  Error scaling load {load_name}: {str(e)}")
            
            # Solve power flow
            dss.Solution.Solve()
            
            if not dss.Solution.Converged():
                print(f"Failed to converge at {step*100:.0f}% loading")
                
                # Check voltages at this point
                print("\nChecking voltages at failure point...")
                v_issues = []
                dss.Circuit.SetActiveBus("")
                for bus in dss.Circuit.AllBusNames():
                    dss.Circuit.SetActiveBus(bus)
                    v_mag = dss.Bus.puVmagAngle()[0]
                    if v_mag < 0.9 or v_mag > 1.1:
                        v_issues.append(f"Bus {bus}: {v_mag:.3f} pu")
                
                if v_issues:
                    print("\nVoltage issues detected:")
                    for issue in v_issues[:5]:  # Show first 5 issues
                        print(issue)
                    if len(v_issues) > 5:
                        print(f"...and {len(v_issues)-5} more issues")
                
                # Try to help the convergence
                print("\nTrying to help convergence...")
                dss.Text.Command('Set MaxControlIter=100')  # Increase control iterations
                dss.Text.Command('Solve mode=snap')        # Try direct snapshot solution
                
                if dss.Solution.Converged():
                    print("Solution converged after adjustments!")
                else:
                    print("Still unable to converge after adjustments.")
                
                break
            else:
                print(f"Successfully converged at {step*100:.0f}% loading")
                
                # Get system metrics at this point
                losses = dss.Circuit.Losses()
                print(f"Active losses: {losses[0]/1000000:.2f} MW")
                print(f"Reactive losses: {losses[1]/1000000:.2f} MVAR")
        
        print("\nSystem check completed.")
        
    except Exception as e:
        print(f"\nError during system check: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")

if __name__ == "__main__":
    check_system_conditions() 