#### Summary Stats ####

# Importing the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
########### Table 3: Pmax Summary Statistics #################

# pmax data
GFT_pmax_data = pd.read_csv('fig_data/500agents_seed3145_pmax/GFT_final_mean_array.csv')
pretrade_water_value_pmax = pd.read_csv('fig_data/500agents_seed3145_pmax/watervalue.csv').sort_values(by='P')

GFT_pmax_df = pd.DataFrame(GFT_pmax_data)
pretrade_water_value_pmax_df = pd.DataFrame(pretrade_water_value_pmax).sort_values(by='P')

# append the pre-trade water value to the GFT data
GFT_pmax_df['TV0'] = pretrade_water_value_pmax_df['TV0'].values
print(GFT_pmax_df)

# divide Central Planning Mean  Smart Market Mean   Bilateral Market Mean  columns    by      TV0 column create new columns
GFT_pmax_df['Central Planning Mean/TV0'] = GFT_pmax_df['Central Planning Mean'] / GFT_pmax_df['TV0']
GFT_pmax_df['Smart Market Mean/TV0'] = GFT_pmax_df['Smart Market Mean'] / GFT_pmax_df['TV0']
GFT_pmax_df['Bilateral Market Mean/TV0'] = GFT_pmax_df['Bilateral Market Mean'] / GFT_pmax_df['TV0']

# divide Central Planning Mean  Smart Market Mean   Bilateral Market Mean  columns    by TV0 at P=1 create new columns
GFT_pmax_df['Central Planning Mean/TV0 at P=1'] = GFT_pmax_df['Central Planning Mean'] / GFT_pmax_df['TV0'][-1]








