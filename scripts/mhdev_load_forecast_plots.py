import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import os 
import numpy as np
from plot_utils import plot_dataframe_lines_with_shading

save_folder = '../results/plots/mhdev_load_forecast_plots'
os.makedirs(save_folder, exist_ok=True)


mhdev_depot_charging_data_file = "D:/Work/eccc/data/formatted_data/mhdev_depot_charge_percent_per_hr.xlsx"
mhdev_depot_charging_data = pd.read_excel(mhdev_depot_charging_data_file, sheet_name='Load_Curves')

opp_charging_f = '../data/formatted_data/mhdev_opportunity_charge_percent_per_hr.csv'
opp_charging = pd.read_csv(opp_charging_f)
mhdev_depot_charging_data.drop(columns=['Category', 'days', 'vocation'], inplace=True)
mhdev_depot_charging_data.rename(columns={'hour': 'Hour of the day', 'charge_percent':'Charging share (%)', 'class':'Class'}, inplace=True)



ax = sns.lineplot(mhdev_depot_charging_data.groupby(['Hour of the day', 'Class'], as_index=False).mean(), 
                    x='Hour of the day', 
                    y='Charging share (%)', 
                    errorbar=None,
                    )
fig = ax.get_figure()
ax.set_xlim(0, 23)
ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))
fig = ax.get_figure()
plt.grid(True, linestyle='--')
plt.savefig(f"{save_folder}/depot_charging.svg", format='svg', bbox_inches='tight')
plt.close()


opp_charging.drop(columns=['Unnamed: 0', 'vehicle_id'], inplace=True)
opp_charging.rename(columns={'class': 'Class', 'hour': 'Hour of the day', 'charge_percent': 'Charging share (%)'}, inplace=True)
ax = sns.lineplot(opp_charging.groupby(['Hour of the day', 'Class'], as_index=False).mean(),
                   x='Hour of the day', 
                   y='Charging share (%)',
                   )
ax.set_xlim(0, 23)
ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))

fig = ax.get_figure()
plt.grid(True, linestyle='--')
fig = ax.get_figure()
plt.savefig(f"{save_folder}/opportunity_charging.svg", format='svg', bbox_inches='tight')
plt.close()

#province wise 24hr load

load_data = pd.read_csv('../results/load_forecast/daily_load_profile_across_year_province_charge_type_high_adopt.csv')

#load_data.drop(columns=['Unnamed: 0'])
load_data.rename(columns={'hour':'Hour of the day', 'year': 'Year', 'province': 'Province'} ,inplace=True)

load_type = ['depot', 'opportunity']
load_data['Load (MW)'] = load_data['load (kw)']/1000

vehicle_type = ['mdev','hdev']
load_data_years = load_data[load_data['Year'].isin(range(2025,2055,5))]
for load in load_type:
    for vehicle in vehicle_type:
        plot_df = pd.DataFrame()
        for year in range(2025,2055,5):
            plot_df[year] = load_data_years[
                                (load_data_years['load_type']==load) &  
                                    (load_data_years['vehicle_type']==vehicle) & 
                                        (load_data_years['Year']==year)
                                        ].groupby('Hour of the day').sum()['Load (MW)']

        #load_spec = load_data_years[(load_data_years['load_type']==load) & (load_data_years['vehicle_type']==vehicle)]

        #ax = sns.lineplot(load_spec, x='Hour of the day', y='Load (MW)', hue='Year', errorbar=None, palette='copper')
        fig, ax = plot_dataframe_lines_with_shading(plot_df, 
                                    color_palette='copper',
                                    alpha=1,
                                    ylabel='Load (MW)',
                                    xlabel='Hour of the day')
        ax.set_xlim(0, 23)
        ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))

        fig = ax.get_figure()
        plt.grid(True, linestyle='--')
        
        plt.savefig(f"{save_folder}/{vehicle}_{load}_24hpattern.svg", format='svg', bbox_inches='tight')
        plt.close()

load_data_2050 = load_data_years[load_data_years['Year']==2050]
ax = sns.lineplot(load_data_2050.groupby(['Province', 'Year', 'Hour of the day'], as_index=False).sum(), 
                  x='Hour of the day', 
                  y='Load (MW)', 
                  hue='Province', 
                  palette='tab20')
ax.set_xlim(0, 23)
ax.set_xticks(ticks=np.arange(0,24,2), labels=np.arange(0,24,2))

fig = ax.get_figure()
plt.grid(True, linestyle='--')
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.savefig(f"{save_folder}/provincewise_load_2050.svg", format='svg', bbox_inches='tight')
plt.close()