import pandas as pd 
import numpy as np 
import math 
from sklearn.neighbors import KNeighborsClassifier
import json
import glob
import pickle 

#get load for an hour
def find_closest_non_nan(arr, index):
    """
    Find the closest non-NaN value to the given index in a numpy array.
    
    Args:
        arr (numpy.ndarray): Input array
        index (int): Index to search around
    
    Returns:
        float: Closest non-NaN value, or NaN if no non-NaN values exist
    """
    if not np.isnan(arr[index]):
        return arr[index]
    
    # Search in both directions
    for offset in range(1, len(arr)):
        print('here')
        left = index - offset
        right = index + offset
        
        # Check left side
        if left >= 0 and not np.isnan(arr[left]):
            return arr[left]
        
        # Check right side
        if right < len(arr) and not np.isnan(arr[right]):
            return arr[right]
    
    return np.nan
    

def build_hpcapacity_classifier(eccc_data, feature_cols=['HEATEDFLOORAREA' , 'EGHSPACEENERGY']):
    '''
    Given ECCC housing data creates a KNN classifier that uses the features 
    ['HEATEDFLOORAREA' , 'EGHSPACEENERGY']
    to predict the size a heatpump to assign to a house.

    eccc_data : Dataframe containing housing information from ECCC 
    feature_cols: Columns to be used as features. Should be floats.

    returns: KNN classifier
    '''

    hp_data_with_hp = eccc_data.loc[eccc_data['HPSOURCE'].isin(['Air', 'Ground', 'Water'])]

    features = np.array(hp_data_with_hp[feature_cols])
    values = np.round((np.array(hp_data_with_hp['HPCAP'])/3500 ))

    neigh = KNeighborsClassifier(n_neighbors=1000, weights='distance')

    neigh.fit(features, values)

    return neigh


def get_hp_electricity_usage_per_hour(hp_size, cur_temp, cur_heat_req, hp_cop_data):
    '''
    Given the current heating load and size of the heat pump, 
    return the COP and the electricity used by the HP for the current load
    for ONE hour
    hp_size: size of the heatpump 
    cur_temp: current temperature
    cur_heat_req: current heating or cooling energy required (KJ)
    hp_cop_info: dictionary containing another dict:
        {hp_size}: {
        'temp_limits': tuple (min, max)
        'CAP_max': list of max capacity values for different temperatures 
        'COP_data': list(list) COP data for different temperature and capacity
                    outer_dim: capacity index
                    inner_dim: temperature index
                    }
    Returns the 
        electric power required (KWh), 
        COP (float)  
        additional heating required from secondary heating (KJ)
    '''
    cur_hp_info = hp_cop_data[str(hp_size)]
    min_temp, max_temp = cur_hp_info['temp_limits']
    min_cap = 0
    max_cap = max(cur_hp_info['CAP_max'])
    max_cap_vals = cur_hp_info['CAP_max']
    cur_temp = max(cur_temp, min_temp) 
    cur_temp = min(cur_temp, max_temp)
    
    temp_indx = int((cur_temp - min_temp)/(max_temp-min_temp)*(len(cur_hp_info['COP_data'][0])-1))
    max_cap_temp = cur_hp_info['CAP_max'][temp_indx]

    # HPsize (in ton) * 3500 = wattage of the HP
    # wattage of HP * 3600 = Joues of heat generated in an hour at 100% capacity
    #Joues of heat generated in an hour at 100% capacity/1000 = KJ of heat genearted at max capacity in an hour
    
    hp_heat_gen_at_100_percent_cap_kj = hp_size*3500*3600/1000 # in KJ 

    cur_load_frac = cur_heat_req/hp_heat_gen_at_100_percent_cap_kj

    cur_load_frac = min(max_cap_temp, cur_load_frac)

    #due to the quirks of the interpolation some edge values are Nan
    #the loop below makes sure if a value is selected from the nan region
    #then it would select the closest non nan value for that given temperature

    cap_indx = math.floor((cur_load_frac - min_cap)/(max_cap - min_cap)*(len(cur_hp_info['COP_data'])-1))
    cur_cop = cur_hp_info['COP_data'][cap_indx][temp_indx]
    
    if np.isnan(cur_cop):
        cur_cop = find_closest_non_nan(np.array(cur_hp_info['COP_data'])[:, temp_indx], cap_indx-1)
    
    #cur_cop = 0.5
    # print(hp_size, cur_hp_info['CAP_max'][temp_indx])
    # print(cur_hp_info['CAP_max'][temp_indx]*hp_size*3500*3600/1000, cur_heat_req)
    
    heat_gen = cur_load_frac*hp_heat_gen_at_100_percent_cap_kj #in KJ
    elec_use = heat_gen/cur_cop/3600 #in KWh (3600KJ = 1KWh)
    return elec_use, cur_cop,  cur_heat_req - heat_gen



def calculate_hourly_annual_heating_cooling_requirement_for_house(housing_data_row, 
                                                          base_indoor_temp=20, 
                                                          cooling_trigger_temp=24,
                                                          weather_filepath='../data/raw_data/weather/by_FSA/{0}_2023-01-01_2024-01-01.csv',
                                                          heating_pattern='../data/formatted_data/heatpump/normalized_24h_heating_pattern.csv'):
    '''
    Given housing information, retrieve yearly temperature and calculate the hourly heating energy
    required by the house
    housing_data: One row from ECCC_2023 db


    Returns 
        hourly_heating_energy_total: numpy array containing annual hourly heating requirement in KJ
        hourly_cooling_energy_total: numpy array containing annual hourly cooling requirement in KJ
        hourly_heating_degrees: array
        hourly_cooling_degrees: array
        hourly_temp_data : array in celcius

    '''
    
    thermal_envelope_metrics = ['EGHHLWALLS', 'EGHHLCEILING', 'EGHHLWINDOOR', 'EGHHLFOUND', 'EGHHLEXPOSEDFLR',  'EGHHLAIR']    
    # read relevant data
    building_fsa = housing_data_row['CLIENTPCODE']
    annual_heating_eng_req = housing_data_row['EGHSPACEENERGY']*1000 #MJ to KJ
    annual_cooling_eng_req = housing_data_row['ERSSPACECOOLENERGY']*1000  #MJ to KJ  
    heatloss_data = np.array(housing_data_row[thermal_envelope_metrics])
    
    weather_data = pd.read_csv(weather_filepath.format(building_fsa))
    if heating_pattern:
        heating_pattern_data = pd.read_csv(heating_pattern)
    
    # calculate the hourly temperature and wind factor 
    temp_contribution = heatloss_data[0:-2].sum()
    wind_contribution = heatloss_data[-1]
    
    temp_fraction = temp_contribution/heatloss_data.sum()
    wind_fraction = 1-temp_fraction
    
    hourly_temp_data = np.array(weather_data['temperature_2m'])
    hourly_wind_data = np.array(weather_data['wind_speed_10m'])
    hourly_heating_degrees = base_indoor_temp - hourly_temp_data
    
    hourly_heating_degrees[ hourly_heating_degrees <= 0] = 0
    hourly_wind_data[hourly_heating_degrees <= 0] = 0
    
    temp_factor = (annual_heating_eng_req*temp_fraction)/hourly_heating_degrees.sum()
    wind_factor = (annual_heating_eng_req*wind_fraction)/np.sum(hourly_wind_data)
    
    # calclulate the hourly heating energy 
    hourly_heating_energy_temp = temp_factor*hourly_heating_degrees 
    hourly_heating_energy_wind = wind_factor*hourly_wind_data
    
    hourly_heating_energy_total = hourly_heating_energy_temp + hourly_heating_energy_wind
    # add heating pattern into the mix 
    if heating_pattern:
        hourly_heating_energy_total = hourly_heating_energy_total.reshape(-1, 24)
        hourly_heating_energy_total_daily = hourly_heating_energy_total.sum(axis=1).reshape(hourly_heating_energy_total.shape[0], 1)
        daily_norm = np.array(heating_pattern_data[heating_pattern_data['building_type']=='SFH']['fraction_of_daily_heating']).reshape(1, 24)
        daily_norm_stacked = np.repeat(daily_norm, hourly_heating_energy_total.shape[0], axis=0)
        hourly_heating_energy_total = np.multiply(daily_norm_stacked, hourly_heating_energy_total_daily).reshape(-1,1)

    
    # calculate the hourly cooling energy
    hourly_cooling_degrees = hourly_temp_data - cooling_trigger_temp
    hourly_cooling_degrees[hourly_cooling_degrees <= 0] = 0
    temp_factor_cooling = (annual_cooling_eng_req)/hourly_cooling_degrees.sum()
    hourly_cooling_energy_total = temp_factor_cooling*hourly_cooling_degrees 
    

    return hourly_heating_energy_total, hourly_cooling_energy_total, hourly_heating_degrees, hourly_cooling_degrees, hourly_temp_data
    

#get electricity consumption for one house over a year
def get_hourly_electricity_usage_for_house(house_data, hp_cop_data):
    '''
    Given the data of a house and the heatpump COP data, return the annual hourly electricity used by that house
    for heating and cooling
    house_data : One row from the ECCC_2023 dataset. Relevant columns include: HPCAP, CLIENTPCODE (for weather), EGHSPACEENERGY, ERSSPACECOOLENERGY
    hp_cop_data: dictionary containing another dict:
        {hp_size}: {
        'temp_limits': tuple (min, max)
        'CAP_max': list of max capacity values for different temperatures 
        'COP_data': list(list) COP data for different temperature and capacity
                    outer_dim: capacity index
                    inner_dim: temperature index
                    }

    returns a dataframe with hp_heating_electricity (KWh), hp_cooling_electricity)(KWh), backup_cooling_electricity (KJ), backup_heating_electricity(KJ)
    '''

    #get hourly heating/cooling energy required
    heat_req, cool_req, _, _, hourly_temp_data = calculate_hourly_annual_heating_cooling_requirement_for_house(house_data)

    #get heatpump size 
    hp_caps_standard = np.arange(1, 5.5, 0.5)
    house_hp_cap = house_data['HPCAP']/3500 #HPCAP is provided in watts
    house_hp_size = hp_caps_standard[np.abs(hp_caps_standard - house_hp_cap).argmin()]
    
    total_hours = len(heat_req)
    hourly_heating_electric_load = np.zeros(total_hours)
    hourly_cooling_electric_load = np.zeros(total_hours)
    heating_cop = np.zeros(total_hours)
    cooling_cop = np.zeros(total_hours)
    addl_heat_hourly = np.zeros(total_hours)
    addl_cool_hourly = np.zeros(total_hours)
    for t in range(total_hours):
        cur_temp = hourly_temp_data[t]
        if heat_req[t] > 0:
            elec_use, cur_cop,  addl_heat_req = get_hp_electricity_usage_per_hour(house_hp_size, cur_temp, heat_req[t].item(), hp_cop_data)
            heating_cop[t] = cur_cop
            addl_heat_hourly[t] = addl_heat_req
            hourly_heating_electric_load[t] = elec_use
            
        if cool_req[t] > 0:
            elec_use, cur_cop,  addl_cool_req = get_hp_electricity_usage_per_hour(house_hp_size, cur_temp, cool_req[t].item(), hp_cop_data)
            cooling_cop[t] = cur_cop
            addl_cool_hourly[t] = addl_cool_req
            hourly_cooling_electric_load[t] = elec_use

    house_hr_load = pd.DataFrame()
    house_hr_load['heating_load_KWh'] = hourly_heating_electric_load
    house_hr_load['heating_load_additional_KJ'] = addl_heat_hourly

    house_hr_load['cooling_load_KWh'] = hourly_cooling_electric_load
    house_hr_load['cooling_load_additional_KJ'] = addl_cool_hourly

    house_hr_load['heating_COP'] = heating_cop
    house_hr_load['cooling_COP'] = cooling_cop 

    house_hr_load['hourly_temp'] = hourly_temp_data

    house_hr_load['province'] = house_data['HOUSEREGION']
    house_hr_load['fsa'] = house_data['CLIENTPCODE']
    
    return house_hr_load

if __name__=='__main__':
    #hp_data_file = '../data/raw_data/heatpump/ECCC_2023.csv'
    data_file = '../data/formatted_data/heatpump/province_yearbuilt_cluster_centers/QC/QC_2011_2015_cluster_centers.csv'

    cluster_center_base_folder = '../data/formatted_data/heatpump/province_yearbuilt_cluster_centers'
    heatpump_data_fname = '../data/formatted_data/heatpump/hp_coeff_data_interpolated.json'

    hp_size_classifier = pickle.load(open('../data/raw_data/heatpump/KNN_HPSIZE_classifier', 'rb'))
    classifier_feature_cols = ['HEATEDFLOORAREA' , 'EGHSPACEENERGY']

    cluster_center_filenames = glob.glob(f'{cluster_center_base_folder}/*/*.csv')

    with open(heatpump_data_fname, 'r') as f:
        heatpump_coeff_interpolated_data = json.load(f)

    rel_output_data_cols = ['heating_load_KWh', 
                         'heating_load_additional_KJ',
                         'cooling_load_KWh',
                         'cooling_load_additional_KJ', 	
                         'heating_COP',  	
                         'cooling_COP', 	
                         'hourly_temp']
    mean_data = np.zeros((8784, 7))

    for cc_fname in cluster_center_filenames:
        hp_data = pd.read_csv(cc_fname)
        #find the cluster with the biggest size 
        idx = hp_data['Cluster Proportion'].argmax()

        row_data = hp_data.iloc[idx]
        
        if row_data['HPSOURCE']=='N/A {no Heat Pump}':
            row_data['HPCAP'] = hp_size_classifier.predict(
                            np.array(row_data[classifier_feature_cols]).reshape(1, 2)
                                ) * 3500 # convert from ton to watts Classifier predicts in Tons
        #row_data['HPCAP'] = 7000
        output = get_hourly_electricity_usage_for_house(row_data, heatpump_coeff_interpolated_data)
        mean_data += np.array(output[rel_output_data_cols])
    
    mean_data/=len(cluster_center_filenames)
    for i in range(len(rel_output_data_cols)):
        output[rel_output_data_cols[i]] = mean_data[:, i]

    output =  output.drop(columns='fsa')  
    output.to_csv('../results/heatpump_forecast/canada_mean_representative_house_heating_cooling_stats.csv')