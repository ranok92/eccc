import os
import glob
import json
from heatpump_utils import *
import pickle
#read the penetration rates for each group
import ipdb
from tqdm import tqdm

def main():
    # eccc_db_fname = '../../data/raw_data/heatpump/ECCC_2023.csv'
    # eccc_data = pd.read_csv(eccc_db_fname)
    group_penrate_forecast_fname = '../data/formatted_data/heatpump/hp_penetration_rate_forecast_by_group_all_province.csv'
    heatpump_data_fname = '../data/formatted_data/heatpump/hp_coeff_data_interpolated.json'
    norm_heating_pattern = '../data/formateed_data/heatpump/normalized_24h_heating_pattern.csv'
    hpsize_classifier_fname = '../data/raw_data/heatpump/KNN_HPSIZE_classifier'
    pop_growth_fname = '../Overload_Assess/data/ldev_load_data/population_change_diff_areas.csv' #in fraction

    save_folder = '../results/heatpump_forecast'
    groupwise_clustering_basefolder = '../data/formatted_data/heatpump/groupwise_cluster_centers/'
    prov_yearbuilt_clustering_basefolder = '../data/formatted_data/heatpump/province_yearbuilt_cluster_centers/'
    cluster_filename_str = '{0}/{1}/{1}_{2}_{3}_cluster_centers.csv'
    prov_yearbuilt_cluster_filename_str= '{0}/{1}/{1}_{2}_cluster_centers.csv'
    feature_cols_KNN = ['HEATEDFLOORAREA' , 'EGHSPACEENERGY']
    hp_size_classifier = pickle.load(open(hpsize_classifier_fname, 'rb'))
    pop_growth = pd.read_csv(pop_growth_fname)

    top_n = 5 #top n days to consider to calculate max load

    #all the areas 'urban', 'suburban' and 'rural' have the same growth rate
    pop_growth= pop_growth[pop_growth['area']=='urban']

    with open(heatpump_data_fname, 'r') as f:
        heatpump_coeff_interpolated_data = json.load(f)

    groupwise_penetration_rate_forecast = pd.read_csv(group_penrate_forecast_fname)
    province_name_dict = {
                            'alberta': 'AB', 
                            'british columbia': 'BC',
                            'manitoba': 'MB',
                            'new brunswick': 'NB',
                            'newfoundland and labrador': 'NF',
                            'nova scotia': 'NS', 
                            'ontario': 'ON', 
                            'prince edward island': 'PE', 
                            'quebec': 'QC', 
                            'saskatchewan': 'SK', 
                            'territories': 'Territories'
    }
    province_list = groupwise_penetration_rate_forecast['province'].unique()
    year_of_constrution_list = groupwise_penetration_rate_forecast['year_of_construction'].unique()
    print(province_list)
    house_type_list = groupwise_penetration_rate_forecast['house_type'].unique()
    year_list = groupwise_penetration_rate_forecast['forecast_year'].unique()
    electic_load_canada_forecast_df = pd.DataFrame()
    for province in tqdm(province_list):
        province_df = pd.DataFrame(columns=['province', 
                                            'forecast_year', 
                                            'total_electric_energy_MWh' , 
                                            'load_profile_24h_mean_MWh', 
                                            'load_profile_24h_mean_MWh' ])
        provincial_yearly_dict = {}
        for year in year_list:
            provincial_yearly_dict[year] = {'total_electric_energy_MWh' : 0, 
                                            'load_profile_24h_mean_MWh' : np.zeros(24), 
                                            'load_profile_24h_max_MWh' : np.zeros(24)}
            
        for year_of_const in year_of_constrution_list:
            for house_type in house_type_list:
                #read the representative house data for each cluster of a group 
                cluster_fname = cluster_filename_str.format(groupwise_clustering_basefolder,
                                                                    province_name_dict[province], 
                                                                    house_type,
                                                                    year_of_const)
                prov_yb_cluster_fname = prov_yearbuilt_cluster_filename_str.format(
                                                        prov_yearbuilt_clustering_basefolder,
                                                        province_name_dict[province], 
                                                        year_of_const
                                                        )
                if os.path.exists(cluster_fname):
                    cluster_pd = pd.read_csv(cluster_fname)
                # else:
                #     print(f'Reading {prov_yb_cluster_fname}')
                #     cluster_pd = pd.read_csv(prov_yb_cluster_fname)

                    #calculate heating for each representative house in the cluster
                    for _, row in cluster_pd.iterrows():
                        #assign heatpump if absent 
                        if row['HPSOURCE']=='N/A {no Heat Pump}':
                            #assign heatpump
                            row['HPSOURCE'] = 'Air'
                            #Classifier returns in Ton. Need to convert that to Watts
                            row['HPCAP'] = hp_size_classifier.predict(np.array([row[feature_cols_KNN]]))*3500 

                        cluster_proportion = row['Cluster Proportion']
                        cluster_id = row['Cluster ID']
                        # electric usage for one representative house
                        hourly_electric_usage = get_hourly_electricity_usage_for_house(row, heatpump_coeff_interpolated_data)

                        for forecast_year in year_list:
                            penrate_row = groupwise_penetration_rate_forecast[
                                (groupwise_penetration_rate_forecast['province']==province) & \
                                    (groupwise_penetration_rate_forecast['house_type']==house_type) & \
                                        (groupwise_penetration_rate_forecast['year_of_construction']==year_of_const) & \
                                            (groupwise_penetration_rate_forecast['forecast_year']==forecast_year)
                                                    ]
                            
                            pop_change_frac = pop_growth[
                                                    pop_growth['year']==forecast_year
                                                ]['rel_pop_change_frac'].item()
                            
                            num_houses = penrate_row['number_of_houses'].item()* pop_change_frac
                                
                            hp_pen_rate = penrate_row['hp_penetration_rate'].item()/100 #converting percentage to fraction
                            electric_house_num = penrate_row['electric'].item()

                            hp_electric_load_heating_mwh = hourly_electric_usage['heating_load_KWh']* \
                                                                    num_houses*hp_pen_rate*cluster_proportion/1000 #in MWh
                            addl_heat_load_kj = hourly_electric_usage['heating_load_additional_KJ']* \
                                                                    num_houses*hp_pen_rate*cluster_proportion # in KJ

                            #this additional load will either come from electric base board or \
                            #non electric source like Natural Gas, Wood, Propane, Oil 
                            # To distribute the additional heating load, we assume the nmber houses that 
                            # convert from their current primary heating mechanism to HP will be 
                            # proportional to the current numbers
                            # for example: if 100 houses convert to HP and there are 1000 houses with
                            # electrc and 4000 houses with non electric, then it is assumed that 20 of the 
                            # houses that have heat pump will have electric and 80 will have non electric heating

                            # To convert from heat to electric, we assume COP of 1
                            addl_heat_load_electric_mwh = addl_heat_load_kj* \
                                                                    (electric_house_num/num_houses)/ \
                                                                        3600/1000 #converting KJ to MWh

                            hp_electric_load_cooling_mwh =hourly_electric_usage['cooling_load_KWh']* \
                                                                num_houses*hp_pen_rate*cluster_proportion/ \
                                                                        1000 #in MWh
                            addl_cool_load_kj = hourly_electric_usage['cooling_load_additional_KJ']* \
                                                            num_houses*hp_pen_rate*cluster_proportion # in KJ

                            # for cooling, the entire additional load comes from electric with a COP of 1
                            addl_cool_load_mwh = addl_cool_load_kj/3600/1000 # in MWh

                            total_hourly_annual_electric_load = np.array(hp_electric_load_heating_mwh + \
                                                                addl_heat_load_electric_mwh + \
                                                                hp_electric_load_cooling_mwh + \
                                                                addl_cool_load_mwh)  #array of size 8760
                            
                            load_profile_24hr_mean = total_hourly_annual_electric_load.reshape(-1, 24).mean(axis=0)
                            top_n_ind = total_hourly_annual_electric_load.reshape(-1, 24).sum(axis=1).argpartition(top_n)[-top_n:]
                            #print(max_load_day)
                            load_profile_24hr_max = total_hourly_annual_electric_load.reshape(-1, 24)[top_n_ind, :].mean(axis=0)

                            provincial_yearly_dict[forecast_year]['total_electric_energy_MWh'] +=total_hourly_annual_electric_load.sum().astype(float)

                            provincial_yearly_dict[forecast_year]['load_profile_24h_mean_MWh'] +=load_profile_24hr_mean
                            provincial_yearly_dict[forecast_year]['load_profile_24h_max_MWh'] +=load_profile_24hr_max
                        #ipdb.set_trace()


        province_df['province'] = [province] * len(year_list)
        province_df['forecast_year'] = year_list 
        province_df['total_electric_energy_MWh'] = [provincial_yearly_dict[year]['total_electric_energy_MWh'] for year in year_list]
        province_df['load_profile_24h_mean_MWh'] = [provincial_yearly_dict[year]['load_profile_24h_mean_MWh'] for year in year_list]
        province_df['load_profile_24h_max_MWh'] = [provincial_yearly_dict[year]['load_profile_24h_max_MWh'] for year in year_list]
        if province_df['total_electric_energy_MWh'].sum()>0:
            electic_load_canada_forecast_df = pd.concat((electic_load_canada_forecast_df, province_df), axis=0)
         
    electic_load_canada_forecast_df.to_csv(f'{save_folder}/electric_energy_n_load_profile_forecast_hp_fixed_penrate.csv')


if __name__=='__main__':
    main()