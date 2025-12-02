import numpy as np 
import matplotlib.pyplot as plt 
import os 
import pandas as pd 
import seaborn as sns 


save_folder = '../results/plots/heatpumps'
os.makedirs(save_folder, exist_ok=True)

heatpumpdata = ['HPCAP', 'HPEquipType', 'HPESTAR' ,'HPSOURCE', 'COP']
building_chars = ['HEATEDFLOORAREA', 'BUILDINGTYPE', 'HOUSEID', 'HOUSEREGION', 'YEARBUILT']
location_data = ['HOUSEREGION', 'CLIENTPCODE', 'CLIENTCITY']

thermal_envelope_metrics = ['EGHHLWALLS', 'EGHHLCEILING', 'EGHHLWINDOOR', 'EGHHLFOUND', 'EGHHLEXPOSEDFLR',  'EGHHLAIR']
energy_performance = ['EGHRATING', 'EGHSPACEENERGY', 'ERSENERGYINTENSITY']
energy_consumption_metrics = ['EGHFCONTOTAL' ,'EGHFCONELEC','EGHFCONNGAS','EGHFCONOIL' , 'EGHFCONPROP','EGHFCONWOOD','EGHFCONWOODGJ']
heating_specific_eng_consumption_metrics = ['EGHHEATFCONSE', 
                                            'EGHHEATFCONSG', 
                                            'EGHHEATFCONSO', 
                                            'EGHHEATFCONSP' ,
                                            'EGHHEATFCONSW',
                                            'ERSWATERHEATINGENERGY',
                                            'EGHSPACEENERGY',
                                            'ERSSPACECOOLENERGY']
weather_data = ['WEATHERLOC', 'WTHDATA', 'CoolingSeasonMonths', 'TMAIN', 'QTOT', 'QWARN']
temperature_setting = ['ThermostatCooling', 'ThermostatHeatingNighttime']
time_info = ['CREATIONDATE', 'ENTRYDATE']

#read the data 

hp_data_file = '../data/raw_data/heatpump/ECCC_2023.csv'
hp_data = pd.read_csv(hp_data_file)

#plot the histogram of the fraction of heatloss through ventiliation

for c in thermal_envelope_metrics:
    print(c, hp_data[c].mean())
thermal_data = np.array(hp_data[thermal_envelope_metrics])
plt.hist(thermal_data[:,-1]/thermal_data.sum(axis=1), bins=100)
plt.xlabel('Fraction of total heat loss from ventilation')
plt.grid(True, linestyle='--')
plt.ylabel('Number of houses')
plt.savefig(f"{save_folder}/hp_ventilation_loss_hist.svg", format='svg', bbox_inches='tight')
plt.close()


#plot histogram of heat pump size 

non_zero_hp_cap = hp_data[hp_data['HPCAP'] > 3500*0.5]
bins= [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5, 5, 5.5, 6, 6.5, 7, 8]
plt.hist(non_zero_hp_cap['HPCAP']/3500, bins=bins)
plt.xlabel('Heat Pump size (in Tons)')
plt.ylabel('Number of houses')
plt.grid(True, linestyle='--')
plt.savefig(f"{save_folder}/hp_heatpumpsize_hist.svg", format='svg', bbox_inches='tight')
plt.close()

