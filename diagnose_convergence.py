import opendssdirect as dss
import os
import sys

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def diagnose_convergence():
    """Diagnose convergence issues in the IEEE 118-bus system"""
    print_section("DIAGNOSING CONVERGENCE ISSUES")
    
    try:
        # Start OpenDSS
        if not dss.Basic.Start(0):
            print("ERROR: Failed to start OpenDSS engine")
            return False
        
        # Clear and create circuit with minimal components
        dss.Text.Command('Clear')
        dss.Text.Command('Set DefaultBaseFrequency=50')
        dss.Text.Command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
        
        # Set very relaxed solution parameters
        dss.Text.Command('Set VoltageBases=[138.0]')
        dss.Text.Command('Calcv')
        dss.Text.Command('set algorithm=NEWTON')
        dss.Text.Command('set maxiterations=1000')
        dss.Text.Command('set maxcontroliter=1000')
        dss.Text.Command('set tolerance=0.1')
        
        print("Circuit initialized with relaxed settings")
        
        # Test 1: Circuit with only generators
        print_section("TEST 1: CIRCUIT WITH ONLY GENERATORS")
        
        # Check if generators.dss exists
        if not os.path.isfile('generators.dss'):
            print("ERROR: generators.dss file not found")
            return False
        
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
            
            # Use the fixed file
            dss.Text.Command('Redirect generators_fixed.dss')
            print("Using fixed generators file")
        else:
            # Use the original file
            dss.Text.Command('Redirect generators.dss')
            print("Using original generators file")
        
        # Try to solve
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("SUCCESS: Circuit with only generators converged")
        else:
            print("FAILED: Circuit with only generators did not converge")
            print("Error:", dss.Error.Description())
            return False
        
        # Test 2: Add lines
        print_section("TEST 2: ADDING LINES")
        
        dss.Text.Command('Redirect lines.dss')
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("SUCCESS: Circuit with generators and lines converged")
        else:
            print("FAILED: Circuit with generators and lines did not converge")
            print("Error:", dss.Error.Description())
            return False
        
        # Test 3: Add transformers
        print_section("TEST 3: ADDING TRANSFORMERS")
        
        dss.Text.Command('Redirect transformers.dss')
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("SUCCESS: Circuit with generators, lines, and transformers converged")
        else:
            print("FAILED: Circuit with generators, lines, and transformers did not converge")
            print("Error:", dss.Error.Description())
            return False
        
        # Test 4: Add shunts
        print_section("TEST 4: ADDING SHUNTS")
        
        dss.Text.Command('Redirect shunts.dss')
        dss.Text.Command('Redirect sw_shunts.dss')
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("SUCCESS: Circuit with generators, lines, transformers, and shunts converged")
        else:
            print("FAILED: Circuit with generators, lines, transformers, and shunts did not converge")
            print("Error:", dss.Error.Description())
            return False
        
        # Test 5: Add loads at reduced level
        print_section("TEST 5: ADDING LOADS AT REDUCED LEVEL")
        
        # Add loads
        dss.Text.Command('Redirect loads.dss')
        
        # Scale all loads to 10%
        dss.Circuit.SetActiveClass('Load')
        load_count = len(dss.ActiveClass.AllNames())
        print(f"Found {load_count} loads")
        
        for load_name in dss.ActiveClass.AllNames():
            try:
                dss.Circuit.SetActiveElement(f'Load.{load_name}')
                orig_kw = float(dss.Properties.Value('kW'))
                orig_kvar = float(dss.Properties.Value('kvar'))
                dss.Text.Command(f'Edit Load.{load_name} kW={orig_kw*0.1:.1f} kvar={orig_kvar*0.1:.1f}')
            except Exception as e:
                print(f"Warning: Error scaling load {load_name}: {str(e)}")
        
        print("Scaled all loads to 10%")
        
        # Try to solve
        dss.Solution.Solve()
        
        if dss.Solution.Converged():
            print("SUCCESS: Circuit with all components at 10% load converged")
        else:
            print("FAILED: Circuit with all components at 10% load did not converge")
            print("Error:", dss.Error.Description())
            return False
        
        # Test 6: Progressive loading
        print_section("TEST 6: PROGRESSIVE LOADING")
        
        load_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
        max_converged_level = 0.1
        
        for level in load_levels:
            print(f"\nTesting at {level*100:.0f}% load...")
            
            # Scale all loads
            for load_name in dss.ActiveClass.AllNames():
                try:
                    dss.Circuit.SetActiveElement(f'Load.{load_name}')
                    orig_kw = float(dss.Properties.Value('kW'))
                    orig_kvar = float(dss.Properties.Value('kvar'))
                    
                    # Calculate new values based on original values (not current values)
                    new_kw = orig_kw * level
                    new_kvar = orig_kvar * level
                    
                    dss.Text.Command(f'Edit Load.{load_name} kW={new_kw:.1f} kvar={new_kvar:.1f}')
                except Exception as e:
                    print(f"Warning: Error scaling load {load_name}: {str(e)}")
            
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
                    break
                else:
                    print(f"  FAILED: Did not converge at {level*100:.0f}% load")
            
            if not converged:
                print(f"\nWARNING: Could not converge at {level*100:.0f}% load")
                print(f"Maximum converged load level: {max_converged_level*100:.0f}%")
                break
        
        # Summary
        print_section("DIAGNOSIS SUMMARY")
        
        if max_converged_level >= 1.0:
            print("RESULT: System converges at full load (100%)")
            print("The time series simulation should work correctly.")
        elif max_converged_level >= 0.6:
            print(f"RESULT: System converges at {max_converged_level*100:.0f}% load")
            print("The time series simulation may work with reduced load levels.")
        else:
            print(f"RESULT: System only converges at {max_converged_level*100:.0f}% load")
            print("The time series simulation will likely fail without significant modifications.")
        
        # Recommendations
        print("\nRECOMMENDATIONS:")
        
        if swing_bus_commented:
            print("1. Use the fixed generators file (generators_fixed.dss) with the uncommented swing bus")
        
        print("2. Use very relaxed solution parameters:")
        print("   - Algorithm: NEWTON")
        print("   - Max iterations: 1000")
        print("   - Tolerance: 0.1")
        
        if max_converged_level < 1.0:
            print(f"3. Limit the maximum load level to {max_converged_level*100:.0f}%")
        
        print("4. Use progressive loading with small steps")
        print("5. Implement robust error handling in your scripts")
        
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        error = dss.Error.Description()
        if error:
            print(f"OpenDSS Error: {error}")
        return False

if __name__ == "__main__":
    diagnose_convergence() 