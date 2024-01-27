"""
Here is a link to a relevant GPT chat that helped restructure the code.
https://chat.openai.com/share/e692c7e4-9d60-4bec-b538-128741793882

This file contains the core functions template for the ABM Baseline simulation. 
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

import numpy as np

def generate_trib_combinations(set1, comb_no):
    # Function to generate all combinations of 0 and 1 of length k
    trib_comb_1 = []
    printAllKLength(set1, comb_no, "", len(set1), comb_no, trib_comb_1)
    trib_comb_list = [item for item in trib_comb_1 if item[0] == '1']
    return trib_comb_list

def printAllKLength(set1, k, prefix, n, k_original, trib_comb_1):
    if k == 0:
        trib_comb_1.append(prefix)
        return
    for i in range(n):
        new_prefix = prefix + set1[i]
        printAllKLength(set1, k - 1, new_prefix, n, k_original, trib_comb_1)

class MyAgent(Agent):
    # Agent class definition
    def __init__(self, agent_id, cu, ex_price, trib_comb_list, riv_m, cur, water, ret_fl, tech, sen, land, tot_water, model):
        super().__init__(agent_id, model)
        self.agent_id = agent_id
        self.cu = cu
        self.ex_price = ex_price
        self.trib_comb = trib_comb_list[agent_id]
        self.riv_m = riv_m
        self.cur = cur
        self.water = water
        self.ret_fl = ret_fl
        self.tech = tech
        self.sen = sen
        self.land = land
        self.tot_water = tot_water
    #More stuff to add here

    def step(self):
        # Agent step logic goes here
        pass

class TradeModel(Model):
    # Model class definition
    def __init__(self, num_of_agents, cu, ex_price, trib_comb_list, riv_m, cur, water, ret_fl, tech, sen_list, land, tot_water, seed=None):
        super().__init__(seed=seed)
        self.num_of_agents = num_of_agents
        self.schedule = RandomActivation(self)
        self.create_agents(cu, ex_price, trib_comb_list, riv_m, cur, water, ret_fl, tech, sen_list, land, tot_water)

    def create_agents(self, cu, ex_price, trib_comb_list, riv_m, cur, water, ret_fl, tech, sen_list, land, tot_water):
        for i in range(self.num_of_agents):
            agent = MyAgent(i, cu[i], ex_price[i], trib_comb_list, riv_m[i], cur[i], water[i], ret_fl[i], tech[i], sen_list[i], land[i], tot_water[i], self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

    def mystep(self):
        for agent in self.schedule.agents:
            agent.step()

# Additional utility functions can be added here
