import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Ensure Seaborn's aesthetics are applied
sns.set(style="whitegrid")
fontlabelsize = 10
linewidth = 3

# Define agent number and random seed
agent_number = 500     # Replace with your actual agent number
random_seed = 3145     # Replace with your actual random seed

# Importing data
CPP_prices = pd.read_csv(f'data/{agent_number}agents_seed{random_seed}/lagrange_multiplier_theta_CPP.csv')
BI_prices = pd.read_csv(f'data/{agent_number}agents_seed{random_seed}/price_collection_array_BI.csv')
SM_prices = pd.read_csv(f'data/{agent_number}agents_seed{random_seed}/price_collection_array_SM.csv')



# Group BI prices by P
BI_prices_grouped = BI_prices.groupby('P').agg({
    'mean_price': 'mean',
    # mean of max
    'max_price': 'mean',
    # mean of min
    'min_price': 'mean',
    #  25th percent of mean
    '25th_percentile_price': 'mean',
    # 75th percent of mean
    '75th_percentile_price': 'mean'
}).reset_index()


# Filter and sort P values for all datasets
BI_prices_grouped = BI_prices_grouped[BI_prices_grouped['P'].isin(np.arange(0, 1.01, 0.01))].sort_values(by='P')
SM_prices = SM_prices[SM_prices['P'] <= 1].sort_values(by='P')
CPP_prices = CPP_prices.dropna(subset=['P', 'lagrange_multiplier_theta_mean' ]).sort_values(by='P')



# Create a single plot
fig, ax = plt.subplots(figsize=(6.5, 2.8), constrained_layout=True)  # Adjust the size as needed

# Define consistent colors
color_cpp = '#A0A09F'       # Gray for CPP
color_bi = '#8CD8C0'        # Teal for BI
color_sm = '#F6DB8C'        # Yellow for SM
color_SMeq = 'red'      



# Plot  prices with confidence band
ax.fill_between(BI_prices_grouped['P'], BI_prices_grouped['min_price'], BI_prices_grouped['max_price'], color=color_bi, alpha=0.2)
ax.fill_between(SM_prices['P'], SM_prices['min_price'], SM_prices['max_price'], color=color_sm, alpha=0.2)

sns.lineplot(x=SM_prices['P'], y=SM_prices['mean_price'], color=color_sm, ax=ax, legend=False, linewidth=linewidth)
sns.lineplot(x=BI_prices_grouped['P'], y=BI_prices_grouped['mean_price'], color=color_bi, ax=ax, legend=False, linewidth=linewidth)

# Plot CPP prices
sns.lineplot(x=CPP_prices['P'], y=CPP_prices['lagrange_multiplier_theta_mean'], color=color_cpp, ax=ax, legend=False, linewidth=linewidth)
ax.fill_between(CPP_prices['P'], CPP_prices['lagrange_multiplier_theta_min'], CPP_prices['lagrange_multiplier_theta_max'], color=color_cpp, alpha=0.2)
ax.plot(CPP_prices['P'], CPP_prices['lagrange_multiplier_theta_25th_percentile'], color=color_cpp, linestyle=':', linewidth=linewidth)
ax.plot(CPP_prices['P'], CPP_prices['lagrange_multiplier_theta_75th_percentile'], color=color_cpp, linestyle=':', linewidth=linewidth)

# plot 25th and 75th percentiles for bi and sm
ax.plot(BI_prices_grouped['P'], BI_prices_grouped['25th_percentile_price'], color=color_bi, linestyle=':', linewidth=linewidth)
ax.plot(BI_prices_grouped['P'], BI_prices_grouped['75th_percentile_price'], color=color_bi, linestyle=':', linewidth=linewidth)

ax.plot(SM_prices['P'], SM_prices['25th_percentile_price'], color=color_sm, linestyle=':', linewidth=linewidth)
ax.plot(SM_prices['P'], SM_prices['75th_percentile_price'], color=color_sm, linestyle=':', linewidth=linewidth)




# Customize axes
ax.set_xlabel("Water availability index (δ)", color='black', fontsize=fontlabelsize)
ax.set_ylabel("Price", color='black', fontsize=fontlabelsize)
ax.tick_params(axis='y', labelcolor='black')
ax.set_xlim(0, 1)
ax.set_xticks(np.linspace(0, 1, num=6))
ax.set_xticklabels([f"{x:.1f}" for x in ax.get_xticks()], fontsize=fontlabelsize)  # Labels as decimal
ax.tick_params(axis='y', labelsize=fontlabelsize)
ax.set_ylim(0, )  # Automatically adjust y-limit to fit the data

# Customize spines
for spine in ax.spines.values():
    spine.set_edgecolor('black')  # Set the color of the bounding box
    spine.set_linewidth(1.5)      # Set the thickness (boldness) of the bounding box

# Customize grid
ax.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# Create handles for the legend
legend_elements = [
    Line2D([0], [0], color=color_cpp, lw=linewidth, label='Full info'),
    Line2D([0], [0], color=color_bi, lw=linewidth, label='BI (mean)'),
    
    Line2D([0], [0], color=color_sm, lw=linewidth, label='SM (mean)'),
    
    Line2D([0], [0], color=color_bi, lw=linewidth, linestyle=':', label='BI (mean 25/75 percentile)'),
    Line2D([0], [0], color=color_sm, lw=linewidth, linestyle=':', label='SM (25/75 percentile)'),
    Line2D([0], [0], color=color_cpp, lw=linewidth, linestyle=':', label='Full info (25/75 percentile)'),
    
    Patch(facecolor=color_cpp, edgecolor='none', alpha=1, label='CPP range'),
    Patch(facecolor=color_bi, edgecolor='none', alpha=1, label='BI range'),
    Patch(facecolor=color_sm, edgecolor='none', alpha=1, label='SM range'),


    
    
]

# Manually create the legend at the bottom with colors matching lines and ranges
fig.legend(handles=legend_elements, loc='lower center', ncol=3, frameon=False, fontsize=fontlabelsize, bbox_to_anchor=(0.5, -0.3))

# Adjust layout to prevent overlapping elements
plt.tight_layout()

# Save the figure
plot_path = f"plots/{agent_number}agents_seed{random_seed}/price_plot_single.png"
os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path, dpi=300, bbox_inches='tight')

# svg
plot_path = f"plots/{agent_number}agents_seed{random_seed}/price_plot_single.svg"
os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path, bbox_inches='tight')

# Show the plot
plt.show()
