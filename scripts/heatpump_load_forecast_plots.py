import pandas as pd 
import seaborn as sns
import os 
import matplotlib.pyplot as plt
import numpy as np
import re
from plot_utils import plot_dataframe_lines_with_shading

save_folder = '../results/plots/heatpumps/'

forecast_penrate_provinces = pd.read_csv('../data/formatted_data/heatpump/hp_penetration_rate_province_yearly.csv')

heating_pattern_24h_all = pd.read_csv('../data/formatted_data/heatpump/normalized_24h_heating_pattern.csv')

load_forecast_data = pd.read_csv('../results/heatpump_forecast/electric_energy_n_load_profile_forecast_hp_fixed_penrate.csv')


########### penetration rate

group_wise_yearly_penetration_rate_forecast = pd.read_csv('../data/formatted_data/heatpump/hp_penetration_rate_forecast_by_group_all_province.csv')
group_wise_yearly_penetration_rate_forecast.rename(
                    columns={ 
                             'hp_penetration_rate': 'Penetration Rate (%)',
                             'province': 'Province'}, inplace=True)


ax = sns.lineplot(group_wise_yearly_penetration_rate_forecast, x='Year', y='Penetration Rate (%)', hue='Province', palette='tab20')
ax.set_xlim(2025, 2050)
plt.grid(True, linestyle='--')
plt.savefig(f'{save_folder}/pernetration_acc_provinces_groups.svg', format='svg', bbox_inches='tight')
plt.close()

########### heating pattern 

heating_pattern_24h_all['fraction_of_daily_heating']*=100
ax = sns.lineplot(heating_pattern_24h_all, x='Hour of the day', y='fraction_of_daily_heating', hue='Building Type', palette='tab20')
ax.set_ylabel("Daily heating load (%)")
plt.grid(True, linestyle='--')
ax.set_xlim(0, 23)

plt.savefig(f'{save_folder}/heating_load_pattern.svg', format='svg', bbox_inches='tight')
plt.close()


########## energy forecast plot

load_forecast_data['Energy required (in TWh)'] = load_forecast_data['total_electric_energy_MWh']/1000000
load_forecast_data.rename(
                columns={'forecast_year': 'Year', 
                         'province':'Province', 
                         'total_electric_energy_MWh': 'Energy required (in MWh)'
                         }, inplace=True)

ax = sns.lineplot(load_forecast_data, x='Year', y='Energy required (in TWh)', hue='Province', palette='tab20')
ax.set_xlim(2025, 2050)
plt.grid(True, linestyle='--')
plt.savefig(f'{save_folder}/HP_provincewise_energy_forecast.svg', format='svg', bbox_inches='tight')
plt.close()

########### load forecast across all provinces 

col_names = ['load_profile_24h_max_MWh', 'load_profile_24h_mean_MWh']
year = 2050
for col_name in col_names:
    provinces = load_forecast_data['Province'].unique()
    provincewise_load_profile = pd.DataFrame()
    for province in provinces:
        load_data_province = load_forecast_data[(load_forecast_data['Province']==province) & (load_forecast_data['Year']==year)]
        load_data_mean_profile = np.array(load_data_province[col_name])
        array_data = []
        for data in load_data_mean_profile:
            data = data.strip('[]')
            data = re.sub(r'\n', '', data)
            data = data.split(' ')
            #print(len(data))
            array_data.append([val for val in data if len(val)>0])
        array_data = np.array(array_data).astype(float)
        provincewise_load_profile[province] = array_data.mean(axis=0)

    ax = sns.lineplot(provincewise_load_profile, palette='tab20')
    # fig, ax = plot_dataframe_lines_with_shading(provincewise_load_profile, 
    #                                        color_palette='tab20',alpha=0.7,
    #                                        xlabel='Energy required (in TWh)')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    ax.set(xlabel ="Hour of the day", ylabel = "Load MW")
    ax.set_xlim(0,23)
    ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))

    plt.grid(True, linestyle='--')
    plt.savefig(f'{save_folder}/hp_provincewise_{col_name}_{year}.svg', format='svg', bbox_inches='tight')
    plt.close()

########## load forecast over years 

    yearwise_load = pd.DataFrame()
    for year in range(2025, 2055,5):
        load_data_year = load_forecast_data[(load_forecast_data['Year']==year)]
        load_data_profile = np.array(load_data_year[col_name])
        array_data = []
        for data in load_data_profile:
            data = data.strip('[]')
            data = re.sub(r'\n', '', data)
            data = data.split(' ')
            #print(len(data))
            array_data.append([val for val in data if len(val)>0])
        array_data = np.array(array_data).astype(float)
        yearwise_load[year] = array_data.sum(axis=0)

    fig, ax = plot_dataframe_lines_with_shading(yearwise_load, 
                                        color_palette='copper',
                                        alpha=1,
                                        xlabel='Load (MW)')
    ax.set_xlim(0,23)
    ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))

    ax.set(xlabel ="Hour of the day", ylabel = "Load MW")
    plt.grid(True, linestyle='--')
    plt.savefig(f'{save_folder}/hp_yearly_load_change_{col_name}.svg', format='svg', bbox_inches='tight')
    plt.close()