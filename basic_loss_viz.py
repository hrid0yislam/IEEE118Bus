import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Define the loss data
losses = {
    'Line 89-92': {'loss': 11.60150, 'from_bus': '89', 'to_bus': '92'},
    'Line 92-94': {'loss': 8.71097, 'from_bus': '92', 'to_bus': '94'},
    'Line 77-82': {'loss': 8.70041, 'from_bus': '77', 'to_bus': '82'},
    'Line 85-89': {'loss': 3.60115, 'from_bus': '85', 'to_bus': '89'},
    'Line 69-77': {'loss': 2.40980, 'from_bus': '69', 'to_bus': '77'}
}

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# 1. Bar plot of losses
lines = list(losses.keys())
loss_values = [data['loss'] for data in losses.values()]

bars = ax1.bar(lines, loss_values, color='skyblue', alpha=0.7)
ax1.set_title('Power Losses in Critical Lines', fontsize=14, pad=20)
ax1.set_xlabel('Transmission Lines')
ax1.set_ylabel('Power Loss (MW)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

# 2. Network diagram with losses
# Define bus positions
bus_pos = {
    '69': (1, 1),
    '77': (2, 1),
    '82': (3, 1),
    '85': (1, 3),
    '89': (2, 3),
    '92': (3, 3),
    '94': (4, 3)
}

# Draw buses
for bus, pos in bus_pos.items():
    ax2.plot(pos[0], pos[1], 'ko', markersize=20)
    ax2.text(pos[0], pos[1], bus, color='white', ha='center', va='center', fontsize=12)

# Draw lines with width proportional to losses
max_loss = max(data['loss'] for data in losses.values())
for line, data in losses.items():
    from_pos = bus_pos[data['from_bus']]
    to_pos = bus_pos[data['to_bus']]
    width = 1 + 3 * (data['loss'] / max_loss)
    ax2.plot([from_pos[0], to_pos[0]], [from_pos[1], to_pos[1]], 
             'r-', linewidth=width, alpha=0.6,
             label=f"{line}: {data['loss']:.2f} MW")

ax2.set_title('Network Topology with Power Losses', fontsize=14, pad=20)
ax2.grid(True, alpha=0.3)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.set_xlim(0.5, 4.5)
ax2.set_ylim(0.5, 3.5)
ax2.axis('equal')
ax2.axis('off')

# Adjust layout and save
plt.tight_layout()
plt.savefig('power_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save summary to text file
with open('power_loss_summary.txt', 'w') as f:
    f.write("Power Loss Analysis Summary\n")
    f.write("==========================\n\n")
    
    total_loss = sum(data['loss'] for data in losses.values())
    f.write(f"Total System Losses: {total_loss:.2f} MW\n\n")
    
    f.write("Losses by Line:\n")
    f.write("--------------\n")
    for line, data in losses.items():
        percentage = (data['loss'] / total_loss) * 100
        f.write(f"{line}: {data['loss']:.2f} MW ({percentage:.1f}%)\n")
    
    f.write("\nCritical Paths:\n")
    f.write("-------------\n")
    f.write(f"1. Path 89-92-94: {losses['Line 89-92']['loss'] + losses['Line 92-94']['loss']:.2f} MW\n")
    f.write(f"2. Path 69-77-82: {losses['Line 69-77']['loss'] + losses['Line 77-82']['loss']:.2f} MW\n")

print("Created power loss visualizations:")
print("1. power_loss_analysis.png - Visual representation of losses")
print("2. power_loss_summary.txt - Detailed loss analysis") 