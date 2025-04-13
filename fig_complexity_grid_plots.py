import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

sns.set(style="whitegrid")

# --- Setup ---
fontlabelsize = 10
output_dir = "complexity_plots_grid"
os.makedirs(output_dir, exist_ok=True)

prorates = [0.1, 0.25, 0.5, 0.75]
prorate_labels = ["δ = 0.1", "δ = 0.25", "δ = 0.5", "δ = 0.75"]
gft_norm_const = 80841.80972730806  # Normalization constant fixed sigma=4

def load_data_by_proration(base_dir, proration):
    sigma_vals, gft_vals, agent_vals = [], [], []

    for sigma in range(1, 11):
        gft_path = f"{base_dir}/500agents_seed3145_sigma{sigma}/GFT_final_mean_array.csv"
        trading_path = f"{base_dir}/500agents_seed3145_sigma{sigma}/num_trading_agents_CPP.csv"

        df_gft = pd.read_csv(gft_path)
        df_trade = pd.read_csv(trading_path)

        gft_val = df_gft.iloc[int(proration * 100)]["Central Planning Mean"]
        trade_val = df_trade[df_trade["P"] == proration]["num_trading_agents_CPP"].values[0]

        sigma_vals.append(sigma)
        gft_vals.append(gft_val)
        agent_vals.append(trade_val)

    zipped = sorted(zip(sigma_vals, agent_vals, gft_vals))
    sigma_sorted, agents_sorted, gft_sorted = zip(*zipped)

    agents_arr = np.array(agents_sorted)
    gft_arr = np.array(gft_sorted)

    max_agents = 500 #agents_arr.max()
    max_gft = gft_arr.max()

    reduction_agents = 100 * (max_agents - agents_arr) / max_agents
    reduction_gft = 100 * (max_gft - gft_arr) / max_gft

    return np.array(sigma_sorted), agents_arr, gft_arr, reduction_agents, reduction_gft

# --- Plot setup ---
fig, axes = plt.subplots(4, 3, figsize=(9, 9.5), constrained_layout=True)
cmap = plt.get_cmap('viridis')
norm = mcolors.Normalize(vmin=1, vmax=10)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

# Formatter to remove scientific notation on symlog axes
formatter = FuncFormatter(lambda x, _: f'{x:.0f}')

for i, (p, label) in enumerate(zip(prorates, prorate_labels)):
    sigma_r, a_r, gft_r, red_a_r, red_gft_r = load_data_by_proration("data_rand", p)
    sigma_f, a_f, gft_f, red_a_f, red_gft_f = load_data_by_proration("data_fixed", p)

    gft_r_norm = gft_r / gft_norm_const
    gft_f_norm = gft_f / gft_norm_const

    # --- Fraction Trading ---
    ax1 = axes[i, 0]
    ax1.plot(sigma_r, a_r / 500, linestyle='--', color='lightgray')
    ax1.plot(sigma_f, a_f / 500, linestyle='-', color='lightgray')
    ax1.scatter(sigma_r, a_r / 500, c=sigma_r, cmap=cmap, norm=norm, s=30, marker='o')
    ax1.scatter(sigma_f, a_f / 500, c=sigma_f, cmap=cmap, norm=norm, s=30, marker='s')
    ax1.set_ylim(0, 1.05)
    ax1.set_xticks(sigma_r)
    if i == 3: ax1.set_xlabel("σ", fontsize=fontlabelsize)
    if i == 0: ax1.set_title("Fraction Trading", fontsize=fontlabelsize)
    ax1.set_ylabel(label, fontsize=fontlabelsize)
    ax1.tick_params(labelsize=fontlabelsize)

    # --- GFT Normalized ---
    ax2 = axes[i, 1]
    ax2.plot(sigma_r, gft_r_norm, linestyle='--', color='lightgray')
    ax2.plot(sigma_f, gft_f_norm, linestyle='-', color='lightgray')
    ax2.scatter(sigma_r, gft_r_norm, c=sigma_r, cmap=cmap, norm=norm, s=30, marker='o')
    ax2.scatter(sigma_f, gft_f_norm, c=sigma_f, cmap=cmap, norm=norm, s=30, marker='s')
    ax2.set_ylim(0, 0.3)
    ax2.set_xticks(sigma_r)
    if i == 3: ax2.set_xlabel("σ", fontsize=fontlabelsize)
    if i == 0: ax2.set_title("GFT / Pre-trade Value", fontsize=fontlabelsize)
    ax2.tick_params(labelsize=fontlabelsize)

    # --- Decline % ---
    ax3 = axes[i, 2]
    ax3.plot(red_a_r, red_gft_r, linestyle='--', color='lightgray')
    ax3.plot(red_a_f, red_gft_f, linestyle='-', color='lightgray')
    ax3.scatter(red_a_r, red_gft_r, c=sigma_r, cmap=cmap, norm=norm, s=30, marker='o')
    ax3.scatter(red_a_f, red_gft_f, c=sigma_f, cmap=cmap, norm=norm, s=30, marker='s')
    ax3.set_xscale('symlog', linthresh=1)
    ax3.set_yscale('symlog', linthresh=1)
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 100)
    ax3.xaxis.set_major_formatter(formatter)
    ax3.yaxis.set_major_formatter(formatter)
    if i == 3: ax3.set_xlabel("% ↓ Agents", fontsize=fontlabelsize)
    if i == 0: ax3.set_title("% ↓ GFT", fontsize=fontlabelsize)
    ax3.tick_params(labelsize=fontlabelsize)

# --- Colorbar ---
cbar_ax = fig.add_axes([0.15, -0.05, 0.3, 0.03])
cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks(np.arange(1, 11))
cbar.set_label("Streamflow Complexity (σ)", fontsize=fontlabelsize)
cbar.ax.tick_params(labelsize=fontlabelsize)

# --- Legend for marker types ---
line_legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=6,
           label='Diversions random across watershed'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=6,
           label='Diversions random across upper reaches')
]

legend_ax = fig.add_axes([0.5, -0.06, 0.3, 0.03])
legend_ax.axis('off')
legend_ax.legend(
    handles=line_legend_elements,
    loc='center left',
    fontsize=fontlabelsize,
    frameon=True,
    ncol=1,
    title_fontsize=fontlabelsize
)

# --- Save ---
plt.savefig(f"{output_dir}/grid_proration_4x3.png", dpi=300, bbox_inches='tight')
plt.savefig(f"{output_dir}/grid_proration_4x3.svg", format='svg', dpi=1000, bbox_inches='tight')
plt.close()
