def read_voltage_data():
    try:
        with open('ieee118bus_VLN_Node.txt', 'r') as f:
            print("File opened successfully")
            lines = f.readlines()
            print(f"Read {len(lines)} lines")
            
            # Print first few lines
            print("\nFirst 5 lines:")
            for line in lines[:5]:
                print(line.strip())
            
            # Try parsing voltage data
            print("\nTrying to parse voltage data...")
            for line in lines[4:10]:  # Process a few lines after header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        bus_name = parts[0]
                        voltage_pu = parts[4]
                        print(f"Bus: {bus_name}, Voltage (pu): {voltage_pu}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting voltage data test...")
    read_voltage_data() 