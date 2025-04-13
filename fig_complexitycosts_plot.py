import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.colors as mcolors
import seaborn as sns

from matplotlib.lines import Line2D


sns.set(style="whitegrid")

# --- Parameters for consistent styling ---
fontlabelsize = 10
linewidth = 1.5

# Create output folder
output_dir = "complexity_plots"
os.makedirs(output_dir, exist_ok=True)

# --------------------------- Load and Process Data ---------------------------

def load_data(base_dir):
    sigma_values = []
    mean_values = []
    mean_trading_agents = []

    for sigma in range(1, 11):
        gft_path = f"{base_dir}/500agents_seed3145_sigma{sigma}/GFT_final_mean_array.csv"
        trading_path = f"{base_dir}/500agents_seed3145_sigma{sigma}/num_trading_agents_CPP.csv"

        df_gft = pd.read_csv(gft_path)
        mean_cp = df_gft["Central Planning Mean"].mean()
        sigma_values.append(sigma)
        mean_values.append(mean_cp)

        df_trading = pd.read_csv(trading_path)
        mean_val = df_trading["num_trading_agents_CPP"].mean()
        mean_trading_agents.append(mean_val)

    zipped = sorted(zip(sigma_values, mean_trading_agents, mean_values))
    sigma_sorted, agents_sorted, gft_sorted = zip(*zipped)

    agents_arr = np.array(agents_sorted)
    gft_arr = np.array(gft_sorted)

    max_agents = agents_arr.max()
    max_gft = gft_arr.max()

    reduction_agents = 100 * (max_agents - agents_arr) / max_agents
    reduction_gft = 100 * (max_gft - gft_arr) / max_gft

    return np.array(sigma_sorted), agents_arr, gft_arr, reduction_agents, reduction_gft

# Load both datasets
sigma_rand, agents_rand, gft_rand, red_agents_rand, red_gft_rand = load_data("data_rand")
sigma_fixed, agents_fixed, gft_fixed, red_agents_fixed, red_gft_fixed = load_data("data_fixed")

# Normalize GFT
gft_rand_norm = gft_rand / 81861.30891806362
gft_fixed_norm = gft_fixed / 81861.30891806362

# --------------------------- Plotting ---------------------------

fig, axes = plt.subplots(1, 3, figsize=(6.5, 3), constrained_layout=True)
cmap = plt.get_cmap('viridis')

# Normalize σ values for colormap
norm = mcolors.Normalize(vmin=1, vmax=10)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

# --- Plot 1: Fraction of agents trading ---
ax1 = axes[0]
ax1.plot(sigma_rand, agents_rand / 500, color='lightgray', linewidth=1, linestyle='--')
ax1.plot(sigma_fixed, agents_fixed / 500, color='lightgray', linewidth=1, linestyle='-')

ax1.scatter(sigma_rand, agents_rand / 500, c=sigma_rand, cmap=cmap, norm=norm, s=30, label='Random', marker='o')
ax1.scatter(sigma_fixed, agents_fixed / 500, c=sigma_fixed, cmap=cmap, norm=norm, s=30, label='Fixed', marker='s')

ax1.set_xlabel("σ", fontsize=fontlabelsize)
ax1.set_title("Fraction of agents trading", fontsize=fontlabelsize)
ax1.set_ylim(0, 1.05)
ax1.set_xticks(sigma_rand)
ax1.tick_params(axis='both', labelsize=fontlabelsize)
ax1.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# --- Plot 2: GFT over pre-trade value ---
ax2 = axes[1]
ax2.plot(sigma_rand, gft_rand_norm, color='lightgray', linewidth=1, linestyle='--')
ax2.plot(sigma_fixed, gft_fixed_norm, color='lightgray', linewidth=1, linestyle='-')

ax2.scatter(sigma_rand, gft_rand_norm, c=sigma_rand, cmap=cmap, norm=norm, s=30, label='Random', marker='o')
ax2.scatter(sigma_fixed, gft_fixed_norm, c=sigma_fixed, cmap=cmap, norm=norm, s=30, label='Fixed', marker='s')

ax2.set_xlabel("σ", fontsize=fontlabelsize)
ax2.set_title("GFT over pre-trade value | δ=1", fontsize=fontlabelsize)
ax2.set_ylim(0, .2)
ax2.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax2.set_xticks(sigma_rand)
ax2.tick_params(axis='both', labelsize=fontlabelsize)
ax2.grid(True, color='lightgray', linestyle='-', linewidth=0.5)

# --- Plot 3: Relative Decline in Trading vs GFT ---
ax3 = axes[2]
ax3.plot(red_agents_rand, red_gft_rand, color='lightgray', linestyle='--', linewidth=1)
ax3.plot(red_agents_fixed, red_gft_fixed, color='lightgray', linestyle='-', linewidth=1)

sc_rand = ax3.scatter(red_agents_rand, red_gft_rand, c=sigma_rand, cmap=cmap, norm=norm, s=30, marker='o', label='Random')
sc_fixed = ax3.scatter(red_agents_fixed, red_gft_fixed, c=sigma_fixed, cmap=cmap, norm=norm, s=30, marker='s', label='Fixed')

ax3.set_xlabel("% ↓ agents trading", fontsize=fontlabelsize)
#ax3.set_ylabel("% ↓ GFT", fontsize=fontlabelsize)  # Optional: add y-label now that axes are log
ax3.set_title("% ↓ GFT", fontsize=fontlabelsize)

# Set both axes to log scale
ax3.set_xscale('symlog', linthresh=1)
ax3.set_yscale('symlog', linthresh=1)
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 100)

# Ticks and grid
ax3.tick_params(axis='both', labelsize=fontlabelsize)
ax3.grid(True, which='both', linestyle='-', linewidth=0.5, color='lightgray')


# --- Add colorbar below all plots ---
cbar_ax = fig.add_axes([0.35, -0.08, 0.3, 0.03])  # [left, bottom, width, height]
cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')

# Show ticks for each sigma value (1 through 10)
sigma_ticks = np.arange(1, 11)
cbar.set_ticks(sigma_ticks)
cbar.set_ticklabels([str(s) for s in sigma_ticks])

cbar.set_label("σ", fontsize=fontlabelsize)
cbar.ax.tick_params(labelsize=fontlabelsize)


# Custom legend for linetypes
line_legend_elements = [
    Line2D([0], [0], color='lightgray', linestyle='--', linewidth=1,
           label=r'$\mathrm{Len}(b^j) \in [1,\sigma]$'),
    Line2D([0], [0], color='lightgray', linestyle='-', linewidth=1,
           label=r'$\mathrm{Len}(b^j) = \sigma$')
]

#Length(b^j) \in [1,σ]
#  

# Create a new invisible axis for placing the legend next to the colorbar

legend_ax = fig.add_axes([0.07, -0.12, 0.3, 0.03])

legend_ax.axis('off')  # hide the axis

# Add the legend to this dummy axis
legend_ax.legend(
    handles=line_legend_elements,
    loc='center left',
    fontsize=fontlabelsize,
    frameon=True,
    ncol=1,
    title_fontsize=fontlabelsize
)



# --- Style tweaks ---
for ax in axes:
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)
    ax.tick_params(axis='y', pad=0)

# --- Save ---
combined_path = os.path.join(output_dir, "combined_fixed_vs_random_1x3_colored.png")
plt.savefig(combined_path, dpi=300, bbox_inches='tight')
plt.savefig(combined_path.replace(".png", ".svg"), format='svg', dpi=1000, bbox_inches='tight')
plt.close()

print(f"Combined comparison plot with colormap saved to {combined_path}")
