import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Critical line loss data (in MW)
line_losses = {
    'Line 89-92': 11.60150,
    'Line 92-94': 8.71097,
    'Line 77-82': 8.70041,
    'Line 85-89': 3.60115,
    'Line 69-77': 2.40980
}

# Create figure
plt.figure(figsize=(10, 6))

# Create bar plot
lines = list(line_losses.keys())
losses = list(line_losses.values())
bars = plt.bar(lines, losses, alpha=0.7)

# Customize plot
plt.title('Power Losses in Critical Lines', fontsize=14, pad=20)
plt.xlabel('Transmission Lines')
plt.ylabel('Power Loss (MW)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

# Adjust layout and save
plt.tight_layout()
plt.savefig('simple_loss_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save summary to text file
with open('simple_loss_summary.txt', 'w') as f:
    f.write("Power Loss Analysis Summary\n")
    f.write("=========================\n\n")
    
    total_loss = sum(line_losses.values())
    f.write(f"Total System Losses: {total_loss:.2f} MW\n\n")
    
    f.write("Losses by Line:\n")
    for line, loss in line_losses.items():
        percentage = (loss / total_loss) * 100
        f.write(f"{line}: {loss:.2f} MW ({percentage:.1f}%)\n")

print("Simple loss analysis has been saved as 'simple_loss_analysis.png'")
print("Loss summary has been saved as 'simple_loss_summary.txt'") 