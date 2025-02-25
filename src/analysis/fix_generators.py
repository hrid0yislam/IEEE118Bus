import os

def fix_generators():
    """Fix the generators.dss file by uncommenting the swing bus"""
    try:
        # Read the file
        with open('generators.dss', 'r') as f:
            lines = f.readlines()
        
        # Create a backup
        with open('generators.dss.bak', 'w') as f:
            f.writelines(lines)
        
        # Find and fix the swing bus line
        fixed_lines = []
        for line in lines:
            if '! New Generator.Gen_at_89_1' in line:
                # Uncomment the line
                fixed_line = line.replace('! New Generator.Gen_at_89_1', 'New Generator.Gen_at_89_1')
                fixed_lines.append(fixed_line)
                print(f"Fixed line: {line.strip()} -> {fixed_line.strip()}")
            else:
                fixed_lines.append(line)
        
        # Write the fixed file
        with open('generators_fixed.dss', 'w') as f:
            f.writelines(fixed_lines)
        
        print(f"Created fixed file: generators_fixed.dss")
        print("To use this file, modify master_file.dss to redirect to generators_fixed.dss instead of generators.dss")
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Fixing generators.dss file...")
    if fix_generators():
        print("Successfully created fixed generators file.")
    else:
        print("Failed to fix generators file.") 