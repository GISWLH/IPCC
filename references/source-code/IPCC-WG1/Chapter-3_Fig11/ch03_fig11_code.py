# ch03_fig11.py

# Description

# Generates Figure 3.11 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 3

# Creator: Chris Brierley (c.brierley@ucl.ac.uk)
# Creator: Anni Zhao (anni.zhao.16@ucl.ac.uk)
# Creation Date: 1 Mar 2021

# Note - this script creates a plot with a key that is plastered down the centre of the image. This was corrected manually using Inkscape.  

# Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib


# Loads the model data for figure 3.11 and then stores the data corresponding to models and CMIPs 
DATA = pd.read_csv('map_midHolocene_models.csv',header=205)
map_PMIP4_CMIP6 = {'AWI-ESM-1-1-LR':np.array(DATA['2'][0:len(DATA['2'])-1]).astype(float),
                      'CESM2':np.array(DATA['3'][0:len(DATA['3'])-1]).astype(float),
                      'EC-Earth3-LR':np.array(DATA['4'][0:len(DATA['4'])-1]).astype(float),
                      'FGOALS-f3-L':np.array(DATA['5'][0:len(DATA['5'])-1]).astype(float),
                      'FGOALS-g3':np.array(DATA['6'][0:len(DATA['6'])-1]).astype(float),
                      'GISS-E2-1-G':np.array(DATA['7'][0:len(DATA['7'])-1]).astype(float),
                      'HadGEM3-GC31-LL':np.array(DATA['8'][0:len(DATA['8'])-1]).astype(float),
                      'INM-CM4-8':np.array(DATA['9'][0:len(DATA['9'])-1]).astype(float),
                      'IPSL-CM6A-LR':np.array(DATA['10'][0:len(DATA['10'])-1]).astype(float),
                      'MIROC-ES2L':np.array(DATA['11'][0:len(DATA['11'])-1]).astype(float),
                      'MPI-ESM1-2-LR':np.array(DATA['12'][0:len(DATA['12'])-1]).astype(float),
                      'MRI-ESM2-0':np.array(DATA['13'][0:len(DATA['13'])-1]).astype(float),
                      'NESM3':np.array(DATA['14'][0:len(DATA['14'])-1]).astype(float),
                      'NorESM1-F':np.array(DATA['15'][0:len(DATA['15'])-1]).astype(float),
                      'NorESM2-LM':np.array(DATA['16'][0:len(DATA['16'])-1]).astype(float),
                      'UofT-CCSM-4':np.array(DATA['17'][0:len(DATA['17'])-1]).astype(float)}
map_PMIP3_CMIP5 = {'BCC-CSM1-1':np.array(DATA['18'][0:len(DATA['18'])-1]).astype(float),
                      'CCSM4':np.array(DATA['19'][0:len(DATA['19'])-1]).astype(float),
                      'CNRM-CM5':np.array(DATA['20'][0:len(DATA['20'])-1]).astype(float),
                      'CSIRO-Mk3L-1-2':np.array(DATA['21'][0:len(DATA['21'])-1]).astype(float),
                      'CSIRO-Mk3-6-0':np.array(DATA['22'][0:len(DATA['22'])-1]).astype(float),
                      'EC-EARTH-2-2':np.array(DATA['23'][0:len(DATA['23'])-1]).astype(float),
                      'FGOALS-g2':np.array(DATA['24'][0:len(DATA['24'])-1]).astype(float),
                      'FGOALS-s2':np.array(DATA['25'][0:len(DATA['25'])-1]).astype(float),
                      'GISS-E2-R':np.array(DATA['26'][0:len(DATA['26'])-1]).astype(float),
                      'HadGEM2-CC':np.array(DATA['27'][0:len(DATA['27'])-1]).astype(float),
                      'HadGEM2-ES':np.array(DATA['28'][0:len(DATA['28'])-1]).astype(float),
                      'IPSL-CM5A-LR':np.array(DATA['29'][0:len(DATA['29'])-1]).astype(float),
                      'MIROC-ESM':np.array(DATA['30'][0:len(DATA['30'])-1]).astype(float),
                      'MPI-ESM-P':np.array(DATA['31'][0:len(DATA['31'])-1]).astype(float),
                      'MRI-CGCM3':np.array(DATA['32'][0:len(DATA['32'])-1]).astype(float)}


# Loads the reconstruction data for figure 3.11 and then stores the data corresponding to region names 
region_name=['Northern Europe','W. & C. Europe','Mediterranean','Sahara/Sahel','West Africa']
# Create a set of empty lists to store data points
data_NEU = []
data_WCE = []
data_MED = [] 
data_SAH = []
data_WAF = []
# Load reconstruction data
data_reconstruction = pd.read_csv('map_midHolocene_reconstructions.csv',header=21)
data_region_names = data_reconstruction['1']
map_reconstruction = data_reconstruction['2']
# For each data point, identify the name of the region and then add the data to the right list
for i,rname in enumerate(data_region_names):
    map_point = map_reconstruction[i]
    if rname == 'Northern Europe':
        data_NEU.append(map_point)
    if rname == 'W. & C. Europe':
        data_WCE.append(map_point)
    if rname == 'Mediterranean':
        data_MED.append(map_point)
    if rname == 'Sahara/Sahel':
        data_SAH.append(map_point)
    if rname == 'West Africa':
        data_WAF.append(map_point)
data_recons = [data_NEU,data_WCE,data_MED,data_SAH,data_WAF]


# Plot figure 3.11

# Dictionary that defines the color for each CMIP6 model in the ensemble 
# Colors are set based on CMIP6_colors.xlsx
CMIP6_model_colors = { 'AWI-ESM-1-1-LR':[0.600000,0.000000,1.000000],
                       'CESM2':[0.262745,0.698039,0.847059],
                       'EC-Earth3-LR':[0.486275,0.388235,0.721569],
                       'FGOALS-f3-L':[0.972549,0.603922,0.109804],
                       'FGOALS-g3':[0.972549,0.603922,0.109804],
                       'GISS-E2-1-G':[0.466667,0.113725,0.482353],
                       'HadGEM3-GC31-LL':[0.478431,0.545098,0.149020],
                       'INM-CM4-8':[0.968627,0.262745,0.262745],
                       'IPSL-CM6A-LR':[0.356863,0.325490,0.682353],
                       'MIROC-ES2L':[0.721569,0.372549,0.713725],
                       'MPI-ESM1-2-LR':[0.364706,0.631373,0.635294],
                       'MRI-ESM2-0':[0.678431,1.000000,0.184314],
                       'NESM3':[0.682353,0.666667,0.666667],
                       'NorESM1-F':[0.945098,0.227451,0.654902],
                       'NorESM2-LM':[0.945098,0.227451,0.654902],
                       'UofT-CCSM-4':[0.803922,0.803922,0.000000]}
# Lists that contains the name of the 
PMIP4_CMIP6_models = ['AWI-ESM-1-1-LR',
                      'CESM2',
                      'EC-Earth3-LR',
                      'FGOALS-f3-L',
                      'FGOALS-g3',
                      'GISS-E2-1-G',
                      'HadGEM3-GC31-LL',
                      'INM-CM4-8',
                      'IPSL-CM6A-LR',
                      'MIROC-ES2L',
                      'MPI-ESM1-2-LR',
                      'MRI-ESM2-0',
                      'NESM3',
                      'NorESM1-F',
                      'NorESM2-LM',
                      'UofT-CCSM-4']
PMIP3_CMIP5_models = ['BCC-CSM1-1',
                      'CCSM4',
                      'CNRM-CM5',
                      'CSIRO-Mk3L-1-2',
                      'CSIRO-Mk3-6-0',
                      'EC-EARTH-2-2',
                      'FGOALS-g2',
                      'FGOALS-s2',
                      'GISS-E2-R',
                      'HadGEM2-CC',
                      'HadGEM2-ES',
                      'IPSL-CM5A-LR',
                      'MIROC-ESM',
                      'MPI-ESM-P',
                      'MRI-CGCM3']

# Set figure size to 18cm x 12cm
# Exchange the size unit from cm to inch by dividing 2.54
plt.figure(figsize = (18/2.54,12/2.54))
ax = plt.subplot(111)
# Setups
# Set title
plt.title('Precipitation change at the Mid-Holocene',loc='left',fontsize=11)
# Set axes limits
plt.ylim((-400,800))
plt.xlim((0,5))
# Set boundary edges
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#Generate plotting positions 
p1 = [0.3,1.3,2.3,3.3,4.3]
p2 = [0.5,1.5,2.5,3.5,4.5]
p3 = [0.7,1.7,2.7,3.7,4.7]

# Plot data
# Plot restructions
plt.boxplot(data_recons,positions=p1,widths=0.1,showfliers =False)
# Plot PMIP3 models
# Color uses categorical CMIP5 color
for model in PMIP3_CMIP5_models:
    # Plot first model and give a label to PMIP3 models
    if model == 'AWI-ESM-1-1-LR':
        plt.plot(p2,map_PMIP3_CMIP5[model],marker='o', color=(37/255,81/255,204/255),fillstyle='none',mew=1, ms=5,linestyle='None',label='PMIP3 models')    
    # Plot other models without labelling
    else:
        plt.plot(p2,map_PMIP3_CMIP5[model],marker='o', color=(37/255,81/255,204/255),fillstyle='none',mew=1, ms=5,linestyle='None')
# Plot PMIP4 models and label each individual model 
for model in PMIP4_CMIP6_models:
    plt.plot(p3,map_PMIP4_CMIP6[model],marker='o',color=(CMIP6_model_colors[model][0],CMIP6_model_colors[model][1],CMIP6_model_colors[model][2]),fillstyle='none',mew=1, ms=6,linestyle='None',label=model)

# Legend
leg = plt.legend(edgecolor='None',facecolor='None', borderaxespad=0.5,fontsize=9)
for line, text in zip(leg.get_lines(), leg.get_texts()):
    text.set_color(line.get_color())

# Add a grey dotted line to indicate the zero level    
plt.axhline(y=0,color='grey',linestyle="dotted",linewidth=0.5)

# Set labels and ticks of axes
#Set region names
region_name=['Northern Europe','W. & C. Europe','Mediterranean','Sahara/Sahel','West Africa']
plt.xticks(p2,region_name,fontsize=9)
plt.ylabel(' (mm yr$^{-1})$',fontsize=9) 
plt.yticks(fontsize=9)
plt.show()
