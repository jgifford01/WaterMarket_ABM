#test merge 2
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

import random
import numpy as np
import sys
from matplotlib.pyplot import *
import random
import pandas as pd
from itertools import product

#a_once=input("How many agents? : ")

perc_sellers=[10,20,30,40,50,60,70,80,90]
pvi_all=[]
trade_percent_all=[]
water_held_all_s=[]
water_held_all_b=[]
water_allow_all_s=[]
water_allow_all_b=[]
av_all_s=[]
av_all_b=[]
gft_all_old=[]
gft_all_new=[]

for ppp in range(10):
	dr_num=[50,100,150,200,250,300,350,400,450] #,510,560,610,660,710,760]
	rand_seed=[11,13,15,17,19,21,23,25,27] #,25,27,29,31,33,35,37]
	rand_seed3=[10,12,14,16,18,20,22,24,26] #,22,24,26,28,30,32,34]
	rand_seed2=[1,2,3,4,5,6,7,8,9]
	#rand_seed=[15,17,19,21,23,25,27,29] #,25,27,29,31,33,35,37]
	#rand_seed3=[14,16,18,20,22,24,26,28] #,22,24,26,28,30,32,34]
	#rand_seed2=[5,6,7,8,9,10,11,12]
	gft_tot_old=[]
	gft_tot_new=[]
	trade_percent=[]
	pvi=[]
	water_held_tot_b=[]
	water_allow_tot_b=[]
	water_held_tot_s=[]
	water_allow_tot_s=[]
	av_tot_s=[]
	av_tot_b=[]

	for jj in range(len(dr_num)):
		a_once=500
		for ii in range(500):
			##main simulation portion
			print('Try number: ',ii+1)
			class MyAgent(Agent):
				def __init__(self, unique_id, model,AV,endow,slope,intercept,c_b,w_b,allow_h2o,conu,exo_price,conur,h2o,ret,distrib_comb,techno,senior,field,tot_h2o,river_m,yield_agents,revenue,pr_wtp,pr_wta,pr_bid,pr_ask):
					super().__init__(unique_id, model)
					self.AV = AV
					self.endow = endow
					self.slope = slope
					self.intercept = intercept
					self.river_m=river_m
					self.c_b=c_b
					self.w_b=w_b
					self.allow_h2o=allow_h2o
					self.conu=conu
					self.exo_price=exo_price
					self.conur=conur
					self.h2o=h2o
					self.ret=ret
					self.distrib_comb=distrib_comb
					self.techno=techno
					self.senior=senior
					self.field=field
					self.tot_h2o=tot_h2o
					self.yield_agents=yield_agents
					self.revenue=revenue
					self.pr_wtp=pr_wtp
					self.pr_wta=pr_wta
					self.pr_bid=pr_bid
					self.pr_ask=pr_ask
					self.price1=0.0
					self.price2=0.0
					self.gain=0.0
					#self.kill_agent=[]
					#self.id_agent=[None]*num_of_agents
	
					#self.schedule = RandomActivation(self)
	
				def trade(self):        
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
					#ex=[1,1]
	
					#if other_agent.unique_id in id_agent:
					#	pass
		
					#CASE_1: self=Seller and other_agent=Buyer
					if self.senior <= dr_no-1 and other_agent.senior > dr_no-1:
						if self.AV < other_agent.AV and self.distrib_comb==other_agent.distrib_comb and self.river_m < other_agent.river_m and self.c_b <= (other_agent.c_b-other_agent.endow) and self.pr_ask <= other_agent.pr_wtp and other_agent.AV > 0.0:# and self.unique_id not in id_agent and other_agent.unique_id not in id_agent:
							other_agent.pr_wtp=(other_agent.intercept-other_agent.slope*self.c_b)*self.c_b
							if self.pr_ask <= other_agent.pr_wtp:
								if other_agent.pr_bid >= self.pr_ask:
									#id_agent[other_agent.unique_id]=other_agent.unique_id
									#id_agent[self.unique_id]=self.unique_id
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
									#id_agent[other_agent.unique_id]=other_agent.unique_id
									#id_agent[self.unique_id]=self.unique_id
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
							#id_agent[other_agent.unique_id]=other_agent.unique_id

					#CASE_2: self=Buyer and other_agent=Seller	
					elif self.senior > dr_no-1 and other_agent.senior <= dr_no-1:
						if self.AV > other_agent.AV and self.distrib_comb == other_agent.distrib_comb and self.river_m > other_agent.river_m and (self.c_b-self.endow) >= other_agent.c_b and self.pr_wtp >= other_agent.pr_ask and other_agent.AV > 0.0:# and other_agent.pr_ask <= self.pr_wtp:# and self.unique_id not in id_agent and other_agent.unique_id not in id_agent:
							self.pr_wtp=(self.intercept-self.slope*other_agent.c_b)*other_agent.c_b
							if other_agent.pr_ask <= self.pr_wtp:						
								if self.pr_bid >= other_agent.pr_ask:
									#id_agent[other_agent.unique_id]=other_agent.unique_id
									#id_agent[self.unique_id]=self.unique_id
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
									#id_agent[other_agent.unique_id]=other_agent.unique_id
									#id_agent[self.unique_id]=self.unique_id
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
							#id_agent[other_agent.unique_id]=other_agent.unique_id
		
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

	
				def step(self): #function to check if agent can at all trade
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

			#class that initialises agents with all properties and initialises the interaction
			class Trade_Model(Model):
				def __init__(self, N,cu,ex_price,trib_comb,riv_m,cur,water,ret_fl,tech,sen_id,land,tot_water,seed=None):
					global gamma
		
					self.num_agents = N #number of total agents
					self.schedule = RandomActivation(self)  #activation of the interaction
					self.running = True #model attribute
					#self.kill_agent=[]
		
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
					#location=random.sample(range(1,num_of_agents+1),num_of_agents)
					#random.seed(int(rand_seed[jj]+2000*ii))
					#assigning the above variables according to dr_no
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
		
				#function for starting the interaction between agents
				def mystep(self):
					self.datacollector.collect(self)
					self.schedule.step() #randomly starts trading
					#for i in self.kill_agent:
					#	self.schedule.remove(self)
					#	self.kill_agent.remove(i)

			a = a_once #input("How many agents? : ")
			b = 1000 #input("How many steps? : ") #initial iteration number

			num_agents = int(a)
			iterations = int(b)
			#no_sen = int((7./100.)*num_agents) #no seniority id for these many agents
			#yes_sen = (num_agents - no_sen) #these many agents have seniority id
			num_of_agents=num_agents #int(no_sen+yes_sen) #total agents

			dr_no =int(dr_num[jj]) #int(num_of_agents/2 +1 ) #random.randint(1,num_of_agents) # #
			print('Random drought number is: ',dr_no)
			num_list=[0.625,1.25,1.875,2.5,3.125,3.75,4.375,5]#[10,50,70,90] #list of consumptive uses
			ex_price_list=[1,2,3,4,5,6,7,8] #crop list
			tech_list=[1,2,3,4,5,6] #technology list
			#trib_num=[0,1] #1 is tributary, 0 is main stream
			#random.seed(int(rand_seed2[jj]+2000*ii))
			sen_list=random.sample(range(1,num_of_agents+1),num_of_agents) #list of seniority id 
			#id_no_sen=[int(2*num_of_agents),int(2*num_of_agents)] #a very high number is assigned as seniority to identify agents with no water right (so they are Buyers)
			#for idx in range(int(no_sen)):
			#	index = random.randint(0, len(sen_list))
			#	sen_list = sen_list[:index] + [random.choice(id_no_sen)] + sen_list[index:] #updating the seniority id list to include agents with no seniority id
			low=0.001 #lower bound of consumptive use rate
			high=0.999 #upper bound of consumptive use rate
			land_low=2 #lower bound of amount of land
			land_high=172 #upper bound of amount of land

			cu=[] #consumptive use
			ex_price=[] #exogenous price of crop
			cur=[] #consumptive use rate
			#trib=[]
			water=[] #amount of water withdrawn
			ret_fl=[] #return flow
			tech=[] #technology
			#sen_id=[]
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
			comb_no=4 #this number defines how complicated the tributary distribution is (larger number means more complicated)
			for i in range(comb_no):
				k=i+1
				printAllKLength(set1,k)
			trib_comb_1=np.array(trib_comb_1)
			for i in range(len(trib_comb_1)):
				if trib_comb_1[i][0]=='1': #tributary combination elements don't start with 0, so make a new list where elements start with 1
					trib_comb_list.append(trib_comb_1[i])
			#print(trib_comb_list)


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
					#trib.append(random.choice(trib_num))
					water.append(cu[i]/cur[i])
					ret_fl.append(water[i]-cu[i])
					tech.append(random.choice(tech_list)) #assigning the technology
					#sen_id.append(sen_list[i])
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
					#trib.append(random.choice(trib_num))
					water.append(0)
					ret_fl.append('NA')
					tech.append(random.choice(tech_list))
					#sen_id.append(sen_list[i])
					land.append(random.uniform(land_low,land_high))
					tot_water.append('NA')
			#print(cu)
			#calling Trade_Model class
			model = Trade_Model(num_of_agents,cu,ex_price,trib_comb,riv_m,cur,water,ret_fl,tech,sen_list,land,tot_water,seed=None)#int(rand_seed3[jj]+2000*ii)) #int(rand_seed2[jj]))

			#initialising empty arrays for these variables
			buy=[] #Buying price
			sell=[] #Selling price
			pr_s=[] #profit Seller
			pr_b=[] #profit Buyer
			gainft=[] #GFT
			stop=[] #stopping criterion
			#id_agent=[None]*num_of_agents*iterations

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

			#for i in range(len(all_agent_endow)):
			#	print((all_agent_endow[i]))
			#print('-------------------')

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
			#print('-------------------')
			#for i in range(len(all_agent_endow)):
			#	print(len(all_agent_endow[i]))

			all_agent_slope=[]
			for i in range(num_of_agents):
				one_agent_slope = agent_variables.xs(i, level="AgentID")
				all_agent_slope.append(one_agent_slope.Slope)

			for i in range(num_of_agents):
				all_agent_slope[i]=np.array(all_agent_slope[i]) 
				for j in range(iterations-len(all_agent_slope[i])):
					all_agent_slope[i]=np.append(all_agent_slope[i],all_agent_slope[i][0])

			#for i in range(len(all_agent_slope)):
			#	print(len(all_agent_slope[i]))


			all_agent_intercept=[]
			for i in range(num_of_agents):
				one_agent_intercept = agent_variables.xs(i, level="AgentID")
				all_agent_intercept.append(one_agent_intercept.Intercept)

			for i in range(num_of_agents):
				all_agent_intercept[i]=np.array(all_agent_intercept[i]) 
				for j in range(iterations-len(all_agent_intercept[i])):
					all_agent_intercept[i]=np.append(all_agent_intercept[i],all_agent_intercept[i][0])
			#for i in range(len(all_agent_intercept)):
			#	print(len(all_agent_intercept[i]))
			
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
					#print(len(all_agent_endow[i]),len(all_agent_slope[i]),len(all_agent_intercept[i]))
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


			if sum(qq_gft) != 0:
				#print('Random Seed 1: ',rand_seed[jj]+2000*ii)
				#print('Random Seed 2: ',rand_seed2[jj]+2000*ii)
				#print('Random Seed 3: ',rand_seed3[jj]+2000*ii)
				
				my_dict={'Step':x}
				df = pd.DataFrame(my_dict)
				for j in range(num_of_agents):
					qq = all_agent_price1[j]
					rr = all_agent_endow[j]
					ss = all_agent_price2[j]
					tt = all_agent_slope[j]
					uu = all_agent_intercept[j]
					vv = all_agent_AV[j]
					ww = all_agent_gain[j]
					xx = all_agent_conu[j]
					#yy = all_agent_conur[j]
					#zz = all_agent_trib_comb[j]
					#aaa = all_agent_water[j]
					#bbb = all_agent_retfl[j]
					#ccc = all_agent_prwith[j]
					#ddd = all_agent_river_m[j]
					eee = all_agent_c_bar[j]
					#fff = all_agent_w_bar[j]
					ggg = all_agent_allow_water[j]
					#hhh = all_agent_tech[j]
					#iii = all_agent_tot_water[j]
					#jjj = all_agent_land[j]
					kkk = all_agent_seniority[j]
					#if kkk[0]==2*num_of_agents:
					#	for l in range(len(kkk)):
					#		kkk[l]='NA'
					#lll = all_agent_ex_price[j]
					#mmm = all_agent_yield[j]
					#nnn = all_agent_rev[j]
					#ooo = all_agent_pr_s[j]
					#ppp = all_agent_pr_b[j]
					#qqq = all_agent_p_wta[j]
					#rrr = all_agent_p_wtp[j]
					#sss = all_agent_p_bid[j]
					#ttt = all_agent_p_ask[j]
					#uuu = all_agent_index_s[j]
					#vvv = all_agent_index_b[j]
					df['Agent'+str(j+1)+'_Buying_Price'] = qq
					df['Agent'+str(j+1)+'_Selling_Price'] = ss
					df['Agent'+str(j+1)+'_Consumptive_Use'] = rr
					df['Agent'+str(j+1)+'_Slope']=tt
					df['Agent'+str(j+1)+'_Intercept']=uu
					df['Agent'+str(j+1)+'_AV']=vv
					df['Agent'+str(j+1)+'_Gain']=ww
					df['Agent'+str(j+1)+'_Crop_based_Consumptive_Use']=xx
					#df['Agent'+str(j+1)+'_Consumptive_Use_Rate']=yy
					#df['Agent'+str(j+1)+'_Tributary_Combination']=zz
					#df['Agent'+str(j+1)+'_Water_Withdrawn']=aaa
					#df['Agent'+str(j+1)+'_Return_Flow']=bbb
					#df['Agent'+str(j+1)+'_Price_per_Withdrawal']=ccc
					#df['Agent'+str(j+1)+'_River_Miles']=ddd
					df['Agent'+str(j+1)+'_c_bar']=eee
					#df['Agent'+str(j+1)+'_w_bar']=fff
					df['Agent'+str(j+1)+'_Allowable_Water']=ggg
					#df['Agent'+str(j+1)+'_Technology']=hhh
					#df['Agent'+str(j+1)+'_Total_Water_Withdrawn']=iii
					#df['Agent'+str(j+1)+'_Land_acres']=jjj
					df['Agent'+str(j+1)+'_Seniority']=kkk
					#df['Agent'+str(j+1)+'_Exogenous_Crop_Price']=lll
					#df['Agent'+str(j+1)+'_Yield']=mmm
					#df['Agent'+str(j+1)+'_Revenue']=nnn
					#df['Agent'+str(j+1)+'_Profit_Seller']=ooo
					#df['Agent'+str(j+1)+'_Profit_Buyer']=ppp
					#df['Agent'+str(j+1)+'_WTA']=qqq
					#df['Agent'+str(j+1)+'_WTP']=rrr
					#df['Agent'+str(j+1)+'_Bid_Price']=sss
					#df['Agent'+str(j+1)+'_Ask_Price']=ttt
					#df['Agent'+str(j+1)+'_AV_Index_Seller']=uuu
					#df['Agent'+str(j+1)+'_AV_Index_Buyer']=vvv
				df.to_csv('bilateral_baseline_datafile/all_agents_data_pos_try23_dr_no.csv',index=False)
				
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
				
				#vat_s=[]
				vat_b=[]
				vbt_s=[]
				#indicator_s = np.zeros(num_of_agents)
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
				#for i in range(num_of_agents):
				#	if sen_list[i]<=dr_no-1:
				#		all_agent_price2[i]=np.array(all_agent_price2[i])
				#		if ((all_agent_price2[i]==0).all())==True:
				#			vat_s.append(all_agent_AV[i][-1]*all_agent_c_bar[i][-1])
				#for i in range(num_of_agents):
				#	if sen_list[i]>dr_no-1:
				#		all_agent_price1[i]=np.array(all_agent_price1[i])
				#		if ((all_agent_price1[i]>0).any())==True:
				#			vat_b.append(all_agent_AV[i][-1]*all_agent_endow[i][-1])
				#for i in range(num_of_agents):
				#	if sen_list[i]<=dr_no-1:
				#		vbt_s.append(all_agent_AV[i][0]*all_agent_c_bar[i][0])

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
					
				pvi.append((sum(qq_gft)/(sum(int_AV_s)+sum(int_AV_b)))*100)
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
				
				print('Total Initial AV for Sellers: ',sum(int_AV_s))
				print('Total Final AV for Sellers: ',sum(fin_AV_s))
				print('Total Initial AV for Buyers: ',sum(int_AV_b))
				print('Total Final AV for Buyers: ',sum(fin_AV_b))
				print('Total Percentage of Agents Trading: ',trade_percent[jj])
			
				##this prints number of agents that are cut-off
				print('Number of agents that are cut-off: ',(num_of_agents-dr_no+1)) #+no_sen,'(',num_of_agents-dr_no+1,'for drought number &',no_sen,'for no seniority)')


				print('-------------------')
				if ii==0:
					print('The model shows trade after ',ii+1,' try!!!')
				if ii>0:
					print('The model shows trade after ',ii+1,' tries!!!')
				print('-------------------')
				##ends here
				break
	pvi_all.append(pvi)
	trade_percent_all.append(trade_percent)
	water_held_all_s.append(water_held_tot_s)
	water_held_all_b.append(water_held_tot_b)
	water_allow_all_s.append(water_allow_tot_s)
	water_allow_all_b.append(water_allow_tot_b)
	av_all_s.append(av_tot_s)
	av_all_b.append(av_tot_b)
	gft_all_old.append(gft_tot_old)
	gft_all_new.append(gft_tot_new)

	my_dict={'Percentage_of_Sellers':perc_sellers,'Percentage_Value_Increased':pvi,'Percentage_of_Agents_Trading':trade_percent,'Consumptive_Use_Sellers':water_held_tot_s,'Consumptive_Use_Buyers':water_held_tot_b,'Volume_Quantity_Filled_Sellers':water_allow_tot_s,'Volume_Quantity_Filled_Buyers':water_allow_tot_b,'Initial_AV_Sellers':av_tot_s,'Initial_AV_Buyers':av_tot_b}
	df=pd.DataFrame(my_dict)
	df.to_csv('bilateral_baseline_datafile/results_data_simulation_'+str(ppp+1)+'.csv',index=False)
	
	print('###############################')
	print('###############################')
	print('Done with simulation number: ',ppp+1,'!! Phew!!')
	print('###############################')
	print('###############################')

pvi_avg=[]
gft_old_avg=[]
gft_new_avg=[]
trade_percent_avg=[]
water_held_avg_s=[]
water_held_avg_b=[]
water_allow_avg_s=[]
water_allow_avg_b=[]
av_avg_s=[]
av_avg_b=[]

for i in range(len(perc_sellers)):
	aaa=[]
	bbb=[]
	ccc=[]
	ddd=[]
	eee=[]
	fff=[]
	ggg=[]
	hhh=[]
	iii=[]
	jjj=[]
	for j in range(10):
		aaa.append(pvi_all[j][i])
		bbb.append(trade_percent_all[j][i])
		ccc.append(water_held_all_s[j][i])
		ddd.append(water_held_all_b[j][i])
		eee.append(water_allow_all_s[j][i])
		fff.append(water_allow_all_b[j][i])
		ggg.append(av_all_s[j][i])
		hhh.append(av_all_b[j][i])
		iii.append(gft_all_old[j][i])
		jjj.append(gft_all_new[j][i])
		
	pvi_avg.append(np.mean(aaa))
	trade_percent_avg.append(np.mean(bbb))
	water_held_avg_s.append(np.mean(ccc))
	water_held_avg_b.append(np.mean(ddd))
	water_allow_avg_s.append(np.mean(eee))
	water_allow_avg_b.append(np.mean(fff))
	av_avg_s.append(np.mean(ggg))
	av_avg_b.append(np.mean(hhh))
	gft_old_avg.append(np.mean(iii))
	gft_new_avg.append(np.mean(jjj))


my_dict={'Percentage_of_Sellers':perc_sellers,'Percentage_Value_Increased':pvi_avg,'GFT_old':gft_old_avg,'GFT_new':gft_new_avg,'Percentage_of_Agents_Trading':trade_percent_avg,'Consumptive_Use_Sellers':water_held_avg_s,'Consumptive_Use_Buyers':water_held_avg_b,'Volume_Quantity_Filled_Sellers':water_allow_avg_s,'Volume_Quantity_Filled_Buyers':water_allow_avg_b,'Initial_AV_Sellers':av_avg_s,'Initial_AV_Buyers':av_avg_b}
df=pd.DataFrame(my_dict)
df.to_csv('bilateral_baseline_datafile/try_23_bilateral_baseline_avg_data.csv',index=False) #,columns=['Percentage_of_Sellers','Percentage_Value_Increased','Percentage_of_Agents_Trading','Water_held_in_Water_Rights'])

