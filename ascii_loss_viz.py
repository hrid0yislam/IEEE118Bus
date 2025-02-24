# Critical line loss data (in MW)
line_losses = {
    'Line 89-92': 11.60150,
    'Line 92-94': 8.71097,
    'Line 77-82': 8.70041,
    'Line 85-89': 3.60115,
    'Line 69-77': 2.40980
}

def create_ascii_bar(value, max_value, width=50):
    """Create an ASCII bar with given value"""
    bar_length = int((value / max_value) * width)
    return '[' + '#' * bar_length + ' ' * (width - bar_length) + ']'

# Find maximum loss for scaling
max_loss = max(line_losses.values())

# Print header
print("\nPower Loss Analysis in IEEE 118-Bus System")
print("=========================================\n")

# Print bars
for line, loss in line_losses.items():
    percentage = (loss / sum(line_losses.values())) * 100
    bar = create_ascii_bar(loss, max_loss)
    print(f"{line:10} {loss:6.2f} MW {bar} ({percentage:5.1f}%)")

# Print summary
print("\nSummary:")
print(f"Total Losses: {sum(line_losses.values()):.2f} MW")
print(f"Maximum Loss: {max_loss:.2f} MW (Line 89-92)")
print(f"Minimum Loss: {min(line_losses.values()):.2f} MW (Line 69-77)")

# Print network diagram
print("\nNetwork Diagram (with relative loss thickness):")
print("==============================================\n")
print("    89 === 92 == 94")
print("    ||")
print("    85")
print("    ")
print("    69 == 77 === 82")
print("\nLegend:")
print("= : Low loss")
print("== : Medium loss")
print("=== : High loss") 