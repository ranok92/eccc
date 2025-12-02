import seaborn as sns 
import pandas as pd 
import os 
import matplotlib.pyplot as plt

save_folder = '../results/plots/mhdev_energy_forecast_plots'
os.makedirs(save_folder, exist_ok=True)
sns.set_palette("tab10")

fnames = ["../results/energy_forecast/canadawide_energy_requirement_forecast_mdev_high_adopt.csv", 
          "../results/energy_forecast/canadawide_energy_requirement_forecast_hdev_high_adopt.csv"]

for fname in fnames:
    data = pd.read_csv(fname)
    vehicle_type = fname.split('_')[-3]
    data.rename(columns={'fuel_type':'Fuel type', 'power_required (GWh)':'Energy required(GWh)', 'province':'Province'}, inplace=True)
    
    #vehicle numbers forecast
    
    axbar = sns.barplot(data[data['Fuel type']=='All fuel type'].groupby(by=['year'], as_index=False).sum(), x='year',y='market_share_numbers')
    plt.grid(True, linestyle='--')

    axbar.set_ylabel('Number of vehicles (in millions)')
    axbar.set_xlabel('Forecast year')
    
    for ind, label in enumerate(axbar.get_xticklabels()):
        if ind % 5 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    
    fig = axbar.get_figure()
    plt.savefig(f"{save_folder}/{vehicle_type}_total_number_forecast.svg", format='svg', bbox_inches='tight')
    plt.close()

    
    #EV sales as a percentage of total sales
    
    axbar = sns.barplot(data.groupby(by=['year','Fuel type'], as_index=False).sum(), hue='Fuel type', x='year',y='sales_numbers')
    #sns.move_legend(axbar, "upper left", bbox_to_anchor=(1, 1))
    plt.grid(True, linestyle='--')

    axbar.set_ylabel('Number of vehicles')
    axbar.set_xlabel('Forecast year')
    for ind, label in enumerate(axbar.get_xticklabels()):
        if ind % 5 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    fig = axbar.get_figure()
    plt.savefig(f"{save_folder}/{vehicle_type}_ev_sales_forecast.svg", format='svg', bbox_inches='tight')
    plt.close()
    

    #EV sales numbers across different provinces

    ax = sns.lineplot(data[data['Fuel type']=='Battery electric'].groupby(['Province', 'year']).sum(), 
                      x='year', 
                      y='market_share_numbers',
                      hue='Province',
                      palette='tab20')
    plt.grid(True, linestyle='--')
    ax.set_ylabel('Number of vehicles')
    ax.set_xlabel('Forecast year')
    ax.set_xlim(2025, 2050)

    for ind, label in enumerate(axbar.get_xticklabels()):
        if ind % 5 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    fig = axbar.get_figure()
    plt.savefig(f"{save_folder}/{vehicle_type}_ev_numbers_forecast_province.svg", format='svg', bbox_inches='tight')
    plt.close()
    

    #Energy required canada
    #data.rename(columns={'power_required (GWh)':'Energy required(GWh)'}, inplace=True)
    ax = sns.lineplot(data[data['Fuel type']=='Battery electric'].groupby('year').sum(), x='year',y='Energy required(GWh)')
    ax.set_xlabel('Forecast year')
    plt.grid(True, linestyle='--')
    ax.set_xlim(2025, 2050)
    for ind, label in enumerate(axbar.get_xticklabels()):
        if ind % 5 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    fig = axbar.get_figure()
    plt.savefig(f"{save_folder}/{vehicle_type}_total_energy_required_canada.svg", format='svg', bbox_inches='tight')
    plt.close()

    #Energy required province
    data.rename(columns={'power_required (GWh)':'Energy required(GWh)', 'province':'Province'}, inplace=True)
    ax = sns.lineplot(data[data['Fuel type']=='Battery electric'].groupby(['year', 'Province']).sum(), 
                                x='year',
                                y='Energy required(GWh)', 
                                hue='Province',  palette='tab20')
    ax.set_xlabel('Forecast year')
    plt.grid(True, linestyle='--')
    ax.set_xlim(2025, 2050)
    for ind, label in enumerate(axbar.get_xticklabels()):
        if ind % 5 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    fig = axbar.get_figure()
    plt.savefig(f"{save_folder}/{vehicle_type}_total_energy_required_provinces.svg", format='svg', bbox_inches='tight')
    plt.close()
