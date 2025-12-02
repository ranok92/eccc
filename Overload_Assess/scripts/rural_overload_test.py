# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:55:03 2025

@author: weixu
"""

import pandapower as pp
import pandas as pd
from build_net import build_net_rural 

from util import get_bus_index_by_name 
import os
import numpy as np
import glob
from copy import deepcopy
from heatpump_overload_utils import get_electricity_24h_heating_elctric_demand_area

import ipdb 


def loading_assess_rural(net, nonEV_info , EV_load = None, heating_load=None):
    '''
    nonEV_info = pandas.df with cols of 
                    bus name, energy use per day
    
    EV_load = {'bus_3':  EV_load_of_bus_3,
               'bus_5': EV_load_of_bus_5,
              ...}
    heating_load = {
                    'bus_3': Heating_load_of_bus_3,
                    'bus_5': Heating_load_of_bus_5. 
                    ...
                    }
    
    '''
    
    dt = pd.read_excel('../data/nonEV_norm_without_heating.xlsx')
    

    if heating_load is not None:
        normalized_res_profile = dt['residential_wo_heating']
    else:
        normalized_res_profile = dt['residential']
    
    
    #  
    time_stamp = dt['time']
    
    output_table = pd.DataFrame()   
    output_table['T_type'] = net.trafo['name']
    output_table[ 'sn_mva']=  net.trafo['sn_mva']
    
    
    output_table_line = pd.DataFrame() 
    for _ in ['std_type','length_km','max_i_ka']:
    
        output_table_line[_] = net.line[_]
    #   
    
    
    
    for t in time_stamp[:]:
        
        for  i in range(len(nonEV_info)):
        # bus, E_per_day in nonEV_info :
            bus, E_per_day   = nonEV_info.iloc[i,0], nonEV_info.iloc[i,1]
            bus_name = 'bus_{}'.format(bus)
            
            
            bus_idx =  get_bus_index_by_name(net,  bus_name)
            # net.bus.name == bus_name
            net.bus.index[ net.bus.name == bus_name]
            # get_bus_index_by_name(net,  bus_name)
            # xx
            load_  =  normalized_res_profile[t]* E_per_day
            
            if EV_load is not None:
                load_  += EV_load[bus_name][t]
            if heating_load is not None:
                load_ +=heating_load[bus_name][t]
        
            pp.create_load(net,  bus_idx ,
                            p_mw = load_ )
        
        
        pp.runpp(net, algorithm='iwamoto_nr',enforce_q_lims=True,  max_iteration=50, tolerance_mva=1e-4,  debug=True)
        time_stamp_key = '{}'.format(t)
        output_table[time_stamp_key ] = net.res_trafo['loading_percent']
        
        
        output_table_line[time_stamp_key ] =net.res_line['loading_percent']
        # print(net.res_line.head(5)  ) 
        # print(net.line.head(5))
        # xx
        
        net.load.drop(net.load.index, inplace=True)
        
    return  output_table,  output_table_line
    


def run_rural_overload_assessment(ev_load_profile_file, include_hp=True):
    ev_load = pd.read_excel(ev_load_profile_file)
            
    parent_folder = ev_load_profile_file.split('/')[-2]
    ev_load_fname = ev_load_profile_file.split('/')[-1].split('.')[0]
    grow_rate = 1.011**5 # updated
    # fig = plt.figure(figsize=(10,15))
    k=grow_rate**2
    data_dict = {}

    for year in range(2025, 2055,5):

        print('running the year of {}'.format(year))
        
        pop_growth_rate = pop_growth_area[
                            pop_growth_area['year']==year
                                    ]['rel_pop_change_frac'].item()
        # A multiplication factor of (0.22/0.48) is applied to only account for 
        
        
        if include_hp:
            E_daily_energy = 13.3*1e-3 *k   # daily energy of a household  [MWh]

        else:
            # non heating related usage.
            E_daily_energy = 41*1e-3 *k   # daily energy of a household  [MWh]


        #non EV non heating load 
        k*= grow_rate
        
        net = build_net_rural ()
        
        charger_info_year = charger_info[charger_info['year']==year]
        # adding Non EV load 
        nonEV_info = deepcopy(rural_grouped)
        nonEV_info.iloc[:,1] *= E_daily_energy 
        nonEV_info = nonEV_info.rename(columns={'NumOfHouse':'E_per_day'})
        ev_load_dict = {}
        heating_load_dict = {}
        total_evs = 0
        total_load_l1 = total_load_l2 = np.zeros(24)
        for bus_info in rural_grouped.itertuples():
            
            num_houses = bus_info.NumOfHouse*pop_growth_rate
            
            #adding EV load 
            pen_rate = ldev_penetration_rate[
                                ldev_penetration_rate['year']==year
                                    ]['penetration_rate'].item()*1e-2
            evs = num_houses*2*pen_rate
            total_evs+=evs
            l1_chargers = charger_info_year['home_l1'].item()
            l2_chargers = charger_info_year['home_l2'].item() 
            l1_l2_ratio = l1_chargers/(l1_chargers+l2_chargers)
            
            l1_load = (ev_load['home_AC1']*evs*l1_l2_ratio)*(1e-3)
            l2_load = (ev_load['home_AC2']*evs*(1-l1_l2_ratio))*(1e-3)
            ev_load_dict[f'bus_{bus_info.Bus}'] = l1_load+l2_load 
            total_load_l1 += l1_load
            total_load_l2 += l2_load   


            # adding heating load 
            if include_hp:
                total_heating_load = get_electricity_24h_heating_elctric_demand_area(
                                                rephouse_data,
                                            housing_ratio[housing_ratio['year']==year],
                                        num_houses)
                heating_load_dict[f'bus_{bus_info.Bus}'] = total_heating_load
            else:
                heating_load_dict = None
                

        data_dict[year] = {'num_evs': total_evs, 
                        'pen_rate': pen_rate, 
                        'L1_L2_ratio': l1_l2_ratio, 
                        'L1 load' : total_load_l1, 
                        'L2_load': total_load_l2}
        
        print(f"Num EVs: {total_evs} \n Penetration rate: {pen_rate} \n total load l1: {total_load_l1} \n total load l2: {total_load_l2} ")
        output_table_tra,  output_table_line= loading_assess_rural(net, 
                                                                nonEV_info, 
                                                                ev_load_dict, 
                                                                heating_load_dict) 


        folder = f'../results_new_non_hp/Results_{parent_folder}_{ev_load_fname}_rural/'
        os.makedirs(os.path.dirname(folder), exist_ok=True)
        os.makedirs(os.path.dirname(folder), exist_ok=True)
        pd.DataFrame(ev_load_dict).to_csv(f'{folder}/{year}_ldev_load.csv')
        pd.DataFrame(heating_load_dict).to_csv(f'{folder}/{year}_space_heat_cool_load.csv')
        pd.DataFrame(data_dict).to_excel('{}evinfo.xlsx'.format(folder, year))
        output_table_tra.to_excel('{}EV{}_tra.xlsx'.format(folder, year))
        output_table_line.to_excel('{}EV{}_line.xlsx'.format(folder, year))

    
if __name__=='__main__':
    
    '''
    rural network nonEV loading assessment
    
    '''    

    # 
    rural_info = pd.read_excel('../data/rural_net_household_distribution.xlsx' ).iloc[:,[0,2]]
    ldev_penetration_rate = pd.read_csv('../data/ldev_load_data/penetration_rate_ldev.csv') #in percentage
    charger_info = pd.read_excel("../data/ldev_load_data/chargers_for_1000_vehicles.xlsx")
    pop_growth = pd.read_csv('../data/ldev_load_data/population_change_diff_areas.csv') #in fraction

    # heat pump related data
    
    housing_ratio = pd.read_csv(
        '../data/heatpump/representative_houses/ratio_of_housetypes_in_network_across_years.csv')
    rephouse_data = pd.read_csv(
        '../data/heatpump/representative_houses/quebec_representative_house_heating_cooling_stats.csv')
    
    # adding multiple EV load pattern files
    base_folder_ev_charging_pattern = '../data/ldev_load_data/alternate_charging_scenarios/profiles_v5'

    #ev_load_profile_files = glob.glob(f'{base_folder_ev_charging_pattern}/EV_load_*.xlsx') 

    ev_load_profile_files = ['../data/ldev_load_data/EV_load_profiles_daily_req.xlsx']
    #ev_load = pd.read_excel('./data/ldev_load_data/EV_load_profiles_daily_req.xlsx') 

    rural_grouped = rural_info .groupby('Bus', as_index=False).sum()    
    # rural_grouped.iloc[:,1] = rural_grouped.iloc[:,1].astype('float64')
    pop_growth_area = pop_growth[pop_growth['area']=='rural']

    for ev_load_profile_file in ev_load_profile_files:


        run_rural_overload_assessment(ev_load_profile_file, include_hp=False)
        