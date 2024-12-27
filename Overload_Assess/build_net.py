# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:05:27 2024

@author: weixu
"""
import numpy as np
import pandapower as pp
from util import  net_visualize, get_bus_index_by_name
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
            "pfe_kw": 50,
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
            "pfe_kw": .2,
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
            "pfe_kw": .2,
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
            "pfe_kw": 5,
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
            "pfe_kw": 5,
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
    T_params_rural = {
        "main_substation": {
            "sn_mva": 20,
            "vn_hv_kv": 110,
            "vn_lv_kv": 27.6,
            "vk_percent": 10,
            "vkr_percent": 0.5,
            "pfe_kw": 20,
            "i0_percent": 0.1,
            "shift_degree": 30,
            "vector_group": "Dyg"
        },

        "T1": {
            "sn_mva":3.6,
            "vn_hv_kv": 27.6,
            "vn_lv_kv": 8.3,
            "vk_percent": 6,
            "vkr_percent": 1,
            "pfe_kw": 3,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Dy"
        },

        "T2": {
            "sn_mva": 15,
            "vn_hv_kv": 27.6,
            "vn_lv_kv": 27.6,
            "vk_percent": 7.3,
            "vkr_percent": 1,
            "pfe_kw": 10,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Yy"
        },

        "T3": {
            "sn_mva": 1,
            "vn_hv_kv": 27.6,
            "vn_lv_kv": 8.3,
            "vk_percent": 4,
            "vkr_percent": 1.5,
            "pfe_kw": 1,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Yy"

        },

        "T4": {
            "sn_mva": 3.6,
            "vn_hv_kv": 27.6,
            "vn_lv_kv": 8.3,
            "vk_percent": 5.65,
            "vkr_percent": 1.5,
            "pfe_kw": 4,
            "i0_percent": 0.1,
            "shift_degree": 0,
            "vector_group": "Dy"

        }      }
    
    L_params_rural = {
    "336AL427": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.169,
        "x_ohm_per_km": 0.418,
        "max_i_ka": 0.665,
        "type": "ol"  # Overhead line
    },
    "10ASR427": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.552,
        "x_ohm_per_km": 0.485,
        "max_i_ka": 0.3,
        "type": "ol"  # Overhead line
    },
    "30ASR427": {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.348,
        "x_ohm_per_km": 0.468,
        "max_i_ka": 0.4,
        "type": "cs"  # underground
    },
    "40ASR427" : {
        "c_nf_per_km": 0,  # Assuming negligible capacitance
        "r_ohm_per_km": 0.277,
        "x_ohm_per_km": 0.459,
        "max_i_ka": 0.460,
        "type": "cs"  # underground 
    }
    }
    param_dict['rural'] = (T_params_rural, L_params_rural)

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


def build_net_suburban(feeder_lines=1, res_num=3):
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

    #substation network 1

    for _ in range(2): #two T1 substations
        bus_lv_1 = pp.create_bus(net, vn_kv=25, name='Subst')
        pp.create_transformer(net, hv_bus= bus_hv, lv_bus=bus_lv_1 , std_type="T1", name='T1')
        pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0, name='')
        pp.create_shunt(net, bus=bus_lv_1, q_mvar=20, name="Capacitor Bank")
        

        for i in range(feeder_lines):
            #crete the external bus
            ext_bus = pp.create_bus(net, vn_kv=24.9, name='ext_bus_{i}')

            
  
            pp.create_line(net, 
                        from_bus=bus_lv_1, 
                        to_bus=ext_bus, 
                        length_km=1, 
                        std_type="Fegr",
                        name='L1')
            backbone_line_names = ['L4', 'L12', 'L20', 'L21']

            for j in range(3): #for lines L2, L3 and L4 originating from ext_bus_{i}
                bus_names = [
                                f'res_ug_bus_{i}_{j}', 
                                f'res_oh_bus_{i}_{j}',
                                f'indst_bus{i}_{j}', 
                                f'comm_bus_{i}_{j}']
                buses_feeder = pp.create_buses(net, nr_buses = 4,vn_kv = 24.9,name=bus_names)
                                            # name = ["Comm_in","Public_in", "Res_in1","Res_in2"])
                
                buses_feeder = np.insert(buses_feeder, 0, ext_bus)
                for i in range(len(backbone_line_names)):
                    pp.create_line(net, 
                                    buses_feeder[i], 
                                    buses_feeder[i+1],
                                    length_km = 5, 
                                    std_type='Mfd',
                                    name=backbone_line_names[i])
                    
                #residential underground
                res_feeder_backbone = buses_feeder[1]
                for _ in range(3): # three lines for underground residence
                    res1_feed = pp.create_buses(net,res_num , 24.9, name='')
                    res1_house = pp.create_buses(net,res_num , 0.208, name='', zone = 'Res UG')
                    pp.create_lines(net, np.insert( res1_feed[:-1], 0 , res_feeder_backbone ),res1_feed ,
                                    length_km =  [1 for _ in range(res_num )], std_type='Lat_UG')
                    
                    for _ in range(res_num ): 
                        pp.create_transformer( net, res1_feed[_], res1_house[_],
                                            std_type='T2',name ='T2')
                #residential overhead
                res_feeder_backbone = buses_feeder[2]
                for _ in range(3): # three lines for underground residence
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


def build_net_rural():

    net = pp.create_empty_network()

    #fetch parameters
    T_params, L_params = Parameters('rural')
    for key, params in T_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="trafo")
    
    for key, params in L_params.items():
        pp.create_std_type(net, params, name=f"{key}", element="line")
    
    #line lengths for rural_network
    line_lengths = [5.7, 1.01, 0.4, 0.38, 0.13, 0.17, 
                    0.26, 0.14, 0.38, 0.56, 0.3, 3.33, 
                    1.03, 1.08, 0.47, 1.94, 0.47, 0.96, 
                    0.19, 1.94, 2.45, 1.63, 1.20, 0.82, 
                    1.55, 2.12, 0.75, 1.07, 2.54, 0.36, 
                    0.26, 3.58, 0.77, 2.08, 4.51, 3.24, 
                    0.30, 0.50]
    
    line_std_types = ["336AL427"]*15 + \
                     ["30ASR427"]*7 + \
                     ["10ASR427"]*3 + \
                     ["30ASR427"] + \
                     ["10ASR427"] * 2 + \
                     ["30ASR427"] + \
                     ["40ASR427"] * 2 + \
                     ["10ASR427"] + \
                     ["40ASR427"] + \
                     ["30ASR427"] + \
                     ["40ASR427"] + \
                     ["336AL427"]* 3
    #create the buses
    bus_hv = pp.create_bus(net, vn_kv=100, name="HV")
    bus_lv_1 = pp.create_bus(net, vn_kv=27.6, name='LV')

    #substation network 1
    substation_trafo = pp.create_transformer(net, 
                          hv_bus=bus_hv, 
                          lv_bus=bus_lv_1, 
                          std_type="main_substation", 
                          name='Substation')
    
    pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0, name='')
    pp.create_shunt(net, bus=bus_lv_1, q_mvar=20, name="Capacitor Bank")
    #create the buses
    #creating the grid part of the grid from 
    # main substation till T2

    #create the buses
    num_buses_part1 = 13
    bus_names_part1 = [ f'bus_{i}' for i in range(1, num_buses_part1+1)]
    buses_part1 = pp.create_buses(net, 
                                  nr_buses=num_buses_part1,
                                  vn_kv = 27.6,
                                  name=bus_names_part1)
                                       # name = ["Comm_in","Public_in", "Res_in1","Res_in2"])
    #connect the lines
    buses_part1_w_subs_trafo = np.insert(buses_part1, 0, bus_lv_1)
    for i in range(4):
        pp.create_line(net,
                    from_bus=buses_part1_w_subs_trafo[i*3], 
                    to_bus=buses_part1_w_subs_trafo[i*3+1], 
                    length_km=line_lengths[i*3], 
                    std_type="336AL427",
                    name=f'L{i*3+1}'
                    )
        pp.create_line(net, 
                    from_bus=buses_part1_w_subs_trafo[i*3+1], 
                    to_bus=buses_part1_w_subs_trafo[i*3+2], 
                    length_km=line_lengths[i*3+1], 
                    std_type="336AL427",
                    name=f'L{i*3+2}')
        pp.create_line(net, 
                    from_bus=buses_part1_w_subs_trafo[i*3+1], 
                    to_bus=buses_part1_w_subs_trafo[i*3+3], 
                    length_km=line_lengths[i*3+3], 
                    std_type="336AL427",
                    name=f'L{i*3+3}')
    pp.create_line(net,
                    from_bus=buses_part1_w_subs_trafo[-2], 
                    to_bus=buses_part1_w_subs_trafo[-1], 
                    length_km=line_lengths[13], 
                    std_type="336AL427",
                    name=f'L13')

    # TODO create load M1-M3 @ bus3 
    # TODO Create load M4-M5 @ bus5, M7 @ bus8, M8 @ bus11, M9-M12 @ bus 12

    #create the second line of buses starting from the 
    #right of T2 till the end in a straight line
    num_buses_part2 = 9
    bus_names_part2 = [f'bus_{i}' for i in range(14, 23)]
    buses_part2 = pp.create_buses(net, 
                                  nr_buses=num_buses_part2,
                                  vn_kv=27.6,
                                  name=bus_names_part2) 
    #add transformer T2
    t2 = pp.create_transformer(net,  
                            hv_bus=buses_part1_w_subs_trafo[-1], 
                            lv_bus=buses_part2[0], 
                            std_type="T2", 
                            name='T2')
    line_names_part2 = [14, 15, 16, 19, 20, 22, 26, 29]
    for l in range(len(line_names_part2)):
        pp.create_line(net, 
                       from_bus=buses_part2[l],
                       to_bus=buses_part2[l+1],
                       length_km=line_lengths[line_names_part2[l]-1],
                       std_type=line_std_types[line_names_part2[l]-1], 
                       name=f'L{line_names_part2[l]}')
        
    #TODO Create load M17-M20 @bus22
        


    #create branch starting from bus after line 19
    num_buses_part3 = 7
    bus_names_part3 = [f'bus_{i}' for i in range(23, 30)]
    buses_part3 = pp.create_buses(net, 
                                  nr_buses=num_buses_part3,
                                  vn_kv=27.6,
                                  name=bus_names_part3) 
    line_names_part3 = [30, 31, 33, 35, 36, 37, 38]
    pp.create_line(net, 
                    from_bus=buses_part2[4],
                    to_bus=buses_part3[0],
                    length_km=line_lengths[line_names_part3[0]],
                    std_type=line_std_types[line_names_part3[0]], 
                    name=f'L{line_names_part3[0]}')
    for l in range(1, len(line_names_part3)):
        pp.create_line(net, 
                       from_bus=buses_part3[l-1],
                       to_bus=buses_part3[l],
                       length_km=line_lengths[line_names_part3[l]-1],
                       std_type=line_std_types[line_names_part3[l]-1], 
                       name=f'L{line_names_part3[l]}')
    
    #add all the smaller branches
    # bus_3 -> M1-M3 
    # bus_6 -> T1
    bus_30 = pp.create_bus(net, vn_kv=8.3, name='bus_30')
    t1 = pp.create_transformer(net,  
                            hv_bus=get_bus_index_by_name(net, 'bus_6'), 
                            lv_bus=bus_30, 
                            std_type="T1", 
                            name='T1')
    # TODO create load M6 




    # bus_5 -> M4, M5 

    # bus_8 -> M7

    # bus_11 -> M8
    
    # bus_12 -> M9-M12

    # bus_17 -> T3 
    bus_31 = pp.create_bus(net, vn_kv=27.6, name='bus_31')
    bus_32 = pp.create_bus(net, vn_kv=8.3, name='bus_32')

    line_names_part4 = [17, 18]
    t3 = pp.create_transformer(net,  
                            hv_bus=bus_31, 
                            lv_bus=bus_32, 
                            std_type="T3", 
                            name='T3')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_17'),
                   to_bus=bus_31, 
                   length_km=line_lengths[line_names_part4[0]-1],
                   std_type=line_std_types[line_names_part4[0]-1], 
                   name=f'L{line_names_part4[0]}')
    # bus_32 -> M13
    

    # bus_18 -> M26 

    # bus_19 -> L21 
    line_names_part5 = [21]
    bus_33 = pp.create_bus(net, vn_kv=27.6, name='bus_33')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_19'),
                   to_bus=bus_33, 
                   length_km=line_lengths[line_names_part5[0]-1],
                   std_type=line_std_types[line_names_part5[0]-1], 
                   name=f'L{line_names_part5[0]}')
    # bus_33 -> M14 


    # bus_20 -> L23 
    line_names_part6 = [23, 24, 25]
    bus_34 = pp.create_bus(net, vn_kv=27.6, name='bus_34')
    bus_35 = pp.create_bus(net, vn_kv=27.6, name='bus_35')
    bus_36 = pp.create_bus(net, vn_kv=27.6, name='bus_36')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_20'),
                   to_bus=bus_34, 
                   length_km=line_lengths[line_names_part6[0]-1],
                   std_type=line_std_types[line_names_part6[0]-1], 
                   name=f'L{line_names_part6[0]}')
    pp.create_line(net, 
                from_bus=bus_34,
                to_bus=bus_35, 
                length_km=line_lengths[line_names_part6[1]-1],
                std_type=line_std_types[line_names_part6[1]-1], 
                name=f'L{line_names_part6[1]}')
    pp.create_line(net, 
                from_bus=bus_34,
                to_bus=bus_36, 
                length_km=line_lengths[line_names_part6[2]-1],
                std_type=line_std_types[line_names_part6[2]-1], 
                name=f'L{line_names_part6[2]}')
    
    # bus_36 -> M15 


    # bus_21 -> L27
    line_names_part7 = [27, 28]
    bus_37 = pp.create_bus(net, vn_kv=27.6, name='bus_37')
    bus_38 = pp.create_bus(net, vn_kv=27.6, name='bus_38')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_21'),
                   to_bus=bus_37, 
                   length_km=line_lengths[line_names_part7[0]-1],
                   std_type=line_std_types[line_names_part7[0]-1], 
                   name=f'L{line_names_part7[0]}')
    pp.create_line(net, 
                from_bus=bus_37,
                to_bus=bus_38, 
                length_km=line_lengths[line_names_part7[1]-1],
                std_type=line_std_types[line_names_part7[1]-1], 
                name=f'L{line_names_part7[1]}')
    
    #  bus_38 ->  M16 

    

    # bus_22 -> M17-M20 

    # bus_24 -> L32 
    line_names_part8 = [32]
    bus_39 = pp.create_bus(net, vn_kv=27.6, name='bus_39')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_24'),
                   to_bus=bus_39, 
                   length_km=line_lengths[line_names_part8[0]-1],
                   std_type=line_std_types[line_names_part8[0]-1], 
                   name=f'L{line_names_part8[0]}')

    # bus_39 -> M21 

    # bus_25 -> L34 
    line_names_part9 = [34]
    bus_40 = pp.create_bus(net, vn_kv=27.6, name='bus_39')
    pp.create_line(net, 
                   from_bus=get_bus_index_by_name(net, 'bus_25'),
                   to_bus=bus_40, 
                   length_km=line_lengths[line_names_part9[0]-1],
                   std_type=line_std_types[line_names_part9[0]-1], 
                   name=f'L{line_names_part9[0]}')
    
    # bus_40 -> M25 


    # bus_26 -> M22, M23

    # bus_29 -> T4
    bus_41 = pp.create_bus(net, vn_kv=8.3, name='bus_41')

    t4 = pp.create_transformer(net,  
                            hv_bus=get_bus_index_by_name(net, 'bus_29'), 
                            lv_bus=bus_41, 
                            std_type="T4", 
                            name='T4')
    # bus_41 -> M24


    return net
    