# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:36:53 2024

@author: weixu
"""


import pandapower as pp

from build_net import build_net ,build_net_2 , net_visualize
from matplotlib import pyplot as plt
import pandas as pd
import os

def loading_assess(net, area_type,  bus_load, EV_load=None):
    

    # net = build_net  ()
    # net = build_net_2  ()
    # net_visualize(net )
    # 
    #%%
    pub_bus_name_by_area = {'urban':'Pub', 'suburban': 'Indst'}

    dt = pd.read_excel('./data/nonEV_norm.xlsx')
    
    load_dt = {}
    
    #  residential load
    # https://energyrates.ca/residential-electricity-natural-gas/
    E_house_perday =  bus_load['Res']
    # 0.48
     # 35 1e-3 * 15# unit: mwh
    load_res_per_bus = dt['residential']  * E_house_perday
    idx = net.bus.index[ net.bus['zone'] =='Res']
    load_dt['Res'] = {'load':load_res_per_bus, 'bus':idx}
    
    
    
    #  commercial load
    E_comm_perday = bus_load['Comm']
    # 20 # unit: mwh
    load_comm_per_bus = dt ['commercial']  * E_comm_perday
    idx = net.bus.index[ net.bus['zone'] =='Comm']
    load_dt['Comm'] = {'load':load_comm_per_bus, 'bus':idx}
    
    
    #  public load
    E_pub_perday = bus_load[pub_bus_name_by_area[area_type]]
    # 6.8  # unit: mwh
    if area_type=='suburban':
        load_pub_per_bus = dt ['industrial']   * E_pub_perday
    if area_type=='urban':
        load_pub_per_bus = dt ['street']   * E_pub_perday

    idx = net.bus.index[ net.bus['zone'] ==pub_bus_name_by_area[area_type]]
    load_dt[pub_bus_name_by_area[area_type]] = {'load':load_pub_per_bus, 'bus':idx}
    

    if EV_load is not None:
        for area , ev in EV_load.items():
            load_dt[area]['load'] +=  ev 
    
    #  
    time_stamp = dt['time']
    
    #results for transformers 
    output_table_trafo = pd.DataFrame()   
    output_table_trafo['T_type'] = net.trafo['name']
    output_table_trafo[ 'sn_mva']=  net.trafo['sn_mva']
    
    #results for lines 
    output_table_line = pd.DataFrame() 
    output_table_line['std_type'] = net.line['std_type']
    output_table_line['length_km'] = net.line['length_km']
    output_table_line['max_i_ka'] = net.line['max_i_ka']

    for t in time_stamp[:]:
        # add_load(net, load_dt)
        for area , dt_ in load_dt.items():
            load_ = dt_['load'][t]
            for bus_temp in dt_['bus']:
                load_name = '{} load'.format(area)
                pp.create_load(net,bus_temp ,
                                p_mw = load_, name= load_name)
            
                
        # debug
        # total_load_calc = load_dt['Res']['load'].iloc[t]*len(load_dt['Res']['bus']) + \
        #                         load_dt['Comm']['load'].iloc[t]*len(load_dt['Comm']['bus']) + \
        #                             load_dt[pub_bus_name_by_area[area_type]]['load'].iloc[t]*len(load_dt[pub_bus_name_by_area[area_type]]['bus'])
        # print("total load cacl :", total_load_calc)
        #
        # total_load = net.load.p_mw.sum()
        # total_generation = net.sgen.p_mw.sum() 
        # print(f"Iteration {t}: Total Load = {total_load}, Total Generation = {total_generation}")

        #######

        try:
            pp.runpp(net, algorithm='iwamoto_nr',enforce_q_lims=True,  max_iteration=50, tolerance_mva=1e-4,  debug=True)
        except:
            print(f"Power flow failed at iteration {t}. Checking network...")
            print(net.res_bus[['vm_pu']])  # Check bus voltages
            #print(net.res_line[['loading_percent']])  # Check line loadings
        time_stamp_key = '{}'.format(t)
        output_table_trafo[time_stamp_key] = net.res_trafo['loading_percent']
        output_table_line[time_stamp_key] = net.res_line['loading_percent']

        net.load.drop(net.load.index, inplace=True)
        
    return  output_table_trafo, output_table_line


if __name__ == '__main__':
    res = 0.48
    comm=20
    pub=6.8
    grow_rate = 1.016**5
    # fig = plt.figure(figsize=(10,15))
    k=1
    for year in range(2015, 2055,5):
        
        print('running the year of {}'.format(year))
        
        bus_load = {'Res':  res*k , 'Comm': comm*k, 'Pub': pub*k} #MWh per day
        k*= grow_rate
        output_table =  loading_assess(bus_load)
        
        
        
        os.makedirs(os.path.dirname('./Results/'), exist_ok=True)
        output_table.to_excel('./Results/NonEV{}.xlsx'.format(year))
        
        '''
        output_table contains
        Transformer_type, max_load_limit[MVA], loading_percent_at_0, loading_percent_at_1, ..., loading_percent_at_23, 
        ___________
        
        
        '''
        
        # xx
        #%%
        # T_example =  output_table #.iloc[[0,1,2,6,27]]
        
        
        
        # P =  T_example.iloc[:,3:].to_numpy() *      T_example.iloc[:,1].to_numpy().reshape((-1,1))/100
        # plt.plot(T_example.iloc[:,3:].transpose())
        # for tt in range(5):
        #     plt.subplot(5,1,tt+1)
        #     plt.plot(P [tt,:])
        #     l_name='T{}'.format (year) 
        #     plt.legend(   l_name  )
    # print(P.transpose())
    # for row in P.transpose():
    #     print(" ".join(f"{value:.3f}" for value in row))
