import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Data with actual circuit losses from OpenDSS
total_losses = {
    'Active': 75072.73,  # kW
    'Reactive': 275444.49  # kVAR
}

# Line loss data
line_data = {
    'Lines': [
        'Line 89-92',
        'Line 92-94',
        'Line 77-82',
        'Line 85-89',
        'Line 69-77'
    ],
    'Voltages': [
        0.678,
        0.550,
        0.227,
        0.526,
        0.161
    ],
    'Active_Losses': [
        11601.50,
        8710.97,
        8700.41,
        3601.15,
        2409.80
    ]
}

# Create figure with multiple subplots
plt.figure(figsize=(15, 12))

# 1. Voltage vs Active Power Losses
plt.subplot(2, 2, 1)
plt.scatter(line_data['Voltages'], line_data['Active_Losses'], 
           color='blue', s=100, alpha=0.6)

# Add trend line
z = np.polyfit(line_data['Voltages'], line_data['Active_Losses'], 1)
p = np.poly1d(z)
x_trend = np.linspace(min(line_data['Voltages']), max(line_data['Voltages']), 100)
plt.plot(x_trend, p(x_trend), "r--", alpha=0.8, label='Trend')

# Add labels for each point
for i, txt in enumerate(line_data['Lines']):
    plt.annotate(txt, (line_data['Voltages'][i], line_data['Active_Losses'][i]),
                xytext=(5, 5), textcoords='offset points')

plt.title('Voltage Level vs Active Power Losses', fontsize=12)
plt.xlabel('Bus Voltage (pu)')
plt.ylabel('Active Power Losses (kW)')
plt.grid(True, alpha=0.3)
plt.legend()

# 2. Line Loss Distribution
plt.subplot(2, 2, 2)
bars = plt.bar(line_data['Lines'], line_data['Active_Losses'], 
               color='skyblue', alpha=0.7)

plt.title('Active Power Losses by Line', fontsize=12)
plt.xlabel('Transmission Lines')
plt.ylabel('Active Power Losses (kW)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

# 3. Total System Losses Pie Chart
plt.subplot(2, 2, 3)
loss_labels = ['Active Losses\n(kW)', 'Reactive Losses\n(kVAR)']
loss_values = [total_losses['Active'], total_losses['Reactive']]
plt.pie(loss_values, labels=loss_labels, autopct='%1.1f%%',
        colors=['lightcoral', 'lightblue'])
plt.title('Distribution of Total System Losses', fontsize=12)

# 4. Loss vs Voltage Relationship
plt.subplot(2, 2, 4)
sorted_idx = np.argsort(line_data['Voltages'])
sorted_v = np.array(line_data['Voltages'])[sorted_idx]
sorted_l = np.array(line_data['Active_Losses'])[sorted_idx]

plt.plot(sorted_v, sorted_l, 'b-o', label='Actual')
plt.fill_between(sorted_v, sorted_l, alpha=0.2)
plt.title('Loss-Voltage Relationship', fontsize=12)
plt.xlabel('Voltage (pu)')
plt.ylabel('Losses (kW)')
plt.grid(True, alpha=0.3)
plt.legend()

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('voltage_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save analysis to text file
with open('voltage_loss_analysis.txt', 'w') as f:
    f.write("Voltage Loss Analysis for IEEE 118-Bus System\n")
    f.write("===========================================\n\n")
    
    f.write("1. Total System Losses:\n")
    f.write(f"   Active Power: {total_losses['Active']:,.2f} kW\n")
    f.write(f"   Reactive Power: {total_losses['Reactive']:,.2f} kVAR\n\n")
    
    f.write("2. Line-wise Loss Analysis:\n")
    f.write("-" * 50 + "\n")
    f.write(f"{'Line':<15} {'Voltage (pu)':<15} {'Losses (kW)':<15}\n")
    f.write("-" * 50 + "\n")
    for i in range(len(line_data['Lines'])):
        f.write(f"{line_data['Lines'][i]:<15} {line_data['Voltages'][i]:<15.3f} {line_data['Active_Losses'][i]:<15.2f}\n")
    f.write("-" * 50 + "\n\n")
    
    # Calculate correlation
    correlation = np.corrcoef(line_data['Voltages'], line_data['Active_Losses'])[0,1]
    f.write(f"3. Voltage-Loss Correlation: {correlation:.3f}\n\n")
    
    f.write("4. Key Findings:\n")
    f.write(f"   - Highest losses: {max(line_data['Active_Losses']):,.2f} kW in {line_data['Lines'][line_data['Active_Losses'].index(max(line_data['Active_Losses']))]}\n")
    f.write(f"   - Lowest losses: {min(line_data['Active_Losses']):,.2f} kW in {line_data['Lines'][line_data['Active_Losses'].index(min(line_data['Active_Losses']))]}\n")
    f.write(f"   - Average losses per analyzed line: {np.mean(line_data['Active_Losses']):,.2f} kW\n")

print("Created voltage_loss_analysis.png and voltage_loss_analysis.txt with comprehensive analysis") 