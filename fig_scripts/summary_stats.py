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

# remove inf, and NAN
GFT_pmax_df = GFT_pmax_df.replace([np.inf, -np.inf], np.nan)
print(GFT_pmax_df)

# divide Central Planning Mean  Smart Market Mean   Bilateral Market Mean  columns    by TV0 at P=1 create new columns
GFT_pmax_df['TV0_p=1'] = GFT_pmax_df['TV0'].iloc[-1]
print(GFT_pmax_df)
# divide Central Planning Mean  Smart Market Mean   Bilateral Market Mean  columns    by      TV0 column create new columns
GFT_pmax_df['Central Planning Mean/TV0_p=1'] = GFT_pmax_df['Central Planning Mean'] / GFT_pmax_df['TV0_p=1']
GFT_pmax_df['Smart Market Mean/TV0_p=1'] = GFT_pmax_df['Smart Market Mean'] / GFT_pmax_df['TV0_p=1']
GFT_pmax_df['Bilateral Market Mean/TV0_p=1'] = GFT_pmax_df['Bilateral Market Mean'] / GFT_pmax_df['TV0_p=1']

print(GFT_pmax_df)

# summary statistics mean and max
GFT_pmax_summary_stats = GFT_pmax_df.describe().loc[['mean', 'max']]
# set to print full display
pd.set_option('display.max_columns', None)
print(GFT_pmax_summary_stats.transpose())

# export to csv
GFT_pmax_summary_stats.to_csv('fig_data/500agents_seed3145_pmax/GFT_pmax_summary_stats.csv')

### agents trading data
agents_trading_SM_pmax = pd.read_csv('fig_data/500agents_seed3145_pmax/num_trading_agents_SM.csv')
agents_trading_BL_pmax = pd.read_csv('fig_data/500agents_seed3145_pmax/num_trading_agents_BI.csv')
agents_trading_CPP_pmax = pd.read_csv('fig_data/500agents_seed3145_pmax/num_trading_agents_CPP.csv')


# pivot find mean of bi trading agents by p
pct_agents_trading_BL_pmax = agents_trading_BL_pmax.pivot_table(index='P', aggfunc='mean')/500
pct_agents_trading_SM_pmax = agents_trading_SM_pmax.pivot_table(index='P', aggfunc='mean')/500
pct_agents_trading_CPP_pmax = agents_trading_CPP_pmax.pivot_table(index='P', aggfunc='mean')/500

# combine into one dataframe
pct_agents_trading_pmax = pd.concat([pct_agents_trading_BL_pmax, pct_agents_trading_SM_pmax, pct_agents_trading_CPP_pmax], axis=1)
pct_agents_trading_pmax.columns = [ 'Smart Market', 'Bilateral Market Mean','Central Planning']

print(pct_agents_trading_pmax)

# compute mean and max stats
pct_agents_trading_pmax_summary_stats = pct_agents_trading_pmax.describe().loc[['mean', 'max']]
print(pct_agents_trading_pmax_summary_stats.transpose())



########### Table 4 non-pec preferences smart market Summary Statistics #################

GFT_SM_10_01_nonpec_data = pd.read_csv('fig_data/500agents_seed3145_10_01_nonpec/GFT_final_mean_array.csv')['Smart Market Mean']
GFT_SM_pmax_data = pd.read_csv('fig_data/500agents_seed3145_pmax/GFT_final_mean_array.csv')['Smart Market Mean']
GFT_SM_U01_10_data = pd.read_csv('fig_data/500agents_seed3145_U01_10/GFT_SM_mean_min_max_U_01_10.csv')['Smart Market Mean']
print(GFT_SM_10_01_nonpec_data)
print(GFT_SM_pmax_data)
print(GFT_SM_U01_10_data)

TVO_nonpec = pretrade_water_value_pmax_df['TV0'].values

# combine into DF
GFT_SM_nonpec_df = pd.DataFrame(GFT_SM_10_01_nonpec_data)
GFT_SM_nonpec_df['GFT_SM_pmax_data'] = GFT_SM_pmax_data
GFT_SM_nonpec_df['GFT_SM_U01_10_data'] = GFT_SM_U01_10_data
GFT_SM_nonpec_df['TV0'] = TVO_nonpec
GFT_SM_nonpec_df = GFT_SM_nonpec_df.rename(columns={'Smart Market Mean': 'GFT_SM_10_01_nonpec_data'})

print(GFT_SM_nonpec_df.head())

# GFT/TV0(P=1)
GFT_SM_nonpec_df['TV0_p=1'] = GFT_SM_nonpec_df['TV0'].iloc[-1]
GFT_SM_nonpec_df['GFT_SM_10_01_nonpec_data/TV0_p=1'] = GFT_SM_nonpec_df['GFT_SM_10_01_nonpec_data'] / GFT_SM_nonpec_df['TV0_p=1']
GFT_SM_nonpec_df['GFT_SM_U01_10_data/TV0_p=1'] = GFT_SM_nonpec_df['GFT_SM_U01_10_data'] / GFT_SM_nonpec_df['TV0_p=1']
GFT_SM_nonpec_df['GFT_SM_pmax_data/TV0_p=1'] = GFT_SM_nonpec_df['GFT_SM_pmax_data'] / GFT_SM_nonpec_df['TV0_p=1']


print(GFT_SM_nonpec_df.head())

# summary statistics mean and max
GFT_SM_nonpec_summary_stats = GFT_SM_nonpec_df.describe().loc[['mean', 'max']]

print(GFT_SM_nonpec_summary_stats.transpose())


# GFT/TV0
GFT_SM_nonpec_df['GFT_SM_10_01_nonpec_data/TV0'] = GFT_SM_nonpec_df['GFT_SM_10_01_nonpec_data'] / GFT_SM_nonpec_df['TV0']   
GFT_SM_nonpec_df['GFT_SM_U01_10_data/TV0'] = GFT_SM_nonpec_df['GFT_SM_U01_10_data'] / GFT_SM_nonpec_df['TV0']
GFT_SM_nonpec_df['GFT_SM_pmax_data/TV0'] = GFT_SM_nonpec_df['GFT_SM_pmax_data'] / GFT_SM_nonpec_df['TV0']

# remove inf as na
GFT_SM_nonpec_df = GFT_SM_nonpec_df.replace([np.inf, -np.inf], np.nan)
print(GFT_SM_nonpec_df)

# summary statistics mean and max
GFT_SM_nonpec_summary_stats = GFT_SM_nonpec_df.describe().loc[['mean', 'max']]
print(GFT_SM_nonpec_summary_stats.transpose())


# number of agents trading
agents_trading_SM_10_01_nonpec = pd.read_csv('fig_data/500agents_seed3145_10_01_nonpec/num_trading_agents_SM.csv')
agents_trading_SM_pmax = pd.read_csv('fig_data/500agents_seed3145_pmax/num_trading_agents_SM.csv')
agents_trading_SM_U01_10 = pd.read_csv('fig_data/500agents_seed3145_U01_10/num_trading_agents_SM.csv')

# pivot find mean of bi trading agents by p
pct_agents_trading_SM_10_01_nonpec = agents_trading_SM_10_01_nonpec.pivot_table(index='P', aggfunc='mean')/500

