#################################################
################## Libraries ###################
#################################################
from model_SM_uniform_random import TradingModel
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import statsmodels.api as sm
import os
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed

#################################################
################## Parameters ###################
#################################################


K = 100  # Number of iterations for each P: 100 as presented in paper
N = 500  # Number of agents: 500 as presented in paper
sigma_complexity = 4  # stream complexity or watershed max dimension

gamma = 0  # 0 as presented in paper
aw = 1  # we are currently setting acreage to one (non random)

random_seed = 3145  # 3145 for N=500 K=100
cores = 40  # Number of CPU cores to use
non_pec_prefs_ind = 1  # 1 => Uniform Random don't touch this value



# x x x x x x x x x x x x x x x x x x x x x x x x
# x x x x x x x x x x x x x x x x x x x x x x x x
# Don't touch these values 
alphaw = 1 
betaw = 1 
cbar0 = 1 
stream_complexity = sigma_complexity - 1  # stochastic component of stream complexity
GFT_final_array = np.full((101, K), np.nan) # Array for storing the gains from trade results, initialized with NaN
# x x x x x x x x x x x x x x x x x x x x x x x x 
# x x x x x x x x x x x x x x x x x x x x x x x x

# Create folder for data
if not os.path.exists(f'data/{N}agents_seed{random_seed}_U01_10'):
    os.makedirs(f'data/{N}agents_seed{random_seed}_U01_10')


def sm_simulation(i, k):
    P = i / 100

    # Smart Market Model
    model2 = TradingModel(N=N, aw=aw, alphaw=alphaw, betaw=betaw, cbar0=cbar0, gamma=gamma,
                          P=P, stream_complexity=stream_complexity, upstream_selling=False,
                          smart_market_ind=True, bilateral_market_ind=False, 
                          CPP_ind=False, random_seed=random_seed, non_pec_prefs_ind=non_pec_prefs_ind, K_iter=k)
    model2.trade_sequence()
    GFT_sm = model2.GFT

    return i, k, GFT_sm


# Main program execution inside the '__main__' block
if __name__ == '__main__':
    # Timing the parallel version
    start_time = time.time()
    
    # Number of CPU cores to use
    num_cores = cores  # Adjust as needed or set dynamically with os.cpu_count()
    print("Running on num cores =", num_cores)

    # Launch parallel tasks
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(sm_simulation, i, k) for i in range(101) for k in range(K)]
        
        for future in as_completed(futures):
            i, k, GFT_sm = future.result()
            GFT_final_array[i, k] = GFT_sm

    print("Finished SM simulations")

    # Timing the end
    end_time = time.time()

    # Print the total time taken
    print(f"Parallel version took {end_time - start_time:.2f} seconds.")

    print("GFT_final_array", GFT_final_array)

    # Take mean across K runs, ignoring NaN values
    GFT_final_mean_array_k = np.nanmean(GFT_final_array, axis=1)

    GFT_range_arraymin = np.nanmin(GFT_final_array, axis=1)  # Min of Smart Market
    GFT_range_arraymax = np.nanmax(GFT_final_array, axis=1)  # Max of Smart Market

    # Save GFT mean, min, and max
    with open(f'data/{N}agents_seed{random_seed}_U01_10/GFT_SM_mean_min_max_U_01_10.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Smart Market Mean", "Smart Market Min", "Smart Market Max"])
        writer.writerows(np.column_stack((GFT_final_mean_array_k[1:], GFT_range_arraymin[1:], GFT_range_arraymax[1:])))
