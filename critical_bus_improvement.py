import matplotlib.pyplot as plt
import numpy as np

# Data for critical buses
critical_buses = {
    '69_SPORN': {
        'initial': 0.161,
        'with_inverter': 0.361,  # 0.161 + 0.20 (expected improvement)
        'target': 0.95,
        'inverter_capacity': '3×50 MVAR'
    },
    '77_TURNER': {
        'initial': 0.227,
        'with_inverter': 0.377,  # 0.227 + 0.15 (expected improvement)
        'target': 0.95,
        'inverter_capacity': '2×50 MVAR'
    }
}

# Create figure
plt.figure(figsize=(12, 6))

# Bar positions
bars = np.arange(len(critical_buses))
width = 0.25

# Create grouped bars
plt.bar(bars - width, [v['initial'] for v in critical_buses.values()], 
        width, label='Initial', color='red', alpha=0.7)
plt.bar(bars, [v['with_inverter'] for v in critical_buses.values()],
        width, label='With Smart Inverters', color='blue', alpha=0.7)
plt.bar(bars + width, [v['target'] for v in critical_buses.values()],
        width, label='Target', color='green', alpha=0.7)

# Add reference line for minimum acceptable voltage
plt.axhline(y=0.95, color='g', linestyle='--', alpha=0.5, label='Minimum Acceptable (0.95 pu)')

# Customize plot
plt.title('Voltage Improvement with Smart Inverter Implementation\nfor Critical Buses', fontsize=14, pad=20)
plt.xlabel('Bus (with Inverter Capacity)', fontsize=12)
plt.ylabel('Voltage (pu)', fontsize=12)
plt.xticks(bars, [f"{bus}\n({data['inverter_capacity']})" for bus, data in critical_buses.items()])
plt.grid(True, alpha=0.3)
plt.legend()

# Add value labels
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')

# Add improvement arrows and labels
for i, (bus, data) in enumerate(critical_buses.items()):
    improvement = data['with_inverter'] - data['initial']
    mid_point = (data['initial'] + data['with_inverter']) / 2
    plt.annotate(f'+{improvement:.2f} pu',
                xy=(i, mid_point),
                xytext=(i-0.4, mid_point),
                arrowprops=dict(arrowstyle='->'),
                ha='right',
                va='center')

plt.tight_layout()
plt.savefig('thesis_figures/critical_bus_improvement.png', dpi=300, bbox_inches='tight')
plt.close()

# Save analysis to text file
with open('thesis_figures/critical_bus_analysis.txt', 'w') as f:
    f.write("Critical Bus Voltage Improvement Analysis\n")
    f.write("======================================\n\n")
    
    for bus, data in critical_buses.items():
        f.write(f"\n{bus} Analysis:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Initial voltage: {data['initial']:.3f} pu\n")
        f.write(f"Smart inverter capacity: {data['inverter_capacity']}\n")
        f.write(f"Expected improvement: {data['with_inverter'] - data['initial']:.3f} pu\n")
        f.write(f"Voltage with inverter: {data['with_inverter']:.3f} pu\n")
        f.write(f"Gap to target: {data['target'] - data['with_inverter']:.3f} pu\n")
        f.write(f"Additional improvement needed: {max(0, data['target'] - data['with_inverter']):.3f} pu\n")

print("Created visualization and analysis for critical buses in thesis_figures directory") 