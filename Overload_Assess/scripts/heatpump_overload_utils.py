import numpy as np


def electricity_requirement_for_house_heating_cooling(rephouse_data, primary_heating_type, secondary_heating_type, top_n=3):
    '''
    Given the annual hourly heating and cooling data of a house, this method calculates the mean 24hr electric load profile 
    of that given house base on the type of heating method used.
    rep_house_data: Dataframe containing 
                        heating_load_KWh 	
                        heating_load_additional_KJ 	
                        cooling_load_KWh 	'
                        cooling_load_additional_KJ 	
                        heating_COP 	
                        cooling_COP 	
    primary_heating_type: str: ['hp', 'electric', 'gas']
    secondary_heating_type: str: ['electric', 'gas'] #only applicable with 'hp' as primary_heating_type

    returns a 24hr load profile: array of size 24
    '''
    if primary_heating_type!='hp':
        secondary_heating_type=primary_heating_type


    top_n_ind = np.array(rephouse_data['heating_load_KWh']+rephouse_data['cooling_load_KWh']).reshape(-1, 24).sum(axis=1).argpartition(top_n)[-top_n:]

    if primary_heating_type=='hp':
        rephouse_data_daily_electric_energy_mean_kwh = np.array(
                            rephouse_data['heating_load_KWh']+rephouse_data['cooling_load_KWh']
                                    ).reshape(-1, 24)[top_n_ind, :].mean(axis=0)
        
    elif primary_heating_type=='electric':
        #electric has a COP of 1
        rephouse_data_daily_electric_energy_mean_kwh = (
                np.array(rephouse_data['heating_load_KWh'])*np.array(rephouse_data['heating_COP']) + \
                np.array(rephouse_data['cooling_load_KWh'])*np.array(rephouse_data['cooling_COP'])
                                    ).reshape(-1, 24)[top_n_ind, :].mean(axis=0)
    else:
        rephouse_data_daily_electric_energy_mean_kwh = np.zeros(24)
    
    if secondary_heating_type=='electric':
    
        rephouse_data_daily_additional_energy_mean_kj = np.array(
                        rephouse_data['heating_load_additional_KJ']+rephouse_data['cooling_load_additional_KJ']
                            ).reshape(-1, 24)[top_n_ind, :].mean(axis=0)
        rephouse_data_daily_additional_energy_mean_kwh = rephouse_data_daily_additional_energy_mean_kj/3600
        
    else:
        rephouse_data_daily_additional_energy_mean_kwh = np.zeros(24)
    
    return rephouse_data_daily_electric_energy_mean_kwh + rephouse_data_daily_additional_energy_mean_kwh



def get_electricity_24h_heating_elctric_demand_area(representative_house, housing_ratio, total_houses):

    hp_house_with_gas_load_profile = electricity_requirement_for_house_heating_cooling(representative_house, 'hp', 'gas')/1000 #converting to MWh
    hp_house_with_electric_load_profile = electricity_requirement_for_house_heating_cooling(representative_house, 'hp', 'electric')/1000
    electric_house_load_profile = electricity_requirement_for_house_heating_cooling(representative_house, 'electric', 'gas')/1000

    electric_frac = housing_ratio['electric'].item()
    gas_frac = housing_ratio['gas'].item()
    hp_pen_rate = housing_ratio['hp'].item()
    hp_from_gas = housing_ratio['hp_from_gas'].item()
    hp_from_electric = housing_ratio['hp_from_electric'].item()

    hp_with_electric = hp_house_with_electric_load_profile* \
                                hp_pen_rate * hp_from_electric
                            
    hp_with_gas = hp_house_with_gas_load_profile* \
                        hp_pen_rate * hp_from_gas
                           
    electric_baseboard = electric_house_load_profile*electric_frac
    total_heating_load = (hp_with_electric + \
                            hp_with_gas + \
                            electric_baseboard ) * total_houses
    
    heating_load_from_hp =  (hp_with_electric + \
                            hp_with_gas ) * total_houses
    

    heating_load_from_electric = electric_baseboard * total_houses
    # print('house ratio : ', hp_pen_rate* total_houses, 
    #                 electric_frac*total_houses, 
    #                 gas_frac*total_houses)

    # print('Energy from  hp : ', (hp_with_electric.sum()+  hp_with_gas.sum())*total_houses)
    # print('Energy from electirc :', electric_baseboard.sum()*total_houses)

    # print("Energy per house")
    # print("HP :", 
    #       (hp_with_electric.sum() + hp_with_gas.sum())/hp_pen_rate)
    # print("Electric :", electric_baseboard.sum()/electric_frac)
    return heating_load_from_hp, heating_load_from_electric