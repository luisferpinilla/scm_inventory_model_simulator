# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 23:13:18 2024

@author: luisf
"""
import pandas as pd
import numpy as np
from inventory_models.demand_models import Demand

def run_simualation(sim_id:int,
                    initial_inventory:float, 
                    demand: Demand,
                    reorder_point:float, 
                    quantity_to_order:float,
                    periods_to_simulate:int,
                    leadtime:int)->pd.DataFrame:
    
    maximun_inventory = reorder_point + quantity_to_order

    period = list()
    arrivals = dict()

    inventario_final = 0
    
    for t in range(periods_to_simulate):
        
        if t == 0:
            inventario_inicial = initial_inventory
        else:
            inventario_inicial = inventario_final
            
        demanda = demand.next_value()
        
        if t in arrivals.keys():
            llegadas = arrivals[t]
        else:
            llegadas=0
            
        inventario_final = inventario_inicial - demanda + llegadas
        
        pedidos = np.sum([arrivals[x] for x in range(t, periods_to_simulate + leadtime) if x in arrivals.keys()])
        
        inventory_position = inventario_inicial - demanda + pedidos
        
        if inventory_position <= reorder_point:
            pedido = quantity_to_order
            arrivals[t+leadtime] = pedido
        else:
            pedido = 0
        
        period.append({
                "id_sim":sim_id,
                "periodo":t,
                "inventario_inicial": inventario_inicial,
                "inventory_position":inventory_position,
                "maximun_inventory":maximun_inventory,
                "reorder_point":reorder_point,
                "quantity_to_order": quantity_to_order,
                "llegadas": llegadas,
                "demanda":demanda,
                "pedido":pedido,
                "inventario_final":inventario_final
            })
        
    return pd.DataFrame(period)
        



    
    