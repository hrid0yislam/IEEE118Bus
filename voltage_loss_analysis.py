import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Create output directory
os.makedirs('thesis_figures', exist_ok=True)

# Sample voltage and loss data for key buses
voltage_loss_data = {
    'Bus': [
        '89-92', '92-94', '77-82', '85-89', '69-77',
        '82-83', '80-96', '80-97', '80-98', '80-99'
    ],
    'Voltage (pu)': [
        0.678, 0.550, 0.227, 0.526, 0.161,
        0.227, 0.227, 0.227, 0.227, 0.227
    ],
    'Losses (kW)': [
        11601.50, 8710.97, 8700.41, 3601.15, 2409.80,
        4309.37, 1978.40, 952.35, 681.19, 1433.04
    ]
}

# 1. Voltage vs Losses Scatter Plot
plt.figure(figsize=(12, 6))
plt.scatter(voltage_loss_data['Voltage (pu)'], voltage_loss_data['Losses (kW)'],
           alpha=0.6, s=100)
plt.plot(np.unique(voltage_loss_data['Voltage (pu)']),
         np.poly1d(np.polyfit(voltage_loss_data['Voltage (pu)'],
                             voltage_loss_data['Losses (kW)'], 1))(np.unique(voltage_loss_data['Voltage (pu)'])),
         color='red', linestyle='--', alpha=0.8)

# Add labels for each point
for i, bus in enumerate(voltage_loss_data['Bus']):
    plt.annotate(bus, (voltage_loss_data['Voltage (pu)'][i],
                      voltage_loss_data['Losses (kW)'][i]),
                xytext=(5, 5), textcoords='offset points')

plt.title('Relationship between Bus Voltage and Line Losses')
plt.xlabel('Voltage (pu)')
plt.ylabel('Losses (kW)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('thesis_figures/voltage_loss_relationship.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Loss Distribution by Voltage Level
voltage_categories = ['Low (<0.90 pu)', 'Medium (0.90-0.95 pu)', 'High (>0.95 pu)']
loss_by_voltage = [35000, 15000, 59918.4]  # Approximate distribution

plt.figure(figsize=(10, 6))
plt.bar(voltage_categories, loss_by_voltage, color=['red', 'yellow', 'green'])
plt.title('Loss Distribution by Voltage Level')
plt.xlabel('Voltage Category')
plt.ylabel('Total Losses (kW)')
plt.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(loss_by_voltage):
    plt.text(i, v, f'{v:,.1f} kW', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('thesis_figures/loss_by_voltage.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Voltage Profile vs Loss Density
voltage_profile = np.linspace(0.084, 0.678, 100)
loss_density = 1000 * (1/voltage_profile)**2  # Theoretical relationship

plt.figure(figsize=(12, 6))
plt.plot(voltage_profile, loss_density, 'b-', label='Theoretical Loss Density')
plt.fill_between(voltage_profile, loss_density, alpha=0.2)
plt.title('Theoretical Loss Density vs Voltage Profile')
plt.xlabel('Voltage (pu)')
plt.ylabel('Relative Loss Density')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('thesis_figures/loss_density.png', dpi=300, bbox_inches='tight')
plt.close()

print("Voltage-Loss analysis visualizations have been created in the thesis_figures directory.") 