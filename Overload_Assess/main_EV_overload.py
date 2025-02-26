# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 05:45:32 2024

@author: weixu & abhi
""" 


from matplotlib import pyplot as plt
import pandas as pd
import os

from overload_assessment import loading_assess 
from build_net import build_net_2, build_net_suburban, build_net_rural
import ipdb


# def EV_growth(ev, rate):
#     out={}
#     for area , ev in EV_load.items():
#         out[area] = ev* rate
#     return out

def get_area_network(area_name):
    if area_name=='urban':
        return build_net_2()
    elif area_name=='suburban':
        return build_net_suburban() 
    elif area_name=='rural':
        return build_net_rural()
    else:
        raise NotImplementedError("Network not implemented")
'''
overloading assessment with EV loads
Based on:
    1. Change in population
    2. Penetration rate 
    3. Population distribution over housing 

'''

#####  Load  data for LDEV ###### 

# Load profiles for different chargers and locations 
# load profile of one charger; each charger assumed to serve one ev per day

ev_load = pd.read_excel('./data/ldev_load_data/EV_load_profiles_gen.xlsx') 

pop_growth = pd.read_csv('./data/ldev_load_data/population_change_diff_areas.csv') #in fraction

penetration_rate = pd.read_csv('./data/ldev_load_data/penetration_rate_ldev.csv') #in percentage

charger_info = pd.read_excel("./data/ldev_load_data/chargers_for_1000_vehicles.xlsx")
charger_count_multiplier = pd.read_excel("./data/ldev_load_data/public_charger_multiplier_by_area.xlsx")
charger_util_multiplier = pd.read_excel("./data/ldev_load_data/public_charger_util_multiplier_by_area.xlsx")

pub_charger_util_rate = pd.read_excel("./data/ldev_load_data/public_charger_utilization_rate.xlsx")

pop_dist_acc_housing = pd.read_excel("./data/ldev_load_data/population_distribution_acc_house_types.xlsx") 

#######     xxx    #######

# MDEV load related data 

mhdev_vehicle_numbers = pd.read_csv('./data/mhdev_load_data/mhdev_numbers_across_diff_areas.csv')
mdev_load_profiles = pd.read_csv('./data/mhdev_load_data/mdev_load_profiles.csv')
hdev_load_profiles = pd.read_csv('./data/mhdev_load_data/hdev_load_profiles.csv')
mhdev_chargers_data = pd.read_csv('./data/mhdev_load_data/charger_numbers_across_networks_and_years.csv')

mhdev_charger_throughput = {'public_l3': 1, 'public_fast': 6, 'private_l3': 1, 'private_fast': 3}

mdev_distribution_over_chargers = {'private_l3' : 0.72, 'private_fast': 0.14 , 'public_l3': 0, 'public_fast': 0.14}
hdev_distribution_over_chargers = {'private_l3' : 0.25, 'private_fast': 0.06 , 'public_l3': 0.44, 'public_fast': 0.25}

#######     xxx    #######


area_type = ['suburban']

comm_bus_name_by_area = {'urban':'Pub', 'suburban': 'Indst'}

for area in area_type: 
    # build the network 
    net0 = get_area_network(area)
    bus_temp = net0.bus['zone']

    total_res_bus = len(bus_temp[bus_temp=='Res']  )
    total_comm_bus = len(bus_temp[bus_temp=='Comm'] )
    total_public_bus = len(bus_temp[bus_temp==comm_bus_name_by_area[area]] )

    #get external data for given area type

    pop_growth_area = pop_growth[pop_growth['area']== area]
    pop_dist_acc_housing_area = pop_dist_acc_housing[pop_dist_acc_housing['area_type']==area]
    pub_charger_count_multiplier = charger_count_multiplier[charger_count_multiplier['area_type']==area]['multiplier'].item()
    pub_charger_util_multiplier = charger_util_multiplier[charger_util_multiplier['area_type']==area]['multiplier'].item()

    # nonEV energy consumption per day on the base year 2015

    #urban
    if area=='urban':
        res = 0.73
        comm= 23
        pub= 6.8
    else:
        # #suburban
        res = 0.73
        comm = 11.65 
        pub = 16.45  #industrial


    grow_rate = 1.016**5
    k=1
    


    for year in range(2025, 2055, 5):

        ev_count_dict = {}
        charger_count_dict = {}

        net = get_area_network(area)
        print('running the year of {}'.format(year))

        # non EV load 

        bus_load = {'Res':  res*k , 'Comm': comm*k, comm_bus_name_by_area[area]: pub*k} #MWh per day
        k*= grow_rate

        # EV load: LDEV

        # residential charging 

        household_per_bus = 15
        vehicles_per_household = 2
        ldev_pen_rate = penetration_rate[
                            penetration_rate['year']==year
                                ]['penetration_rate'].item()
        pop_growth_rate = pop_growth_area[
                                pop_growth_area['year']==year
                                        ]['rel_pop_change_frac'].item()
        
        ev_per_resbus = household_per_bus * vehicles_per_household * pop_growth_rate * ldev_pen_rate /100 #
        ev_count_dict['EV_per_res_bus'] = ev_per_resbus 
        l1_charger_per_res_bus = charger_info[charger_info['year']==year]['home_l1'].item()*ev_per_resbus/1000 
        l2_charger_per_res_bus = charger_info[charger_info['year']==year]['home_l2'].item()*ev_per_resbus/1000 
        
        charger_count_dict['home_l1_per_resbus'] = l1_charger_per_res_bus
        charger_count_dict['home_l2_per_resbus'] = l2_charger_per_res_bus
        
        # calculate EVs doing home vs public charging

        sfu_percent = pop_dist_acc_housing_area[
                                (pop_dist_acc_housing_area['year']==year) & \
                                (pop_dist_acc_housing_area['house_type']=='single_family_unit')
                                                ]['population_percent'].item()
        sfu_ev_ready_percent = pop_dist_acc_housing_area[
                                (pop_dist_acc_housing_area['year']==year) & \
                                (pop_dist_acc_housing_area['house_type']=='single_family_unit')
                                                ]['ev_ready_percent'].item()
        mfu_ev_ready_percent = pop_dist_acc_housing_area[
                            (pop_dist_acc_housing_area['year']==year) & \
                            (pop_dist_acc_housing_area['house_type']=='multi_family_unit')
                                            ]['ev_ready_percent'].item()
        
        ev_per_bus_sfu = ev_per_resbus * sfu_percent / 100
        ev_per_bus_mfu = ev_per_resbus * (100-sfu_percent) /100

        ev_count_dict['ev_per_bus_sfu'] = ev_per_bus_sfu
        ev_count_dict['ev_per_bus_mfu'] = ev_per_bus_mfu

        # 85% times people with home charging charge at home 
        ev_per_bus_sfu_res_charging = ev_per_bus_sfu * sfu_ev_ready_percent/100 * 0.85 
        ev_per_bus_mfu_res_charging = ev_per_bus_mfu * mfu_ev_ready_percent/100 * 0.85 

        ev_per_res_bus_res_charging = ev_per_bus_sfu_res_charging + ev_per_bus_mfu_res_charging
        ev_count_dict['ev_per_res_bus_res_charging'] = ev_per_res_bus_res_charging

        # we assume residential EV charging is distributed 
        # between L1 and L2 according to the proportion of each type of charger available

        l1charger_fraction = (charger_info[charger_info['year']==year]['home_l1'] /  \
                                    (charger_info[charger_info['year']==year]['home_l1'] + \
                                             charger_info[charger_info['year']==year]['home_l2'])).item()
        
        ev_per_res_bus_res_charging_l1 = ev_per_res_bus_res_charging * l1charger_fraction
        ev_per_res_bus_res_charging_l2 = ev_per_res_bus_res_charging - ev_per_res_bus_res_charging_l1

        ev_count_dict['ev_per_res_bus_res_charging_l1'] = ev_per_res_bus_res_charging_l1
        ev_count_dict['ev_per_res_bus_res_charging_l2'] = ev_per_res_bus_res_charging_l2



        ev_per_res_bus_nonres_charging = ev_per_resbus - ev_per_res_bus_res_charging
        ev_count_dict['ev_per_res_bus_nonres_charging'] = ev_per_res_bus_nonres_charging

        # calculate total ev on a net, based on the num of residents
        total_ev =  ev_per_resbus * total_res_bus
        total_ev_nonres_charging = ev_per_res_bus_nonres_charging * total_res_bus
        

        # work area chargers
        
        # no L1 work charger acc. to Dunsky
        # charger numbers are avg across canada. We multiply by a factor 
        # to differentiate between urban, suburban and rural areas
        charger_mult = pub_charger_count_multiplier
        work_chargers_per_1000_ev = charger_mult*charger_info[charger_info['year']==year]['work_l2'].item()

        l2_charger_per_comm_bus =  work_chargers_per_1000_ev *total_ev/(1000 * total_comm_bus)
        
        charger_count_dict['l2_charger_per_comm_bus'] = l2_charger_per_comm_bus

        # public area chargers
        pub_dc_chargers_per_1000_ev = charger_mult*charger_info[charger_info['year']==year]['public_dc'].item()
        pub_l2_chargers_per_1000_ev = charger_mult*charger_info[charger_info['year']==year]['public_l2'].item()

        dc_charger_per_pub_bus = pub_dc_chargers_per_1000_ev*total_ev/(1000 * total_public_bus) 
        l2_charger_per_pub_bus = pub_l2_chargers_per_1000_ev*total_ev/(1000 * total_public_bus) 

        charger_count_dict['dc_charger_per_pub_bus'] = dc_charger_per_pub_bus
        charger_count_dict['l2_charger_per_pub_bus'] = l2_charger_per_pub_bus


        # vehicles distribution over commercial or public charging are calculated 
        # proportional to available chargers 
        # not being used any more 
        work_chargers = charger_mult*charger_info[charger_info['year']==year]['work_l2'].item()
        pub_chargers = pub_dc_chargers_per_1000_ev + pub_l2_chargers_per_1000_ev
        pub_chargers_dc_frac = pub_dc_chargers_per_1000_ev/pub_chargers

        ev_per_comm_bus = (total_ev_nonres_charging * (work_chargers/(work_chargers + pub_chargers)))/total_comm_bus
        ev_count_dict['ev_per_comm_bus'] = ev_per_comm_bus

        ev_per_pub_bus = (total_ev_nonres_charging * (pub_chargers/(work_chargers + pub_chargers)))/total_public_bus
        ev_per_pub_bus_dc = ev_per_pub_bus * pub_chargers_dc_frac
        ev_per_pub_bus_l2 = ev_per_pub_bus - ev_per_pub_bus_dc
        ev_count_dict['ev_per_pub_bus_dc'] = ev_per_pub_bus_dc
        ev_count_dict['ev_per_pub_bus_l2'] = ev_per_pub_bus_l2
        #    ---xXx---    # 
        # vehicle distribuion across different non residential chargers are calculated based on
        # their utilization rate

        energy_per_charge = 40 #KWh
        dc_charge_rate = 200
        l2_charge_rate = 20 

        util_mult = pub_charger_util_multiplier
        pub_charger_util_rate_year = pub_charger_util_rate[pub_charger_util_rate['year']==year]

        public_dc_util_rate = util_mult*pub_charger_util_rate_year[
                                    pub_charger_util_rate_year['charger_type']=='public_dcfc'
                                                ]['utilization_percent'].item()
        public_l2_util_rate = util_mult*pub_charger_util_rate_year[
                                        pub_charger_util_rate_year['charger_type']=='public_l2'
                                                ]['utilization_percent'].item()
        work_l2_util_rate = util_mult*pub_charger_util_rate_year[
                                        pub_charger_util_rate_year['charger_type']=='work_l2'
                                                ]['utilization_percent'].item()

        ev_per_public_dc_charger = (1/energy_per_charge)*dc_charge_rate*(24/100)*public_dc_util_rate
        ev_per_public_l2_charger = (1/energy_per_charge)*l2_charge_rate*(24/100)*public_l2_util_rate
        ev_per_work_l2_charger = (1/energy_per_charge)*l2_charge_rate*(24/100)* work_l2_util_rate


        total_ev_in_pub_charge_from_util_calc = [ev_per_public_dc_charger, 
                                                 ev_per_public_l2_charger, 
                                                 ev_per_work_l2_charger]

        total_ev_in_pub_charge_from_numbers = {
            'public_DC': ev_per_pub_bus_dc/dc_charger_per_pub_bus,
            'public_AC2': ev_per_pub_bus_l2/l2_charger_per_pub_bus,
            'work_AC2': ev_per_comm_bus/l2_charger_per_comm_bus
        }

        ldev_load_dict={}
        mhdev_load_dict = {}
        ev_load_dict = {}
        # adding the load to the buses 

        # residential charging 
        ldev_load_dict['Res'] = (ev_load['home_AC2'] * ev_per_res_bus_res_charging_l2 + \
                                   ev_load['home_AC1'] * ev_per_res_bus_res_charging_l1) * 1e-3 # converting to MW


        # commercial/work charging
        # max 8 vehicles can be charged by one charger per day for L2
        ldev_load_dict["Comm"] = (ev_load['work_AC2'] * \
                            l2_charger_per_comm_bus * \
                              ev_per_work_l2_charger)* 1e-3


        # public charging
        # max 8 vehicles can be charged by one charger per day for L2 and 2 for L1

        ldev_load_dict[comm_bus_name_by_area[area]] = (ev_load['public_AC2'] * 
                                                        l2_charger_per_pub_bus * 
                                                            ev_per_public_l2_charger   
                                                                     + \
                                                ev_load['public_DC'] * \
                                                    dc_charger_per_pub_bus * \
                                                        ev_per_public_dc_charger
                                                                    ) * \
                                                                      1e-3

        # MHDEV load 

        # private/commercial 
        mdevs_for_area_year = mhdev_vehicle_numbers.loc[(mhdev_vehicle_numbers['year']==year) & \
                                                            (mhdev_vehicle_numbers['area']==area) \
                                                                ]['mdev'].item()
        
        hdevs_for_area_year = mhdev_vehicle_numbers.loc[(mhdev_vehicle_numbers['year']==year) & \
                                                (mhdev_vehicle_numbers['area']==area)
                                                                ]['hdev'].item()
        ev_count_dict['mdev_in_network'] = mdevs_for_area_year
        ev_count_dict['hdev_in_network'] = hdevs_for_area_year

        #m/hdevs in commercial bus



        total_mhdevs_area_year = mdevs_for_area_year+hdevs_for_area_year
        mhdev_chargers_nums = mhdev_chargers_data.loc[(mhdev_chargers_data['year']==year) & \
                                                        (mhdev_chargers_data['area']==area)]

        private_l3_chargers_per_bus = mhdev_chargers_nums['private_l3'].item()/total_comm_bus

        private_fast_chargers_per_bus = mhdev_chargers_nums['private_fast'].item()/total_comm_bus

        charger_count_dict['private_l3_per_bus'] = private_l3_chargers_per_bus
        charger_count_dict['private_fast_per_bus'] = private_fast_chargers_per_bus 

        # the throughput of each charger is assumed to have M and HDEVs proportional to their numbers 
        # in the network

        ###########################
        # mdevs_per_private_l3_charger = mhdev_charger_throughput['private_l3']* \
        #                                     (mdevs_for_area_year/ total_mhdevs_area_year)
        
        # hdevs_per_private_l3_charger = mhdev_charger_throughput['private_l3'] - \
        #                                                     mdevs_per_private_l3_charger
        

        # mdevs_per_private_fast_charger = mhdev_charger_throughput['private_fast']* \
        #                                     (mdevs_for_area_year/total_mhdevs_area_year)
        
        # hdevs_per_private_fast_charger = mhdev_charger_throughput['private_fast'] - \
        #                                                     mdevs_per_private_fast_charger
        #############################
        mdevs_per_private_l3_charger = mdevs_for_area_year*mdev_distribution_over_chargers['private_l3']/ \
                                               mhdev_chargers_nums['private_l3'].item()
        mdevs_per_private_fast_charger = mdevs_for_area_year*mdev_distribution_over_chargers['private_fast']/ \
                                               mhdev_chargers_nums['private_fast'].item()


        hdevs_per_private_l3_charger = hdevs_for_area_year*hdev_distribution_over_chargers['private_l3']/ \
                                                mhdev_chargers_nums['private_l3'].item()
        hdevs_per_private_fast_charger = hdevs_for_area_year*hdev_distribution_over_chargers['private_fast']/ \
                                                mhdev_chargers_nums['private_fast'].item()



        mhdev_load_commercial_bus =  ((mdev_load_profiles['depot_l3']* \
                                    private_l3_chargers_per_bus* \
                                        mdevs_per_private_l3_charger) + \
                                (hdev_load_profiles['depot_l3']*
                                    private_l3_chargers_per_bus*
                                        hdevs_per_private_l3_charger) + \
                                (mdev_load_profiles['opp_fast']* \
                                    private_fast_chargers_per_bus* \
                                        mdevs_per_private_fast_charger) + \
                                (hdev_load_profiles['opp_fast']* \
                                    private_fast_chargers_per_bus* \
                                        hdevs_per_private_fast_charger)) * 1e-3 
        
        ev_count_dict['mdev_in_comm_zone_charger_tput'] = (private_l3_chargers_per_bus*mdevs_per_private_l3_charger+ \
                                                            private_fast_chargers_per_bus*mdevs_per_private_fast_charger)* \
                                                                total_comm_bus
        
        ev_count_dict['hdev_in_comm_zone_charger_tput'] = (private_l3_chargers_per_bus*hdevs_per_private_l3_charger+ \
                                                            private_fast_chargers_per_bus*hdevs_per_private_fast_charger)* \
                                                                total_comm_bus



        mhdev_load_dict['Comm'] = mhdev_load_commercial_bus
        # public / industrial 

        #m/hdevs in public bus

        public_l3_chargers_per_bus = mhdev_chargers_nums['public_l3'].item()/total_public_bus

        public_fast_chargers_per_bus = mhdev_chargers_nums['public_fast'].item()/total_public_bus

        charger_count_dict['public_l3_per_bus'] = public_l3_chargers_per_bus
        charger_count_dict['public_fast_per_bus'] = public_fast_chargers_per_bus 

        # the throughput of each charger is assumed to have M and HDEVs proportional to their numbers 
        # in the network
        #########################
        # mdevs_per_public_l3_charger = mhdev_charger_throughput['public_l3']* \
        #                                     (mdevs_for_area_year/total_mhdevs_area_year)
        
        # hdevs_per_public_l3_charger = mhdev_charger_throughput['public_l3'] - \
        #                                             mdevs_per_public_l3_charger
        

        # mdevs_per_public_fast_charger = mhdev_charger_throughput['public_fast']* \
        #                                     (mdevs_for_area_year/total_mhdevs_area_year)
        
        # hdevs_per_public_fast_charger = mhdev_charger_throughput['public_fast'] -\
        #                                              mdevs_per_public_fast_charger
        ##########################

        mdevs_per_public_l3_charger = mdevs_for_area_year*mdev_distribution_over_chargers['public_l3']/ \
                                               mhdev_chargers_nums['public_l3'].item()
        mdevs_per_public_fast_charger = mdevs_for_area_year*mdev_distribution_over_chargers['public_fast']/ \
                                               mhdev_chargers_nums['public_fast'].item()


        hdevs_per_public_l3_charger = hdevs_for_area_year*hdev_distribution_over_chargers['public_l3']/ \
                                                mhdev_chargers_nums['public_l3'].item()
        hdevs_per_public_fast_charger = hdevs_for_area_year*hdev_distribution_over_chargers['public_fast']/ \
                                                mhdev_chargers_nums['public_fast'].item()


        mhdev_load_public_bus = ((mdev_load_profiles['depot_l3']* \
                                    public_l3_chargers_per_bus* \
                                        mdevs_per_public_l3_charger) + \
                                (hdev_load_profiles['depot_l3']*
                                    public_l3_chargers_per_bus*
                                        hdevs_per_public_l3_charger) + \
                                (mdev_load_profiles['opp_fast']* \
                                    public_fast_chargers_per_bus* \
                                        mdevs_per_public_fast_charger) + \
                                (hdev_load_profiles['opp_fast']* \
                                    public_fast_chargers_per_bus* \
                                        hdevs_per_public_fast_charger))* 1e-3 

        ev_count_dict['mdev_in_pub_zone_charger_tput'] = (public_l3_chargers_per_bus*mdevs_per_public_l3_charger+ \
                                                            public_fast_chargers_per_bus*mdevs_per_public_fast_charger)* \
                                                                total_public_bus
        
        ev_count_dict['hdev_in_pub_zone_charger_tput'] = (public_l3_chargers_per_bus*hdevs_per_public_l3_charger+ \
                                                            public_fast_chargers_per_bus*hdevs_per_public_fast_charger)* \
                                                                total_public_bus


        ev_count_dict['mdev_in_network_charger_tput'] = ev_count_dict['mdev_in_pub_zone_charger_tput'] + \
                                                          ev_count_dict['mdev_in_comm_zone_charger_tput']
        
        
        ev_count_dict['hdev_in_network_charger_tput'] = ev_count_dict['hdev_in_pub_zone_charger_tput'] + \
                                                          ev_count_dict['hdev_in_comm_zone_charger_tput']
        
        
        mhdev_load_dict[comm_bus_name_by_area[area]] = mhdev_load_public_bus
        #ipdb.set_trace()
        #ev_load_dict[comm_bus_name_by_area[area]] += mhdev_load_public_bus
        # # table 21: res area AC2 : AC1 = 12:3
        # # assume AC2 serve 0.7 ev per day
        # EV_load['Res'] = (EV_load0['home_AC2'] * 12/15 * .7 +  EV_load0['home_AC1']* 3/15 ) \
        #     *1e-3 *  charger_per_res_bus 
        
        # # tab 21: work area AC2:AC1=13:5
        # EV_load['Comm'] = (EV_load0['work_AC2'] *13/18 +  EV_load0['work_AC1'] *5/18 )    \
        #     *  charger_per_comm_bus*1e-3 
            
        # # tab 21: pub area AC2:DC=9:3
        # EV_load['Pub'] = ( EV_load0['public_AC2'] *9/12 +  EV_load0['public_DC'] * 3/12 ) \
        #     *1e-3 *    charger_per_public_bus
        for key, value in ev_count_dict.items():
            print(f'{key} : {value}')
        
        for key, value in charger_count_dict.items():
            print(f'{key} : {value}')
        

        # print(total_ev_in_pub_charge_from_util_calc)
        # print(total_ev_in_pub_charge_from_numbers)
        # #ipdb.set_trace()
        ev_load_dict["Res"] = ldev_load_dict['Res']
        ev_load_dict['Comm'] = ldev_load_dict['Comm'] + mhdev_load_dict['Comm']
        ev_load_dict[comm_bus_name_by_area[area]] = ldev_load_dict[comm_bus_name_by_area[area]] + mhdev_load_dict[comm_bus_name_by_area[area]]  

        output_table_trafo, output_table_line =  loading_assess(net, area, bus_load ,ev_load_dict)
        folder = f'./results/ResultsJan10_v8_{area}/'
        os.makedirs(os.path.dirname(folder), exist_ok=True)

        pd.DataFrame(ev_count_dict, index=[0]).to_csv(f'{folder}/{year}_ev_numbers.csv')
        pd.DataFrame(charger_count_dict, index=[0]).to_csv(f'{folder}/{year}_chargers_numbers.csv')

        pd.DataFrame(mhdev_load_dict).to_csv(f'{folder}/{year}_mhdev_load.csv')
        pd.DataFrame(ldev_load_dict).to_csv(f'{folder}/{year}_ldev_load.csv')
        output_table_trafo.to_excel('{}withEV{}_tra.xlsx'.format(folder, year))
        output_table_line.to_excel('{}withEV{}_line.xlsx'.format(folder, year))
        
    



