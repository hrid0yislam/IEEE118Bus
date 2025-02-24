import matplotlib.pyplot as plt
import numpy as np

# Create loading levels from 0 to 100%
loading_levels = np.linspace(0, 1, 100)

# Calculate losses (proportional to square of loading)
nominal_loss = 1000  # kW at 100% loading
losses = nominal_loss * loading_levels**2

# Create figure
plt.figure(figsize=(12, 8))

# Plot 1: Loading vs Losses
plt.subplot(2, 1, 1)
plt.plot(loading_levels * 100, losses, 'b-', linewidth=2)
plt.title('Relationship Between System Loading and Losses', pad=20)
plt.xlabel('Loading Level (%)')
plt.ylabel('Losses (kW)')
plt.grid(True, alpha=0.3)

# Add reference points
plt.plot([50], [nominal_loss * 0.5**2], 'ro', label='50% Loading → 25% Losses')
plt.plot([100], [nominal_loss], 'go', label='100% Loading → 100% Losses')
plt.legend()

# Plot 2: Daily Pattern
hours = np.arange(24)
# Load multipliers from our time series
load_multipliers = [0.65, 0.60, 0.58, 0.56, 0.55, 0.57, 0.62, 0.72, 0.85, 
                   0.95, 0.98, 1.00, 0.99, 0.97, 0.95, 0.93, 0.94, 0.98, 
                   1.00, 0.97, 0.92, 0.85, 0.75, 0.68]
losses_daily = [nominal_loss * mult**2 for mult in load_multipliers]

plt.subplot(2, 1, 2)
plt.plot(hours, load_multipliers, 'b-', label='Load Level', linewidth=2)
plt.plot(hours, [l/nominal_loss for l in losses_daily], 'r--', 
         label='Loss Ratio', linewidth=2)
plt.title('Daily Load Pattern and Corresponding Losses', pad=20)
plt.xlabel('Hour')
plt.ylabel('Per Unit')
plt.grid(True, alpha=0.3)
plt.legend()

# Add annotations for key points
plt.annotate('Peak Hours', xy=(11, 1), xytext=(11, 1.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')
plt.annotate('Minimum Load', xy=(4, 0.55), xytext=(4, 0.4),
            arrowprops=dict(facecolor='black', shrink=0.05),
            ha='center')

plt.tight_layout()
plt.savefig('loss_relationship.png', dpi=300, bbox_inches='tight')
plt.close()

# Print summary statistics
avg_load = np.mean(load_multipliers)
avg_loss_ratio = np.mean([m**2 for m in load_multipliers])
print("\nDaily Load and Loss Statistics:")
print(f"Average Load Level: {avg_load:.2%}")
print(f"Average Loss Ratio: {avg_loss_ratio:.2%}")
print(f"Peak Loss: {nominal_loss:.0f} kW")
print(f"Minimum Loss: {nominal_loss * min(load_multipliers)**2:.0f} kW")
print(f"Average Loss: {nominal_loss * avg_loss_ratio:.0f} kW") 