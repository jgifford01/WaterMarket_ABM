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

# Data for each panel (converted to fractions)
categories = ['Smart Market', 'Bilateral Mean', 'Full Information']
mean_values = {
    'GFT/no-drought water value': [6.6/100, 4.3/100, 16.6/100],
    'GFT/available water value': [20.7/100, 12.6/100, 52.2/100],
    'Fraction of agents trading': [47.8/100, 44.3/100, 95.6/100]
}
max_values = {
    'GFT/no-drought water value': [10.0/100, 6.9/100, 24.5/100],
    'GFT/available water value': [65.6/100, 30.2/100, 134.9/100],
    'Fraction of agents trading': [75.6/100, 71.0/100, 100.0/100]
}

# Define colors for each category
colors = {
    'Smart Market': ('#F6DB8C', '#FFF2CC'),  # Light yellow and slightly darker yellow
    'Bilateral Mean': ('#8CD8C0', '#E6F6F1'),  # Light green and lighter green
    'Full Information': ('gray', '#D3D3D3')  # Darker blue and lighter blue for distinction
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
        
        # Annotate mean and max values above the bars in fraction format
        ax.annotate(f"{mean[j]:.2f}", xy=(x[j] - width/2, mean[j]), xytext=(0, -10), textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontlabelsize*0.7, color='black')
        ax.annotate(f"{max_val[j]:.2f}", xy=(x[j] + width/2, max_val[j]), xytext=(0, -10), textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontlabelsize*0.7, color='black')
        
    # Title, labels, and grid styling
    ax.set_title(title, fontsize=fontlabelsize)
    ax.set_xticks(x)
    #if i == 0:
        #ax.set_ylabel('Fraction', fontsize=fontlabelsize)
    ax.tick_params(axis='y', labelsize=fontlabelsize)
    ax.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    
    # Style spines to match appearance
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)

# Custom legend for categories
smart_market_mean_patch = mpatches.Patch(color='#F6DB8C', label='Mean smart market')
bilateral_mean_mean_patch = mpatches.Patch(color='#8CD8C0', label='Mean bilateral mean')
full_information_mean_patch = mpatches.Patch(color='gray', label='Mean full Information')
smart_market_max_patch = mpatches.Patch(color='#FFF2CC', label='Max smart market')
bilateral_mean_max_patch = mpatches.Patch(color='#E6F6F1', label='Max bilateral mean')
full_information_max_patch = mpatches.Patch(color='#D3D3D3', label='Max full Information')

# Shared legend at the bottom
fig.legend(handles=[smart_market_mean_patch, smart_market_max_patch, bilateral_mean_mean_patch, bilateral_mean_max_patch, full_information_mean_patch, full_information_max_patch],
           loc='lower center', ncol=3, frameon=False, fontsize=fontlabelsize, bbox_to_anchor=(0.5, -0.15))

# Save and display the figure with specified filenames
combined_plot_path = os.path.join(plots_dir, "3_panel_bars_fractions.png")
plt.savefig(combined_plot_path, dpi=300, bbox_inches='tight')
plt.savefig(f"{plots_dir}/3_panel_bars_fractions.svg", format='svg', dpi=1000, bbox_inches='tight')
