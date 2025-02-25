import matplotlib.pyplot as plt
import numpy as np

# Data for voltage improvements
buses = ['69_SPORN', '77_TURNER', '92_SALTVLLE', '85_BEAVERCK', '89_CLINCHRV']
weeks = ['Initial', 'Week 2', 'Week 4', 'Month 2']
voltages = np.array([
    [0.161, 0.35, 0.65, 0.95],  # 69_SPORN
    [0.227, 0.40, 0.70, 0.95],  # 77_TURNER
    [0.550, 0.65, 0.85, 0.98],  # 92_SALTVLLE
    [0.526, 0.60, 0.80, 0.97],  # 85_BEAVERCK
    [0.678, 0.75, 0.90, 1.00]   # 89_CLINCHRV
])

# Create figure and axis
plt.figure(figsize=(12, 8))

# Plot voltage trajectories
for i, bus in enumerate(buses):
    plt.plot(weeks, voltages[i], marker='o', linewidth=2, markersize=8, label=bus)

# Add reference lines
plt.axhline(y=0.95, color='g', linestyle='--', alpha=0.5, label='Target (0.95 pu)')
plt.axhline(y=1.05, color='r', linestyle='--', alpha=0.5, label='Upper Limit (1.05 pu)')

# Customize plot
plt.title('Voltage Improvement Trajectory with Smart Inverter Implementation', fontsize=14, pad=20)
plt.xlabel('Implementation Timeline', fontsize=12)
plt.ylabel('Voltage (pu)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout and save
plt.tight_layout()
plt.savefig('thesis_figures/voltage_improvement_trajectory.png', dpi=300, bbox_inches='tight')
plt.close()

print("Voltage improvement trajectory visualization has been saved to thesis_figures/voltage_improvement_trajectory.png") 