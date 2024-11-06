import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# Ensure Seaborn's aesthetics are applied
sns.set(style="whitegrid")
fontlabelsize= 10
linewidth = 1.5
# --------------------------- Step 1: Define Parameters and File Paths ---------------------------

# Define your agent number and random seed
agent_number = 500      # Replace with your actual agent number
random_seed = 3145         # Replace with your actual random seed

# Define directories
data_dir = f"data/{agent_number}agents_seed{random_seed}"
plots_dir = f"plots/{agent_number}agents_seed{random_seed}"

# Create the plots directory if it doesn't exist
os.makedirs(plots_dir, exist_ok=True)

# --------------------------- Step 2: Load and Process Data ---------------------------

# --- Plot 1: Gains from Trade (GFT) Plot ---

# Load GFT final mean array and BI range array for Plot 1
GFT_final_mean_df_plot1 = pd.read_csv(os.path.join(data_dir, "GFT_final_mean_array.csv"))
GFT_final_mean_array_plot1 = GFT_final_mean_df_plot1.to_numpy().T  # Transpose as per original code

BI_range_df_plot1 = pd.read_csv(os.path.join(data_dir, "BI_range_array.csv"))
BI_range_array_plot1 = BI_range_df_plot1.to_numpy()

GFT_bi_range_arraymax_plot1 = BI_range_array_plot1[:, 1]
GFT_bi_range_arraymin_plot1 = BI_range_array_plot1[:, 0]

# Define Proration rate from 0 to 1
# Assuming there are 101 points corresponding to PP_reversed_plot1 from 100 to 0
proration_rate_plot1 = np.linspace(0, 1, len(GFT_final_mean_array_plot1[0, :]))

# --- Plot 2: GFT/TV0 Plot ---

# Load GFT final mean array for Plot 2 (reload to avoid duplication issues

GFT_final_mean_df_plot2 = pd.read_csv(os.path.join(data_dir, "GFT_final_mean_array.csv"))
GFT_final_mean_array_plot2 = GFT_final_mean_df_plot2.to_numpy()

# Load water value data
water_value_df_plot2 = pd.read_csv(os.path.join(data_dir, "watervalue.csv"))
water_value_df_plot2 = water_value_df_plot2.sort_values(by=water_value_df_plot2.columns[0])
water_value_no_trade_plot2 = water_value_df_plot2.to_numpy()

# Calculate GFT/TV0 values
GFT_bilat_TV0_plot2 = GFT_final_mean_array_plot2[:, 2] / water_value_no_trade_plot2[:, 1]
GFT_smart_TV0_plot2 = GFT_final_mean_array_plot2[:, 1] / water_value_no_trade_plot2[:, 1]
GFT_cent_TV0_plot2 = GFT_final_mean_array_plot2[:, 0] / water_value_no_trade_plot2[:, 1]

# Calculate range for fill_between
range_min_TVO_plot2 = GFT_bi_range_arraymin_plot1 / water_value_no_trade_plot2[:, 1]
range_max_TVO_plot2 = GFT_bi_range_arraymax_plot1 / water_value_no_trade_plot2[:, 1]

# --- Plot 3: Number of Agents Trading Over Usable Rights ---

# Load bilateral agent trading data
num_trading_agents_bi_df_plot3 = pd.read_csv(os.path.join(data_dir, "num_trading_agents_BI.csv"))

# Group by 'P' and calculate mean, min, max for 'num_trading_agents_BM'
num_trading_agents_summary_plot3 = num_trading_agents_bi_df_plot3.groupby('P').agg(
    mean_num_agents=('num_trading_agents_BM', 'mean'),
    min_num_agents=('num_trading_agents_BM', 'min'),
    max_num_agents=('num_trading_agents_BM', 'max')
).reset_index()

# Load Smart Market agent trading data
num_trading_agents_SM_df_plot3 = pd.read_csv(os.path.join(data_dir, "num_trading_agents_SM.csv"))
num_trading_agents_SM_plot3 = num_trading_agents_SM_df_plot3.sort_values(by='P')

# load central planning data
num_trading_agents_CP_df_plot3 = pd.read_csv(os.path.join(data_dir, "num_trading_agents_CPP.csv"))
num_trading_agents_CP_plot3 = num_trading_agents_CP_df_plot3.sort_values(by='P')    

# --------------------------- Step 3: Create Combined Figure ---------------------------

# Create a figure with 1 row and 3 columns
fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.8),constrained_layout=True)  # Adjust figsize as needed

# --------------------------- Plot 1: Gains from Trade (GFT) Plot ---------------------------

ax1 = axes[0]

# find total value at p=1
TVP1 = water_value_no_trade_plot2[-1, 1]


""" Full value
# Plot the three market types
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[0, :],
             label="Full information", color='#A0A09F', ax=ax1, legend=False,linewidth=linewidth)
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[1, :],
             label="Smart market", color='#F6DB8C', ax=ax1, legend=False,linewidth=linewidth)
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[2, :],
             label="Bilateral market", color='#8CD8C0', ax=ax1, legend=False,linewidth=linewidth)

# Fill between for range
ax1.fill_between(proration_rate_plot1, GFT_bi_range_arraymin_plot1, GFT_bi_range_arraymax_plot1,
                 color='#E6F6F1', alpha=0.8, label="Bilateral range")  #
"""
# GFT lines divided by TVP1
# Plot the three market types
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[0, :]/TVP1,
             label="Full information", color='#A0A09F', ax=ax1, legend=False,linewidth=linewidth)
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[1, :]/TVP1,
                label="Smart market", color='#F6DB8C', ax=ax1, legend=False,linewidth=linewidth)
sns.lineplot(x=proration_rate_plot1, y=GFT_final_mean_array_plot1[2, :]/TVP1,
                label="Bilateral market", color='#8CD8C0', ax=ax1, legend=False,linewidth=linewidth)

# Fill between for range
ax1.fill_between(proration_rate_plot1, GFT_bi_range_arraymin_plot1/TVP1, GFT_bi_range_arraymax_plot1/TVP1,
                    color='#E6F6F1', alpha=0.8, label="Bilateral range")  #

# Customize axes
#ax1.set_xlabel("Proration rate", color='black', fontsize=10)
#ax1.set_ylabel("Gains from Trade", color='black', fontsize=10)
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_ylim(0, )

# Set x-axis from 0 to 1 without percentage labels
ax1.set_xlim(0, 1)
ax1.set_xticks(np.linspace(0, 1, num=6))
ax1.set_xticklabels([f"{x:.1f}" for x in ax1.get_xticks()], fontsize=fontlabelsize)  # Labels as decimal
ax1.set_xlabel("Water availability index", color='black', fontsize=fontlabelsize)


# set y-axis labels fontsize
ax1.tick_params(axis='y', labelsize=fontlabelsize)
#ax1.set_yticks(np.linspace(0, 350, num=6))
#ax1.set_yticks(np.linspace(0, 3200, num=20))

# plot title
ax1.set_title("GFT over pre-trade value | δ=1", fontsize=fontlabelsize)

# --------------------------- Plot 2: GFT/TV0 Plot ---------------------------

ax2 = axes[1]

# Plot the three market types
sns.lineplot(x=water_value_no_trade_plot2[:, 0], y=GFT_cent_TV0_plot2,
             label="Central Planning", color='#A0A09F', ax=ax2, legend=False, linewidth=linewidth)
sns.lineplot(x=water_value_no_trade_plot2[:, 0], y=GFT_smart_TV0_plot2,
             label="Smart Market", color='#F6DB8C', ax=ax2, legend=False, linewidth=linewidth)
sns.lineplot(x=water_value_no_trade_plot2[:, 0], y=GFT_bilat_TV0_plot2,
             label="Bilateral Market", color='#8CD8C0', ax=ax2, legend=False, linewidth=linewidth)

# Fill between for range
ax2.fill_between(water_value_no_trade_plot2[:, 0], range_min_TVO_plot2, range_max_TVO_plot2,
                 color='#E6F6F1', alpha=0.8, label="_nolegend_")

# Customize axes
ax2.set_xlabel("Water availability index", color='black', fontsize=fontlabelsize)
#ax2.set_ylabel("GFT/TV0", color='black', fontsize=10)
ax2.tick_params(axis='y', labelcolor='black')
ax2.set_ylim(0,  )
ax2.set_xlim(0, 1)

# Set x-axis from 0 to 1 without percentage labels
ax2.set_xticks(np.linspace(0, 1, num=6))
ax2.set_xticklabels([f"{x:.1f}" for x in ax2.get_xticks()], fontsize=fontlabelsize)  # Labels as decimal

# set y-axis labels fontsize
ax2.tick_params(axis='y', labelsize=fontlabelsize)
# Set y-axis ticks to have 1 decimal place
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax2.set_yticks(np.linspace(0, 2, num=6))

# add plot title
ax2.set_title("GFT over pre-trade value | δ", fontsize=fontlabelsize)

# --------------------------- Plot 3: Number of Agents Trading Over Usable Rights ---------------------------

ax3 = axes[2]

# Plot Bilateral Market mean
sns.lineplot(x=num_trading_agents_summary_plot3['P'],
             y=num_trading_agents_summary_plot3['mean_num_agents'] / agent_number,
             label="Bilateral Market", color='#8CD8C0', ax=ax3, legend=False,linewidth=linewidth)

# Fill between for Bilateral Market min and max
ax3.fill_between(num_trading_agents_summary_plot3['P'],
                num_trading_agents_summary_plot3['min_num_agents'] / agent_number,
                num_trading_agents_summary_plot3['max_num_agents'] / agent_number,
                color='#E6F6F1', alpha=0.8, label="Bilateral Range")

# Plot Smart Market
sns.lineplot(x=num_trading_agents_SM_plot3['P'],
             y=num_trading_agents_SM_plot3['num_trading_agents_SM'] / agent_number,
             label="Smart Market", color='#F6DB8C', ax=ax3, legend=False,linewidth=linewidth)

# Plot Central Planning line
sns.lineplot(x=num_trading_agents_CP_plot3['P'],
                y=num_trading_agents_CP_plot3['num_trading_agents_CPP'] / agent_number,
                label="Full information", color='#A0A09F', ax=ax3, legend=False,linewidth=linewidth)

# Customize axes
ax3.set_xlabel(" ", color='black', fontsize=fontlabelsize)
ax3.set_ylabel(" ", color='black', fontsize=fontlabelsize)
ax3.tick_params(axis='y', labelcolor='black')
ax3.set_ylim(0, 1.2)
ax3.set_xlim(0, 1)

# Set x-axis from 0 to 1 without percentage labels
ax3.set_xticks(np.linspace(0, 1, num=6))
ax3.set_xticklabels([f"{x:.1f}" for x in ax3.get_xticks()], fontsize=fontlabelsize)  # Labels as decimal
ax3.set_xlabel("Water availability index", color='black', fontsize=fontlabelsize)
# set y-axis labels fontsize
ax3.tick_params(axis='y', labelsize=fontlabelsize)

# add plot title
ax3.set_title("Fraction of agents trading", fontsize=fontlabelsize)

# --------------------------- Step 4: Create Shared Legend ---------------------------

# Collect handles and labels from the first subplot (ax1)
handles, labels = ax1.get_legend_handles_labels()


# Create a single legend for the entire figure
fig.legend(handles, labels, loc='lower center', ncol=4, frameon=False, fontsize=fontlabelsize,
           bbox_to_anchor=(0.5, -0.05))  # Adjust this tuple to control the legend position (x, y)
           #borderaxespad=-0.35)  # Increase this value to add more padding around the legend




# --------------------------- Step 5: extra things ---------------------------
# Disable grid for each subplot

# Plot 1: Gains from Trade (GFT) Plot
ax1.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# Plot 2: GFT/TV0 Plot
ax2.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# Plot 3: Number of Agents Trading Over Usable Rights
ax3.grid(True, color='lightgray', linestyle='-', linewidth=0.5)


# make grid very faint

# Loop through each subplot axis and customize the spines
for ax in axes:
    # Customize all 4 spines (top, bottom, left, right)
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # Set the color of the bounding box
        spine.set_linewidth(1.5)      # Set the thickness (boldness) of the bounding box

for ax in axes:
    ax.tick_params(axis='y', pad=0)  # Adjust y-axis tick label padding for all subplots


# --------------------------- Step 5: Final Adjustments and Save ---------------------------

# Adjust layout to prevent overlapping elements
plt.tight_layout()

plt.subplots_adjust(left = 0.0, right = 1, wspace=0.2)  # Adjust the width space between subplots




# Save the combined figure
combined_plot_path = os.path.join(plots_dir, "3_panel_facet.png")
plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')  # Adjust DPI as needed


# save as svg
plt.savefig(os.path.join(plots_dir, "3_panel_facet.svg"), format='svg', dpi=1000, bbox_inches='tight')  # Adjust DPI as needed
