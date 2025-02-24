import numpy as np

# Data
voltages = [0.678, 0.550, 0.227, 0.526, 0.161]
losses = [11601.50, 8710.97, 8700.41, 3601.15, 2409.80]
lines = ['Line 89-92', 'Line 92-94', 'Line 77-82', 'Line 85-89', 'Line 69-77']

# Create ASCII art visualization
def create_ascii_plot(x, y, labels, width=60, height=20):
    # Normalize data to plot size
    x_norm = np.array([(x_i - min(x)) / (max(x) - min(x)) * (width-1) for x_i in x])
    y_norm = np.array([(y_i - min(y)) / (max(y) - min(y)) * (height-1) for y_i in y])
    
    # Create empty plot
    plot = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Add points
    for i in range(len(x)):
        x_pos = int(x_norm[i])
        y_pos = int(y_norm[i])
        plot[height-1-y_pos][x_pos] = '*'
        
        # Add label
        if x_pos < width-10:
            label_pos = min(x_pos + 1, width-len(labels[i]))
            for j, char in enumerate(labels[i]):
                if label_pos + j < width:
                    plot[height-1-y_pos][label_pos + j] = char
    
    # Add axes
    for i in range(width):
        plot[height-1][i] = '-'
    for i in range(height):
        plot[i][0] = '|'
    
    # Print plot
    print("\nVoltage Level vs Power Losses in IEEE 118-Bus System")
    print("=" * width)
    for row in plot:
        print(''.join(row))
    print("=" * width)
    print("X-axis: Voltage (pu) from {:.3f} to {:.3f}".format(min(voltages), max(voltages)))
    print("Y-axis: Losses (kW) from {:.1f} to {:.1f}".format(min(losses), max(losses)))

# Create visualization
create_ascii_plot(voltages, losses, lines)

# Print tabular data
print("\nDetailed Data:")
print("-" * 50)
print("Line         Voltage (pu)    Losses (kW)")
print("-" * 50)
for i in range(len(lines)):
    print(f"{lines[i]:<12} {voltages[i]:>11.3f} {losses[i]:>13.2f}")
print("-" * 50)

# Calculate correlation
correlation = np.corrcoef(voltages, losses)[0,1]
print(f"\nCorrelation coefficient between voltage and losses: {correlation:.3f}")

# Save output to file
with open('voltage_loss_analysis.txt', 'w') as f:
    f.write("Voltage Loss Analysis for IEEE 118-Bus System\n")
    f.write("===========================================\n\n")
    f.write("Key Findings:\n")
    f.write(f"1. Highest losses: {max(losses):.2f} kW in {lines[losses.index(max(losses))]}\n")
    f.write(f"2. Lowest losses: {min(losses):.2f} kW in {lines[losses.index(min(losses))]}\n")
    f.write(f"3. Correlation between voltage and losses: {correlation:.3f}\n")
    f.write("\nDetailed Data:\n")
    f.write("-" * 50 + "\n")
    f.write("Line         Voltage (pu)    Losses (kW)\n")
    f.write("-" * 50 + "\n")
    for i in range(len(lines)):
        f.write(f"{lines[i]:<12} {voltages[i]:>11.3f} {losses[i]:>13.2f}\n")
    f.write("-" * 50 + "\n")

print("\nAnalysis has been saved to 'voltage_loss_analysis.txt'") 