import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
os.makedirs('thesis_figures', exist_ok=True)

# Key voltage and loss data from OpenDSS results
data = {
    'Bus_Lines': [
        'Line 89-92',
        'Line 92-94',
        'Line 77-82',
        'Line 85-89',
        'Line 69-77'
    ],
    'Voltages': [
        0.678,  # Bus 89 voltage
        0.550,  # Bus 92 voltage
        0.227,  # Bus 77 voltage
        0.526,  # Bus 85 voltage
        0.161   # Bus 69 voltage
    ],
    'Losses': [
        11601.50,
        8710.97,
        8700.41,
        3601.15,
        2409.80
    ]
}

# Create figure with multiple subplots
plt.figure(figsize=(15, 10))

# 1. Voltage vs Losses Plot
plt.subplot(2, 1, 1)
plt.scatter(data['Voltages'], data['Losses'], color='blue', s=100, alpha=0.6)

# Add trend line
z = np.polyfit(data['Voltages'], data['Losses'], 1)
p = np.poly1d(z)
x_trend = np.linspace(min(data['Voltages']), max(data['Voltages']), 100)
plt.plot(x_trend, p(x_trend), "r--", alpha=0.8)

# Add labels for each point
for i, txt in enumerate(data['Bus_Lines']):
    plt.annotate(txt, (data['Voltages'][i], data['Losses'][i]), 
                xytext=(10, 10), textcoords='offset points')

plt.title('Voltage Level vs Power Losses', fontsize=14, pad=20)
plt.xlabel('Bus Voltage (pu)', fontsize=12)
plt.ylabel('Power Losses (kW)', fontsize=12)
plt.grid(True, alpha=0.3)

# 2. Loss Distribution
plt.subplot(2, 1, 2)
bars = plt.bar(data['Bus_Lines'], data['Losses'], color='skyblue')
plt.title('Power Losses by Transmission Line', fontsize=14, pad=20)
plt.xlabel('Transmission Lines', fontsize=12)
plt.ylabel('Power Losses (kW)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('thesis_figures/voltage_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Voltage loss visualization has been created as 'voltage_loss_analysis.png'") 