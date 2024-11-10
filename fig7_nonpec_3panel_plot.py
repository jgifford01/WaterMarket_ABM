import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# Ensure Seaborn's aesthetics are applied
sns.set(style="whitegrid")
fontlabelsize = 10
linewidth = 1.5

# --------------------------- Step 1: Define Parameters and Load Data ---------------------------

# Define agent number and random seed
agent_number = 500
random_seed = 3145

# Define directories and ensure plots directory exists
data_dir = f"data/{agent_number}agents_seed{random_seed}"
plots_dir = f"plots/{agent_number}agents_seed{random_seed}"
os.makedirs(plots_dir, exist_ok=True)

# Load datasets with corrected directories
data_01to10 = pd.read_csv(f'{data_dir}_U01_10/GFT_SM_mean_min_max_U_01_10.csv')
data_10to01 = pd.read_csv(f'{data_dir}_10_01_nonpec/GFT_final_mean_array.csv')
data_pmax = pd.read_csv(f'{data_dir}_pmax/GFT_final_mean_array.csv')
water_value_df = pd.read_csv(f'{data_dir}_pmax/watervalue.csv')

# Extract relevant columns
data_U_mean, data_U_min, data_U_max = data_01to10.iloc[:, 0], data_01to10.iloc[:, 1], data_01to10.iloc[:, 2]
data_10to01_mean = data_10to01.iloc[:, 1]
data_pmax_mean = data_pmax.iloc[:, 1]
water_value_df = water_value_df.sort_values(by=water_value_df.columns[0]).to_numpy()

# Trim arrays to matching length if necessary
min_length = 101 #ensure all arrays are the same length
data_U_mean, data_U_min, data_U_max = data_U_mean[:min_length], data_U_min[:min_length], data_U_max[:min_length]
data_10to01_mean, data_pmax_mean = data_10to01_mean[:min_length], data_pmax_mean[:min_length]
water_value_no_trade = water_value_df

# Calculate GFT/TV0 values
GFT_SM_profmax_TV0 = data_pmax_mean / water_value_no_trade[:, 1]
GFT_SM_U_TV0 = data_U_mean / water_value_no_trade[:, 1]
GFT_SM_preffarm_TV0 = data_10to01_mean / water_value_no_trade[:, 1]
GFT_SM_U_max_TV0 = data_U_max / water_value_no_trade[:, 1]
GFT_SM_U_min_TV0 = data_U_min / water_value_no_trade[:, 1]


# Load data for the number of agents trading
num_trading_agents_profmax = pd.read_csv(f'{data_dir}_pmax/num_trading_agents_SM.csv')
num_trading_agents_preffarm = pd.read_csv(f'{data_dir}_10_01_nonpec/num_trading_agents_SM.csv')
num_trading_agents_U_full = pd.read_csv(f'{data_dir}_U01_10/num_trading_agents_SM.csv')

# Aggregate trading agents by proration rate
num_trading_agents_U = num_trading_agents_U_full.groupby('P').agg(['mean', 'min', 'max']).reset_index()

# --------------------------- Step 3: Create Combined Figure ---------------------------

fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.8), constrained_layout=True)

# Proration rate for consistent x-axis
proration_rate_plot1 = np.linspace(0, 1, min_length)

# --------------------------- Plot 1: Gains from Trade (GFT) Plot ---------------------------
# TVP1 compute
TVP1 = 80128.190760988 ## replace if run with different sim seed values

# value over pretrade nodrought value
ax1 = axes[0]
sns.lineplot(x=proration_rate_plot1, y=data_10to01_mean/TVP1, label="Seniority-based prefs", color='#CC444B', ax=ax1, linewidth=linewidth, legend=False)
sns.lineplot(x=proration_rate_plot1, y=data_U_mean/TVP1, label="Random prefs mean", color='#094074', ax=ax1, linewidth=linewidth, legend=False)
ax1.fill_between(proration_rate_plot1, data_U_min/TVP1, data_U_max/TVP1, color='#094074', label = "Random prefs range",alpha=0.2)
sns.lineplot(x=proration_rate_plot1, y=data_pmax_mean/TVP1, label="Profit maximization", color='#F6DB8C', ax=ax1, linewidth=linewidth, legend=False)

# stats
print("mean GFT_SM_preffarm_TV1|delta=1", data_10to01_mean.mean()/TVP1, "max GFT_SM_preffarm_TV1|delta=1", data_10to01_mean.max()/TVP1)
print("mean GFT_SM_U_TV1|delta=1", data_U_mean.mean()/TVP1, "max GFT_SM_U_TV1|delta=1", data_U_mean.max()/TVP1)
print("mean GFT_SM_pmax_TV1|delta=1", data_pmax_mean.mean()/TVP1, "max GFT_SM_pmax_TV1|delta=1", data_pmax_mean.max()/TVP1)

ax1.set_title("GFT over pre-trade value | δ=1", fontsize=fontlabelsize)
ax1.set_xlim(0, 1)
ax1.set_xlabel("Water availability index (δ)", fontsize=fontlabelsize)
ax1.tick_params(axis='y', labelsize=fontlabelsize)
ax1.set_xticklabels([f"{x:.2f}" for x in ax1.get_xticks()], fontsize=fontlabelsize)  # Labels as decimal
ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax1.set_ylabel("")
ax1.yaxis.set_major_locator(mticker.MaxNLocator(6))
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(4))

# --------------------------- Plot 2: GFT/TV0 Plot ---------------------------

ax2 = axes[1]
sns.lineplot(x=water_value_no_trade[:, 0], y=GFT_SM_preffarm_TV0, label="10 to 0.1", color='#CC444B', ax=ax2, linewidth=linewidth, legend=False)
sns.lineplot(x=water_value_no_trade[:, 0], y=GFT_SM_profmax_TV0, label="Profit Maximization", color='#F6DB8C', ax=ax2, linewidth=linewidth, legend=False)
sns.lineplot(x=water_value_no_trade[:, 0], y=GFT_SM_U_TV0, label="Mean U(0.1,10)", color='#094074', ax=ax2, linewidth=linewidth, legend=False)
ax2.fill_between(water_value_no_trade[:, 0], GFT_SM_U_min_TV0, GFT_SM_U_max_TV0, label = "U(0.1,10) range",color='#094074', alpha=0.2)
ax2.set_title("GFT over pre-trade value | δ", fontsize=fontlabelsize)
ax2.set_xlabel("Water availability index (δ)", fontsize=fontlabelsize)
ax2.set_xlim(0, 1)
ax2.set_ylim(0,)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
ax2.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax2.set_ylabel("")
ax2.yaxis.set_major_locator(mticker.MaxNLocator(6))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(4))
# stats
print("mean GFT_SM_preffarm_TV0|delta", GFT_SM_preffarm_TV0.mean(), "max GFT_SM_preffarm_TV0|delta", GFT_SM_preffarm_TV0.max())
print("mean GFT_SM_U_TV0|delta", GFT_SM_U_TV0.mean(), "max GFT_SM_U_TV0|delta", GFT_SM_U_TV0.max())
print("mean GFT_SM_pmax_TV0|delta", GFT_SM_profmax_TV0.mean(), "max GFT_SM_pmax_TV0|delta", GFT_SM_profmax_TV0.max())



# --------------------------- Plot 3: Fraction of Agents Trading ---------------------------

ax3 = axes[2]
sns.lineplot(x=num_trading_agents_preffarm['P'], y=num_trading_agents_preffarm['num_trading_agents_SM']/agent_number, label="10 to 0.1", color='#CC444B', ax=ax3, linewidth=linewidth, legend=False)
sns.lineplot(x=num_trading_agents_profmax['P'], y=num_trading_agents_profmax['num_trading_agents_SM']/agent_number, label="Profit Maximization", color='#F6DB8C', ax=ax3, linewidth=linewidth, legend=False)
sns.lineplot(x=num_trading_agents_U['P'], y=num_trading_agents_U['num_trading_agents_SM']['mean']/agent_number, label="U(0.1,10)", color='#094074', ax=ax3, linewidth=linewidth, legend=False)
ax3.fill_between(num_trading_agents_U['P'], num_trading_agents_U['num_trading_agents_SM']['min']/agent_number, num_trading_agents_U['num_trading_agents_SM']['max']/agent_number, label = "U(0.1,10) range",color='#094074', alpha=0.2)
ax3.set_title("Fraction of agents trading", fontsize=fontlabelsize)
ax3.set_xlabel("Water availability index (δ)", fontsize=fontlabelsize)
ax3.set_ylim(0,)
ax3.set_xlim(0, 1)
ax3.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
ax3.set_ylabel("")
# set number of y ticks
ax3.yaxis.set_major_locator(mticker.MaxNLocator(6))
ax3.xaxis.set_major_locator(mticker.MaxNLocator(4))

# print prof max series
# set prinmt options to print full series all rows
pd.set_option('display.max_rows', None)
print("num_trading_agents_profmax series", num_trading_agents_profmax['num_trading_agents_SM']/500)
# stats
print("mean num_trading_agents_preffarm", num_trading_agents_preffarm['num_trading_agents_SM'].mean()/500, "max num_trading_agents_preffarm", num_trading_agents_preffarm['num_trading_agents_SM'].max()/500)
print("mean num_trading_agents_profmax", num_trading_agents_profmax['num_trading_agents_SM'].mean()/500, "max num_trading_agents_profmax", num_trading_agents_profmax['num_trading_agents_SM'].max()/500)
print("mean num_trading_agents_U", num_trading_agents_U['num_trading_agents_SM']['mean'].mean()/500, "max num_trading_agents_U", num_trading_agents_U['num_trading_agents_SM']['max'].max()/500)

# --------------------------- Step 5: extra things ---------------------------
# Disable grid for each subplot

# Plot 1: Gains from Trade (GFT) Plot
ax1.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# Plot 2: GFT/TV0 Plot
ax2.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# Plot 3: Number of Agents Trading Over Usable Rights
ax3.grid(True, color='lightgray', linestyle='-', linewidth=0.5)


# --------------------------- Shared Legend -----------------------------------
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, frameon=False, fontsize=fontlabelsize, bbox_to_anchor=(0.5, -0.15))

# Apply grid and spine adjustments
for ax in axes:
    ax.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)
plt.tight_layout()
plt.subplots_adjust(left = 0.0, right = 1, wspace=0.3)  # Adjust the width space between subplots

# Save and display the figure
combined_plot_path = os.path.join(plots_dir, "3_panel_facet_nonpec.png")
plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
plt.savefig(f"{plots_dir}/3_panel_facet_nonpec.svg", format='svg', dpi=1000, bbox_inches='tight')



