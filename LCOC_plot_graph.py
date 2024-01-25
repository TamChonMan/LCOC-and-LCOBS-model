#Author: Tam Chon-Man

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


def lcoc_utization_graph(df_u_c, baseline_result):
    u_c = df_u_c['utilzation_rate']
    lcoc_7 = df_u_c['7kw']
    lcoc_50 = df_u_c['50kw']
    lcoc_162 = df_u_c['163kw']
    lcoc_350 = df_u_c['350kw']

    ax1 = plt.figure(figsize=(20,15), dpi=400).add_subplot(111)
    ax3 = ax1.twinx()

    ax1.axhline(baseline_result, color='black',linewidth = 5, linestyle =':', label='Resi. L1: 1 - 3 kW')
    ax1.plot(u_c, lcoc_7, linewidth = 4.5, color = '#FFEA20', label ='Resi. L2/Work: 7 kW', marker = 'o', markevery=10 , markersize = 10)
    ax1.plot(u_c, lcoc_50, linewidth = 4.5, color = '#379237', label ='Public: ≤ 50 kW', marker ='o', markevery=10, markersize = 10)
    ax1.plot(u_c, lcoc_162, linewidth = 4.5 ,color = '#82CD47', label= 'Public: 150~175 kW' , marker ='D', markevery=10, markersize = 10)
    ax1.plot(u_c, lcoc_350, linewidth = 4.5 ,color = '#54B435', label = 'Public: ≥ 350kW', marker ='s', markevery=10, markersize = 10)


    ax1.grid(True,axis='y',linestyle = '-.' )
    ax1.grid(True,axis='x',linestyle = '-.' )

    ax1.set_xlim(0, 0.26)
    ax1.set_ylim(0.4, 2.6)
    ax1.set_xticklabels(['     0%','5%','10%','15%','20%','25%'],fontsize = 28)

    ax1.set_yticklabels([round(x ,2) for x in ax1.get_yticks()],fontsize = 28)

    ax3.set_yticks(ax1.get_yticks())
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([round(x * 11.98,1) for x in ax1.get_yticks()],fontsize = 28)

    ax1.legend(fontsize='35')

    plt.show()

def all_utilization_graph(df_u_c,df_u_s):
    u = df_u_s['Utilization rate']
    u_c = df_u_c['utilzation_rate']
    lcoc_7 = df_u_c['7kw']
    lcoc_50 = df_u_c['50kw']
    lcoc_162 = df_u_c['163kw']
    lcoc_350 = df_u_c['350kw']

    lcos_kwh = df_u_s['LCOB_r']

    u_range = np.arange(-0.1,1.1,0.2)

    ax1 = plt.figure(figsize=(25,18), dpi=400).add_subplot(111)
    ax3 = ax1.twinx()

    ax1.plot(u_c, lcoc_7, linewidth = 2.5, color = '#FFEA20', label ='Resi. L2/Work: 7 kW', marker = 'o', markevery=10 , markersize = 5)
    ax1.plot(u_c, lcoc_50, linewidth = 2.5, color = '#379237', label ='Public: ≤ 50 kW', marker ='o', markevery=10, markersize = 5)
    ax1.plot(u_c, lcoc_162, linewidth = 2.5 ,color = '#82CD47', label= 'Public: 150~175 kW' , marker ='D', markevery=10, markersize = 5)
    ax1.plot(u_c, lcoc_350, linewidth = 2.5 ,color = '#54B435', label = 'Public: ≥ 350kW', marker ='s', markevery=10, markersize = 5)

    ax1.plot(u, lcos_kwh, linewidth = 6 ,color = '#2D4263', label = 'LCOS')

    ax1.fill_between(u_range, 5.71-1.82, 5.71+1.82, color='#B2B2B2',alpha = 0.6)

    ax1.axhline(5.71, color='#3C4048', linestyle ='-.',linewidth = 3)
    ax1.set_xlim(0, 1.05)
    ax1.grid(True,axis='both',linestyle = '-.' )

    ax1.set_xticklabels(['0%','20%','40%','60%','80%','100%'],fontsize = 25)
    ax1.set_yticklabels(['',0.0,5.0,10.0,15.0,20.0,25.0],fontsize = 25)

    ax3.set_yticks(ax1.get_yticks())
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([round((x * 11.98),1) for x in ax1.get_yticks()],fontsize = 25)

    ax1.yaxis.set_label_coords(-.05, 0.5)
    ax1.set_xlabel("Utilization rate",fontsize=35)
    ax1.set_ylabel("Levelized cost of EV recharging  (RMB/kWh)",fontsize=35)

    ax3.yaxis.set_label_coords(1.06, 0.5)
    ax3.set_ylabel("RMB/100km",fontsize =35)

def plot_reduction_sensitivity(df_lcos_sen):
    u = df_lcos_sen['Reduction']
    case1 = df_lcos_sen['Random Charging'] 
    case3 = df_lcos_sen['Valley Charging']
    case1_no = df_lcos_sen['Random Charing w/o Subsidy']
    case3_no = df_lcos_sen['Valley Charing w/o Subsidy'] 

    ax1 = plt.figure(figsize=(20,12), dpi=200).add_subplot(111)

    # ax2 = ax1.twiny()
    ax3 = ax1.twinx()

    # ax1.axhline(5.71, color = 'black', linewidth = 2.8, linestyle='--',alpha = 0.7,label ='8 Years Average Fuel cost')
    ax1.plot(u, case1, linewidth = 4, color = '#5F9DF7', label ='Random Charging')
    ax1.plot(u, case3, linewidth = 4,color = '#FB2576', label= 'Valley Charging')
    ax1.plot(u, case1_no, linewidth = 4 ,color = 'blue', label= 'Random Charging w/o subsidy', marker = 'o' , markersize = 10 )
    ax1.plot(u, case3_no, linewidth = 4 ,color = 'red', label= 'Valley Charging w/o subsidy',marker = 'o', markersize = 10)

    ax1.grid(True,axis='both',linestyle = '-.' )
    ax1.legend(prop={'family':'Times New Romane', 'size':20}, loc = 'lower left')

    ax1.tick_params(axis='both', colors='black', labelsize=25)

    ax1.set_ylabel("LCOBS  (RMB/kWh)",fontsize=25)
    ax3.set_ylabel("RMB/100km",fontsize=25)
    ax1.set_xlabel("Battery price reduction",fontsize=25)

    ax3.set_yticks(ax1.get_yticks())
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([round(x * 11.98 ,1)for x in ax1.get_yticks()])
    ax3.tick_params(axis='both', colors='black', labelsize=25)

    plt.show()
