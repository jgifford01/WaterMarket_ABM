from mesa import Agent
import numpy as np

class WaterAgent(Agent):
    def __init__(self, unique_id, model, acreage, alpha, beta, cbar, 
                 avbar, acbar, pro, c, sigma, trib_vector):
        super().__init__(unique_id, model)
        self.acreage = acreage
        self.alpha = alpha
        self.beta = beta
        self.cbar = cbar
        self.avbar = avbar
        self.acbar = acbar
        self.pro = pro
        self.c = c
        self.sigma = sigma
        self.trib_vector =trib_vector 

    @classmethod
    def create_agent(cls, unique_id, model, aw, alphaw, betaw, cbar0, stream_complexity):
        acreage = 1 #aw * np.random.rand() + 1 // this allows for the GFT to be accurate to paper
        alpha = alphaw * np.random.uniform(20, 40)
        beta = betaw * np.random.uniform(1, 2)
        cbar = alpha / (2 * beta)
        avbar = alpha - beta * cbar
        acbar = acreage * cbar

        trib_vector = np.concatenate(([1], np.random.binomial(1, 0.5, 
                                      size=np.random.randint(1, stream_complexity)), 
                                      [np.random.rand()]))
        return cls(unique_id, model, acreage, alpha, beta, cbar, avbar, acbar, pro=None, c=None, sigma=None, trib_vector=trib_vector)
