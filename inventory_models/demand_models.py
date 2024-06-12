# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 18:24:03 2024

@author: luisf
"""

import numpy as np


class Demand():
    
    def next_value(self):
        pass


class Normal_Demand(Demand):
    
    def __init__(self, mean:float, std_dev:float, allow_negative=False):
        
    
        self.mean = mean
        self.std_dev = std_dev
        self.negative = allow_negative
        
    def next_value(self) -> float:
        
        value = -1.0
        
        while value < 0.0 and not self.negative:
            value = np.random.normal(loc=self.mean, scale=self.std_dev)
        
        return value

class Poisson_Demand(Demand):
    
    def __init__(self, mean:float):
            
        self.mean = mean
        
    def next_value(self) -> int:
        
        value = np.random.poisson(lam=self.mean)
        
        return value