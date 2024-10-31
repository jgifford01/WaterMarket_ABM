import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter

# Define your agent number and random seed
agent_number = 500        # Replace with your actual agent number
random_seed = 3145         # Replace with your actual random seed
ftsz = 9
# Define directories
data_dir = f"data/{agent_number}agents_seed{random_seed}"
plots_dir = f"plots/{agent_number}agents_seed{random_seed}"

# Create the plots directory if it doesn't exist
os.makedirs(plots_dir, exist_ok=True)

# Load supply and demand data
supply_demand_df = pd.read_csv(os.path.join(data_dir, "agent_data_SM_P0.1.csv"))
supply_demand_df = supply_demand_df.sort_values(by='sigma', ascending=True)

#### create a unit bid_ask column by cbar
supply_demand_df['unit_bid_ask'] = supply_demand_df['wtp_wta_max'] / supply_demand_df['cbar']

# Define the proration levels you want to plot
proration_levels = [0.10, 0.25, 0.50, 0.75, 0.90]

# Create a figure with 5 subplots (1 row, 5 columns)
fig, axes = plt.subplots(1, 5, figsize=(6.5, 2.8), sharey=True)  # Share the y-axis for consistency

def divide_by_number(x, pos):
    return '{:.0f}'.format(x / 1000)


# Iterate through each proration level and plot the supply and demand curves
for idx, P in enumerate(proration_levels):
    # Set proration column: 1 for sigma <= P, otherwise 0
    supply_demand_df['pro'] = np.where(supply_demand_df['sigma'] <= P, 1, 0)
    
    # Split into buyers and sellers
    sellers = supply_demand_df[supply_demand_df['pro'] == 1]
    buyers = supply_demand_df[supply_demand_df['pro'] == 0]

    
    
    # Sort sellers by WTA (ascending) and buyers by WTP (descending)
    sellers = sellers.sort_values(by='unit_bid_ask', ascending=True)
    buyers = buyers.sort_values(by='unit_bid_ask', ascending=False)

    # do the same for non-pec
    #sellers_nonpec = sellers.sort_values(by='bid_ask_nonpec', ascending=True)
    #buyers_nonpec = buyers.sort_values(by='bid_ask_nonpec', ascending=False)
    



    
    # Create cumulative quantities for sellers and buyers
    sellers['supply_cumul'] = sellers['cbar'].cumsum()
    buyers['demand_cumul'] = buyers['cbar'].cumsum()

    #sellers_nonpec['supply_cumul'] = sellers_nonpec['cbar'].cumsum()
    #buyers_nonpec['demand_cumul'] = buyers_nonpec['cbar'].cumsum()


    # Append (0, max(WTP)) to buyers to start the demand curve from the maximum WTP
    buyers = pd.concat([pd.DataFrame({'demand_cumul': [0], 'unit_bid_ask': [buyers['unit_bid_ask'].max()]}), buyers], ignore_index=True)
    #buyers_nonpec = pd.concat([pd.DataFrame({'demand_cumul': [0], 'wtp_wta_max': [buyers_nonpec['wtp_wta_max'].max()]}), buyers_nonpec], ignore_index=True)

    # Append (max(Q), infinity) to sellers to extend the supply curve to infinity price
    sellers = pd.concat([sellers, pd.DataFrame({'supply_cumul': [sellers['supply_cumul'].max()], 'unit_bid_ask': [350]})], ignore_index=True)
    #sellers_nonpec = pd.concat([sellers_nonpec, pd.DataFrame({'supply_cumul': [sellers_nonpec['supply_cumul'].max()], 'wtp_wta_max': [350]})], ignore_index=True)
    
    # append max demanded quantity, 0
    buyers = pd.concat([buyers, pd.DataFrame({'demand_cumul': [buyers['demand_cumul'].max()], 'unit_bid_ask': [0]})], ignore_index=True)
    #buyers_nonpec = pd.concat([buyers_nonpec, pd.DataFrame({'demand_cumul': [buyers_nonpec['demand_cumul'].max()], 'wtp_wta_max': [0]})], ignore_index=True)

    # Plot the supply and demand curves
    ax = axes[idx]
    ax.plot(sellers['supply_cumul'], sellers['unit_bid_ask'], label='Supply', color='#8CD8C0', linewidth=2)
    ax.plot(buyers['demand_cumul'], buyers['unit_bid_ask'], label='Demand', color='#A0A09F',linewidth=2)
    #ax.plot(sellers_nonpec['supply_cumul'], sellers_nonpec['bid_ask_nonpec'], label='Supply non-pec', color='red', linestyle='-', linewidth=2)
    #ax.plot(buyers_nonpec['demand_cumul'], buyers_nonpec['bid_ask_nonpec'], label='Demand non-pec', color='blue', linestyle='-', linewidth=2)

    
    # Customize axes
    ax.set_xlabel('Q (thousands)', fontsize=ftsz)
    if idx == 0:
        ax.set_ylabel('WTP/WTA per unit', fontsize=ftsz)  # Only label the y-axis on the first plot
    ax.set_title(f'{P} WAI', fontsize=ftsz)

    if idx != 0:
        ax.tick_params(left=False, right=False, labelleft=False)  # Remove ticks and labels from the y-axis
    
    # Adjust layout to remove space between the plots
    plt.subplots_adjust(wspace=-1)  # Set width space between subplots to zero   
    
    # Set tick label size
    ax.tick_params(axis='both', labelsize=ftsz)
    # x axis limits
    ax.set_xlim(0, 2000)
    # y axis limits
    ax.set_ylim(0, 25)


    # add x axis ticks
    #ax.set_xticks(np.linspace(0, , num=3))
    # add y axis ticks
    #ax.set_yticks(np.linspace(0, , num=6))
    
    # Add grid
    ax.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

    ax.xaxis.set_major_formatter(FuncFormatter(divide_by_number))
    
# Add a single legend for the entire figure
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, fontsize=ftsz, frameon=False, bbox_to_anchor=(0.5, -0.2))

# remove whitespace in between subplots
plt.subplots_adjust(left = 0.0, right = 1,wspace=0.10)


# Adjust layout to prevent overlap
#plt.tight_layout()
for ax in axes:
    # Set the thickness of the borders (spines)
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # Set border color to black
        spine.set_linewidth(1.5)   
# Save the combined figure as PNG and SVG
plt.savefig(os.path.join(plots_dir, "supply_demand_proration_panel.png"), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(plots_dir, "supply_demand_proration_panel.svg"), format='svg', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
