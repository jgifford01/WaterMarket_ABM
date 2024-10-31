from mesa import  Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import cvxpy as cp
from agent import WaterAgent
import csv
from datetime import datetime
import os



class TradingModel(Model):
    def __init__(self, N, aw, alphaw, betaw, cbar0, gamma, P, stream_complexity,
                 upstream_selling, smart_market_ind, bilateral_market_ind, CPP_ind, random_seed, non_pec_prefs_ind, K_iter, GFT = 0):
        super().__init__()
        self.N = N
        self.aw = aw
        self.alphaw = alphaw
        self.betaw = betaw
        self.cbar0 = cbar0
        self.gamma = gamma
        self.P = P
        self.stream_complexity = stream_complexity
        self.upstream_selling = upstream_selling
        self.smart_market_ind = smart_market_ind
        self.bilateral_market_ind = bilateral_market_ind
        self.CPP_ind = CPP_ind
        self.GFT = GFT
        self.non_pec_prefs_ind = non_pec_prefs_ind
        self.K_iter = K_iter
        self.random_seed = random_seed
        self.create_agents()
        self.initialize_model()
        


    
    
    def create_agents(self):      
        self.schedule = RandomActivation(self)
        self.agents_list = []

        np.random.seed(self.random_seed)
        for i in range(1, self.N + 1):
            agent = WaterAgent.create_agent(i, self, self.aw, self.alphaw, 
                                            self.betaw, self.cbar0, self.stream_complexity)
            self.schedule.add(agent)
            self.agents_list.append(agent)
            
        ACbar = np.cumsum([agent.acbar for agent in self.schedule.agents])
        sigma_array = ACbar/ACbar[-1]
        
        
        
        for agent in self.schedule.agents:
            agent.sigma = sigma_array[agent.unique_id - 1]
            agent.pro = 1 if agent.sigma <= self.P else 0
            agent.c = agent.cbar*agent.pro
            
            # add non-pecuniary preferences if non_pec_prefs_ind is True
            if self.non_pec_prefs_ind == 2: #     0 => pmax, 1 => Uniform Random, 2 => Seniors prefer farming
                #### If seniors prefer farming relative to juniors ####
                pec_pref_array = np.linspace(10, 0.1, self.N) ## seniority in the code is ranked 1 most senior to N least senior

            elif self.non_pec_prefs_ind == 1:  
                
                #print("k: ", self.K_iter)
                # create a local random seed or each k iteration then go back to the original random seed
                rng_state = np.random.get_state()
                # RS as function of K_iter
                np.random.seed(self.random_seed + self.K_iter*10)
                pec_pref_array = np.random.uniform(0.1, 10, self.N)
                np.random.set_state(rng_state)
                
            
            elif self.non_pec_prefs_ind == 0:
                 ##### pmax #####
                pec_pref_array = np.ones(self.N)


            agent.non_pec_pref = pec_pref_array[agent.unique_id - 1]
             
            # add bidmax and askmax
            agent.wtp_wta_max = agent.cbar*(agent.alpha-agent.beta*agent.cbar)
            agent.bidmax = agent.wtp_wta_max*(1-self.gamma*(1-self.P))*agent.non_pec_pref # (1-self.P) is curtailment rate
            agent.askmax = agent.wtp_wta_max*(1+self.gamma*(1-self.P))*agent.non_pec_pref # if a seller has a 10x weighted ask, then the buyer has wants to be compensated 10x more than if they were pmax 
            agent.unitbidmax = agent.bidmax/agent.cbar 
            agent.unitaskmax = agent.askmax/agent.cbar


    def initialize_model(self):
        self.GFT = 0
        self.GFT_array = []
        self.catalog_of_buyers = [agent for agent in self.agents_list if agent.pro == 0]
        self.catalog_of_sellers = [agent for agent in self.agents_list if agent.pro == 1]
        self.datacollector = DataCollector(model_reporters={"GFT_array": lambda m: m.GFT_array})




        if self.smart_market_ind:
            self.catalog_of_buyers.sort(key=lambda agent: agent.unitbidmax, reverse=True)
            self.catalog_of_sellers.sort(key=lambda agent: agent.unitaskmax, reverse=False)
        
        if self.bilateral_market_ind:
            rng_state = np.random.get_state()
            # RS as function of K_iter
            np.random.seed(self.random_seed + self.K_iter*10)
            np.random.shuffle(self.catalog_of_buyers)
            np.random.shuffle(self.catalog_of_sellers)
            np.random.set_state(rng_state)

                                                     

    def reg_enviro(self, seller, buyer):
        # If buyer is upstream of seller, then trade is not restricted
        if len(buyer) > len(seller):
            #print("Trade is restricted: Buyer is upstream of seller")
            return False
        
        if len(buyer) <= len(seller):
            buyer_subvector = buyer[:-1]  # Adjusted to match seller's length minus 1
            seller_subvector = seller[:len(buyer)-1]

            if np.array_equal(buyer_subvector, seller_subvector):
                if buyer[-1] > seller[-1]:
                    #print("Trade is restricted: Buyer is upstream of seller")
                    return False
                else:
                    #print("Trade is not restricted")
                    return True
            else:
                #print("Trade is restricted: Buyer is upstream of seller")
                return False

    ##################################################################################################################################
    ##################################################################################################################################
    ####### Bilateral and Smart Market ###############################################################################################
    ##################################################################################################################################
    ##################################################################################################################################


    def trade_sequence(self):


        # write all agent data to CSV
        if self.smart_market_ind == True:
            if self.P == 0.1:
                with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/agent_data_SM_P0.1.csv", mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['agent_id', 'c', 'alpha', 'beta', 'acbar', 'sigma', 'pro', 'cbar', 'wtp_wta_max'])
                    for agent in self.schedule.agents:
                        writer.writerow([agent.unique_id, agent.c, agent.alpha, agent.beta, agent.acbar, agent.sigma, agent.pro, agent.cbar, agent.wtp_wta_max])


   
        # create cumulative water value data pretrade #
        if self.smart_market_ind == True:
                #print("TV0: ", TV0, "P: ", self.P)
                TV0 = np.sum([agent.c * (agent.alpha - agent.beta * agent.c) for agent in self.schedule.agents])
                # Open the CSV file in append mode
                with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/watervalue.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Check if the file is empty to write headers only once
                    if file.tell() == 0:  # If the file is empty, write the headers
                        writer.writerow(['P', 'TV0'])
                    
                    # Write the P and TV0 values to the CSV file
                    writer.writerow([self.P, TV0])
 
        

        # End trading if buyer or seller list is empty
        if not self.catalog_of_buyers or not self.catalog_of_sellers:
            self.GFT = 0
            return

        # Total value before trading
        TV0 = np.sum([agent.c * (agent.alpha - agent.beta * agent.c) for agent in self.schedule.agents])
        # initial allocation vector
        c_init = np.array([agent.c for agent in self.schedule.agents])

        # initial price collection array P by N
        price_collection_array = []

        for j in range(len(self.catalog_of_buyers)):
            buyer = self.catalog_of_buyers[j]
            for s in range(len(self.catalog_of_sellers)):
                seller = self.catalog_of_sellers[s]

                if seller.c == 0: # early exit if seller has no water for code efficiency
                    continue

                # check reg enviro conditions
                if self.upstream_selling == False:
                    if self.reg_enviro(seller.trib_vector, buyer.trib_vector) == False:
                        continue
                    
                  

                x = min(seller.c, buyer.cbar - buyer.c)

                avBr_1 = buyer.alpha - buyer.beta * buyer.c
                avBr = buyer.alpha - buyer.beta * (buyer.c + x)
                wtp = avBr_1 + avBr - buyer.alpha # per unit wtp
                bid = wtp * (1 - self.gamma*(1-self.P))* buyer.non_pec_pref 
                # (1-self.P) is curtailment rate
                
                
                avSr_1 = seller.alpha - seller.beta * seller.c
                avSr = seller.alpha - seller.beta * (seller.c - x)
                wta = avSr_1 + avSr - seller.alpha # per unit wta
                ask = wta * (1 + self.gamma*(1-self.P)) * seller.non_pec_pref
                # (1-self.P)is curtailment rate

                
                if bid > ask:
                    buyer.c += x
                    seller.c -= x
                    
                    if x > 0:
                        price = ((bid + ask) / 2) #### price  of one unit transferred
                        #print("price: ", price)
                        price_collection_array.append(price)

                else:
                    continue

        # Total value after trading
        TV1 = np.sum([agent.c * (agent.alpha - agent.beta * agent.c) for agent in self.schedule.agents])
        # compute GFT
        self.GFT = TV1 - TV0
        
        # if array is not empty
        if price_collection_array != []:
            #compute price stats
            mean_price = np.mean(price_collection_array)
            min_price = np.min(price_collection_array)
            max_price = np.max(price_collection_array)
            percentile_25_price = np.percentile(price_collection_array, 25)
            percentile_75_price = np.percentile(price_collection_array, 75)
        else: 
            mean_price = min_price = max_price = percentile_25_price = percentile_75_price = np.nan


        #### count how many agents are trading of N by counting how many c values changed from initial allocation to final ####
        # final allocation vector
        c_final = np.array([agent.c for agent in self.schedule.agents])
        # count how many agents are trading
        num_trading_agents = np.sum(c_init != c_final)

        # Ensure the directory exists
        output_dir = f"data/{self.N}agents_seed{self.random_seed}"
        os.makedirs(output_dir, exist_ok=True)

        # create smart market num agents array csv
        if self.smart_market_ind == True:
            # save P and num trading agents to csv
            with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_SM.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                # Check if the file is empty to write headers only once
                if file.tell() == 0:  # If the file is empty, write the headers
                    writer.writerow(['P', 'num_trading_agents_SM'])
                # Write the P and num trading agents values to the CSV file
                writer.writerow([self.P, num_trading_agents])
            
            # save prices mean, min, max and p to csv
            with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/price_collection_array_SM.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # If the file is empty, write the headers
                    writer.writerow(['P', 'mean_price', 'min_price', 'max_price', '25th_percentile_price', '75th_percentile_price'])
                writer.writerow([self.P, mean_price, min_price, max_price, percentile_25_price, percentile_75_price])
        
        # creat number agents trading array
        if self.bilateral_market_ind == True:
            file_exists = os.path.isfile(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_BI.csv")
            is_empty = os.path.getsize(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_BI.csv") == 0 if file_exists else True

            with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_BI.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                # Check if the file is empty to write headers only once
                if file.tell() == 0:  # If the file is empty, write the headers
                    writer.writerow(['P', 'num_trading_agents_BM'])
                writer.writerow([self.P, num_trading_agents])
            

            # save prices mean, min, max and p to csv
            with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/price_collection_array_BI.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                # Check if the file is empty to write headers only once
                if file.tell() == 0:
                    writer.writerow(['P', 'mean_price', 'min_price', 'max_price', '25th_percentile_price', '75th_percentile_price'])
                writer.writerow([self.P, mean_price, min_price, max_price, percentile_25_price, percentile_75_price])
                    
    ##################################################################################################################################
    ##################################################################################################################################
    ####### CENTRAL PLANNER PROBLEM ##################################################################################################
    ##################################################################################################################################
    ##################################################################################################################################
        
        
    def central_planner_problem(self):
        agent_array = np.array([[agent.alpha , agent.c, agent.beta, agent.acreage, agent.cbar] 
                                for agent in self.schedule.agents])
        c_init = agent_array[:,1]
        beta_array = agent_array[:,2]
        alpha_array = agent_array[:,0]
        initial_value = (alpha_array * (c_init) - beta_array * (c_init**2))
        # create list of trib vectors
        trib_vector_list = [agent.trib_vector for agent in self.schedule.agents]
        # create elig matrix based on reg environment from agent i (seller) to agent j (buyer) 
        # make sure the elig matrix is correct corresponding to the reg enviro
        elig_matrix = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                elig_matrix[i,j] = self.reg_enviro(trib_vector_list[i], trib_vector_list[j])
        # eligibility matrix is all ones if no restrictions
        if self.upstream_selling == True:
            elig_matrix = np.ones((self.N, self.N))
        c_opt = cp.Variable(self.N)
        x = cp.Variable((self.N, self.N), nonneg=True)  # Transfer matrix
        Cs = np.sum(c_init) # Total resource constraint
        # Define the objective function
        objective = cp.Maximize(alpha_array.T @ c_opt - beta_array.T @ cp.square(c_opt))
        # Constraints
        constraints = [cp.sum(c_opt) == Cs] 

        if self.upstream_selling == False:
            constraints.append(c_opt == cp.sum(cp.multiply(x,elig_matrix), axis = 0) - 
                               cp.sum(cp.multiply(x,elig_matrix), axis = 1) + c_init)
        
        constraints.append(c_opt >= 0)
        # Define and solve the problem
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.OSQP, verbose= False)
        c_opt_value = c_opt.value  # numpy array of optimal values
        # compute GFT
        value_after_trade = (alpha_array * c_opt_value - beta_array * (c_opt_value**2))
        gains_from_trade = value_after_trade - initial_value
        tot_gft = np.sum(gains_from_trade)
        self.GFT = tot_gft
        
        epsilon = 1e-4  # Define your epsilon tolerance

        #Count how many agents are trading using an epsilon tolerance
        num_trading_agents = np.sum(np.abs(c_init - c_opt_value) > epsilon)


        file_exists = os.path.isfile(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_CPP.csv")
        is_empty = os.path.getsize(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_CPP.csv") == 0 if file_exists else True

        with open(f"data/{self.N}agents_seed{self.random_seed}_U01_10/num_trading_agents_CPP.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            # Check if the file is empty to write headers only once
            if is_empty:  # If the file is empty, write the headers
                writer.writerow(['P', 'num_trading_agents_CPP'])
            # Write the P and num trading agents values to the CSV file if a value already exists for that P, then create new column
            writer.writerow([self.P, num_trading_agents])
    

    
        return 




    def step(self):
        # Schedule step function for all agents
        if self.smart_market_ind == True:
            self.trade_sequence()
        
        elif self.bilateral_market_ind == True:
            self.trade_sequence()

        elif self.CPP_ind == True:
            self.central_planner_problem()

        self.schedule.step()
        self.datacollector.collect(self)
