"""
02-06-2024 Notes:
- we will want docustring comments for all functions and classes
- no more than 79 characters per line
- utilize iter tools to condense loops
- https://stackoverflow.com/questions/19561900/keeping-to-79-char-line-limit-in-python-with-multiple-indents
"""



###############################################################################
# Preamble and Global Variable Initialization
###############################################################################
from mesa import Agent, Model

"""
Mesa.time handles the time component of the model. It contains schedulers 
that handle agent activations. RandomActivation is a scheduler that 
activates each agent once per step, in random order with the order 
reshuffled every step. DataCollector is a standard way to collect data 
generated by a Mesa model. They can be model-level data, agent-level data, 
and tables.
"""

from mesa.time import RandomActivation 
from mesa.datacollection import DataCollector  
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
# random.seed(4) 

# Initializing empty arrays
trade_percent_all=[]   # Percent of agents who trade
water_held_all_s=[]    # Quantity of water held by sellers	
water_held_all_b=[]    # Quantity of water held by buyers
water_allow_all_s=[]   # Allowable quantity of water to divert by sellers
water_allow_all_b=[]   # Allowable quantity of water to divert by buyers
av_all_s=[]            # Average value of water held by sellers
av_all_b=[]            # Average value of water held by buyers
gft_all_old=[]         # !!!Same as gft_tot_old
gft_all_new=[]         # !!!Same as gft_tot_new
gft_tot_old=[]         # !!!same as gft_all_old
gft_tot_new=[]         # !!!same as gft_all_new
trade_percent=[]       # !!!same as trade_percent_all
water_held_tot_b=[]    # !!!same as water_held_all_b
water_allow_tot_b=[]   # !!!same as water_allow_all_b
water_held_tot_s=[]    # !!!same as water_held_all_s
water_allow_tot_s=[]   # !!!same as water_allow_all_s
av_tot_s=[]            # !!!same as av_all_s
av_tot_b=[]            # !!!same as av_all_b

# Initializing drought and agent parameters
num_agents = int(200)  # Sets the number of agents in the model
dr_num = int(51)  # Number of agents remaining with water rights after drought
perc_sellers = dr_num/num_agents 
dr_severity = np.round(1-perc_sellers,decimals=2) # Severity of drought


# Controls the number of steps in the model, see first column of csv output
iterations = int(1000) 

###############################################################################
# Simulation
###############################################################################

print('##############################################################')
print('simulation begins')
print('##############################################################')
start_time = time.time()



"""
Variable Descriptions:
AV = average value. 
endow = c. 
slope and intercept stand for the same from the yield equation in the ABM. 
c_b = cbar. 
w_b = wbar. 
allow_h2o = allowable water to divert for each water right. 
exo_price = exogenous price. 
conur = consumptive use rate. 
h2o = actual water withdrawn. 
ret = return flow. 
distrib_combo = the array that determines the exact location of the diversion of a water right along a river. 
techno = technology. 
senior = seniority rank. 
field = land acreage. 
tot_h2o = actual water withdrawn * land acreage. 
river_m = river miles. 
yield is the production of the crop portfolio. 
revenue is the revenue generated from selling or purchasing a water right. 
pr_wtp = Willingness to Pay. 
pr_wta = Willingness to accept. 
pr_bid = Bid Price. 
pr_ask = Ask Price.
"""


"""
MyAgent class inherits the Agent class from the mesa package. 
The MyAgent class inherits all of the methods and attributes from the mesa.Agent class. 
Unique id is assigned to each agent.
# super() Passes unique ID and model to the parent class. This line is typically 
# used when you're inheriting from a parent class, and you want to 
# initialize the attributes of the parent class before adding or modifying 
# attributes specific to the child class. In this case, the parent class is mesa.Agent
"""

class MyAgent(Agent): 
	def __init__(self, unique_id, model,AV,endow,slope,intercept,c_b,w_b,allow_h2o,
	             conu,exo_price,conur,h2o,ret,distrib_comb,techno,senior,field,
				 tot_h2o,river_m,yield_agents,revenue,pr_wtp,pr_wta,pr_bid,pr_ask):
		super().__init__(unique_id, model) 
		self.AV = AV
		self.endow = endow                # endowment = c
		self.slope = slope                # from ABM yield equation
		self.intercept = intercept
		self.river_m = river_m
		self.c_b = c_b
		self.w_b = w_b
		self.allow_h2o = allow_h2o
		self.conu = conu                  # consumptive use
		self.exo_price = exo_price        # exogenous price
		self.conur = conur                # consumptive use rate
		self.h2o = h2o                    # actual water withdrawn
		self.ret = ret                    # return flow 
		self.distrib_comb = distrib_comb  # array locating diversion 
		self.techno = techno              # Technology
		self.senior = senior              # The seniority rank of agent
		self.field = field                # land acreage
		self.tot_h2o = tot_h2o            # actual water withdrawn * land acreage
		self.yield_agents = yield_agents  # 
		self.revenue = revenue
		self.pr_wtp = pr_wtp
		self.pr_wta = pr_wta
		self.pr_bid = pr_bid
		self.pr_ask = pr_ask
		self.price1 = 0.0  # (Buying Price) 
		self.price2 = 0.0  # (Selling Price)
		self.gain = 0.0

	def trade(self):  # Trading Method, # Self defines generic instance of the class. We check for if trade can happen:
		if self.senior<=dr_no-1: 
			arr=[]
			ww=self.model.schedule.get_agent_count()
			for kk in range(ww):
				if self.model.schedule.agents[kk].senior>dr_no-1:
					arr.append(self.model.schedule.agents[kk])
			if len(arr)>0:
				other_agent = self.random.choice(arr) #choosing the other agent
			if len(arr)==0:
				other_agent = self.random.choice(self.model.schedule.agents)
		
		if self.senior>dr_no-1:
			arr=[]
			ww=self.model.schedule.get_agent_count()
			for kk in range(ww):
				if self.model.schedule.agents[kk].senior<=dr_no-1:
					arr.append(self.model.schedule.agents[kk])
			if len(arr)>0:
				other_agent = self.random.choice(arr) #choosing the other agent
			if len(arr)==0:
				other_agent = self.random.choice(self.model.schedule.agents)

		#CASE_1: self=Seller and other_agent=Buyer # self=Seller and self.other_agent=Buyer (the self-agent picked is a seller and the other agent picked is a buyer)
		if self.senior <= dr_no-1 and other_agent.senior > dr_no-1:
			if self.AV < other_agent.AV and self.distrib_comb==other_agent.distrib_comb and self.river_m < other_agent.river_m and self.c_b <= (other_agent.c_b-other_agent.endow) and self.pr_ask <= other_agent.pr_wtp and other_agent.AV > 0.0:# and self.unique_id not in id_agent and other_agent.unique_id not in id_agent:
				other_agent.pr_wtp=(other_agent.intercept-other_agent.slope*self.c_b)*self.c_b
				if self.pr_ask <= other_agent.pr_wtp:
					if other_agent.pr_bid >= self.pr_ask:
						self.price2 = other_agent.pr_bid #(self.AV + other_agent.AV)/2. #updating selling price of the Seller
						other_agent.price1 = other_agent.pr_bid #(self.AV + other_agent.AV)/2. #updating buying price of the Buyer
						ss_s[self.unique_id]=self.revenue+self.price2*self.conu #storing profit of Seller
						ss_b[other_agent.unique_id]=other_agent.revenue-other_agent.price1*other_agent.conu #Storing profit of Buyer
						self.endow = self.endow - self.c_b #updating the consumptive use of Seller
						other_agent.endow = other_agent.endow + self.c_b #updating the consumptive use of Buyer
						pp[other_agent.unique_id]=other_agent.price1 #storing Buying price
						qq[self.unique_id]=self.price2 #storing Selling price
						self.gain = (other_agent.pr_wtp-self.pr_wta)*other_agent.endow #other_agent.AV - self.AV #updating the gain
						other_agent.gain = (other_agent.pr_wtp-self.pr_wta)*other_agent.endow #other_agent.AV - self.AV
						rr[self.unique_id]=self.gain #storing gain of Seller
						rr[other_agent.unique_id]=other_agent.gain #storing gain of Buyer
						self.AV = -self.slope*self.endow + self.intercept #updating the AV of Seller
						other_agent.AV = -other_agent.slope*other_agent.endow + other_agent.intercept #updating the AV of Buyer
						if other_agent.endow >= other_agent.c_b: 
							self.model.schedule.remove(other_agent) #removing the Buyer (as its endow equals conu)
						if self.endow <=0: #can also be set equal to 0
							self.model.schedule.remove(self) #removing the Seller
					elif other_agent.pr_bid < self.pr_ask:
						self.price2 = self.pr_ask #(self.AV + other_agent.AV)/2. #updating selling price of the Seller
						other_agent.price1 = self.pr_ask #(self.AV + other_agent.AV)/2. #updating buying price of the Buyer
						ss_s[self.unique_id]=self.revenue+self.price2*self.conu #storing profit of Seller
						ss_b[other_agent.unique_id]=other_agent.revenue-other_agent.price1*other_agent.conu #Storing profit of Buyer
						self.endow = self.endow - self.c_b #updating the consumptive use of Seller
						other_agent.endow = other_agent.endow + self.c_b #updating the consumptive use of Buyer
						pp[other_agent.unique_id]=other_agent.price1 #storing Buying price
						qq[self.unique_id]=self.price2 #storing Selling price
						self.gain = (other_agent.pr_wtp-self.pr_wta)*other_agent.endow #other_agent.AV - self.AV #updating the gain
						other_agent.gain = (other_agent.pr_wtp-self.pr_wta)*other_agent.endow #other_agent.AV - self.AV
						rr[self.unique_id]=self.gain #storing gain of Seller
						rr[other_agent.unique_id]=other_agent.gain #storing gain of Buyer
						self.AV = -self.slope*self.endow + self.intercept #updating the AV of Seller
						other_agent.AV = -other_agent.slope*other_agent.endow + other_agent.intercept #updating the AV of Buyer
						if other_agent.endow >= other_agent.c_b: 
							self.model.schedule.remove(other_agent) #removing the Buyer (as its endow equals conu)
						if self.endow <=0: #can also be set equal to 0
							self.model.schedule.remove(self) #removing the Seller
		
			elif self.price2 > 0.0: #if Seller has already traded in this iteration, then its Selling price should not go to 0
				qq[self.unique_id]=self.price2 + 0.0

		#CASE_2: self=Buyer and other_agent=Seller	
		elif self.senior > dr_no-1 and other_agent.senior <= dr_no-1:
			if self.AV > other_agent.AV and self.distrib_comb == other_agent.distrib_comb and self.river_m > other_agent.river_m and (self.c_b-self.endow) >= other_agent.c_b and self.pr_wtp >= other_agent.pr_ask and other_agent.AV > 0.0:# and other_agent.pr_ask <= self.pr_wtp:# and self.unique_id not in id_agent and other_agent.unique_id not in id_agent:
				self.pr_wtp=(self.intercept-self.slope*other_agent.c_b)*other_agent.c_b
				if other_agent.pr_ask <= self.pr_wtp:						
					if self.pr_bid >= other_agent.pr_ask:
						self.price1 = self.pr_bid #(self.AV + other_agent.AV)/2.
						other_agent.price2 = self.pr_bid #(self.AV + other_agent.AV)/2.
						ss_s[other_agent.unique_id]=other_agent.revenue+other_agent.price2*other_agent.conu
						ss_b[self.unique_id]=self.revenue-self.price1*self.conu
						self.endow = self.endow + other_agent.c_b
						other_agent.endow = other_agent.endow - other_agent.c_b
						pp[self.unique_id]=self.price1
						qq[other_agent.unique_id]=other_agent.price2
						self.gain = (self.pr_wtp-other_agent.pr_wta)*self.endow #self.AV - other_agent.AV
						other_agent.gain = (self.pr_wtp-other_agent.pr_wta)*self.endow #self.AV - other_agent.AV
						rr[self.unique_id]=self.gain
						rr[other_agent.unique_id]=other_agent.gain
						self.AV = -self.slope*self.endow + self.intercept
						other_agent.AV = -other_agent.slope*other_agent.endow + other_agent.intercept
						if self.endow >= self.c_b:
							self.model.schedule.remove(self)
						if other_agent.endow <= 0:
							self.model.schedule.remove(other_agent)
					elif self.pr_bid < other_agent.pr_ask:
						self.price1 = other_agent.pr_ask #(self.AV + other_agent.AV)/2.
						other_agent.price2 = other_agent.pr_ask #(self.AV + other_agent.AV)/2.
						ss_s[other_agent.unique_id]=other_agent.revenue+other_agent.price2*other_agent.conu
						ss_b[self.unique_id]=self.revenue-self.price1*self.conu
						self.endow = self.endow + other_agent.c_b
						other_agent.endow = other_agent.endow - other_agent.c_b
						pp[self.unique_id]=self.price1
						qq[other_agent.unique_id]=other_agent.price2
						self.gain = (self.pr_wtp-other_agent.pr_wta)*self.endow #self.AV - other_agent.AV
						other_agent.gain = (self.pr_wtp-other_agent.pr_wta)*self.endow #self.AV - other_agent.AV
						rr[self.unique_id]=self.gain
						rr[other_agent.unique_id]=other_agent.gain
						self.AV = -self.slope*self.endow + self.intercept
						other_agent.AV = -other_agent.slope*other_agent.endow + other_agent.intercept
						if self.endow >= self.c_b:
							self.model.schedule.remove(self)
						if other_agent.endow <= 0:
							self.model.schedule.remove(other_agent)
			elif other_agent.price2 > 0.0:
				qq[other_agent.unique_id]=other_agent.price2 + 0.0

		#if they do not trade anymore in this iteration, then their Selling and Buying prices should not be 0
		elif self.senior > dr_no-1 and other_agent.senior > dr_no-1:
			pp[self.unique_id] = self.price1 + 0.0
			qq[other_agent.unique_id] = other_agent.price2 + 0.0
			qq[self.unique_id] = self.price2 + 0.0
			pp[other_agent.unique_id] = other_agent.price1 + 0.0
		elif self.senior <= dr_no-1 and other_agent.senior <= dr_no-1:
			pp[self.unique_id] = self.price1 + 0.0
			qq[other_agent.unique_id] = other_agent.price2 + 0.0
			qq[self.unique_id] = self.price2 + 0.0
			pp[other_agent.unique_id] = other_agent.price1 + 0.0


	def step(self): #method to check if agent can at all trade
		if self.AV > 0.0:
			self.trade() #function for trading
		elif self.AV < 0.0:
			pp[self.unique_id]=0.0 #Buying price set to 0
			qq[self.unique_id]=0.0 #Selling price set to 0
		else:
			pass

def compute_price(model):
	agent_price = [agent.price1 for agent in model.schedule.agents]
	return agent_price

# class that initialises agents with all properties and initialises the interaction, how are the attributes randomly assigned?
class Trade_Model(Model): # Trading Class
	def __init__(self, N,cu,ex_price,trib_comb,riv_m,cur,water,ret_fl,tech,sen_id,land,tot_water,seed=None):
		global gamma

		self.num_agents = N #number of total agents
		self.schedule = RandomActivation(self)  #activation of the interaction, agents are selected randomly
		self.running = True # starts the simulation

		#initialising empty arrays
		return_water=[]
		avg_val=[]
		endowment=[]
		sl=[]
		interc=[]
		c_bar=[]
		w_bar=[]
		allow_water=[]
		yield_all=[]
		rev=[]
		P_wtp=[]
		P_wta=[]
		P_bid=[]
		P_ask=[]
		gamma=1.0
		eps_s=(dr_no-1)/self.num_agents #number of sellers is (dr_no-1)
		eps_b=(self.num_agents-(dr_no-1))/self.num_agents #number of buyers is (num_agents-dr_no+1)

		for i in range(self.num_agents):
			if sen_list[i] <= dr_no-1: #checking if sen_id is less than dr_no
				sl.append(random.uniform(0,2))
				interc.append(random.uniform(20,40))#(2*sl[i]*endowment[i])
				c_bar.append(interc[i]/(2*sl[i]))
				endowment.append(c_bar[i])
				avg_val.append(interc[i]-sl[i]*endowment[i])
				P_wtp.append('NA')
				P_wta.append(avg_val[i]*c_bar[i])
				P_bid.append('NA')
				P_ask.append(P_wta[i]*(1+gamma*eps_b))
				w_bar.append(c_bar[i]/cur[i])
				return_water.append(w_bar[i]-c_bar[i])
				allow_water.append(w_bar[i]*land[i])
				yield_all.append(interc[i]*c_bar[i]-sl[i]*(c_bar[i])**2)
				rev.append(ex_price[i]*yield_all[i])
	

			elif sen_list[i] > dr_no-1: #checking if sen_id is more than dr_no
				sl.append(random.uniform(0,2))
				interc.append(random.uniform(20,40))#(2*sl[i]*cu[i])
				c_bar.append(interc[i]/(2*sl[i]))
				endowment.append(0)
				avg_val.append(interc[i]-sl[i]*endowment[i])
				P_wtp.append(avg_val[i]*c_bar[i])
				P_wta.append('NA')
				P_bid.append(P_wtp[i]*(1-gamma*eps_s))
				P_ask.append('NA')
				w_bar.append(c_bar[i]/cur[i])
				return_water.append(w_bar[i]-c_bar[i])
				allow_water.append(w_bar[i]*land[i])
				yield_all.append(interc[i]*c_bar[i]-sl[i]*(c_bar[i])**2)
				rev.append(ex_price[i]*yield_all[i])

		for i in range(self.num_agents): #runs over all the agents (one at a time)
			#initialising each agent
			a = MyAgent(i, self,avg_val[i],endowment[i],sl[i],interc[i],c_bar[i],w_bar[i],allow_water[i],cu[i],ex_price[i],cur[i],water[i],ret_fl[i],trib_comb[i],tech[i],sen_list[i],land[i],tot_water[i],riv_m[i],yield_all[i],rev[i],P_wtp[i],P_wta[i],P_bid[i],P_ask[i])
			#adding to the scheduler
			self.schedule.add(a)
		#for collecting the data
		self.datacollector = DataCollector(
			model_reporters = {"Agent Price": compute_price},
			agent_reporters={"Price1": "price1","Price2": "price2","Endowment": "endow","AV": "AV","Slope":"slope","Intercept":"intercept","c_bar":"c_b","w_bar":"w_b","Allowable_water":"allow_h2o","gft":"gain","Con_use":"conu","Exo_price":"exo_price","Con_use_r":"conur","Water":"h2o","Return":"ret","Trib_comb":"distrib_comb","Technology":"techno","Seniority":"senior","Land":"field","Total_water":"tot_h2o","River_m":"river_m","Yield":"yield_agents","Revenue":"revenue","Pr_wtp":"pr_wtp","Pr_wta":"pr_wta","Pr_bid":"pr_bid","Pr_ask":"pr_ask"})

	# method for starting the interaction between agents
	def mystep(self):
		self.datacollector.collect(self)
		self.schedule.step() #randomly starts trading


#GPT Split line, character maxed out


num_of_agents=num_agents #int(no_sen+yes_sen) #total agents
# Why are we setting all of these inside of the for loop? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dr_no =int(dr_num) #int(num_of_agents/2 +1 ) #random.randint(1,num_of_agents) # # 
print('Random drought number is: ',dr_no)
num_list=[0.625,1.25,1.875,2.5,3.125,3.75,4.375,5]#[10,50,70,90] #list of consumptive uses
ex_price_list=[1,2,3,4,5,6,7,8] #crop list // it could be cool to add a random variable here rather than a list
tech_list=[1,2,3,4,5,6] #technology list
sen_list=random.sample(range(1,num_of_agents+1),num_of_agents) #list of seniority id 
low=0.001 #lower bound of consumptive use rate
high=0.999 #upper bound of consumptive use rate
land_low=2 #lower bound of amount of land
land_high=172 #upper bound of amount of land

cu=[] #consumptive use
ex_price=[] #exogenous price of crop
cur=[] #consumptive use rate
water=[] #amount of water withdrawn
ret_fl=[] #return flow
tech=[] #technology
land=[] #amount of land
tot_water=[] #water*land
trib_comb=[] #tributary position
trib_comb_1=[] #temporary tributary position
trib_comb_list=[] #all possible tributary positions
riv_m_start=[] #start river miles range
riv_m_end=[] #end of river miles range
riv_m=[] #actual river miles for each agent

#functions to produce all combinations of 0 and 1 of length k
def printAllKLength(set, k):

	n = len(set)
	printAllKLengthRec(set, "", n, k)

def printAllKLengthRec(set, prefix, n, k):
	if (k == 0) :
		trib_comb_1.append(prefix)
		return
	for i in range(n):
		newPrefix = prefix + set[i]
		printAllKLengthRec(set, newPrefix, n, k - 1)

set1=['0','1']
comb_no=4 #this number defines how complicated the tributary distribution is (larger number means more complicated), larger set of 0 and 1
for i in range(comb_no):
	k=i+1
	printAllKLength(set1,k)
trib_comb_1=np.array(trib_comb_1)
for i in range(len(trib_comb_1)):
	if trib_comb_1[i][0]=='1': #tributary combination elements don't start with 0, so make a new list where elements start with 1
		trib_comb_list.append(trib_comb_1[i])

for i in range(num_of_agents):
	if sen_list[i] <= dr_no-1:
		rand_id=random.randrange(len(num_list))
		cu.append(num_list[rand_id]) #assigning consumptive use randomly
		ex_price.append(ex_price_list[rand_id]) #assigning crop price randomly
		trib_comb.append(random.choice(trib_comb_list)) #assigning tributary combination randomly
		for j in range(comb_no):
			if len(trib_comb[i])==j+1: #depending on length of tributary combination, end of range is assigned
				riv_m_end.append((j+1)*1001)
		riv_m_start.append(riv_m_end[i]-1000) #assigning start of range which is 1000 less than end of range
		riv_m.append(random.randint(riv_m_start[i],riv_m_end[i])) #assigning the particular river miles
		cur.append(random.uniform(low,high)) #assigning consumptive use rate
		water.append(cu[i]/cur[i])
		ret_fl.append(water[i]-cu[i])
		tech.append(random.choice(tech_list)) #assigning the technology
		land.append(random.uniform(land_low,land_high)) #assigning amount of land
		tot_water.append(water[i]*land[i])
	elif sen_list[i] > dr_no-1:
		rand_id=random.randrange(len(num_list))
		cu.append(num_list[rand_id])
		ex_price.append(ex_price_list[rand_id])
		trib_comb.append(random.choice(trib_comb_list))
		for j in range(comb_no):
			if len(trib_comb[i])==j+1:
				riv_m_end.append((j+1)*1001)
		riv_m_start.append(riv_m_end[i]-1000)
		riv_m.append(random.randint(riv_m_start[i],riv_m_end[i]))
		cur.append(random.uniform(low,high))
		water.append(0)
		ret_fl.append('NA')
		tech.append(random.choice(tech_list))
		land.append(random.uniform(land_low,land_high))
		tot_water.append('NA')
#calling Trade_Model class
model = Trade_Model(num_of_agents,cu,ex_price,trib_comb,riv_m,cur,water,ret_fl,tech,sen_list,land,tot_water,seed=None)

#initialising empty arrays for these variables
buy=[] #Buying price
sell=[] #Selling price
pr_s=[] #profit Seller
pr_b=[] #profit Buyer
gainft=[] #GFT
stop=[] #stopping criterion

#interactions go on for 'iterations' number of times
for i in range(iterations):
	ww=model.schedule.get_agent_count() #how many agents are there at that particular iteration
	#setting price (for both B and S) after every iteration to 0
	for j in range(ww):
		model.schedule.agents[j].price1 = 0.0 #price1 is Buying price
		model.schedule.agents[j].price2 = 0.0 #price2 is Selling price
	pp=np.zeros(num_of_agents) #array for storing Buying price for each iteration
	qq=np.zeros(num_of_agents) #array for storing Selling price for each iteration
	rr=np.zeros(num_of_agents) #array for storing GFT for each iteration
	ss_s=np.zeros(num_of_agents) #array for storing profit_seller for each iteration
	ss_b=np.zeros(num_of_agents) #array for storing profit_buyer for each iteration
	model.mystep() 
	buy.append(pp)
	sell.append(qq)
	pr_s.append(ss_s)
	pr_b.append(ss_b)
	gainft.append(rr)
	for j in range(num_of_agents):
		stop.append(pp[j]) #appends the Selling price of all agents in 'stop' for each iteration
	if sum(stop[-10*num_of_agents:])==0: #if sum of last 10*num_agents selling price is zero, then model stops running
		break
iterations = int(len(buy))


agent_variables = model.datacollector.get_agent_vars_dataframe()

all_agent_price1=[]
for i in range(num_of_agents):
	aa=[]
	for j in range(iterations):
		aa.append(buy[j][i])
	all_agent_price1.append(aa)

all_agent_price2=[]
for i in range(num_of_agents):
	aa=[]
	for j in range(iterations):
		aa.append(sell[j][i])
	all_agent_price2.append(aa)

all_agent_gain=[]
for i in range(num_of_agents):
	aa=[]
	for j in range(iterations):
		aa.append(gainft[j][i])
	all_agent_gain.append(aa)

all_agent_c_bar=[]
for i in range(num_of_agents):
	one_agent_c_bar=agent_variables.xs(i,level='AgentID')
	all_agent_c_bar.append(one_agent_c_bar.c_bar)
for i in range(num_of_agents):
	all_agent_c_bar[i]=np.array(all_agent_c_bar[i])
	for j in range(iterations-len(all_agent_c_bar[i])):
		all_agent_c_bar[i]=np.append(all_agent_c_bar[i],all_agent_c_bar[i][0])

all_agent_endow=[]
for i in range(num_of_agents):
	one_agent_endow = agent_variables.xs(i, level="AgentID")
	all_agent_endow.append(one_agent_endow.Endowment)


for i1 in range(num_of_agents):
	all_agent_endow[i1]=np.array(all_agent_endow[i1])
	#print(all_agent_gain[i])
	if sen_list[i1]>dr_no-1:
		dd1=0
		for i2 in range(num_of_agents):
			if sen_list[i2]<=dr_no-1:
				for i3 in range(iterations):
					if all_agent_gain[i1][i3] != 0 and all_agent_gain[i1][i3]==all_agent_gain[i2][i3]:
						dd1=dd1+all_agent_c_bar[i2][i3] #all_agent_endow[i1][-1]-cu[i2]
		dd2=all_agent_endow[i1][0]+dd1
		for i4 in range(iterations-len(all_agent_endow[i1])):
				all_agent_endow[i1]=np.append(all_agent_endow[i1],dd2)
	elif sen_list[i1]<=dr_no-1:
		cc=all_agent_endow[i1][0]-all_agent_c_bar[i1][0]
		#print(cc)
		for i5 in range(iterations-len(all_agent_endow[i1])):
			all_agent_endow[i1]=np.append(all_agent_endow[i1],cc)

all_agent_slope=[]
for i in range(num_of_agents):
	one_agent_slope = agent_variables.xs(i, level="AgentID")
	all_agent_slope.append(one_agent_slope.Slope)

for i in range(num_of_agents):
	all_agent_slope[i]=np.array(all_agent_slope[i]) 
	for j in range(iterations-len(all_agent_slope[i])):
		all_agent_slope[i]=np.append(all_agent_slope[i],all_agent_slope[i][0])


all_agent_intercept=[]
for i in range(num_of_agents):
	one_agent_intercept = agent_variables.xs(i, level="AgentID")
	all_agent_intercept.append(one_agent_intercept.Intercept)

for i in range(num_of_agents):
	all_agent_intercept[i]=np.array(all_agent_intercept[i]) 
	for j in range(iterations-len(all_agent_intercept[i])):
		all_agent_intercept[i]=np.append(all_agent_intercept[i],all_agent_intercept[i][0])

all_agent_allow_water=[]
for i in range(num_of_agents):
	one_agent_allow_water=agent_variables.xs(i,level='AgentID')
	all_agent_allow_water.append(one_agent_allow_water.Allowable_water)
for i in range(num_of_agents):
	all_agent_allow_water[i]=np.array(all_agent_allow_water[i])
	for j in range(iterations-len(all_agent_allow_water[i])):
		all_agent_allow_water[i]=np.append(all_agent_allow_water[i],all_agent_allow_water[i][0])
		
all_agent_seniority=[]
for i in range(num_of_agents):
	aa=[]
	for j in range(iterations):
		aa.append(sen_list[i])
	all_agent_seniority.append(aa)
			

all_agent_AV=[]
for i in range(num_of_agents):
	#print(i)
	ll=[]
	for j in range(iterations):
		ll.append(-all_agent_slope[i][j]*all_agent_endow[i][j]+all_agent_intercept[i][j])
	all_agent_AV.append(ll)

all_agent_conu=[] #this is actually the crop based consumptive use
for i in range(num_of_agents):
	aa=[]
	for j in range(iterations):
		aa.append(cu[i])
	all_agent_conu.append(aa)

x = list(range(1,iterations+1))


##this prints total gain from trade
qq_gft=[]
for i in range(num_of_agents):
	if sen_list[i]<=dr_no-1:
		qq_gft.append(sum(all_agent_gain[i]))
print('Total Gain from Trade: ',sum(qq_gft))

### I rewrote this section. Saves 18 seconds of time
if sum(qq_gft) != 0:  # else, repeat loop
    my_dict = {'Step': x}
    df = pd.DataFrame(my_dict)

    data = {
        'Buying_Price': all_agent_price1,
        'Selling_Price': all_agent_price2,
        'Consumptive_Use': all_agent_endow,
        'Slope': all_agent_slope,
        'Intercept': all_agent_intercept,
        'AV': all_agent_AV,
        'Gain': all_agent_gain,
        'Crop_based_Consumptive_Use': all_agent_conu,
        'c_bar': all_agent_c_bar,
        'Allowable_Water': all_agent_allow_water,
        'Seniority': all_agent_seniority
    }

    for j in range(num_of_agents):
        agent_data = {f'Agent{j+1}_{key}': data[key][j] for key in data}
        df = pd.concat([df, pd.DataFrame(agent_data)], axis=1)

    df.to_csv('all_agents_data_pos_try23_dr_no.csv', index=False)


    gft_tot_new.append(sum(qq_gft))
    count_s=0
    count_b=0
    indicator_s = np.zeros(num_of_agents)
    for i in range(num_of_agents):
        if sen_list[i]<=dr_no-1:
            for j in range(iterations):
                if all_agent_price2[i][j] != 0.0:
                    indicator_s[i] = 1
    indicator_b = np.zeros(num_of_agents)
    for i in range(num_of_agents):
        if sen_list[i]>dr_no-1:
            for j in range(iterations):
                if all_agent_price1[i][j] != 0.0:
                    indicator_b[i] = 1
    for i in range(len(indicator_s)):
        if indicator_s[i] != 0.0:
            count_s=count_s+1
    for i in range(len(indicator_b)):
        if indicator_b[i] != 0.0:
            count_b=count_b+1
    trade_percent.append(((count_s+count_b)/(num_of_agents))*100)
    vat_b=[]
    vbt_s=[]
    for i in range(num_of_agents):
        if sen_list[i]>dr_no-1:
            abc=[]
            for j in range(iterations):
                if all_agent_price1[i][j] != 0.0:
                    abc.append(all_agent_AV[i][j+1]*all_agent_endow[i][j+1])
            vat_b.append(np.sum(abc))
    for i in range(num_of_agents):
        if sen_list[i]<=dr_no-1:
            abc=[]
            for j in range(iterations):
                if all_agent_price2[i][j] != 0.0:
                    abc.append(all_agent_AV[i][0]*all_agent_c_bar[i][0])
            vbt_s.append(np.sum(abc))


	##this prints total initial and final AV (before and after trade)
    int_AV_s=[]
    fin_AV_s=[]
    int_AV_b=[]
    fin_AV_b=[]
    for i in range(num_of_agents):
        if sen_list[i]<=dr_no-1:
            int_AV_s.append(all_agent_AV[i][0]*all_agent_endow[i][0])
            fin_AV_s.append(all_agent_AV[i][-1]*all_agent_endow[i][-1])
        if sen_list[i]>dr_no-1:
            int_AV_b.append(all_agent_AV[i][0]*all_agent_endow[i][0])
            fin_AV_b.append(all_agent_AV[i][-1]*all_agent_endow[i][-1])
			
    av_cu_i=[]
    av_cu_f=[]
    for i in range(num_of_agents):
        av_cu_i.append(all_agent_AV[i][0]*all_agent_endow[i][0])
        av_cu_f.append(all_agent_AV[i][-1]*all_agent_endow[i][-1])
		

    av_tot_s.append(sum(int_AV_s))
    av_tot_b.append(sum(int_AV_b))
    gft_tot_old.append(sum(vat_b)-sum(vbt_s))
	

    water_held_s=[]
    for i in range(num_of_agents):
        if sen_list[i]<=dr_no-1:
            water_held_s.append(all_agent_conu[i][0])
    water_held_tot_s.append(sum(water_held_s))

    water_held_b=[]
    for i in range(num_of_agents):
        if sen_list[i]>dr_no-1:
            water_held_b.append(all_agent_conu[i][0])
    water_held_tot_b.append(sum(water_held_b))

    water_allow_s=[]
    for i in range(num_of_agents):
        if sen_list[i]<=dr_no-1:
            water_allow_s.append(all_agent_allow_water[i][0])
    water_allow_tot_s.append(sum(water_allow_s))

    water_allow_b=[]
    for i in range(num_of_agents):
        if sen_list[i]>dr_no-1:
            water_allow_b.append(all_agent_allow_water[i][0])
    water_allow_tot_b.append(sum(water_allow_b))
	

    print('-------------------')
    print('The model shows trade')
    print('-------------------')

    print('Total Initial AV for Sellers: ',sum(int_AV_s))
    print('Total Final AV for Sellers: ',sum(fin_AV_s))
    print('Total Initial AV for Buyers: ',sum(int_AV_b))
    print('Total Final AV for Buyers: ',sum(fin_AV_b))
    print('Total Percentage of Agents Trading: ',trade_percent)
    print('drought severity:', dr_severity)

	##this prints number of agents that are cut-off
    print('Number of agents that are cut-off: ',(num_of_agents-dr_no+1)) #+no_sen,'(',num_of_agents-dr_no+1,'for drought number &',no_sen,'for no seniority)')



	##ends here
else:
	print('failed')


trade_percent_all.append(trade_percent)
water_held_all_s.append(water_held_tot_s)
water_held_all_b.append(water_held_tot_b)
water_allow_all_s.append(water_allow_tot_s)
water_allow_all_b.append(water_allow_tot_b)
av_all_s.append(av_tot_s)
av_all_b.append(av_tot_b)
gft_all_old.append(gft_tot_old)
gft_all_new.append(gft_tot_new)

my_dict={'Percentage_of_Sellers':perc_sellers,'Percentage_of_Agents_Trading':trade_percent,'Consumptive_Use_Sellers':water_held_tot_s,'Consumptive_Use_Buyers':water_held_tot_b,'Volume_Quantity_Filled_Sellers':water_allow_tot_s,'Volume_Quantity_Filled_Buyers':water_allow_tot_b,'Initial_AV_Sellers':av_tot_s,'Initial_AV_Buyers':av_tot_b}
df=pd.DataFrame(my_dict)
df.to_csv('results_data_simulation1.csv',index=False)
end_time = time.time()-start_time
print('##############################################################')
print('##############################################################')
print('Done with simulation number 1 in ',end_time, 'seconds ')
print('##############################################################')
print('##############################################################')



