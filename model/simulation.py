import time
import pandas as pd
from core import TradeModel, generate_trib_combinations, MyAgent
import random

def initialize_agents(num_of_agents, dr_no, num_list, ex_price_list, tech_list, sen_list, land_low, land_high):
    # Function to initialize agent data
    cu = []
    ex_price = []
    trib_comb_list = generate_trib_combinations(['0', '1'], 4)
    riv_m = []
    cur = []
    water = []
    ret_fl = []
    tech = []
    land = []
    tot_water = []

    for i in range(num_of_agents):
        if sen_list[i] <= dr_no - 1:
            rand_id = random.randrange(len(num_list))
            cu.append(num_list[rand_id])
            ex_price.append(ex_price_list[rand_id])
            trib_comb_list.append(random.choice(trib_comb_list))
            for j in range(4):
                if len(trib_comb_list[i]) == j + 1:
                    riv_m.append((j + 1) * 1001)
            riv_m_start = riv_m[-1] - 1000
            riv_m.append(random.randint(riv_m_start, riv_m[-1]))
            cur.append(random.uniform(0.001, 0.999))
            water.append(cu[i] / cur[i])
            ret_fl.append(water[i] - cu[i])
            tech.append(random.choice(tech_list))
            land.append(random.uniform(land_low, land_high))
            tot_water.append(water[i] * land[i])
        elif sen_list[i] > dr_no - 1:
            rand_id = random.randrange(len(num_list))
            cu.append(num_list[rand_id])
            ex_price.append(ex_price_list[rand_id])
            trib_comb_list.append(random.choice(trib_comb_list))
            for j in range(4):
                if len(trib_comb_list[i]) == j + 1:
                    riv_m.append((j + 1) * 1001)
            riv_m_start = riv_m[-1] - 1000
            riv_m.append(random.randint(riv_m_start, riv_m[-1]))
            cur.append(random.uniform(0.001, 0.999))
            water.append(0)
            ret_fl.append('NA')
            tech.append(random.choice(tech_list))
            land.append(random.uniform(land_low, land_high))
            tot_water.append('NA')

    return num_of_agents, cu, ex_price, trib_comb_list, riv_m, cur, water, ret_fl, tech, sen_list, land, tot_water

def run_simulation(iterations, model):
    # Function to run the simulation
    for i in range(iterations):
        model.mystep()

def collect_agent_data(model, num_of_agents, iterations):
    # Function to collect agent data
    agent_variables = model.datacollector.get_agent_vars_dataframe()

    all_agent_data = {'AgentID': list(range(num_of_agents))}

    for i in range(num_of_agents):
        one_agent_data = agent_variables.xs(i, level='AgentID')
        for key in one_agent_data.keys():
            if key not in all_agent_data:
                all_agent_data[key] = [one_agent_data[key][0]] * iterations
            else:
                all_agent_data[key].extend(list(one_agent_data[key]))

    return all_agent_data

def save_simulation_results(all_agent_data, num_of_agents, iterations):
    # Function to save simulation results to a CSV file
    my_dict = {'Step': list(range(1, iterations + 1))}
    df = pd.DataFrame(my_dict)

    for j in range(num_of_agents):
        agent_data = {f'Agent{j+1}_{key}': all_agent_data[key][j] for key in all_agent_data}
        df = pd.concat([df, pd.DataFrame(agent_data)], axis=1)

    df.to_csv('all_agents_data_pos_try23_dr_no.csv', index=False)

def main():
    start_time = time.time()

    # Simulation parameters
    num_of_agents = 10
    dr_no = 5
    num_list = [0.625, 1.25, 1.875, 2.5, 3.125, 3.75, 4.375, 5]
    ex_price_list = [1, 2, 3, 4, 5, 6, 7, 8]
    tech_list = [1, 2, 3, 4, 5, 6]
    land_low = 2
    land_high = 172
    iterations = 100

    # Initialize agents
    agents_data = initialize_agents(num_of_agents, dr_no, num_list, ex_price_list, tech_list, sen_list, land_low, land_high)

    # Create an instance of TradeModel
    model = TradeModel(*agents_data)

    # Run the simulation
    run_simulation(iterations, model)

    # Collect agent data
    all_agent_data = collect_agent_data(model, num_of_agents, iterations)

    # Save simulation results
    save_simulation_results(all_agent_data, num_of_agents, iterations)

    end_time = time.time() - start_time
    print('Simulation completed in', end_time, 'seconds.')

if __name__ == "__main__":
    main()
