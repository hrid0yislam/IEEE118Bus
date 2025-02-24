import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Time series data
hours = list(range(24))
load_multipliers = [0.65, 0.60, 0.58, 0.56, 0.55, 0.57, 0.62, 0.72, 0.85, 
                   0.95, 0.98, 1.00, 0.99, 0.97, 0.95, 0.93, 0.94, 0.98, 
                   1.00, 0.97, 0.92, 0.85, 0.75, 0.68]

# Critical bus base voltages
critical_buses = {
    'Bus 89_CLINCHRV': 0.678,
    'Bus 69_SPORN': 0.161,
    'Bus 77_TURNER': 0.227,
    'Bus 92_SALTVLLE': 0.550
}

# Create plots
plt.figure(figsize=(10, 12))

# 1. Load Profile
plt.subplot(3, 1, 1)
plt.plot(hours, load_multipliers, 'b-', marker='o')
plt.title('24-Hour Load Profile')
plt.xlabel('Hour of Day')
plt.ylabel('Load Multiplier (p.u.)')
plt.grid(True)

# 2. Voltage Profiles
plt.subplot(3, 1, 2)
for bus, base_voltage in critical_buses.items():
    voltages = [base_voltage * m for m in load_multipliers]
    plt.plot(hours, voltages, marker='o', label=bus)
plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit')
plt.axhline(y=1.05, color='r', linestyle='--', label='Upper Limit')
plt.title('Critical Bus Voltage Profiles')
plt.xlabel('Hour of Day')
plt.ylabel('Voltage (p.u.)')
plt.legend()
plt.grid(True)

# 3. System Losses
plt.subplot(3, 1, 3)
base_loss = 76353.20  # kW
losses = [base_loss * (m**2) / 1000 for m in load_multipliers]  # Convert to MW
plt.plot(hours, losses, 'g-', marker='o')
plt.title('System Losses Over Time')
plt.xlabel('Hour of Day')
plt.ylabel('Losses (MW)')
plt.grid(True)

plt.tight_layout()
plt.savefig('time_series_results.png', dpi=300, bbox_inches='tight')
plt.close()

print("Time series visualization has been saved as 'time_series_results.png'") 