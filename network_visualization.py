import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

def read_voltage_data():
    voltage_data = {}
    with open('ieee118bus_VLN_Node.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[4:]:  # Skip header lines
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    bus_name = parts[0].replace('_', '')
                    voltage_pu = float(parts[4])
                    voltage_data[bus_name] = voltage_pu
    return voltage_data

def create_network_visualization():
    # Create output directory
    os.makedirs('latex_report', exist_ok=True)
    
    # Create graph
    G = nx.Graph()
    
    # Read voltage data
    voltage_data = read_voltage_data()
    
    # Add nodes
    for bus, voltage in voltage_data.items():
        G.add_node(bus, voltage=voltage)
    
    # Add edges (simplified connections between consecutive buses)
    bus_list = list(voltage_data.keys())
    for i in range(len(bus_list)-1):
        G.add_edge(bus_list[i], bus_list[i+1])
    
    # Create visualization
    plt.figure(figsize=(24, 18))
    pos = nx.spring_layout(G, k=2, iterations=100, seed=42)
    
    # Draw nodes with colors based on voltage levels
    node_colors = []
    node_sizes = []
    labels = {}
    
    for node in G.nodes():
        voltage = G.nodes[node]['voltage']
        
        # Node color based on voltage level
        if voltage > 1.05:
            color = 'red'  # High voltage
        elif voltage < 0.95:
            color = 'blue'  # Low voltage
        else:
            color = 'green'  # Normal voltage
        
        node_colors.append(color)
        node_sizes.append(1000)  # Fixed size for better visibility
        labels[node] = f"{node}\nV: {voltage:.3f} pu"
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    
    # Add labels
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Add legend
    legend_elements = [
        plt.scatter([0], [0], c='red', s=100, label='High Voltage (>1.05 pu)'),
        plt.scatter([0], [0], c='green', s=100, label='Normal Voltage'),
        plt.scatter([0], [0], c='blue', s=100, label='Low Voltage (<0.95 pu)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
    
    plt.title('IEEE 118-Bus System Voltage Profile', fontsize=16, pad=20)
    plt.axis('off')
    
    # Save the plot
    plt.savefig('latex_report/voltage_profile.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create voltage summary
    with open('latex_report/voltage_summary.txt', 'w') as f:
        f.write("IEEE 118-Bus System Voltage Summary\n")
        f.write("=================================\n\n")
        
        voltages = list(voltage_data.values())
        f.write(f"Number of Buses: {len(voltages)}\n")
        f.write(f"Maximum Voltage: {max(voltages):.3f} pu\n")
        f.write(f"Minimum Voltage: {min(voltages):.3f} pu\n")
        f.write(f"Average Voltage: {sum(voltages)/len(voltages):.3f} pu\n\n")
        
        f.write("Buses with High Voltage (>1.05 pu):\n")
        for bus, v in voltage_data.items():
            if v > 1.05:
                f.write(f"  {bus}: {v:.3f} pu\n")
        
        f.write("\nBuses with Low Voltage (<0.95 pu):\n")
        for bus, v in voltage_data.items():
            if v < 0.95:
                f.write(f"  {bus}: {v:.3f} pu\n")

def main():
    try:
        print("Creating network visualization...")
        create_network_visualization()
        print("Visualization completed. Check the latex_report directory for:")
        print("1. voltage_profile.png - Visual representation of bus voltages")
        print("2. voltage_summary.txt - Detailed voltage statistics")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 