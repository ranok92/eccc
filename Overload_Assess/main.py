# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 05:45:32 2024

@author: weixu
""" 


from matplotlib import pyplot as plt
import pandas as pd
import os

from overload_assessment import loading_assess 

def EV_growth(ev, rate):
    out={}
    for area , ev in EV_load.items():
        out[area] = ev* rate
    return out



'''
overloading assessment with EV loads

'''



EV_load0 = pd.read_excel('EV_load.xlsx')
EV_load={}
EV_load['Res'] = EV_load0['Residential']*1e-3 * 2*2 
EV_load['Comm'] = EV_load0['Commercial']*1e-3 * 10
EV_load['Pub'] = EV_load0['Public']*1e-3 *1
ev_growth_rate = 1.05**5


res = 0.48
comm=20
pub=6.8
grow_rate = 1.016**5
# fig = plt.figure(figsize=(10,15))
k=1
k_ev =1
for year in range(2015, 2055,5):
    print('running the year of {}'.format(year))
    bus_load = {'Res':  res*k , 'Comm': comm*k, 'Pub': pub*k} #MWh per day
    k*= grow_rate
    
    
    ev_load =  EV_growth(EV_load, k_ev) 
    k_ev  *= ev_growth_rate 
    
    output_table =  loading_assess(bus_load ,ev_load )
    
    
    os.makedirs(os.path.dirname('./Results/'), exist_ok=True)
    output_table.to_excel('./Results/withEV{}.xlsx'.format(year))
    
    



