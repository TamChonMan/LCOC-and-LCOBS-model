import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
import geopandas as gpd
import matplotlib.pyplot as plt
import scipy.stats
import matplotlib.ticker as mtick

def scneario_max_min_graph(short_name,price_Upper_case,price_lower_case,baseline_without,baseline):
    x = np.arange(len(short_name))
    plt.figure(figsize=(25, 11), dpi=200)
    plt.bar(x, price_Upper_case,width=0.08,color='teal')
    plt.bar(x, price_lower_case,width=0.08,color='white')

    plt.plot(x, baseline_without,c='seagreen',marker='o',linestyle='none',markersize=9, label ='Baseline scenairo without home charger')
    plt.plot(x, baseline,c='red',marker='D',linestyle='none',markersize=9, label ='Baseline scenario with home charger')

    plt.ylim([0.2,3.0])
    plt.grid(True,axis='x',linestyle = '-.',c ='grey') 

    plt.xticks(x, short_name, fontsize=25)
    plt.yticks(fontsize=25)
    plt.ylabel("LCOC  (RMB/kWh)",fontsize=27)
    plt.xlabel("Province",fontsize=27)
    plt.legend(loc='upper right',fontsize=25)

    ax = plt.gca()        
    plt.show()

def plot_mm_graph(x,s,Upper_bound,Lower_bound,AVG,s1,s2):
    plt.figure(figsize=(25,8), dpi=200)

    plt.barh(s,s2, color='lightseagreen', height = 0.4)
    plt.barh(s,s1, color='white', height = 0.4)

    plt.barh(x, Upper_bound,color='deepskyblue',height= 0.4)
    plt.barh(x, Lower_bound,color='white',height= 0.4)

    plt.grid(True,axis='x',linestyle = '-.' ) 
    plt.plot(AVG,x, c='teal',marker='o',linestyle='none',markersize=15, label='National average')

    # plt.legend(loc = 'upper right',prop={'family':'Times New Romane', 'size':20})
    plt.xlim([0.20,4.4])
    plt.ylim([-0.5,4.8])
    plt.xticks([0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.2,4.4],fontsize =25)
    # plt.yticks([])
    plt.yticks(fontsize=25)
    plt.xlabel("RMB/kWh",fontsize=25)
    plt.show()


def plot_map(ax, data, color, linewidth, edgecolor, legend, legend_kwds, boundary_linewidth, boundary_edgecolor,vmax):
    # Load shapefile as df1
    df1 = gpd.read_file('./color_map/chn_admbnda_adm1_ocha_2020.shp')

    # Load shapecode as df2
    df2 = pd.read_csv('./province_map_code.csv')

    # Merge data
    df2['data'] = data

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    Asia = world[world["continent"] == "Asia"]
    Asia_no = Asia.drop("geometry", axis=1)
    asia_name_list = Asia_no["name"]

    df3 = gpd.read_file('./world_country/World_Countries__Generalized_.shp')
    Rusia = df3[df3["ISO"] == "RU"]

    Asia_merged = df3[df3['COUNTRY'].isin(asia_name_list)]
    plotingmap = pd.concat([Asia_merged, Rusia])

    # Merge the two datasets with the common identifier ADM1_PCODE
    merged = df1.merge(df2, left_on='ADM1_PCODE', right_on='ADM1_PCODE', how='outer')

    # Clean up the file
    merged.fillna(0, inplace=True)
    merged_no_drop = merged.drop(index=[10, 13])
    merged = merged_no_drop.drop(index=[8, 26])

    # Create the map
    merged.plot(column='data', cmap=color, linewidth=linewidth, ax=ax, edgecolor=edgecolor, legend=legend, legend_kwds=legend_kwds,vmax = vmax)
    plotingmap.boundary.plot(linewidth=boundary_linewidth, edgecolor=boundary_edgecolor, ax=ax)
    ax.legend(fontsize=25)
    ax.axis('off')

    xmin, ymin, xmax, ymax = merged[merged.ADM0_EN == 'China'].total_bounds
    # add a padding around the geometry
    xpad = 10
    ypad = 3
    ax.set_xlim(xmin - xpad, xmax + xpad)
    ax.set_ylim(ymin - ypad, ymax + ypad)

def sen_lcoc_grahp(df_base_sen):
    _type = df_base_sen["type"]
    _Upper_bound = df_base_sen["upper bound"]
    _Lower_bound = df_base_sen["lower bound"]

    plt.figure(figsize=(25,12), dpi=200)
    plt.grid(color='grey',axis='x',linestyle = '-.') 

    plt.barh(_type, _Upper_bound,color='tomato',height= 0.7)
    plt.barh(_type, 0.973 ,color='seagreen',height= 0.7)
    plt.barh(_type, _Lower_bound,color='white',height= 0.7)

    plt.axvline(x = 0.973, color = 'black', linewidth = 3)

    plt.xlim([0.0,2.6])
    plt.xticks([0,0.15,0.3,0.45,0.6,0.75,0.9,1.05,1.2,1.35,1.5,1.65,1.8,1.95,2.10,2.25,2.40,2.55],fontsize=27)
    plt.yticks(fontsize=27)
    plt.xlabel("RMB/kWh",fontsize=27)



