# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 05:45:32 2024

@author: weixu & abhi
""" 


from matplotlib import pyplot as plt
import pandas as pd
import os

from overload_assessment import loading_assess 
from build_net import build_net_2  

def EV_growth(ev, rate):
    out={}
    for area , ev in EV_load.items():
        out[area] = ev* rate
    return out



'''
overloading assessment with EV loads

based on penetration rate

'''



EV_load0 = pd.read_excel('./data/EV_load_profiles_gen.xlsx')
# load profile of one charger; each charger assumed to serve one ev per day


penetrationRate = pd.read_excel('./data/penetrationRate.xlsx').set_index('year' )


net0 = build_net_2()
bus_temp = net0.bus['zone']

total_res_bus = len(bus_temp[bus_temp=='Res']  )
total_comm_bus = len(bus_temp[bus_temp=='Comm'] )
total_public_bus = len(bus_temp[bus_temp=='Pub'] )




# nonEV energy consumption per day on the base year 2015
res = 0.48
comm=20
pub=6.8
grow_rate = 1.016**5
# fig = plt.figure(figsize=(10,15))
k=1
# k_ev =1
for year in range(2015, 2055,5):
    net = build_net_2()
    print('running the year of {}'.format(year))
    bus_load = {'Res':  res*k , 'Comm': comm*k, 'Pub': pub*k} #MWh per day
    k*= grow_rate
    
    
    
    ev_per_resbus = 15 *  2 *penetrationRate.loc[year, 'penetr'] /100
    charger_per_res_bus =  ev_per_resbus * 1   # assume one charger port per ev in residential area 
    
    # calculate total ev on a net, based on the num of residents
    total_ev =  ev_per_resbus * total_res_bus
    # work area charger ratio tab 20
    charger_per_comm_bus = total_ev * 60/1000    / total_comm_bus  
    
    # public area charger ratio tab 20
    charger_per_public_bus = total_ev * 40/1000 /  total_public_bus 
    
    
    
    
    
    
    EV_load={}
    
    # table 21: res area AC2 : AC1 = 12:3
    # assume AC2 serve 0.7 ev per day
    EV_load['Res'] = (EV_load0['home_AC2'] * 12/15 * .7 +  EV_load0['home_AC1']* 3/15 ) \
        *1e-3 *  charger_per_res_bus 
    
    # tab 21: work area AC2:AC1=13:5
    EV_load['Comm'] = (EV_load0['work_AC2'] *13/18 +  EV_load0['work_AC1'] *5/18 )    \
        *  charger_per_comm_bus*1e-3 
        
    # tab 21: pub area AC2:DC=9:3
    EV_load['Pub'] = ( EV_load0['public_AC2'] *9/12 +  EV_load0['public_DC'] * 3/12 ) \
        *1e-3 *    charger_per_public_bus
    
    
    ev_load = EV_load
    
    
    
    output_table =  loading_assess(net, bus_load ,ev_load )
    
    folder = './results/ResultsJan2/'
    os.makedirs(os.path.dirname(folder), exist_ok=True)
    output_table.to_excel('{}withEV{}.xlsx'.format(folder, year))
    
    



