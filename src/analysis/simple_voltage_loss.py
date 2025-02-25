import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Create the data
voltages = [0.678, 0.550, 0.227, 0.526, 0.161]
losses = [11601.50, 8710.97, 8700.41, 3601.15, 2409.80]
lines = ['Line 89-92', 'Line 92-94', 'Line 77-82', 'Line 85-89', 'Line 69-77']

# Create the figure
plt.figure(figsize=(10, 6))

# Create scatter plot
plt.scatter(voltages, losses, c='blue', s=100)

# Add labels for each point
for i, txt in enumerate(lines):
    plt.annotate(txt, (voltages[i], losses[i]), 
                xytext=(5, 5), textcoords='offset points')

# Add trend line
z = np.polyfit(voltages, losses, 1)
p = np.poly1d(z)
x_trend = np.linspace(min(voltages), max(voltages), 100)
plt.plot(x_trend, p(x_trend), "r--", alpha=0.8)

# Add labels and title
plt.title('Voltage Level vs Power Losses in IEEE 118-Bus System')
plt.xlabel('Bus Voltage (pu)')
plt.ylabel('Power Losses (kW)')
plt.grid(True, alpha=0.3)

# Save the plot
plt.savefig('voltage_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Created voltage_loss_analysis.png") 