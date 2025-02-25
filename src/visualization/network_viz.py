import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os

def clean_bus_name(name):
    """Clean bus name by removing special characters"""
    return name.replace('_', '').replace('/', '')

# Create output directory
os.makedirs('thesis_figures', exist_ok=True)

# Define the key buses and their voltage levels
bus_data = {
    'bus89': {'voltage': 0.678, 'name': 'CLINCHRV'},
    'bus92': {'voltage': 0.550, 'name': 'SALTVLLE'},
    'bus77': {'voltage': 0.227, 'name': 'TURNER'},
    'bus85': {'voltage': 0.526, 'name': 'BEAVERCK'},
    'bus69': {'voltage': 0.161, 'name': 'SPORN'}
}

# Create graph
G = nx.Graph()

# Add nodes
for bus_id, data in bus_data.items():
    G.add_node(bus_id, 
               voltage=data['voltage'],
               name=data['name'])

# Add edges (connections between buses)
edges = [
    ('bus89', 'bus92', {'loss': 11601.50}),
    ('bus92', 'bus77', {'loss': 8710.97}),
    ('bus77', 'bus85', {'loss': 8700.41}),
    ('bus85', 'bus69', {'loss': 3601.15})
]

G.add_edges_from(edges)

# Create the visualization
plt.figure(figsize=(15, 10))

# Create layout
pos = nx.spring_layout(G, k=1, iterations=50)

# Draw nodes with colors based on voltage levels
node_colors = []
node_sizes = []
for node in G.nodes():
    voltage = G.nodes[node]['voltage']
    if voltage > 0.95:
        color = 'red'
    elif voltage > 0.90:
        color = 'yellow'
    else:
        color = 'blue'
    node_colors.append(color)
    node_sizes.append(2000)  # Size proportional to voltage

# Draw edges with width based on losses
edge_widths = []
edge_colors = []
for (u, v, d) in G.edges(data=True):
    if 'loss' in d:
        # Normalize loss for width
        width = d['loss'] / 2000  # Adjust divisor to scale line width
        edge_widths.append(width)
        edge_colors.append('gray')

# Draw the network
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.6)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.7)

# Add labels
labels = {node: f"{G.nodes[node]['name']}\n{G.nodes[node]['voltage']:.3f} pu" 
         for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

# Add title and legend
plt.title('IEEE 118-Bus System: Voltage Levels and Power Losses', pad=20)

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='High V (>0.95 pu)',
               markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Medium V (0.90-0.95 pu)',
               markerfacecolor='yellow', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Low V (<0.90 pu)',
               markerfacecolor='blue', markersize=10)
]
plt.legend(handles=legend_elements, loc='upper right')

# Remove axis
plt.axis('off')

# Save the figure
plt.savefig('thesis_figures/network_voltage_loss.png', dpi=300, bbox_inches='tight')
plt.close()

# Save analysis to text file
with open('thesis_figures/network_analysis.txt', 'w') as f:
    f.write("Network Analysis of IEEE 118-Bus System\n")
    f.write("=====================================\n\n")
    
    f.write("1. Voltage Levels:\n")
    for bus_id, data in bus_data.items():
        f.write(f"   {data['name']}: {data['voltage']:.3f} pu\n")
    
    f.write("\n2. Power Losses:\n")
    total_loss = sum(d['loss'] for _, _, d in G.edges(data=True) if 'loss' in d)
    f.write(f"   Total losses in analyzed section: {total_loss:.2f} kW\n")
    for u, v, d in G.edges(data=True):
        if 'loss' in d:
            f.write(f"   {G.nodes[u]['name']} - {G.nodes[v]['name']}: {d['loss']:.2f} kW\n")

print("Created network visualization and analysis in thesis_figures directory") 