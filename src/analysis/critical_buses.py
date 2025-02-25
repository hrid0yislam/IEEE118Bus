import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Critical bus data
data = {
    'Bus': ['89_CLINCHRV', '92_SALTVLLE', '77_TURNER', '85_BEAVERCK', '69_SPORN'],
    'Voltage': [0.678, 0.550, 0.227, 0.526, 0.161],
    'Loss_In': [11601.50, 8710.97, 8700.41, 3601.15, 2409.80],
    'Loss_Out': [8710.97, 8700.41, 3601.15, 2409.80, 0.0]
}

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 1. Voltage Profile
ax1.plot(range(len(data['Bus'])), data['Voltage'], 'bo-', linewidth=2)
ax1.set_xticks(range(len(data['Bus'])))
ax1.set_xticklabels(data['Bus'], rotation=45)
ax1.set_ylabel('Voltage (pu)')
ax1.set_title('Voltage Profile of Critical Buses')
ax1.grid(True, alpha=0.3)

# Add voltage values on points
for i, v in enumerate(data['Voltage']):
    ax1.text(i, v, f'{v:.3f}', ha='center', va='bottom')

# 2. Loss Flow
width = 0.35
x = np.arange(len(data['Bus']))
rects1 = ax2.bar(x - width/2, data['Loss_In'], width, label='Loss In', color='red', alpha=0.6)
rects2 = ax2.bar(x + width/2, data['Loss_Out'], width, label='Loss Out', color='blue', alpha=0.6)

ax2.set_ylabel('Power Loss (kW)')
ax2.set_title('Power Loss Flow Through Critical Buses')
ax2.set_xticks(x)
ax2.set_xticklabels(data['Bus'], rotation=45)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Add value labels on bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0:  # Only label non-zero values
            ax2.text(rect.get_x() + rect.get_width()/2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

# Adjust layout and save
plt.tight_layout()
plt.savefig('critical_buses_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save analysis to text file
with open('critical_buses_analysis.txt', 'w') as f:
    f.write("Critical Buses Analysis in IEEE 118-Bus System\n")
    f.write("===========================================\n\n")
    
    f.write("1. Voltage Profile:\n")
    f.write("-" * 50 + "\n")
    f.write(f"{'Bus':<15} {'Voltage (pu)':<15}\n")
    f.write("-" * 50 + "\n")
    for i in range(len(data['Bus'])):
        f.write(f"{data['Bus'][i]:<15} {data['Voltage'][i]:<15.3f}\n")
    
    f.write("\n2. Power Loss Flow:\n")
    f.write("-" * 50 + "\n")
    f.write(f"{'Bus':<15} {'Loss In (kW)':<15} {'Loss Out (kW)':<15}\n")
    f.write("-" * 50 + "\n")
    for i in range(len(data['Bus'])):
        f.write(f"{data['Bus'][i]:<15} {data['Loss_In'][i]:<15.2f} {data['Loss_Out'][i]:<15.2f}\n")
    
    f.write("\n3. Key Findings:\n")
    f.write(f"- Highest voltage: {max(data['Voltage']):.3f} pu at {data['Bus'][data['Voltage'].index(max(data['Voltage']))]}\n")
    f.write(f"- Lowest voltage: {min(data['Voltage']):.3f} pu at {data['Bus'][data['Voltage'].index(min(data['Voltage']))]}\n")
    f.write(f"- Maximum loss: {max(data['Loss_In']):.2f} kW at {data['Bus'][data['Loss_In'].index(max(data['Loss_In']))]}\n")
    f.write(f"- Total loss in critical section: {sum(data['Loss_In']) - sum(data['Loss_Out']):.2f} kW\n")

print("Created critical buses analysis files: critical_buses_analysis.png and critical_buses_analysis.txt") 