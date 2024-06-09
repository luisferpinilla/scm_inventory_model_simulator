# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 22:36:15 2024

@author: luisf
"""

import pandas as pd
import numpy as np
from inventory_models.periodic_order import run_simualation as run_periodic
from inventory_models.reorder_point import run_simualation as run_reorder
from inventory_models.demand_models import Normal_Demand
from tqdm import tqdm
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Inventory Simulators", layout="wide")

st.markdown(body="# General Parameters")

demand_mean = st.number_input(label="Expected demand mean", min_value=0, value=50)
demand_std = st.number_input(label="Expected standar deviation demand", min_value=0, value=5)
replics= st.number_input(label="how many replics do you want to run?", min_value=100, max_value=500, value=200)
initial_inventory = st.number_input(label="What is the initial inventory?", min_value=0, value= 500)
periods_to_simulate = st.number_input(label="How many periods do you want to simulate?", min_value=0, value=52)
lead_time = st.number_input(label="What is the Lead Time?", min_value=0, value=3)

reorder_parameters_column, periodic_parameters_column = st.columns(2)

with reorder_parameters_column:
    st.markdown("## Reorder point inventory model")
    reorder_point = st.number_input(label="What is the reorder point?", min_value=1, value=200)
    quantity_to_order = st.number_input(label="What is the quantity to order when get the reorder point?", min_value=0, value=400)

with periodic_parameters_column:
    st.markdown("## Periodic inventory model")
    maximun_inventory = st.number_input(label="What is the maximun inventory?", min_value=1, value=600)
    review_period = st.number_input(label="What is the review period?", min_value=1, value=4)

submit = st.button(label="Run simulation")

if submit:
    normal_demand = Normal_Demand(mean=demand_mean, std_dev=demand_std)

    with st.spinner(text="Running simulations..."):

        reorder_df = pd.concat([run_reorder(sim_id=idsim,
                                            initial_inventory=initial_inventory,
                                            demand=normal_demand,
                                            reorder_point=reorder_point,
                                            quantity_to_order=quantity_to_order,
                                            periods_to_simulate=periods_to_simulate,
                                            leadtime=lead_time) for idsim in tqdm(range(replics))])

        periodic_df = pd.concat([run_periodic(sim_id=idsim,
                            initial_inventory=initial_inventory,
                            demand=normal_demand,
                            maximun_inventory=maximun_inventory,
                            review_period=review_period,
                            periods_to_simulate=periods_to_simulate,
                            leadtime=lead_time) for idsim in tqdm(range(replics))])
    
    reorder_column, periodic_column = st.columns(2)

    with reorder_column:

        report_df = reorder_df.groupby(['periodo']).agg(min =  pd.NamedAgg(column='inventario_final', aggfunc='min'),
                                                        max =  pd.NamedAgg(column='inventario_final', aggfunc='max'),
                                                        mean = pd.NamedAgg(column='inventario_final', aggfunc='mean'),
                                                        p_75 =   pd.NamedAgg(column='inventario_final', aggfunc=lambda x: np.percentile(x, 75)), 
                                                        p_25 =   pd.NamedAgg(column='inventario_final', aggfunc=lambda x: np.percentile(x, 25))).reset_index()
                                                                                         
        
        report_df = pd.melt(frame=report_df, id_vars='periodo', 
                            value_vars=['min', 
                                        'max', 
                                        'mean',
                                        'p_75', 
                                        'p_25'],
                            value_name='value',
                            var_name='stats')
        
        fig = px.line(report_df, x="periodo", y="value", symbol='stats', color='stats')
        
        fig.update_layout(title='Reorder Point Model', xaxis_title='Period', yaxis_title='Final')

        st.plotly_chart(fig, use_container_width=True)


    with periodic_column:

        report_df = periodic_df.groupby(['periodo']).agg(min =  pd.NamedAgg(column='inventario_final', aggfunc='min'),
                                                        max =  pd.NamedAgg(column='inventario_final', aggfunc='max'),
                                                        mean = pd.NamedAgg(column='inventario_final', aggfunc='mean'),
                                                        p_75 =   pd.NamedAgg(column='inventario_final', aggfunc=lambda x: np.percentile(x, 75)), 
                                                        p_25 =   pd.NamedAgg(column='inventario_final', aggfunc=lambda x: np.percentile(x, 25))).reset_index()
                                                                                         
        
        report_df = pd.melt(frame=report_df, id_vars='periodo', 
                            value_vars=['min', 
                                        'max', 
                                        'mean'],
                            value_name='value',
                            var_name='stats')
        
        fig = px.line(report_df, x="periodo", y="value", symbol='stats', color='stats')
        
        fig.update_layout(title='Periodic Model', xaxis_title='Period', yaxis_title='Final')
        st.plotly_chart(fig, use_container_width=True)

    






