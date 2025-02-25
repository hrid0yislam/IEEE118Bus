import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())

try:
    import opendssdirect as dss
    print("OpenDSS Direct version:", dss.__version__)
    
    # Test basic functionality
    if dss.Basic.Start(0):
        print("OpenDSS engine started successfully")
    else:
        print("Failed to start OpenDSS engine")
    
    # Create a simple circuit
    dss.Text.Command('Clear')
    dss.Text.Command('New Circuit.test basekv=4.16 phases=3')
    
    # Add a source
    dss.Text.Command('New Vsource.source bus1=sourcebus basekv=4.16 pu=1.0 phases=3')
    
    # Add a line
    dss.Text.Command('New Line.line1 bus1=sourcebus bus2=loadbus length=1 r1=0.1 x1=0.1 units=km')
    
    # Add a load
    dss.Text.Command('New Load.load1 bus1=loadbus kv=4.16 kw=1000 pf=0.95 phases=3')
    
    # Solve
    dss.Text.Command('Solve')
    
    # Check if solved
    if dss.Solution.Converged():
        print("Simple test circuit solved successfully")
        
        # Get some results
        losses = dss.Circuit.Losses()
        print(f"Losses: {losses[0]/1000:.2f} kW, {losses[1]/1000:.2f} kVAR")
        
        # Get voltage at load bus
        dss.Circuit.SetActiveBus('loadbus')
        v_pu = dss.Bus.puVmagAngle()[0]
        print(f"Voltage at load bus: {v_pu:.4f} pu")
    else:
        print("Failed to solve simple test circuit")
        print("Error:", dss.Error.Description())
    
except ImportError:
    print("ERROR: Could not import opendssdirect module")
    print("Please install it with: pip install opendssdirect")
except Exception as e:
    print(f"ERROR: {str(e)}") 