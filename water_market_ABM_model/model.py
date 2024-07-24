from mesa import  Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import cvxpy as cp
from agent import WaterAgent
from scipy.optimize import minimize

class TradingModel(Model):
    def __init__(self, N, aw, alphaw, betaw, cbar0, gamma, P, stream_complexity,
                 upstream_selling, smart_market_ind, bilateral_market_ind, CPP_ind, random_seed, GFT = 0):
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
        
    def initialize_model(self):
        self.GFT = 0
        self.GFT_array = []
        self.catalog_of_buyers = [agent for agent in self.agents_list if agent.pro == 0]
        self.catalog_of_sellers = [agent for agent in self.agents_list if agent.pro == 1]
        self.datacollector = DataCollector(model_reporters={"GFT_array": lambda m: m.GFT_array})

        if self.smart_market_ind:
            self.catalog_of_buyers.sort(key=lambda agent: agent.avbar, reverse=True)
            self.catalog_of_sellers.sort(key=lambda agent: agent.avbar, reverse=False)

        if self.bilateral_market_ind:
            np.random.shuffle(self.catalog_of_buyers)
            np.random.shuffle(self.catalog_of_sellers)
                                                     

    def reg_enviro(self, buyer, seller):
        # If buyer is upstream of seller, then trade is not restricted
        if len(buyer) > len(seller):
            #print("Trade is restricted: Buyer is upstream of seller")
            return False
        
        if len(buyer) <= len(seller):
            buyer_subvector = buyer[:len(seller)-1]  # Adjusted to match seller's length minus 1
            seller_subvector = seller[:-1]

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

    def trade_sequence(self):
                #print out avbars of buyers and sellers
        #print("Buyers avbar")
        #print([agent.avbar for agent in self.catalog_of_buyers])
        #print("Sellers avbar")
        #print([agent.avbar for agent in self.catalog_of_sellers])

   
        # End trading if buyer or seller list is empty
        if not self.catalog_of_buyers or not self.catalog_of_sellers:
            self.GFT = 0
            return
        #print(f"Number of buyers: {len(self.catalog_of_buyers)}")
        #print(f"Number of sellers: {len(self.catalog_of_sellers)}")
        
       
        # Total value before trading
        TV0 = np.sum([agent.c * (agent.alpha - agent.beta * agent.c) for agent in self.schedule.agents])


        for j in range(len(self.catalog_of_buyers)):
            buyer = self.catalog_of_buyers[j]
            for s in range(len(self.catalog_of_sellers)):
                seller = self.catalog_of_sellers[s]

                if seller.c == 0: # early exit if seller has no water for speed
                    continue

                # check reg enviro conditions
                if self.upstream_selling == False:
                    if self.reg_enviro(buyer.trib_vector, seller.trib_vector) == False:
                        continue
                    
                    

                x = min(seller.c, buyer.cbar - buyer.c)

                avBr_1 = buyer.alpha - buyer.beta * buyer.c
                avBr = buyer.alpha - buyer.beta * (buyer.c + x)
                wtp = avBr_1 + avBr - buyer.alpha # per unit wtp
                bid = wtp * (1 - self.gamma*buyer.sigma)
                
                
                avSr_1 = seller.alpha - seller.beta * seller.c
                avSr = seller.alpha - seller.beta * (seller.c - x)
                wta = avSr_1 + avSr - seller.alpha # per unit wta
                ask = wta * (1 + self.gamma*seller.sigma)
                """
                # print statements to check values
                print("##########################################################")
                print(f"Buyer ID: {buyer.unique_id}, Seller ID: {seller.unique_id}")
                print(f"buyer cbar: {buyer.cbar}, seller cbar: {seller.cbar}")
                print(f"Buyer initial c: {buyer.c}, Seller initial c: {seller.c}")
                print(f"buyer avbar {buyer.avbar}, seller avbar: {seller.avbar}")
                print(f"buyer pro: {buyer.pro}, seller pro: {seller.pro}")
                print(f"buyer sigma: {buyer.sigma}, seller sigma: {seller.sigma}")
                print(f"x: {x}")
                print(f"Bid: {bid}, Ask: {ask}")
                """
                if bid > ask:
                    buyer.c += x
                    seller.c -= x
                    price = (bid + ask) / 2
                    #print("Trade executed")
                else:
                    continue

                #print(f"Buyer final c: {buyer.c}, Seller final c: {seller.c}")
                #print(f"Price: {price}" if bid > ask else "No trade executed")

                
                
                
                
                #print(f"buyer gains")
                #print(f"TV0: {TV0}, TV1: {TV1}")
                #print(f"GFT: {self.GFT}")
        """
        # Farmer's below cbar c=0
        for agent in self.schedule.agents:
            #print("c",agent.unique_id,agent.c)
            #print("cbar",agent.cbar)
            if agent.c < agent.cbar:
                agent.c = 0
        """
        # Total value after trading
        TV1 = np.sum([agent.c * (agent.alpha - agent.beta * agent.c) for agent in self.schedule.agents])
        # compute GFT
        self.GFT = TV1 - TV0

# we need a way to force farmers who don't have c bar to have 0 at the end of trading

    def central_planner_problem(self):
        agent_array = np.array([[agent.alpha , agent.c, agent.beta, agent.acreage, agent.cbar] 
                                for agent in self.schedule.agents])
        c_init = agent_array[:,1]
        beta_array = agent_array[:,2]
        alpha_array = agent_array[:,0]
        initial_value = (alpha_array * (c_init) - beta_array * (c_init**2))
        # create list of trib vectors
        trib_vector_list = [agent.trib_vector for agent in self.schedule.agents]
        # create adjacency matrix based on reg environment
        adj_matrix = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                adj_matrix[i,j] = self.reg_enviro(trib_vector_list[i], trib_vector_list[j])
        # ajd matrix is all ones if no restrictions
        if self.upstream_selling == True:
            adj_matrix = np.ones((self.N, self.N))
        c_opt = cp.Variable(self.N)
        x = cp.Variable((self.N, self.N), nonneg=False)  # Transfer matrix
        Cs = np.sum(c_init) # Total resource constraint
        # Define the objective function
        objective = cp.Maximize(alpha_array.T @ c_opt -  beta_array.T @ cp.square(c_opt))
        # Constraints
        constraints = [cp.sum(c_opt) == Cs]  
        if self.upstream_selling == False:
            for i in range(self.N):
                for j in range(self.N):
                    if adj_matrix[i, j] == 1:
                        constraints.append(c_opt[i] - cp.sum(x[i, :]) + cp.sum(x[:, i]) == c_init[i])
                    else:
                        constraints.append(x[i, j] == 0)  # No transfers allowed
        constraints.append(c_opt >= 0)
        # Define and solve the problem
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS, verbose= False)
        c_opt_value = c_opt.value  # numpy array of optimal values
        # compute GFT
        value_after_trade = (alpha_array * c_opt_value - beta_array * (c_opt_value**2))
        gains_from_trade = value_after_trade - initial_value
        tot_gft = np.sum(gains_from_trade)
        self.GFT = tot_gft
        print(f"Total GFT: {tot_gft}")
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
