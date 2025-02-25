import os
import re

def fix_generators_file():
    """Fix the swing bus in the generators.dss file"""
    print("Fixing swing bus in generators.dss file...")
    
    # Read the generators file
    try:
        with open('generators.dss', 'r') as f:
            content = f.read()
        
        # Check if the swing bus is commented out
        swing_pattern = r'! swing bus - bus: 89_clinchrv\s*\n! New Generator\.Gen_at_89_1'
        if re.search(swing_pattern, content):
            print("Found commented swing bus. Uncommenting and fixing...")
            
            # Uncomment the swing bus
            fixed_content = content.replace(
                '! swing bus - bus: 89_clinchrv\n! New Generator.Gen_at_89_1',
                '! swing bus - bus: 89_clinchrv\nNew Generator.Gen_at_89_1'
            )
            
            # Create a backup of the original file
            backup_file = 'generators.dss.bak'
            with open(backup_file, 'w') as f:
                f.write(content)
            print(f"Created backup of original file: {backup_file}")
            
            # Write the fixed content
            with open('generators.dss', 'w') as f:
                f.write(fixed_content)
            print("Fixed generators.dss file")
            
            return True
        else:
            print("Swing bus is not commented out or has a different format.")
            return False
    
    except Exception as e:
        print(f"Error fixing generators file: {str(e)}")
        return False

def create_modified_generators_file():
    """Create a modified version of the generators file with the swing bus fixed"""
    print("Creating modified generators file...")
    
    try:
        # Read the original file
        with open('generators.dss', 'r') as f:
            lines = f.readlines()
        
        # Create a new file
        with open('generators_fixed.dss', 'w') as f:
            for line in lines:
                # Check if this is the commented swing bus line
                if '! New Generator.Gen_at_89_1' in line:
                    # Uncomment the line and write it
                    f.write(line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1'))
                else:
                    # Write the line as is
                    f.write(line)
        
        print("Created generators_fixed.dss with uncommented swing bus")
        
        # Create a modified master file that uses the fixed generators file
        with open('master_file_fixed.dss', 'w') as f:
            f.write("""Clear

! Set system base frequency
Set DefaultBaseFrequency=50

! Define the circuit
New Circuit.ieee118bus
~ basekv=138.0 
~ phases=3 
~ pu=1.005 
~ angle=39.69 
~ frequency=50.0 
~ baseMVA=728.5374813610073 
~ puZ1=[0.001, 0.2] 
~ bus1=89_clinchrv

! Load circuit components
! Generator definitions (choose one)
redirect generators_fixed.dss              ! Using fixed generator models with swing bus

! Load other circuit elements
redirect lines.dss                   ! Line definitions
redirect transformers.dss            ! Transformer definitions
redirect loads.dss                   ! Load definitions
redirect shunts.dss                  ! Fixed shunt definitions
redirect sw_shunts.dss              ! Switched shunt definitions
redirect dc_and_facts_equiv_elements.dss     ! DC and FACTS elements

! Set voltage bases and calculate voltage bases for all buses
Set VoltageBases = [138.0]
Calcv
redirect confirm_kv_bases.dss

! Solution parameters
set algorithm=NEWTON                   ! Newton method
set maxcontroliter=100              ! Maximum control iterations
set maxiterations=1000               ! Maximum power flow iterations
set tolerance=0.01                ! Relaxed convergence tolerance
set controlmode=OFF                 ! Disable automatic controls initially

! Solve options
set loadmodel=1                     ! Constant power load model
Solve mode=snap                     ! Snapshot power flow solution

! Show results
show voltages ln Nodes              ! Show voltage profile
show powers MVA Elem                ! Show power flows
show losses                         ! Show system losses
summary                             ! Show system summary
""")
        
        print("Created master_file_fixed.dss that uses the fixed generators file")
        return True
    
    except Exception as e:
        print(f"Error creating modified files: {str(e)}")
        return False

def main():
    """Main function"""
    print("=" * 80)
    print("FIXING SWING BUS ISSUE")
    print("=" * 80)
    
    # Try to fix the generators file directly
    if fix_generators_file():
        print("\nSuccessfully fixed generators.dss file.")
    else:
        # If direct fix fails, create modified files
        if create_modified_generators_file():
            print("\nCreated modified files instead of modifying original files.")
            print("To use the fixed files, run OpenDSS with master_file_fixed.dss")
        else:
            print("\nFailed to fix the swing bus issue.")

if __name__ == "__main__":
    main() 