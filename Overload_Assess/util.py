# import pandapower as pp
import pandapower.networks as nw
import numpy as np
import matplotlib.pyplot as plt
import pandapower 
import pandapower.plotting as plotting
import matplotlib.pyplot as plt





def get_bus_index_by_name(net, name):
    return net.bus[net.bus["name"] == name].index[0]


def net_visualize(net_ ):
    net= net_
    ax=plotting.simple_plot(net,   plot_gens=True, line_width=2, bus_size=1, show_plot=False , gen_size=2.5)
    
    # Annotate each bus with its number
    for bus_idx, row in net.bus.iterrows():
        # if bus_idx==28:
        #     continue
        
        x, y = net.bus_geodata.loc[bus_idx, ['x', 'y']]
        ax.text(
            x+0.2  , y-0.15  ,  '{}'.format(net.bus.name[bus_idx])  ,  fontsize=8,ha="right", va="top"
        )
        # ax.text(
        #     x , y  ,  'Bus{}\n{}'.format(bus_idx,net.bus.name[bus_idx])  ,  fontsize=15,ha="left", va="top"
        # )
    
    # Annotate each transformer with its number
    for idx, row in net.trafo.iterrows() :
        # Use the locations of the 'hv_bus' and 'lv_bus' to position the transformer text 
        
        hv_bus = row['hv_bus']
        lv_bus = row['lv_bus']
        x_hv, y_hv = net.bus_geodata.loc[hv_bus, ['x', 'y']]
        x_lv, y_lv = net.bus_geodata.loc[lv_bus, ['x', 'y']]
        # Position the text between the high-voltage and low-voltage buses
        x_mid = (x_hv + x_lv) / 2
        y_mid = (y_hv + y_lv) / 2
        ax.text(
            x_mid-0.2, y_mid-0.3, f"{net.trafo.name[idx]}",  # Transformer number
            color="black", fontsize=15, ha="left", va="top"
        )
        # ax.text(
        #     x_mid, y_mid, f"T{idx}",  # Transformer number
        #     color="black", fontsize=15, ha="left", va="top"
        # )
    
     # Annotate each line with its number
    for idx, line in net.line.iterrows() :
        # Use the locations of the 'hv_bus' and 'lv_bus' to position the transformer text 
        
        from_bus_coord = net.bus_geodata.loc[line.from_bus]
        to_bus_coord = net.bus_geodata.loc[line.to_bus]
        # Position the text between the high-voltage and low-voltage buses
        x_mid = (from_bus_coord['x'] + to_bus_coord['x']) / 2
        y_mid = (from_bus_coord['y'] + to_bus_coord['y']) / 2
        ax.text(
            x_mid+0.15, y_mid+0.12, f"{net.line.name[idx]}",  # Transformer number
            color="black", fontsize=8, ha="right", va="bottom"
        )
        # ax.text(
        #     x_mid, y_mid, f"T{idx}",  # Transformer number
        #     color="black", fontsize=15, ha="left", va="top"
        # )
    
     
    plt.show(ax)











if __name__ == "__main__":
    

    # Load the IEEE 14-bus test case
    # net = nw.case39()
    # net = nw.create_cigre_network_hv(length_km_6a_6b=0.1)
    # net = nw.create_cigre_network_mv(with_der=False)
    # net = nw.case14()
    # net = nw.create_cigre_network_hv(length_km_6a_6b=0.1)
    net = nw.create_cigre_network_lv()
    # Remove all generators
    # net.gen.drop(net.gen.index, inplace=True)
    # net.bus_geodata['y'] *= .1
    # net.bus_geodata['y'][0] =0 
    
    net_visualize(net)
    
    # pandapower.create_continuous_elements_index (net, start=0)
    # net_visualize(net)
    
    xx
    #%%
    # Assume a 24-hour daily load profile
    # Create a time series load profile with a peak of 3 kW (0.003 MW)
    hours = np.arange(0, 24)
    load_profile = 0.01 * np.ones(hours.shape)  # Peak load at midday, in MW
    # load_profile = 0.005 * np.sin((hours / 24) * 2 * np.pi) + 0.005  # Peak load at midday, in MW
    
    # Assign the load profile to each load in the network
    # for load_idx in net.load.index:
    #     net.load.loc[load_idx, 'p_mw'] = load_profile.mean()  # Initialize with mean value
    
    # Simulate hourly power flows and record transformer absolute load
    transformer_loads = []
    
    for hour in hours:
        # Scale the load dynamically for the given hour
        for load_idx in net.load.index:
            net.load.loc[load_idx, 'p_mw'] = load_profile[hour]  # Set load for the hour
    
        # Run a power flow
        pp.runpp(net)
    
        # Calculate absolute power on transformers
        # Use the `res_trafo.p_hv_mw` (high-voltage side power flow in MW)
        # power_mw = abs(net.res_trafo['p_hv_mw'].values)   # Absolute power flow in MW
        power_mw = net.res_trafo['p_hv_mw'].values  # Absolute power flow in MW
        transformer_loads.append(power_mw)
    
    # Convert transformer loads to a NumPy array for easier handling
    transformer_loads = np.array(transformer_loads)
    
    # Plot the absolute load values on each transformer
    for trafo_idx, trafo in enumerate(net.trafo.index):
        plt.plot(hours, transformer_loads[:, trafo_idx], label=f'Transformer {trafo}')
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Transformer Load (MW)')
    plt.title('Daily Absolute Transformer Load')
    plt.legend()
    plt.grid()
    plt.show()
