import glob
import json
from heatpump_utils import *
import pickle
#read the penetration rates for each group


def main():
    # eccc_db_fname = '../../data/raw_data/heatpump/ECCC_2023.csv'
    # eccc_data = pd.read_csv(eccc_db_fname)
    group_penrate_forecast_fname = '../data/formatted_data/heatpump/hp_penetration_rate_forecast_by_group_all_province.csv'
    heatpump_data_fname = '../data/formatted_data/heatpump/hp_coeff_data_interpolated.json'
    norm_heating_pattern = '../data/formateed_data/heatpump/normalized_24h_heating_pattern.csv'
    hpsize_classifier_fname = '../data/formatted_data/heatpump/KNN_HPSIZE_classifier'

    groupwise_clustering_basefolder = '../../data/formatted_data/heatpump/groupwise_cluster_centers/'
    cluster_filename_str = '{0}/{1}/{1}_{2}_{3}_cluster_centers.csv'
    feature_cols_KNN = ['HEATEDFLOORAREA' , 'EGHSPACEENERGY']
    hp_size_classifier = pickle.load(open(hpsize_classifier_fname))

    with open(heatpump_data_fname, 'r') as f:
        heatpump_coeff_interpolated_data = json.load(f)

    groupwise_penetration_rate_forecast = pd.read_csv(group_penrate_forecast_fname)
    province_name_dict = {
                            'alberta': 'AB', 
                            'british columbia': 'BC',
                            'manitoba': 'MN',
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
    house_type_list = groupwise_penetration_rate_forecast['house_type'].unique()
    year_list = groupwise_penetration_rate_forecast['forecast_year'].unique()

    for province in province_list:
        for year_of_const in year_of_constrution_list:
            for house_type in house_type_list:
                #read the representative house data for each cluster of a group 
                try:
                    cluster_pd = pd.read_csv(cluster_filename_str.format(groupwise_clustering_basefolder,
                                                                        province_name_dict[province], 
                                                                        house_type,
                                                                        year_of_const))

                    #calculate heating for each representative house in the cluster
                    print(cluster_filename_str.format(groupwise_clustering_basefolder,
                                                                        province_name_dict[province], 
                                                                        house_type,
                                                                        year_of_const))
                    for _, row in cluster_pd.iterrows():
                        #assign heatpump if absent 
                        if row['HPSOURCE']=='N/A {no Heat Pump}':
                            #assign heatpump
                            row['hp_coeff_data_interpolated'] = 'Air'
                            row['HPCAP'] = neigh.predict(np.array([row[feature_cols_KNN]]))
                        
                        hourly_electric_usage = get_hourly_electricity_usage_for_house(row, heatpump_coeff_interpolated_data)
                            
                    
                except Exception as e:
                    #print(f'{cluster_filename_str.format(groupwise_clustering_basefolder, province_name_dict[province], house_type,year_of_const)} was not found.')
                    print(e)
                    pass


if __name__=='__main__':
    main()