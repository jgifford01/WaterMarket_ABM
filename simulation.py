from core import Trade_Model
import random
import numpy as np
import random
import pandas as pd


perc_sellers=[10,20,30,40,50,60,70,80,90] #Percentage sellers indicate that out of 500 agents 10% or 20% are sellers: 10% sellers = 50 sellers and 450 buyers. These correspond to the inverse? dr_num variable -> 10%,20%,...,90% of sellers ==50,100,...,450
pvi_all=[] # percentage value increased
trade_percent_all=[] #percent of agents who trade
water_held_all_s=[] # qty of water held by sellers	
water_held_all_b=[] # qty of water held by buyers
water_allow_all_s=[] # allowable qty of water to divert by sellers
water_allow_all_b=[] # allowable qty of water to divert by buyers
av_all_s=[] # average value of water held by sellers
av_all_b=[] # average value of water held by buyers

# gains from trade after 10 iterations
gft_all_old=[] # same as gft_tot_old
gft_all_new=[] # same as gft_tot_new


for ppp in range(10): # model will run through the simulation 10 times 
	dr_num=[50,100,150,200,250,300,350,400,450] # if 50, agents 1-50 are sellers, and 51-500 are buyers
	gft_tot_old=[] # same as gft_all_old
	gft_tot_new=[] # same as gft_all_new
	trade_percent=[] # same as trade_percent_all
	pvi=[] # same as pvi_all
	water_held_tot_b=[] # same as water_held_all_b
	water_allow_tot_b=[] # same as water_allow_all_b
	water_held_tot_s=[] # same as water_held_all_s
	water_allow_tot_s=[] # same as water_allow_all_s
	av_tot_s=[] # same as av_all_s
	av_tot_b=[] # same as av_all_b

	for jj in range(len(dr_num)): # runs simulation for each drought number (each scenario)
		a_once=500
		for ii in range(500):
			##main simulation portion
			print('Try number: ',ii+1)
			

			a = a_once #input("How many agents? : ") /// a_once = 500 from above
			b = 1000 #input("How many steps? : ") #initial iteration number

			num_agents = int(a) # =a=a_once=500
			iterations = int(b)

			num_of_agents=num_agents #int(no_sen+yes_sen) #total agents
			# Why are we setting all of these inside of the for loop? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			dr_no =int(dr_num[jj]) #int(num_of_agents/2 +1 ) #random.randint(1,num_of_agents) # #
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


			if sum(qq_gft) != 0:
				
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
					eee = all_agent_c_bar[j]
					ggg = all_agent_allow_water[j]
					kkk = all_agent_seniority[j]
					df['Agent'+str(j+1)+'_Buying_Price'] = qq
					df['Agent'+str(j+1)+'_Selling_Price'] = ss
					df['Agent'+str(j+1)+'_Consumptive_Use'] = rr
					df['Agent'+str(j+1)+'_Slope']=tt
					df['Agent'+str(j+1)+'_Intercept']=uu
					df['Agent'+str(j+1)+'_AV']=vv
					df['Agent'+str(j+1)+'_Gain']=ww
					df['Agent'+str(j+1)+'_Crop_based_Consumptive_Use']=xx
					df['Agent'+str(j+1)+'_c_bar']=eee
					df['Agent'+str(j+1)+'_Allowable_Water']=ggg
					df['Agent'+str(j+1)+'_Seniority']=kkk

				df.to_csv('all_agents_data_pos_try23_dr_no.csv',index=False)
				
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
	df.to_csv('results_data_simulation_'+str(ppp+1)+'.csv',index=False)
	
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
df.to_csv('try_23_bilateral_baseline_avg_data.csv',index=False) #,columns=['Percentage_of_Sellers','Percentage_Value_Increased','Percentage_of_Agents_Trading','Water_held_in_Water_Rights'])
