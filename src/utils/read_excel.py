import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the absolute path to the repository root
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Read the Excel file using the correct path
excel_path = os.path.join(repo_root, 'data', 'profiles', 'Comparissons.xlsx')
df = pd.read_excel(excel_path)

# Create results directory if it doesn't exist
results_dir = os.path.join(repo_root, 'results', 'figures')
os.makedirs(results_dir, exist_ok=True)

# Create figure with multiple subplots
plt.figure(figsize=(15, 10))

# Plot 1: Active Power Comparison (PG vs PGdss)
plt.subplot(2, 1, 1)
plt.plot(df['I'], df['PG'], 'b-', label='PG (Original)')
plt.plot(df['I'], df['PGdss'], 'r--', label='PGdss (DSS)')
plt.title('Active Power Comparison')
plt.xlabel('Generator Bus Number')
plt.ylabel('Active Power (MW)')
plt.grid(True)
plt.legend()

# Plot 2: Reactive Power Comparison (QG vs QGdss)
plt.subplot(2, 1, 2)
plt.plot(df['I'], df['QG'], 'g-', label='QG (Original)')
plt.plot(df['I'], df['QGdss'], 'm--', label='QGdss (DSS)')
plt.title('Reactive Power Comparison')
plt.xlabel('Generator Bus Number')
plt.ylabel('Reactive Power (MVAR)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'power_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

# Create error analysis plots
plt.figure(figsize=(15, 5))

# Plot absolute errors
plt.subplot(1, 2, 1)
plt.bar(df['I'], abs(df['P_Err']), label='Active Power Error', alpha=0.5)
plt.bar(df['I'], abs(df['Q_Err']), label='Reactive Power Error', alpha=0.5)
plt.title('Absolute Power Errors')
plt.xlabel('Generator Bus Number')
plt.ylabel('Absolute Error (MW/MVAR)')
plt.legend()
plt.grid(True)

# Plot error distribution
plt.subplot(1, 2, 2)
sns.histplot(data=df[['P_Err', 'Q_Err']], bins=20)
plt.title('Error Distribution')
plt.xlabel('Error Value (MW/MVAR)')
plt.ylabel('Count')

plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'error_analysis.png'), dpi=300, bbox_inches='tight')
plt.close()

# Get statistics
pg_stats = df['PG'].describe()
qg_stats = df['QG'].describe()
p_err_mean = df['P_Err'].mean()
q_err_mean = df['Q_Err'].mean()
p_err_max = df['P_Err'].abs().max()
q_err_max = df['Q_Err'].abs().max()

# Find outliers (generators with large errors)
outliers = df[abs(df['Q_Err']) > 1.0][['I', 'Element', 'QG', 'QGdss', 'Q_Err']]

# Save statistics to a file for LaTeX
stats_dir = os.path.join(repo_root, 'results', 'data')
os.makedirs(stats_dir, exist_ok=True)
with open(os.path.join(stats_dir, 'statistics.txt'), 'w') as f:
    f.write("Active Power (PG) Statistics:\n")
    f.write(str(pg_stats))
    f.write("\n\nReactive Power (QG) Statistics:\n")
    f.write(str(qg_stats))
    f.write("\n\nError Statistics:\n")
    f.write(f"Average Active Power Error: {p_err_mean:.6f} MW\n")
    f.write(f"Average Reactive Power Error: {q_err_mean:.6f} MVAR\n")
    f.write(f"Maximum Active Power Error: {p_err_max:.6f} MW\n")
    f.write(f"Maximum Reactive Power Error: {q_err_max:.6f} MVAR\n")
    f.write("\nOutliers (|Q_Err| > 1.0 MVAR):\n")
    f.write(outliers.to_string()) 