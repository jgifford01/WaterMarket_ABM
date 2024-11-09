#################################################
################## Libraries ###################
#################################################
from model import TradingModel
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import statsmodels.api as sm
import os
import csv

#################################################
################## Parameters ###################
#################################################


K = 100 # Number of iterations for each P: 100 as presented in paper
N = 500 # Number of agents: 500 as presented in paper
sigma = 4 # stream complexity or watershed max dimension
gamma = 0 # 0 as presented in paper
aw = 1 # we are currently setting acreage to one (non random)
random_seed =  3145 #  3145 for N=500 K=100 
non_pec_prefs_ind = 2 #####  0 => pmax, 1 => Uniform Random, 2 => Seniors prefer farming (10.0 to 0.1)
cores_num = 40 # Number of cores to use for parallel processing/single threading

# x x x x x x x x x x x x x x x x x x x x x x x x
# x x x x x x x x x x x x x x x x x x x x x x x x
# Don't touch these values 
alphaw = 1 
stream_complexity = sigma - 1 # stochastic component of stream complexity
betaw = 1 
cbar0 = 1 
GFT_final_array = np.full((3, 101, K), np.nan) # Array for storing the gains from trade results, initialized with NaN
# x x x x x x x x x x x x x x x x x x x x x x x x 
# x x x x x x x x x x x x x x x x x x x x x x x x

# The functions for parallel processing should be defined outside the main block
def bilateral_trade_simulation(i, k):
    P = i / 100
    model3 = TradingModel(N=N, aw=aw, alphaw=alphaw, betaw=betaw, cbar0=cbar0, gamma=gamma,
                          P=P, stream_complexity=stream_complexity, upstream_selling=False,
                          smart_market_ind=False, bilateral_market_ind=True, 
                          CPP_ind=False, random_seed=random_seed, non_pec_prefs_ind=non_pec_prefs_ind) 
    model3.trade_sequence()
    return i, k, model3.GFT

def cpp_and_sm_simulation(i):
    P = i / 100
    # Central Planning Model
    model1 = TradingModel(N=N, aw=aw, alphaw=alphaw, betaw=betaw, cbar0=cbar0, gamma=gamma,
                            P=P, stream_complexity=stream_complexity, upstream_selling=False,
                            smart_market_ind=False, bilateral_market_ind=False, 
                            CPP_ind=True, random_seed=random_seed, non_pec_prefs_ind=non_pec_prefs_ind) 
    model1.central_planner_problem()
    GFT_cpp = model1.GFT


    # Smart Market Model
    model2 = TradingModel(N=N, aw=aw, alphaw=alphaw, betaw=betaw, cbar0=cbar0, gamma=gamma,
                            P=P, stream_complexity=stream_complexity, upstream_selling=False,
                            smart_market_ind=True, bilateral_market_ind=False, 
                            CPP_ind=False, random_seed=random_seed, non_pec_prefs_ind=non_pec_prefs_ind)
    model2.trade_sequence()
    GFT_sm = model2.GFT

    return i, GFT_cpp, GFT_sm


# Main program execution
if __name__ == '__main__':
    # Timing the parallel version
    start_time = time.time()
    # check max number of cores
    num_cores = cores_num #os.cpu_count()
    print("running on num cores =", num_cores)

    ################ Parallel Bilateral Market Loop #################
    with ProcessPoolExecutor(max_workers=num_cores) as executor:  # You can set max_workers to the number of cores
        futures = [executor.submit(bilateral_trade_simulation, i, k) for k in range(K) for i in range(101)]
        
        for future in as_completed(futures):
            i, k, GFT = future.result()
            GFT_final_array[2, i, k] = GFT
        
        print(f"Finished bilateral market simulations")

    ################ Parallel CPP and SM Loop #####################
    with ProcessPoolExecutor(max_workers=num_cores) as executor:  # You can set max_workers to the number of cores
        futures = [executor.submit(cpp_and_sm_simulation, i) for i in range(101)]
        
        for future in as_completed(futures):
            i, GFT_cpp, GFT_sm = future.result()
            GFT_final_array[0, i, 0] = GFT_cpp
            GFT_final_array[1, i, 0] = GFT_sm
        
        print(f"Finished CPP and SM simulations")

    # Timing the end
    end_time = time.time()

    # Print the total time taken
    print(f"Parallel version took {end_time - start_time:.2f} seconds.")



    # Take mean across K runs, ignoring NaN values
    GFT_final_mean_array_k = np.nanmean(GFT_final_array, axis=2)

    # Take range across K runs, ignoring NaN values
    GFT_range_arraymin = np.nanmin(GFT_final_array, axis =2)  # Min of Bilateral Market
    GFT_range_arraymax = np.nanmax(GFT_final_array, axis =2)  # Max of Bilateral Market

    # Selecting the Bilateral Market row
    GFT_bi_range_arraymin = GFT_range_arraymin[2, :]  # Selecting the Bilateral Market row
    GFT_bi_range_arraymax = GFT_range_arraymax[2, :]  # Selecting the Bilateral Market row
  

    # Save GFT final mean array to a csv file with labels
    with open(f'data/{N}agents_seed{random_seed}/GFT_final_mean_array.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Central Planning Mean", "Smart Market Mean ", "Bilateral Market Mean"])
        writer.writerows(GFT_final_mean_array_k.T)   
        
    # Save GFT range array to a csv file with labels
    with open(f'data/{N}agents_seed{random_seed}/BI_range_array.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bilateral Market Min", "Bilateral Market Max"])
        writer.writerows(np.column_stack((GFT_bi_range_arraymin, GFT_bi_range_arraymax)))
    


