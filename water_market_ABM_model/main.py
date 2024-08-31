from model import TradingModel
import numpy as np
import matplotlib.pyplot as plt

K = 1
N= 10
stream_complexity = 2

GFT_final_array = np.zeros((4,101,K))
for k in range(K):
    random_seed = np.random.randint(0,1000)


#### We can do a batch run here
    
    for i in range(100):
        P = i/100
        # Central Planning 

        model1 = TradingModel(N=N, aw=2, alphaw=10, betaw=2, cbar0=1, gamma= 0,
                            P=P, stream_complexity=stream_complexity, upstream_selling=False,
                            smart_market_ind=False, bilateral_market_ind=False, 
                            CPP_ind=True, random_seed=random_seed)
        # CPP without streamflow restrictions
        model4 = TradingModel(N=N, aw=2, alphaw=10, betaw=2, cbar0=1, gamma= 0,
                            P=P, stream_complexity=stream_complexity, upstream_selling=True,
                            smart_market_ind=False, bilateral_market_ind=False, 
                            CPP_ind=True, random_seed=random_seed)
        
        # SMART MARKET
        model2 = TradingModel(N=N, aw=2, alphaw=10, betaw=2, cbar0=1, gamma= 0,
                            P=P, stream_complexity=stream_complexity, upstream_selling=False,
                            smart_market_ind=True, bilateral_market_ind=False, 
                            CPP_ind=False, random_seed=random_seed)
       

        # Bilateral Market
        model3 = TradingModel(N=N, aw=2, alphaw=10, betaw=2, cbar0=1, gamma= 0,
                            P=P, stream_complexity=stream_complexity, upstream_selling=False,
                            smart_market_ind=False, bilateral_market_ind=True, 
                            CPP_ind=False, random_seed=random_seed)
        
        

        # Run central planner problem
        model1.central_planner_problem()
        GFT_final_array[0,i,k] = model1.GFT
        #print("Gains from Trade CPP:", model1.GFT)
        
        # Run SMART MARKET
        model2.trade_sequence()
        GFT_final_array[1,i,k] = model2.GFT
        #print("Gains from Trade SM:", model2.GFT)
        
        # Run Bilateral Market 
        model3.trade_sequence()
        GFT_final_array[2,i,k] = model3.GFT
        #print("Gains from Trade BM:", model3.GFT)

        # Run central planner problem without streamflow restrictions
        model4.central_planner_problem()
        GFT_final_array[3,i,k] = model4.GFT


        
    print(f"Finished {k+1} iterations")


# plotting 

GFT_final_mean_array_k = np.mean(GFT_final_array,axis=2)
GFT_se_array = np.std(GFT_final_array, axis=2)/np.sqrt(K)

PP_reversed = 1 * np.arange(100, -1, -1).reshape(100+1, 1)
fig, ax1 = plt.subplots(figsize=(6, 4))  # Adjust figsize as needed
ax1.plot (PP_reversed, GFT_final_mean_array_k[0,:], label = "Central Planning")
ax1.plot (PP_reversed, GFT_final_mean_array_k[1,:], label = "Smart Market")
ax1.plot (PP_reversed, GFT_final_mean_array_k[2,:], label = "Bilateral Market")
ax1.plot (PP_reversed, GFT_final_mean_array_k[3,:], label = "Central Planning without streamflow restrictions")


# plot SE
for i in range(4):
    ax1.fill_between(PP_reversed.flatten(), GFT_final_mean_array_k[i,:] - GFT_se_array[i,:], GFT_final_mean_array_k[i,:] + GFT_se_array[i,:], alpha=0.2)

ax1.set_xlabel("Curtailment percent")
ax1.set_ylabel("Gains from Trade", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_ylim(0, )
print("check 1")
ax2 = ax1.twiny()
ax2.set_xlim(0, 100)
ax2.set_xlabel("Proration percent")
ax2.set_xticks(np.linspace(0, 100, num=11))  
ax2.set_xticklabels([f"{100-x:.0f}%" for x in ax2.get_xticks()], rotation=0, ha='right', va='bottom', fontsize=8)  
print("check 2")
ax1.set_xlim(0, 100)  # Set x-axis limits from 0 to 100
ax1.set_xticks(np.linspace(0, 100, num=11))  
ax1.set_xticklabels([f"{x:.0f}%" for x in ax1.get_xticks()], rotation=0, ha='left', va='center', fontsize=8)  
ax1.legend(loc='upper left', frameon=False)
plt.title("Gains from Trade")
plt.tight_layout()
plt.show()



