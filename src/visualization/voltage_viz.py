import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

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

# Create figure with subplots
plt.style.use('default')  # Use default style instead of seaborn
fig = plt.figure(figsize=(15, 20))

# 1. Load Profile
plt.subplot(3, 1, 1)
plt.plot(hours, load_multipliers, 'b-', linewidth=2, marker='o')
plt.fill_between(hours, load_multipliers, alpha=0.2)
plt.title('24-Hour Load Profile', pad=20, fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Load Multiplier (p.u.)')
plt.grid(True, alpha=0.3)
plt.ylim([0.5, 1.1])

# Annotate key points
plt.annotate('Peak Load', xy=(11, 1.0), xytext=(11, 1.05),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')
plt.annotate('Minimum Load', xy=(4, 0.55), xytext=(4, 0.45),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')

# 2. Critical Bus Voltages
plt.subplot(3, 1, 2)
for bus, voltages in critical_buses.items():
    plt.plot(hours, voltages, '-', linewidth=2, label=bus, marker='o')
plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
plt.axhline(y=1.05, color='r', linestyle='--', label='Upper Limit')
plt.title('Critical Bus Voltage Profiles', pad=20, fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Voltage (p.u.)')
plt.grid(True, alpha=0.3)
plt.legend()

# 3. Voltage Violations
plt.subplot(3, 1, 3)
violations = {bus: [1 if v < 0.95 or v > 1.05 else 0 for v in voltages] 
             for bus, voltages in critical_buses.items()}
bottom = np.zeros(24)

for bus, violation in violations.items():
    plt.bar(hours, violation, bottom=bottom, label=bus, alpha=0.7)
    bottom += np.array(violation)

plt.title('Voltage Violations Over Time', pad=20, fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Number of Violations')
plt.grid(True, alpha=0.3)
plt.legend()

# Adjust layout and save
plt.tight_layout()
plt.savefig('voltage_profile_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Voltage profile visualization has been saved as 'voltage_profile_analysis.png'") 