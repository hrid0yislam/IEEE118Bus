import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Time series data
hours = np.arange(24)
load_multipliers = [0.65, 0.60, 0.58, 0.56, 0.55, 0.57, 0.62, 0.72, 0.85, 
                   0.95, 0.98, 1.00, 0.99, 0.97, 0.95, 0.93, 0.94, 0.98, 
                   1.00, 0.97, 0.92, 0.85, 0.75, 0.68]

# Critical bus voltages over time
critical_buses = {
    'Bus 89_CLINCHRV': [0.678 * m for m in load_multipliers],
    'Bus 69_SPORN': [0.161 * m for m in load_multipliers],
    'Bus 77_TURNER': [0.227 * m for m in load_multipliers],
    'Bus 92_SALTVLLE': [0.550 * m for m in load_multipliers]
}

# System losses (approximated using quadratic relationship)
losses = {
    'Line Losses': [76353.20 * (m**2) for m in load_multipliers],
    'Transformer Losses': [30.54 * (m**2) for m in load_multipliers]
}

# Create figure with subplots
plt.style.use('default')
fig = plt.figure(figsize=(15, 20))

# 1. Load Profile
ax1 = plt.subplot(4, 1, 1)
ax1.plot(hours, load_multipliers, 'b-', linewidth=2, marker='o')
ax1.fill_between(hours, load_multipliers, alpha=0.2)
ax1.set_title('24-Hour Load Profile', pad=20, fontsize=14)
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Load Multiplier (p.u.)')
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0.5, 1.1])

# Annotate key points
ax1.annotate('Peak Load', xy=(11, 1.0), xytext=(11, 1.05),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')
ax1.annotate('Minimum Load', xy=(4, 0.55), xytext=(4, 0.45),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')

# 2. Critical Bus Voltages
ax2 = plt.subplot(4, 1, 2)
for bus, voltages in critical_buses.items():
    ax2.plot(hours, voltages, '-', linewidth=2, label=bus, marker='o')
ax2.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
ax2.axhline(y=1.05, color='r', linestyle='--', label='Upper Limit')
ax2.set_title('Critical Bus Voltage Profiles', pad=20, fontsize=14)
ax2.set_xlabel('Hour of Day')
ax2.set_ylabel('Voltage (p.u.)')
ax2.grid(True, alpha=0.3)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 3. System Losses
ax3 = plt.subplot(4, 1, 3)
ax3.plot(hours, [l/1000 for l in losses['Line Losses']], 'b-', 
         linewidth=2, label='Line Losses (MW)', marker='o')
ax3.plot(hours, [l/1000 for l in losses['Transformer Losses']], 'r--', 
         linewidth=2, label='Transformer Losses (MW)', marker='o')
ax3.set_title('System Losses Over Time', pad=20, fontsize=14)
ax3.set_xlabel('Hour of Day')
ax3.set_ylabel('Losses (MW)')
ax3.grid(True, alpha=0.3)
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 4. Loss vs Loading Relationship
ax4 = plt.subplot(4, 1, 4)
total_losses = [(l1 + l2)/1000 for l1, l2 in zip(losses['Line Losses'], 
                                                 losses['Transformer Losses'])]
ax4.scatter(load_multipliers, total_losses, alpha=0.6, s=100)
ax4.set_title('Total Losses vs System Loading', pad=20, fontsize=14)
ax4.set_xlabel('Load Multiplier (p.u.)')
ax4.set_ylabel('Total Losses (MW)')
ax4.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(load_multipliers, total_losses, 2)
p = np.poly1d(z)
x_trend = np.linspace(min(load_multipliers), max(load_multipliers), 100)
ax4.plot(x_trend, p(x_trend), "r--", alpha=0.8, label='Quadratic Trend')
ax4.legend()

# Adjust layout
plt.tight_layout()
plt.savefig('time_series_visualization.png', dpi=300, bbox_inches='tight')
plt.close()

# Create additional visualization for regional voltage patterns
plt.figure(figsize=(12, 8))

# Regional voltage patterns
regions = {
    'Northern': [0.161, 0.227, 0.350],  # Average of northern buses
    'Central': [0.450, 0.500, 0.550],   # Average of central buses
    'Southern': [0.550, 0.600, 0.678]   # Average of southern buses
}

# Box plot for regional voltage distribution
data = [voltages for voltages in regions.values()]
plt.boxplot(data, labels=regions.keys())
plt.title('Regional Voltage Distribution', pad=20, fontsize=14)
plt.ylabel('Voltage (p.u.)')
plt.grid(True, alpha=0.3)

# Add reference lines
plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
plt.axhline(y=1.05, color='r', linestyle='--', label='Upper Limit')
plt.legend()

plt.savefig('regional_voltage_patterns.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations have been created:")
print("1. time_series_visualization.png - Shows load profile, voltages, and losses over time")
print("2. regional_voltage_patterns.png - Shows voltage distribution by region") 