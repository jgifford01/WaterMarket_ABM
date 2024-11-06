import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Set Seaborn aesthetics
sns.set(style="whitegrid")
fontlabelsize = 10
linewidth = 1.5

# Define output directory for plots
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

# Data for each panel converted to fractions by dividing by 100
categories = ['10 to 0.1', 'U(0.1 to 10) mean', 'Profit max']
mean_values = {
    'GFT/no-drought value': [2.8 / 100, 2.7 / 100, 6.6 / 100],
    'GFT/pre-trade value': [12.0 / 100, 10.7 / 100, 20.7 / 100],
    'Fraction of agents trading': [13.5 / 100, 35.6 / 100, 44.3 / 100]
}
max_values = {
    'GFT/no-drought value': [5.1 / 100, 4.1 / 100, 10.0 / 100],
    'GFT/pre-trade value': [47.1 / 100, 79.0 / 100, 65.6 / 100],
    'Fraction of agents trading': [24.4 / 100, 53.1 / 100, 71.0 / 100]
}

# Color definitions with a lighter dark blue
colors = {
    '10 to 0.1': ('#CC444B', '#F28E8E'),  # Dark red and lighter red
    'U(0.1 to 10) mean': ('#1D5EA8', '#A3C4F3'),  # Adjusted dark blue and lighter blue
    'Profit max': ('#F6DB8C', '#FFF2CC')  # Dark yellow and lighter yellow
}

# Set up figure and axes
fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.8), constrained_layout=True)

# Titles for each subplot
subplot_titles = [
    "GFT over pre-trade value | δ=1",
    "GFT over pre-trade value | δ",
    "Fraction of agents trading"
]

# Plot each panel with consistent style
for i, (title, mean, max_val) in enumerate(zip(subplot_titles, mean_values.values(), max_values.values())):
    ax = axes[i]
    x = np.arange(len(categories))  # Label locations
    width = 0.35  # Width of bars
    
    # Plotting mean and max with specified colors and annotating values
    for j, cat in enumerate(categories):
        mean_color, max_color = colors[cat]
        
        # Plot mean bar
        mean_bar = ax.bar(x[j] - width/2, mean[j], width, color=mean_color, label="Mean" if j == 0 else "")
        # Plot max bar
        max_bar = ax.bar(x[j] + width/2, max_val[j], width, color=max_color, label="Max" if j == 0 else "")
        
        # Annotate mean and max values above the bars as fractions with two decimal places
        ax.annotate(f"{mean[j]:.2f}", xy=(x[j] - width/2, mean[j]), xytext=(0, -10), textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontlabelsize*0.7, color='black')
        ax.annotate(f"{max_val[j]:.2f}", xy=(x[j] + width/2, max_val[j]), xytext=(0, -10), textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontlabelsize*0.7, color='black')
    
    # Title, labels, and grid styling
    ax.set_title(title, fontsize=fontlabelsize)
    ax.set_xticks(x)
    ax.tick_params(axis='y', labelsize=fontlabelsize)
    ax.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    
    # Style spines to match appearance
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)

# Custom legend for categories
pref_10_01_mean_patch = mpatches.Patch(color='#CC444B', label='Mean 10 to 0.1')
pref_10_01_max_patch = mpatches.Patch(color='#F28E8E', label='Max 10 to 0.1')
U_01_10_mean_patch = mpatches.Patch(color='#1D5EA8', label='Mean U(0.1 to 10) mean')
U_01_10_max_patch = mpatches.Patch(color='#A3C4F3', label='Max U(0.1 to 10)')
Profit_max_mean_patch = mpatches.Patch(color='#F6DB8C', label='Mean profit max')
Profit_max_max_patch = mpatches.Patch(color='#FFF2CC', label='Max profit max')


# Shared legend at the bottom
fig.legend(handles=[pref_10_01_mean_patch, pref_10_01_max_patch, U_01_10_mean_patch, U_01_10_max_patch, Profit_max_mean_patch, Profit_max_max_patch],
           loc='lower center', ncol=3, frameon=False, fontsize=fontlabelsize, bbox_to_anchor=(0.5, -0.15))

# Save and display the figure with specified filenames
combined_plot_path = os.path.join(plots_dir, "3_panel_bars_nonpec_fraction.png")
plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
plt.savefig(f"{plots_dir}/3_panel_bars_nonpec_fraction.svg", format='svg', dpi=1000, bbox_inches='tight')
