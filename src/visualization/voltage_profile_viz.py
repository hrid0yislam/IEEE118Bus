import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import opendssdirect as dss
import os

def initialize_opendss():
    """Initialize OpenDSS and load the circuit"""
    # Clear any existing circuit
    dss.run_command('Clear')
    
    # Set the frequency
    dss.run_command('Set DefaultBaseFrequency=50')
    
    # Create new circuit
    dss.run_command('New Circuit.ieee118bus basekv=138.0 phases=3 bus1=89_clinchrv')
    
    # Redirect all component files
    dss.run_command('Redirect generators.dss')
    dss.run_command('Redirect lines.dss')
    dss.run_command('Redirect transformers.dss')
    dss.run_command('Redirect loads.dss')
    dss.run_command('Redirect shunts.dss')
    dss.run_command('Redirect sw_shunts.dss')
    dss.run_command('Redirect dc_and_facts_equiv_elements.dss')
    
    # Set voltage bases
    dss.run_command('Set VoltageBases=[138.0]')
    dss.run_command('Calcv')
    dss.run_command('Redirect confirm_kv_bases.dss')
    
    # Solution parameters
    dss.run_command('set algorithm=NCIM')
    dss.run_command('set maxcontroliter=100')
    dss.run_command('set maxiterations=100')
    dss.run_command('set tolerance=0.0001')
    dss.run_command('set loadmodel=1')
    
    # Solve
    dss.run_command('solve mode=snap')

def get_voltage_data():
    """Get voltage data for all buses"""
    voltages = []
    bus_names = []
    
    # Get all bus names
    dss.Circuit.SetActiveBus('')
    for bus in dss.Circuit.AllBusNames():
        dss.Circuit.SetActiveBus(bus)
        # Get voltage in kV
        v_mag = dss.Bus.puVmagAngle()[0]  # Get per unit voltage magnitude
        voltages.append(v_mag)
        bus_names.append(bus)
    
    return pd.DataFrame({
        'Bus': bus_names,
        'Voltage (pu)': voltages
    })

def plot_voltage_profile(df):
    """Create voltage profile visualizations"""
    # Set style
    plt.style.use('default')
    
    # Set the figure size and DPI for better quality
    plt.rcParams['figure.figsize'] = [15, 10]
    plt.rcParams['figure.dpi'] = 300
    
    # Create figure with multiple subplots
    fig = plt.figure()
    
    # Plot 1: Bar plot of voltage magnitudes
    plt.subplot(2, 1, 1)
    bars = plt.bar(range(len(df)), df['Voltage (pu)'], alpha=0.6, color='skyblue')
    plt.axhline(y=1.05, color='r', linestyle='--', label='Upper Limit (1.05 pu)')
    plt.axhline(y=0.95, color='r', linestyle='--', label='Lower Limit (0.95 pu)')
    plt.title('Voltage Profile of IEEE 118-Bus System', fontsize=14, pad=20)
    plt.xlabel('Bus Number', fontsize=12)
    plt.ylabel('Voltage (pu)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Add some padding between subplots
    plt.subplots_adjust(hspace=0.3)
    
    # Plot 2: Voltage distribution
    plt.subplot(2, 1, 2)
    sns.histplot(data=df['Voltage (pu)'], bins=30, kde=True, color='skyblue')
    plt.axvline(x=1.05, color='r', linestyle='--', label='Upper Limit (1.05 pu)')
    plt.axvline(x=0.95, color='r', linestyle='--', label='Lower Limit (0.95 pu)')
    plt.title('Voltage Distribution', fontsize=14, pad=20)
    plt.xlabel('Voltage (pu)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(fontsize=10)
    
    # Save the figure
    plt.savefig('latex_report/voltage_profile.png', bbox_inches='tight')
    plt.close()
    
    # Create voltage status summary
    voltage_status = pd.cut(df['Voltage (pu)'], 
                          bins=[-np.inf, 0.95, 1.05, np.inf],
                          labels=['Low', 'Normal', 'High'])
    status_counts = voltage_status.value_counts()
    
    # Calculate percentages
    total = len(df)
    percentages = (status_counts / total * 100).round(2)
    
    # Create summary table
    summary_data = {
        'Count': status_counts,
        'Percentage (%)': percentages
    }
    summary_df = pd.DataFrame(summary_data)
    
    # Save summary to file
    with open('latex_report/voltage_summary.txt', 'w') as f:
        f.write("Voltage Profile Summary\n")
        f.write("=====================\n\n")
        f.write(str(summary_df))
        f.write("\n\nVoltage Statistics:\n")
        f.write("------------------\n")
        f.write(f"Mean Voltage: {df['Voltage (pu)'].mean():.4f} pu\n")
        f.write(f"Maximum Voltage: {df['Voltage (pu)'].max():.4f} pu\n")
        f.write(f"Minimum Voltage: {df['Voltage (pu)'].min():.4f} pu\n")
        f.write(f"Standard Deviation: {df['Voltage (pu)'].std():.4f} pu\n")

def main():
    # Initialize OpenDSS
    initialize_opendss()
    
    # Get voltage data
    voltage_data = get_voltage_data()
    
    # Create visualizations
    plot_voltage_profile(voltage_data)
    
    print("Voltage profile analysis completed. Check the latex_report directory for outputs.")

if __name__ == "__main__":
    main() 