import sys
import os
import platform

def check_environment():
    """Check the Python environment and system information"""
    print("=" * 80)
    print("ENVIRONMENT INFORMATION")
    print("=" * 80)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if OpenDSS is installed
    try:
        import opendssdirect
        print(f"OpenDSS Direct version: {opendssdirect.__version__}")
        print("OpenDSS Direct is installed correctly")
    except ImportError:
        print("ERROR: OpenDSS Direct is not installed")
        print("Try installing it with: pip install opendssdirect")
        return False
    except Exception as e:
        print(f"ERROR loading OpenDSS Direct: {str(e)}")
        return False
    
    # Check other dependencies
    try:
        import numpy
        print(f"NumPy version: {numpy.__version__}")
    except ImportError:
        print("WARNING: NumPy is not installed")
    
    try:
        import matplotlib
        print(f"Matplotlib version: {matplotlib.__version__}")
    except ImportError:
        print("WARNING: Matplotlib is not installed")
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n" + "=" * 80)
    print("FILE CHECK")
    print("=" * 80)
    
    required_files = [
        'master_file.dss',
        'generators.dss',
        'lines.dss',
        'transformers.dss',
        'loads.dss',
        'shunts.dss',
        'sw_shunts.dss',
        'confirm_kv_bases.dss'
    ]
    
    all_files_exist = True
    
    for file in required_files:
        if os.path.isfile(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
            all_files_exist = False
    
    return all_files_exist

def check_opendss_functionality():
    """Check if OpenDSS can create a simple circuit"""
    print("\n" + "=" * 80)
    print("OPENDSS FUNCTIONALITY TEST")
    print("=" * 80)
    
    try:
        import opendssdirect as dss
        
        # Start OpenDSS
        if not dss.Basic.Start(0):
            print("ERROR: Failed to start OpenDSS engine")
            return False
        
        print("OpenDSS engine started successfully")
        
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
            
            return True
        else:
            print("ERROR: Failed to solve simple test circuit")
            print("Error:", dss.Error.Description())
            return False
    
    except Exception as e:
        print(f"ERROR testing OpenDSS functionality: {str(e)}")
        return False

def main():
    """Main function"""
    print("\nOPENDSS INSTALLATION CHECK")
    print("========================\n")
    
    # Check environment
    env_ok = check_environment()
    if not env_ok:
        print("\nEnvironment check failed. Please fix the issues before continuing.")
    
    # Check files
    files_ok = check_files()
    if not files_ok:
        print("\nFile check failed. Please make sure all required files are present.")
    
    # Check OpenDSS functionality
    func_ok = check_opendss_functionality()
    if not func_ok:
        print("\nOpenDSS functionality test failed. Please check the OpenDSS installation.")
    
    # Overall result
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if env_ok and files_ok and func_ok:
        print("All checks passed. OpenDSS is installed correctly and ready to use.")
    else:
        print("Some checks failed. Please fix the issues before running the time series simulation.")

if __name__ == "__main__":
    main() 