class MyAgent(Agent): #Agent Class
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
	
				def trade(self):  # Trading Method
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

					#CASE_1: self=Seller and other_agent=Buyer
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

			