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
    'GFT/no-drought value': [0.03, 0.03, 0.07],
    'GFT/pre-trade value': [0.13, 0.11, 0.22],
    'Fraction of agents trading': [0.15, 0.37, 0.48]
}
max_values = {
    'GFT/no-drought value': [0.06, 0.05, 0.11],
    'GFT/pre-trade value': [0.75, 0.67, 0.65],
    'Fraction of agents trading': [0.28, 0.58, 0.77]
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
pref_10_01_mean_patch = mpatches.Patch(color='#CC444B', label='Mean sen.-based prefs')
pref_10_01_max_patch = mpatches.Patch(color='#F28E8E', label='Max sen.-based prefs')
U_01_10_mean_patch = mpatches.Patch(color='#1D5EA8', label='Mean random prefs')
U_01_10_max_patch = mpatches.Patch(color='#A3C4F3', label='Max random prefs')
Profit_max_mean_patch = mpatches.Patch(color='#F6DB8C', label='Mean profit max')
Profit_max_max_patch = mpatches.Patch(color='#FFF2CC', label='Max profit max')


# Shared legend at the bottom
fig.legend(handles=[pref_10_01_mean_patch, pref_10_01_max_patch, U_01_10_mean_patch, U_01_10_max_patch, Profit_max_mean_patch, Profit_max_max_patch],
           loc='lower center', ncol=3, frameon=False, fontsize=fontlabelsize, bbox_to_anchor=(0.5, -0.15))

# Save and display the figure with specified filenames
combined_plot_path = os.path.join(plots_dir, "3_panel_bars_nonpec_fraction.png")
plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
plt.savefig(f"{plots_dir}/3_panel_bars_nonpec_fraction.svg", format='svg', dpi=1000, bbox_inches='tight')
