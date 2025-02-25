import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Create output directory
os.makedirs('thesis_figures', exist_ok=True)

# Time series data
hours = np.arange(24)
load_multipliers = [0.65, 0.60, 0.58, 0.56, 0.55, 0.57, 0.62, 0.72, 0.85, 
                   0.95, 0.98, 1.00, 0.99, 0.97, 0.95, 0.93, 0.94, 0.98, 
                   1.00, 0.97, 0.92, 0.85, 0.75, 0.68]

# Critical line loss data (in MW)
line_losses = {
    'Line 89-92': 11.60150,
    'Line 92-94': 8.71097,
    'Line 77-82': 8.70041,
    'Line 85-89': 3.60115,
    'Line 69-77': 2.40980
}

# Bus connections for network visualization
bus_connections = [
    ('89', '92'),
    ('92', '94'),
    ('77', '82'),
    ('85', '89'),
    ('69', '77')
]

# Bus positions (approximate layout)
bus_positions = {
    '69': (0, 0),
    '77': (1, 0),
    '82': (2, 0),
    '85': (0, 2),
    '89': (1, 2),
    '92': (2, 2),
    '94': (3, 2)
}

# Create figure with multiple subplots
plt.figure(figsize=(15, 20))

# 1. Line Losses Over Time
plt.subplot(3, 1, 1)
for line, base_loss in line_losses.items():
    # Calculate losses for each hour based on load multiplier squared
    losses = [base_loss * (m ** 2) for m in load_multipliers]
    plt.plot(hours, losses, '-o', label=line, linewidth=2)

plt.title('Line Losses Over 24 Hours', pad=20, fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Power Loss (MW)')
plt.grid(True, alpha=0.3)
plt.legend()

# 2. Loss Distribution
plt.subplot(3, 1, 2)
lines = list(line_losses.keys())
losses = list(line_losses.values())
plt.bar(lines, losses, alpha=0.7)
plt.title('Power Losses by Line', pad=20, fontsize=14)
plt.xlabel('Transmission Lines')
plt.ylabel('Power Loss (MW)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for i, v in enumerate(losses):
    plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

# 3. Network Visualization with Losses
plt.subplot(3, 1, 3)

# Draw buses
for bus, pos in bus_positions.items():
    plt.plot(pos[0], pos[1], 'ko', markersize=20, label=f'Bus {bus}')
    plt.text(pos[0], pos[1], bus, color='white', ha='center', va='center')

# Draw lines with width proportional to losses
max_loss = max(line_losses.values())
for (bus1, bus2) in bus_connections:
    pos1 = bus_positions[bus1]
    pos2 = bus_positions[bus2]
    
    # Find loss for this line
    line_key = f'Line {bus1}-{bus2}'
    if line_key not in line_losses:
        line_key = f'Line {bus2}-{bus1}'
    
    if line_key in line_losses:
        loss = line_losses[line_key]
        width = 1 + 4 * (loss / max_loss)  # Scale line width based on loss
        plt.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                'r-', linewidth=width, alpha=0.6,
                label=f'{line_key}: {loss:.2f} MW')

plt.title('Network Topology with Power Losses', pad=20, fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.axis('equal')

# Adjust layout and save
plt.tight_layout()
plt.savefig('loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save loss summary to text file
with open('loss_summary.txt', 'w') as f:
    f.write("Power Loss Analysis Summary\n")
    f.write("=========================\n\n")
    
    total_loss = sum(line_losses.values())
    f.write(f"Total System Losses: {total_loss:.2f} MW\n\n")
    
    f.write("Losses by Line:\n")
    for line, loss in line_losses.items():
        percentage = (loss / total_loss) * 100
        f.write(f"{line}: {loss:.2f} MW ({percentage:.1f}%)\n")
    
    f.write("\nTime-based Analysis:\n")
    f.write(f"Peak Loss Hours: 11:00, 18:00 (Load Factor: 1.00)\n")
    f.write(f"Minimum Loss Hour: 04:00 (Load Factor: 0.55)\n")

print("Loss analysis visualizations have been saved as 'loss_analysis.png'")
print("Loss summary has been saved as 'loss_summary.txt'")

# Data for major line losses
major_lines = {
    'Line 89-92': 11601.50,
    'Line 92-94': 8710.97,
    'Line 77-82': 8700.41,
    'Line 85-89': 3601.15,
    'Line 69-77': 2409.80
}

# Data for regional losses
regional_losses = {
    'Region 89-92-94': 20312,
    'Region 77-82-83': 13009,
    'Region 85-89': 3601
}

# Data for reactive compensation
reactive_compensation = {
    'Bus 82 (Cap)': -3174.91,
    'Bus 105 (Cap)': -3128.30,
    'Bus 83 (Cap)': -2161.94,
    'Bus 79 (Cap)': -1418.04,
    'Bus 5 (React)': 466.64,
    'Bus 37 (React)': 356.38
}

# 1. Major Line Losses Plot
plt.figure(figsize=(12, 6))
plt.bar(major_lines.keys(), major_lines.values(), color='skyblue')
plt.title('Major Line Losses in IEEE 118-Bus System')
plt.xlabel('Transmission Lines')
plt.ylabel('Losses (kW)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for i, v in enumerate(major_lines.values()):
    plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('thesis_figures/major_line_losses.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Regional Loss Distribution
plt.figure(figsize=(10, 6))
plt.pie(regional_losses.values(), labels=regional_losses.keys(), autopct='%1.1f%%',
        colors=sns.color_palette("pastel"))
plt.title('Distribution of Regional Losses')
plt.axis('equal')
plt.savefig('thesis_figures/regional_losses.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Reactive Power Compensation
plt.figure(figsize=(12, 6))
colors = ['red' if v > 0 else 'blue' for v in reactive_compensation.values()]
plt.bar(reactive_compensation.keys(), reactive_compensation.values(), color=colors)
plt.title('Reactive Power Compensation')
plt.xlabel('Bus Location')
plt.ylabel('Reactive Power (kVAR)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for i, v in enumerate(reactive_compensation.values()):
    plt.text(i, v, f'{v:.1f}', ha='center', va='bottom' if v > 0 else 'top')

plt.tight_layout()
plt.savefig('thesis_figures/reactive_compensation.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. System Loss Overview
loss_components = {
    'Line Losses': 109913.9,
    'Transformer Losses': 4.4
}

plt.figure(figsize=(8, 8))
plt.pie(loss_components.values(), labels=loss_components.keys(), autopct='%1.3f%%',
        colors=['lightcoral', 'lightblue'])
plt.title('Distribution of Total System Losses')
plt.axis('equal')
plt.savefig('thesis_figures/system_losses.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations have been created in the thesis_figures directory.") 