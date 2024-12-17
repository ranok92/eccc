# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:05:27 2024

@author: weixu
"""
import numpy as np
import pandapower as pp
from util import  net_visualize 
# Create an empty network

def Parameters(network_type):
    
    '''
    parameters of transformers and lines in UofT report Tab.35 and Tab.36

    Returns
    -------
    net 

    '''
    param_dict = {}
    T_params_urban = {
        "T1": {
            "sn_mva": 50,
            "vn_hv_kv": 120,
            "vn_lv_kv": 12.5,
            "vk_percent": 10,
            "vkr_percent": 0.1,
            "pfe_kw": 50,
            "i0_percent": 0.1,
            "shift_degree": 30,
            "vector_group": "Dyg"
        },
        "T2": {
            # "sn_mva": 0.1,
            "sn_mva":2,
            "vn_hv_kv": 12.5,
            "vn_lv_kv": 0.6,
            "vk_percent": 3,
            "vkr_percent": 0.1,
            "pfe_kw": 10,
            "i0_percent": 0.1,
            "shift_degree": 30,
            "vector_group": "Dyg"
        },
        "T3": {
            "sn_mva": 0.5,
            "vn_hv_kv": 12.5,
            "vn_lv_kv": 0.208,
            "vk_percent": 4,
            "vkr_percent": 0.2,
            "pfe_kw": 5,
            "i0_percent": 0.1,
            "shift_degree": 30,
            "vector_group": "Dyg"
        },
        "T4": {
            "sn_mva": 0.1,
            "vn_hv_kv": 12.5,
            "vn_lv_kv": 0.208,
            "vk_percent": 4,
            "vkr_percent": 0.2,
            "pfe_kw": 2,
            "i0_percent": 0.1,
            "shift_degree": 0
        },
        "T5": {
            "sn_mva": 0.1,
            "vn_hv_kv": 12.5,
            "vn_lv_kv": 0.208,
            "vk_percent": 5,
            "vkr_percent": 0.2,
            "pfe_kw": 2,
            "i0_percent": 0.1,
            "shift_degree": 0
        }      }
    L_params_urban = {
    "Mfd": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.07,
        "x_ohm_per_km": 0.106,
        "max_i_ka": 0.4,
        "type": "ol"  # Overhead line
    },
    "Lat": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.6,
        "x_ohm_per_km": 0.38,
        "max_i_ka": 0.12,
        "type": "ol"  # Overhead line
    },
    "Lat_UG": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.6,
        "x_ohm_per_km": 0.38,
        "max_i_ka": 0.12,
        "type": "cs"  # underground
    }
    }
    param_dict['urban'] = (T_params_urban, L_params_urban)

    #adding the suburban parameters 
    T_params_suburban = {
        "T1": {
            "sn_mva": 100,
            "vn_hv_kv": 240,
            "vn_lv_kv": 25,
            "vk_percent": 10,
            "vkr_percent": .5,
            "pfe_kw": 1,
            "i0_percent": 0.1,
            "shift_degree": 30,
            "vector_group": "YGyg"
        },
        #residential underground 
        "T2": {
            # "sn_mva": 0.1,
            "sn_mva":0.1,
            "vn_hv_kv": 25,
            "vn_lv_kv": 0.208,
            "vk_percent": 4,
            "vkr_percent": 1,
            "pfe_kw": .002,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Dyg"
        },
        #residential overhead
        "T3": {
            "sn_mva": 0.1,
            "vn_hv_kv": 25,
            "vn_lv_kv": 0.208,
            "vk_percent": 4,
            "vkr_percent": 1,
            "pfe_kw": .002,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Dyg"
        },
        #industrial
        "T4": {
            "sn_mva": 1,
            "vn_hv_kv": 25,
            "vn_lv_kv": 0.208,
            "vk_percent": 3,
            "vkr_percent": 1.5,
            "pfe_kw": .01,
            "i0_percent": 0.1,
            "shift_degree": 0
        },
        #commercial
        "T5": {
            "sn_mva": 1,
            "vn_hv_kv": 25,
            "vn_lv_kv": 0.208,
            "vk_percent": 3,
            "vkr_percent": 1.5,
            "pfe_kw": 0.01,
            "i0_percent": 0.1,
            "shift_degree": 0
        }      }
    
    L_params_suburban = {
    "Mfd": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.128,
        "x_ohm_per_km": 0.114,
        "max_i_ka": 0.4,
        "type": "ol"  # Overhead line
    },
    "Lat": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.6,
        "x_ohm_per_km": 0.38,
        "max_i_ka": 0.12,
        "type": "ol"  # Overhead line
    },
    "Lat_UG": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.6,
        "x_ohm_per_km": 0.38,
        "max_i_ka": 0.12,
        "type": "cs"  # underground
    },
    "Fegr" : {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.08,
        "x_ohm_per_km": 0.06,
        "max_i_ka": 0.4,
        "type": "cs"  # underground 
    }
    }
    param_dict['suburban'] = (T_params_suburban, L_params_suburban)


    return param_dict[network_type][0], param_dict[network_type][1]



def build_net():
    '''
    build a network with 1 main feeder as shown in Fig.56 in UofT report
    This is for plotting the bus diagram for demonstration
    Returns
    -------
    net 

    '''
    
    net = pp.create_empty_network()
    
    
    T_params, L_params = Parameters('urban')
    for key, params in T_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="trafo")
    
    for key, params in L_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="line")
    
    
    
    # Step 1: Add buses for different voltage levels
    # Main Substation HV and LV buses
    bus_hv = pp.create_bus(net, vn_kv=120, name="HV")
    bus_lv = pp.create_bus(net, vn_kv=12.5, name="Subst")
    # feeder_bus = pp.create_bus(net, vn_kv=12.5, name="Feeder Bus")
    # Create a transformer (step down from 120 kV to 12.5 kV)
    pp.create_transformer(net, hv_bus= bus_hv, lv_bus=bus_lv , std_type="T1", name='T1')
    pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0, name='')
    pp.create_shunt(net, bus=bus_lv, q_mvar=10, name="Capacitor Bank")
                       # "HV Slack Bus")
    
    # Create a line (transfer power at 12.5 kV)
    
    
    
    buses_feeder = pp.create_buses(net, nr_buses = 4,vn_kv = 12.5,name='')
                                   # name = ["Comm_in","Public_in", "Res_in1","Res_in2"])
    
    
    pp.create_line(net, from_bus=bus_lv, to_bus=buses_feeder[0], length_km=1, std_type="Mfd")
    pp.create_lines(net, buses_feeder[:-1], buses_feeder[1:],length_km = [1,1,1], std_type='Mfd')
    
    #commercial 
    bus_comm =  pp.create_bus(net, vn_kv=0.6,name='Comm', zone='Comm')
    pp.create_transformer(net, buses_feeder[0], bus_comm,std_type='T2', name='T2')
    # public
    pub_num = 4
    bus_public_feeder = pp.create_buses(net, pub_num ,12.5, name = '')
                                        # ['PubFeed{}'.format(_) for _ in range(pub_num )] )
    bus_public = pp.create_buses(net, pub_num ,0.208, name = ['Pub{}'.format(_) for _ in range(pub_num )] ,
                                 zone = 'Pub')
    
    pp.create_lines( net, [buses_feeder[1] for _ in range(pub_num)],bus_public_feeder
                    ,length_km = [1 for _ in range(pub_num)], std_type='Mfd')
    
    for _ in range(pub_num): 
        pp.create_transformer( net,bus_public_feeder[_], bus_public[_],
                              std_type='T3',name ='T3')
    
    # Res
    res_num = 7 
    res_feeder0 = buses_feeder[2]
    for res_sub_feeder in range(3):
        res1_feed = pp.create_buses(net,res_num , 12.5, name='')
        res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res')
        pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder0 ),res1_feed ,
                        length_km =  [1 for _ in range(res_num )], std_type='Lat_UG')
        
        for _ in range(res_num ): 
            pp.create_transformer( net, res1_feed[_], res1_house[_],
                                  std_type='T4',name ='T4')
    
    res_num = 7 
    res_feeder0 = buses_feeder[3]
    for res_sub_feeder in range(3):
        res1_feed = pp.create_buses(net,res_num , 12.5, name='')
        res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res')
        pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder0 ),res1_feed ,
                        length_km =  [1 for _ in range(res_num )], std_type='Lat')
        
        for _ in range(res_num ): 
            pp.create_transformer( net, res1_feed[_], res1_house[_],
                                  std_type='T5',name ='T5')
    
    
    
    net_visualize(net  )
    net.bus_geodata['y'] ,net.bus_geodata['x']  = -net.bus_geodata['x'] , -net.bus_geodata['y'] 
    # net_visualize(net  )
    
    return net


def build_net_2():
    '''
    build a network with 6 main feeder 

    Returns
    -------
    net 

    '''
    net = pp.create_empty_network()
    
    
    T_params, L_params = Parameters('urban')
    for key, params in T_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="trafo")
    
    for key, params in L_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="line")
    
    
    
    # Step 1: Add buses for different voltage levels
    # Main Substation HV and LV buses
    bus_hv = pp.create_bus(net, vn_kv=120, name="HV")
    bus_lv = pp.create_bus(net, vn_kv=12.5, name="Subst")
    # feeder_bus = pp.create_bus(net, vn_kv=12.5, name="Feeder Bus")
    # Create a transformer (step down from 120 kV to 12.5 kV)
    pp.create_transformer(net, hv_bus= bus_hv, lv_bus=bus_lv , std_type="T1", name='T1')
    pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0, name='')
    pp.create_shunt(net, bus=bus_lv, q_mvar=10, name="Capacitor Bank")
                       # "HV Slack Bus")
    
    # Create a line (transfer power at 12.5 kV)
    
    for T1_feeder in range(6):
    
        buses_feeder = pp.create_buses(net, nr_buses = 4,vn_kv = 12.5,name='')
                                       # name = ["Comm_in","Public_in", "Res_in1","Res_in2"])
        
        
        pp.create_line(net, from_bus=bus_lv, to_bus=buses_feeder[0], length_km=1, std_type="Mfd")
        pp.create_lines(net, buses_feeder[:-1], buses_feeder[1:],length_km = [1,1,1], std_type='Mfd')
        
        #commercial 
        bus_comm =  pp.create_bus(net, vn_kv=0.6,name='Comm', zone='Comm')
        pp.create_transformer(net, buses_feeder[0], bus_comm,std_type='T2', name='T2')
        # public
        pub_num = 4
        bus_public_feeder = pp.create_buses(net, pub_num ,12.5, name = '')
                                            # ['PubFeed{}'.format(_) for _ in range(pub_num )] )
        bus_public = pp.create_buses(net, pub_num ,0.208, name = ['Pub{}'.format(_) for _ in range(pub_num )] ,
                                     zone = 'Pub')
        
        pp.create_lines( net, [buses_feeder[1] for _ in range(pub_num)],bus_public_feeder
                        ,length_km = [1 for _ in range(pub_num)], std_type='Mfd')
        
        for _ in range(pub_num): 
            pp.create_transformer( net,bus_public_feeder[_], bus_public[_],
                                  std_type='T3',name ='T3')
        
        # Res
        res_num = 7 
        res_feeder0 = buses_feeder[2]
        for res_sub_feeder in range(3):
            res1_feed = pp.create_buses(net,res_num , 12.5, name='')
            res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res')
            pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder0 ),res1_feed ,
                            length_km =  [1 for _ in range(res_num )], std_type='Lat_UG')
            
            for _ in range(res_num ): 
                pp.create_transformer( net, res1_feed[_], res1_house[_],
                                      std_type='T4',name ='T4')
        
        res_num = 7 
        res_feeder0 = buses_feeder[3]
        for res_sub_feeder in range(3):
            res1_feed = pp.create_buses(net,res_num , 12.5, name='')
            res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res')
            pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder0 ),res1_feed ,
                            length_km =  [1 for _ in range(res_num )], std_type='Lat')
            
            for _ in range(res_num ): 
                pp.create_transformer( net, res1_feed[_], res1_house[_],
                                      std_type='T5',name ='T5')
    
    
    
    # net_visualize(net  )
    net.bus_geodata['y'] ,net.bus_geodata['x']  = -net.bus_geodata['x'] , -net.bus_geodata['y'] 
    # net_visualize(net  )
    
    return net


def build_net_suburban(feeder_lines=1, res_units=3):
    '''
    Building the suburban network
    '''
    net = pp.create_empty_network()

    #fetch parameters
    T_params, L_params = Parameters('suburban')
    for key, params in T_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="trafo")
    
    for key, params in L_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="line")
    
    #create the buses
    bus_hv = pp.create_bus(net, vn_kv=120, name="HV")
    bus_lv_1 = pp.create_bus(net, vn_kv=25, name='Subst')

    #substation network 1
    pp.create_transformer(net, hv_bus= bus_hv, lv_bus=bus_lv_1 , std_type="T1", name='T1')
    pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0, name='')
    pp.create_shunt(net, bus=bus_lv_1, q_mvar=20, name="Capacitor Bank")
    

    line_counter = 1
    for i in range(feeder_lines):
        #crete the buses
        bus_names = [f'ext_bus_{i}', 
                     f'res_ug_bus_{i}', 
                     f'res_oh_bus_{i}',
                     f'indst_bus{i}', 
                     f'comm_bus_{i}']
        
        buses_feeder = pp.create_buses(net, nr_buses = 5,vn_kv = 24.9,name=bus_names)
                                       # name = ["Comm_in","Public_in", "Res_in1","Res_in2"])
        
        
        pp.create_line(net, 
                      from_bus=bus_lv_1, 
                      to_bus=buses_feeder[0], 
                      length_km=1, 
                      std_type="Fegr",
                      name='L1')
        backbone_line_names = ['L4', 'L12', 'L20', 'L21']
        pp.create_lines(net, 
                        buses_feeder[:-1], 
                        buses_feeder[1:],
                        length_km = [5,5,5,5], 
                        std_type='Mfd',
                        names=backbone_line_names)
        
        #residential underground
        res_num = res_units
        res_feeder_backbone = buses_feeder[1]
        for res_sub_feeder in range(3):
            res1_feed = pp.create_buses(net,res_num , 24.9, name='')
            res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res UG')
            pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder_backbone ),res1_feed ,
                            length_km =  [1 for _ in range(res_num )], std_type='Lat_UG')
            
            for _ in range(res_num ): 
                pp.create_transformer( net, res1_feed[_], res1_house[_],
                                      std_type='T2',name ='T2')
        #residential overhead
        res_num = res_units
        res_feeder_backbone = buses_feeder[2]
        for res_sub_feeder in range(3):
            res1_feed = pp.create_buses(net,res_num , 24.9, name='')
            res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res')
            pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder_backbone ),res1_feed ,
                            length_km =  [1 for _ in range(res_num )], std_type='Lat')
            
            for _ in range(res_num ): 
                pp.create_transformer( net, res1_feed[_], res1_house[_],
                                      std_type='T3',name ='T3')
        
        #industrial 
        indst_feeder_backbone = buses_feeder[3]
        indst_feeder = pp.create_bus(net, 0.208, name='Indst', zone='Indst')
        pp.create_transformer(net, indst_feeder_backbone, indst_feeder, std_type='T4', name='T4')
        net.bus_geodata['y'] ,net.bus_geodata['x']  = -net.bus_geodata['x'] , -net.bus_geodata['y'] 

        
        #commercial 
        comm_feeder_backbone = buses_feeder[4]
        comm_feeder = pp.create_bus(net, 0.208, name='Comm', zone='Comm')
        pp.create_transformer(net, comm_feeder_backbone, comm_feeder, std_type='T5', name='T5')
    


    return net

    