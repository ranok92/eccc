import glob 
import pandas as pd 
import numpy as np


def get_24h_ev_load(foldername, bus_name, year, ev_types=['ldev', 'mhdev']):
    fnames = []
    for ev in ev_types:
        fnames.append(glob.glob(f"{foldername}/{year}_{ev}_load.csv")[0])
    
    load_data = []
    for filename in fnames:
        try:
            df = pd.read_csv(filename)
            load_data.append(df[bus_name])
        except:
            print('Cant find ', bus_name, filename)
            continue
    load_data_arr = np.array(load_data)
    return load_data_arr.sum(axis=0)


def get_total_load(base_folders, year):
    '''
    base_folder: dictionary containing results of overload analysis for different 
    representative network
        {'rural' : 'path1', 'urban': 'path2', 'suburban': 'path3'}
    '''
    rep_area_pop = {'urban': 9450, 'suburban': 28350, 'rural': 6280}

    canada_pop = {'urban' : [2922179,
                        1563021,
                        1038785,
                        863690,
                        236605,
                        186811,
                        138862,
                        97911,
                        74502,
                        17836,
                        5852,
                        5783,
                        4308,
                        ],
    'suburban': [11688717, 
                        6252082,
                        4155139,
                        3454760,
                        946418,
                        747244,
                        555446,
                        391646,
                        298005,
                        71346,
                        23406,
                        23132,
                        17232,
                        ],
    'rural' : [2011334,
                        1738395,
                        675266,
                        693924,
                        359245,
                        394010,
                        419553,
                        410100,
                        227264,
                        82181,
                        13582,
                        13925,
                        21301,
                        ]
    }
    load_multiplier = {'urban' : {'Res': 252, 'Comm': 6, 'Pub': 24}, 
                  'suburban': {'Res': 756, 'Comm': 18, 'Indst': 18},
                  'rural': {'Res' : 1}}
    
    area_load = {'urban': {'Res': 0, 'Comm': 0, 'Pub': 0}, 
                 'suburban': {'Res': 0, 'Comm': 0, 'Indst': 0},
                 'rural': 0}
    for area, base_folder in base_folders.items():
        fnames = glob.glob(f'{base_folder}/{year}*load.csv')
        
        data_full = pd.DataFrame()
        for fname in fnames:
            data = pd.read_csv(fname)
            if 'ldev' in fname:
                data['vehicle_type'] = 'ldev'
                data_full = pd.concat([data_full, data])
    
            if 'mhdev' in fname:
                data['vehicle_type'] = 'mhdev'
                data_full = pd.concat([data_full, data])
    
    
        if area=='rural':
            colnames = data_full.columns
            for col in colnames:
                if 'bus' in col:
                    area_load[area] += data_full[col].sum()
            area_load[area] = area_load[area]*1*sum(canada_pop[area])/rep_area_pop[area]*365/(1000*1000)
        else:    
            for key in load_multiplier[area].keys():
                rep_network_load = data_full[key].sum()*load_multiplier[area][key]
                #print(f'{area} -> {key} : {rep_network_load}')
                area_load[area][key]+=rep_network_load*sum(canada_pop[area])/rep_area_pop[area]*365/(1000*1000)
    
    return area_load