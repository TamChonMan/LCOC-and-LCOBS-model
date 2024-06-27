#Author: Tam Chon-Man

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
import geopandas as gpd
import matplotlib.pyplot as plt
import scipy.stats
import matplotlib.ticker as mtick
import matplotlib.patches as patches
from matplotlib import rcParams

# 设置全局字体为 Times New Roman
rcParams['font.family'] = 'Times New Roman'

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
    plt.legend(loc='upper right',fontsize=18)

    ax = plt.gca()        
    plt.show()

def plot_mm_graph(x,s,Upper_bound,Lower_bound,AVG,s1,s2):
    fig, ax = plt.subplots(figsize=(25, 8), dpi=500)

    # 設置整張圖的背景顏色為白色
    fig.patch.set_facecolor('white')

    ax.barh(s,s2, color='lightseagreen', height = 0.4)
    ax.barh(s,s1, color='white', height = 0.4)
    
    # plt.barh(" ",s1, color='white', height = 0.4)
    
    ax.barh(x, Upper_bound,color='deepskyblue',height= 0.4)
    ax.barh(x, Lower_bound,color='white',height= 0.4)

    ax.grid(True,axis='x',linestyle = '-.' ) 
    ax.plot(AVG,x, c='teal',marker='o',linestyle='none',markersize=15, label='National average')

    # plt.legend(loc = 'upper right',prop={'family':'Times New Romane', 'size':20})
    ax.set_xlim([0.20,4.61])
    ax.set_ylim([-0.5,4.7])
    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4])
    ax.set_xticklabels([0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.2,4.4],fontsize =25)
    ax.set_yticklabels(['       ','     ','     ','     ','     '],fontsize=25)
    # 設置 X 軸標籤
    ax.set_xlabel("RMB/kWh", fontsize=25)
    
    ax.annotate(
    '',
    xy=(0.812, 0.0563), xycoords='axes fraction',
    xytext=(0.812, 0.135), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='#595959', linestyle='-', linewidth=5.5))

    ax.annotate(
    '',
    xy=(0.88, 0.0563), xycoords='axes fraction',
    xytext=(0.88, 0.135), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='#595959', linestyle='-', linewidth=5.5))

    ax.annotate(
    '',
    xy=(0, 0.18), xycoords='axes fraction',
    xytext=(1, 0.18), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='black', linestyle='-', linewidth=1.5))
    
    ax.text(0.028, 0.285, 'IM:0.43', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.142, 0.285, 'GD:0.70', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.086, 0.37, 'Lower Bound', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')

    ax.text(0.095, 0.48, 'XJ:0.75', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.24, 0.48, 'SH:1.10', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.18, 0.56, 'Baseline w/ Home Charger', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')

    ax.text(0.12, 0.67, 'XJ:0.87', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.29, 0.67, 'BJ:1.33', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.21, 0.75, 'Baseline w/o Home Charger', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')

    ax.text(0.356, 0.86, 'NX:1.90', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.65, 0.86, 'GD:2.91', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20, fontfamily='Times New Roman')
    ax.text(0.515, 0.94, 'Upper Bound', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')

    ax.text(0.77, 0.09, 'Random\n Charging ', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')
    ax.text(0.922, 0.09, 'Vally\n Charging ', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=21, fontfamily='Times New Roman')
    
    ax.text(-0.01, 0.09, 'LCOBS', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=22, fontfamily='Times New Roman',rotation=90,fontweight ='bold')
    ax.text(-0.01, 0.6, 'LCOC', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontweight = 'bold', fontsize=22, fontfamily='Times New Roman',rotation=90)

    ax.annotate(
    '',
    xy=(0.5135, 0.86), xycoords='axes fraction',
    xytext=(0.5135, 0.60), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='grey', linestyle='--', linewidth=2)
    )

    ax.annotate(
   'National average\nweight by population',
    xy=(0.5135, 0.60), xycoords='axes fraction',
    xytext=(0.7, 0.60), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='<-', color='grey', linestyle='--', linewidth=2),
    fontsize=25, fontfamily='Times New Roman', color='black', horizontalalignment='center', verticalalignment='center'
    )
    plt.show()


def plot_map(ax, data, color, linewidth, edgecolor, legend, legend_kwds, boundary_linewidth, boundary_edgecolor, vmax):
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
    merged.plot(column='data', cmap=color, linewidth=linewidth, ax=ax, edgecolor=edgecolor, legend=legend, legend_kwds=legend_kwds, vmax=vmax)
    plotingmap.boundary.plot(linewidth=boundary_linewidth, edgecolor=boundary_edgecolor, ax=ax)
    ax.axis('off')

    xmin, ymin, xmax, ymax = merged[merged.ADM0_EN == 'China'].total_bounds
    # add a padding around the geometry
    xpad = 10
    ypad = 3
    ax.set_xlim(xmin - xpad, xmax + xpad)
    ax.set_ylim(ymin - ypad, ymax + ypad)

    # Remove the legend if it exists
    if ax.get_legend() is not None:
        ax.get_legend().remove()

def plot_result_map(ax, data, color, linewidth, edgecolor, legend, legend_kwds, boundary_linewidth, boundary_edgecolor, vmax, title):
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
    merged.plot(column='data', cmap=color, linewidth=linewidth, ax=ax, edgecolor=edgecolor, legend=legend, legend_kwds=legend_kwds, vmax=vmax)
    plotingmap.boundary.plot(linewidth=boundary_linewidth, edgecolor=boundary_edgecolor, ax=ax)
    ax.axis('off')

    xmin, ymin, xmax, ymax = merged[merged.ADM0_EN == 'China'].total_bounds
    # add a padding around the geometry
    xpad = 10
    ypad = 3
    ax.set_xlim(xmin - xpad, xmax + xpad)
    ax.set_ylim(ymin - ypad, ymax + ypad)

    # Remove the legend if it exists
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    
    # Set the title
    ax.set_title(title, fontsize=23, fontweight = 'bold', pad=28)


def sen_lcoc_grahp(ax, df_base_sen,baseline_result):
    _type = df_base_sen["type"]
    _Upper_bound = df_base_sen["upper bound"]
    _Lower_bound = df_base_sen["lower bound"]

    ax.grid(color='grey',axis='x',linestyle = '-.') 

    ax.barh(_type, _Upper_bound,color='tomato',height= 0.7)
    ax.barh(_type, baseline_result ,color='seagreen',height= 0.7)
    ax.barh(_type, _Lower_bound,color='white',height= 0.7)

    ax.axvline(x = baseline_result , color = 'black', linewidth = 3)

    ax.set_xlim([0.0,2.6])
    ax.set_xticks([0,0.15,0.3,0.45,0.6,0.75,0.9,1.05,1.2,1.35,1.5,1.65,1.8,1.95,2.10,2.25,2.40,2.55])
    ax.set_xticklabels([0,0.15,0.3,0.45,0.6,0.75,0.9,1.05,1.2,1.35,1.5,1.65,1.8,1.95,2.10,2.25,2.40,2.55],fontsize=27)
    ax.set_yticks(_type)
    ax.set_yticklabels(_type,fontsize=27)
    ax.set_xlabel("RMB/kWh",fontsize=27)

    ax.annotate(
    '',
    xy=(0, 0.160), xycoords='axes fraction',
    xytext=(1, 0.160), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='grey', linestyle='--', linewidth=2))

def sen_lcobs_graph(ax, sensitivity_LCOBS_result,baseline,title):
    LCOBS_type = sensitivity_LCOBS_result ["type"]
    LCOBS_Upper_bound = sensitivity_LCOBS_result ["upper bound"]
    LCOBS_Lower_bound = sensitivity_LCOBS_result ["lower bound"]

    ax.grid(color='grey',axis='x',linestyle = '-.') 

    ax.barh(LCOBS_type, LCOBS_Upper_bound,color='tomato',height= 0.7)
    ax.barh(LCOBS_type, baseline ,color='seagreen',height= 0.7)
    ax.barh(LCOBS_type, LCOBS_Lower_bound,color='white',height= 0.7)

    ax.axvline(x = baseline, color = 'black', linewidth = 3)

    ax.set_xlim([0.8,5.4])
    ax.set_xticks([1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
    ax.set_xticklabels([1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0],fontsize =25)
    ax.set_yticks(LCOBS_type)
    ax.set_yticklabels(LCOBS_type,fontsize = 30)
    ax.set_xlabel("RMB/kWh",fontsize=25)

    ax.annotate(
    '',
    xy=(0, 0.377), xycoords='axes fraction',
    xytext=(1, 0.377), textcoords='axes fraction',
    arrowprops=dict(arrowstyle='-', color='grey', linestyle='--', linewidth=2))

    # Set the title
    ax.set_title(title, fontsize=35, fontweight = 'bold', pad=28)

def lcoc_utization_graph(ax1,df_u_c, baseline_result):
    u_c = df_u_c['utilzation_rate']
    lcoc_7 = df_u_c['7kw']
    lcoc_50 = df_u_c['50kw']
    lcoc_162 = df_u_c['163kw']
    lcoc_350 = df_u_c['350kw']

    # ax3 = ax1.twinx()

    ax1.axhline(baseline_result, color='black',linewidth = 5, linestyle =':', label='Resi. L1: 1 - 3 kW')
    ax1.plot(u_c, lcoc_7, linewidth = 2.5, color = '#F4B86E', label ='Resi. L2/Work: 7 kW', marker = 'o', markevery=10 , markersize = 4)
    ax1.plot(u_c, lcoc_50, linewidth = 2.5, color = '#2D5E76', label ='Public: ≤ 50 kW', marker ='o', markevery=10, markersize = 4)
    ax1.plot(u_c, lcoc_162, linewidth = 2.5 ,color = '#C07755', label= 'Public: 150~175 kW' , marker ='D', markevery=10, markersize = 4)
    ax1.plot(u_c, lcoc_350, linewidth = 2.5 ,color = '#53B69D', label = 'Public: ≥ 350kW', marker ='s', markevery=10, markersize = 4)

    ax1.grid(True,axis='y',linestyle = '-.' )
    ax1.grid(True,axis='x',linestyle = '-.' )

    ax1.set_xlim(0, 0.26)
    ax1.set_ylim(0.4, 2.6)
    ax1.set_xticklabels(['     0%','5%','10%','15%','20%','25%'],fontsize = 20)
    ax1.set_yticks([0.5,1.0,1.5,2.0,2.5])
    ax1.set_yticklabels([round(x ,2) for x in ax1.get_yticks()],fontsize = 20)

    # ax3.set_yticks(ax1.get_yticks())
    # ax3.set_ybound(ax1.get_ybound())
    # ax3.set_yticklabels([round(x * 11.98,1) for x in ax1.get_yticks()],fontsize = 28)

    ax1.legend(fontsize='35')

    plt.show()

def all_utilization_graph(ax1, df_u_c,df_u_s):
    u = df_u_s['Utilization rate']
    u_c = df_u_c['utilzation_rate']
    lcoc_7 = df_u_c['7kw']
    lcoc_50 = df_u_c['50kw']
    lcoc_162 = df_u_c['163kw']
    lcoc_350 = df_u_c['350kw']

    lcos_kwh = df_u_s['LCOB_r']

    u_range = np.arange(-0.1,1.1,0.2)
    ax3 = ax1.twinx()

    ax1.plot(u_c, lcoc_7, linewidth = 2.5, color = '#F4B86E', label ='Resi. L2/Work: 7 kW', marker = 'o', markevery=10 , markersize = 4)
    ax1.plot(u_c, lcoc_50, linewidth = 2.5, color = '#2D5E76', label ='Public: ≤ 50 kW', marker ='o', markevery=10, markersize = 4)
    ax1.plot(u_c, lcoc_162, linewidth = 2.5 ,color = '#C07755', label= 'Public: 150~175 kW' , marker ='D', markevery=10, markersize = 4)
    ax1.plot(u_c, lcoc_350, linewidth = 2.5 ,color = '#53B69D', label = 'Public: ≥ 350kW', marker ='s', markevery=10, markersize = 4)

    ax1.plot(u, lcos_kwh, linewidth = 6 ,color = '#2D4263', label = 'LCOS')

    ax1.fill_between(u_range, 5.327-1.707, 5.327+1.707, color='#B2B2B2',alpha = 0.6)
    ax1.axhline(5.327, color='#3C4048', linestyle ='-.',linewidth = 3)

    ax1.set_xlim(0, 1.05)
    ax1.grid(True,axis='both',linestyle = '-.' )

    ax1.set_xticklabels(['0%','20%','40%','60%','80%','100%'],fontsize = 25)
    ax1.set_yticklabels(['',0.0,5.0,10.0,15.0,20.0,25.0],fontsize = 25)

    ax3.set_yticks(ax1.get_yticks())
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([round((x * 12.84),1) for x in ax1.get_yticks()],fontsize = 25)

    ax1.yaxis.set_label_coords(-.05, 0.5)
    ax1.set_xlabel("Utilization rate",fontsize=35)
    ax1.set_ylabel("Levelized cost of EV recharging  (RMB/kWh)",fontsize=35)

    ax3.yaxis.set_label_coords(1.06, 0.5)
    ax3.set_ylabel("RMB/100km",fontsize =35)

def plot_reduction_sensitivity(ax1, df_lcos_sen):
    u = df_lcos_sen['Reduction']
    case1 = df_lcos_sen['Random Charging'] 
    case3 = df_lcos_sen['Valley Charging']
    case1_no = df_lcos_sen['Random Charing w/o Subsidy']
    case3_no = df_lcos_sen['Valley Charing w/o Subsidy'] 

    # ax2 = ax1.twiny()
    ax3 = ax1.twinx()

    # ax1.axhline(5.71, color = 'black', linewidth = 2.8, linestyle='--',alpha = 0.7,label ='8 Years Average Fuel cost')
    ax1.plot(u, case1, linewidth = 4, color = '#5F9DF7', label ='Random Charging')
    ax1.plot(u, case3, linewidth = 4,color = '#FB2576', label= 'Valley Charging')
    ax1.plot(u, case1_no, linewidth = 4 ,color = 'blue', label= 'Random Charging w/o subsidy', marker = 'o' , markersize = 10 )
    ax1.plot(u, case3_no, linewidth = 4 ,color = 'red', label= 'Valley Charging w/o subsidy',marker = 'o', markersize = 10)

    ax1.grid(True,axis='both',linestyle = '-.' )
    ax1.legend(prop={'family':'Times New Romane', 'size':30}, loc = 'lower left')

    ax1.tick_params(axis='both', colors='black', labelsize=25)

    ax1.set_ylabel("LCOBS  (RMB/kWh)",fontsize=35)
    ax3.set_ylabel("RMB/100km",fontsize=35)
    ax1.set_xlabel("Battery price reduction",fontsize=35)

    ax3.set_yticks(ax1.get_yticks())
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([round(x * 12.84 ,1)for x in ax1.get_yticks()])
    ax3.tick_params(axis='both', colors='black', labelsize=25)

    plt.show()

def plot_breakdown_LCOBS(ax, df_result):
    case = df_result['case']
    captialcost = df_result['captial cost']
    cost_of_electricity = df_result['cost_of_electricity']
    cost_of_mL = df_result['cost_of_mL']

    x = [0.7,1]
    width = 0.18  # Adjust the width to increase spacing

    # Plot the bars with increased spacing
    ax.bar(x , captialcost, color='teal', label='Captial costs', width=width)
    ax.bar(x , cost_of_mL, color='darkgreen', label='Maintenance costs', bottom=captialcost, width=width)
    ax.bar(x , cost_of_electricity, color='greenyellow', label='Electricity costs', 
           bottom=[captialcost[i] + cost_of_mL[i] for i in range(len(captialcost))], width=width)

    # Setting the labels and ticks
    ax.set_xticks(x)
    ax.set_xticklabels(case, fontsize=25)
    ax.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5 ])
    ax.set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5], fontsize=23)
    ax.set_ylabel("LCOBS  (RMB/kWh)", fontsize=25)
    ax.set_ylim([0, 5])

    # Adjusting legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), loc='upper left', fontsize=25)