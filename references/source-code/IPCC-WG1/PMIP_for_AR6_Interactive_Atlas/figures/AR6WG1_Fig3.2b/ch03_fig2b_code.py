
# ch03_fig2b.py

# Description

# Generates Figure 3.2 panel b in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 3

# Creator: Anni Zhao (anni.zhao.16@ucl.ac.uk)
# Creator: Chris Brierley (c.brierley@ucl.ac.uk)
# Creation Date: 1 Mar 2021


# Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib


# Define markers for CMIP indicidual models:
markers = {'CMIP6':['o'],
           'CMIP5':['x'],
           'nonCMIP':['+']}
# Define markers for CMIP multi-model means:
avemarkers = {'CMIP6':['s'],
              'CMIP5':['X'],
              'nonCMIP':['P']}
# Define colors for experiments:
colors = {'LGM':['blue'],
          'LIG':['lightblue'],
          'MH':['lightsalmon'],
          'mPWP':['red'],
          'EECO':['darkred'],
          '1pctCO2':['limegreen'],
          'abrupt4xCO2':['violet']}
# Define experiment names
expt_names = {'LGM':['Last Glacial Maximum'],
       'LIG':['Last Inter Glacial'],
       'MH':['mid-Holocene'],
       'mPWP':['mid-Piacenzian Warm Period'],
       'EECO':['Early Eocene Climatic Optimum'],
       '1pctCO2':['1pctCO2'],
        'abrupt4xCO2':['abrupt4xCO2']}


# Function that loads and plots land and ocean temperature contrasts simulated by CMIP6 individual models
# Syntax
# [output] = ch03_fig2b_function1(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the right CMIP6 data points in right color and marker according to the experiment name

def ch03_fig2b_function1(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_CMIP6.csv' %expt
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="o",s=30,color=colors[expt][0],linewidths=1,facecolors='none',edgecolors=colors[expt][0])
    return fig           


# Function that loads and plots land and ocean temperature contrasts simulated by CMIP5 individual models
# Syntax
# [output] = ch03_fig2b_function2(input)

# Input argument
# input - experiment name

# Output argument
# output - Plots the right CMIP5 data points in right color and marker according to the experiment name

def ch03_fig2b_function2(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_CMIP5.csv' %expt
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="x",s=30,color=colors[expt][0],linewidths=1,edgecolors=colors[expt][0])
    return fig


# Function that loads and plots land and ocean temperature contrasts simulated by nonCMIP individual models
# Syntax
# [output] = ch03_fig2b_function3(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the right CMIP6 data points in right color and marker according to the experiment name

def ch03_fig2b_function3(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_nonCMIP.csv' %expt
    DATA = pd.read_csv(fname,header=19)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="+",s=30,color=colors[expt][0],linewidths=1,edgecolors=colors[expt][0])
    return fig


# Function that loads and plots the ensemble mean of land and ocean temperature contrast in the CMIP6
# Syntax
# [output] = ch03_fig2b_function4(input)

# Input argument
# input - experiment name

# Output argument
# output - Plots the right CMIP6 data point in right color and marker according to the experiment name

def ch03_fig2b_function4(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_CMIP6_ensemble_mean.csv' %expt
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="s",s=75,color=colors[expt][0],linewidths=1,facecolors='none',edgecolors=colors[expt][0],label=expt)
    return fig           


# Function that loads and plots the ensemble mean of land and ocean temperature contrast in the CMIP5
# Syntax
# [output] = ch03_fig2b_function5(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the right CMIP5 data point in right color and marker according to the experiment name

def ch03_fig2b_function5(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_CMIP5_ensemble_mean.csv' %expt
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="X",s=75,color=colors[expt][0],linewidths=1,edgecolors=colors[expt][0])
    return fig


# Function that loads and plots the ensemble mean of land and ocean temperature contrast in the nonCMIP
# Syntax
# [output] = ch03_fig2b_function6(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the right nonCMIP data point in right color and marker according to the experiment name

def ch03_fig2b_function6(expt):  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_%s_nonCMIP_ensemble_mean.csv' %expt
    DATA = pd.read_csv(fname,header=19)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea,Tland,marker="P",s=75,color=colors[expt][0],linewidths=1,edgecolors=colors[expt][0])
    return fig            


# Function that loads and plots the Instrumental land and sea temperature contrast
# Syntax
# [output] = ch03_fig2b_function7(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the instrumental data point in right color and marker according to the experiment name

def ch03_fig2b_function7():  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_observation_instrumental.csv'
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.scatter(Tsea, Tland,marker='D',s=60,color='k',linewidths=1,facecolors='none',label='Instrumental')
    return fig


# Function that loads and plots the reconstructed land and sea temperature contrast
# Syntax
# [output] = ch03_fig2b_function8(input)

# Input arguments
# input - experiment name

# Output argument
# output - Plots the reconstruction data point in right color and marker according to the experiment name

def ch03_fig2b_function8():  
    # load data
    # Define the filename according to the input exoeriment name
    fname = 'fig3.2b_observation_reconstruction.csv'
    DATA = pd.read_csv(fname,header=18)
    Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float)
    Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float)
    fig = plt.errorbar(Tsea, Tland, xerr=0.01,yerr=0.01,marker='*',ecolor='k',color='lightsalmon',ms=6,ls='none',label='Reconstruction')
    return fig


# Plot the panel b in figure 2 in chapter 3
# Set figure size to 9cm x 12cm
# Change the size unit from cm to inch by deviding 2.54
plt.figure(figsize=(9/2.54,12/2.54))
ax = plt.subplot(111)
# Setups
# Set title
plt.title('b) Global temperature change over \nland and ocean for a range of climates',fontsize=9,pad=5,loc='left')
# Set labels and ticks of axes
plt.xlabel('Temperature change over sea (%sC)'%(chr(176)),fontsize=9)
plt.ylabel('Temperature change over land (%sC)'%(chr(176)),fontsize=9)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
# Add grey dotted lines to indicate the zero levels
plt.axvline(x=0,color='grey',linestyle="dotted",linewidth=0.5)
plt.axhline(y=0,color='grey',linestyle="dotted",linewidth=0.5)
# Set axes limits
plt.xlim([-11,20])
plt.ylim([-15,25])
# Set boundary edges
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Plotting individual models
# CMIP6
ch03_fig2b_function1('LGM')
ch03_fig2b_function1('LIG')
ch03_fig2b_function1('MH')
ch03_fig2b_function1('mPWP')
ch03_fig2b_function1('EECO')
ch03_fig2b_function1('1pctCO2')
ch03_fig2b_function1('abrupt4xCO2')
#CMIP5
ch03_fig2b_function2('MH')
ch03_fig2b_function2('LGM')
ch03_fig2b_function2('1pctCO2')
ch03_fig2b_function2('abrupt4xCO2')
# nonCMIP
ch03_fig2b_function3('LGM')
ch03_fig2b_function3('LIG')
ch03_fig2b_function3('MH')
ch03_fig2b_function3('mPWP')
ch03_fig2b_function3('EECO')
# Plotting multi-model means
# CMIP6
ch03_fig2b_function4('LGM')
ch03_fig2b_function4('MH')
ch03_fig2b_function4('LIG')
ch03_fig2b_function4('mPWP')
ch03_fig2b_function4('EECO')
ch03_fig2b_function4('1pctCO2')
ch03_fig2b_function4('abrupt4xCO2')
#CMIP5
ch03_fig2b_function5('MH')
ch03_fig2b_function5('LGM')
ch03_fig2b_function5('1pctCO2')
ch03_fig2b_function5('abrupt4xCO2')
# nonCMIP
ch03_fig2b_function6('LGM')
ch03_fig2b_function6('MH')
ch03_fig2b_function6('LIG')
ch03_fig2b_function6('mPWP')
ch03_fig2b_function6('EECO')
# Instrumental
ch03_fig2b_function7()
# Reconstruction
ch03_fig2b_function8()
# Regression line
XX = np.arange(-11,20,0.5)
X2 = XX*XX
Yall = X2*(-0.019470) + XX*(1.580454)
plt.plot(XX,Yall,'k',label='Fit to data:')
# Set legend names
# Individual models
plt.scatter(-50, -50,marker=markers['CMIP6'][0],s=30,color='k',linewidths=1,edgecolors='k',facecolors='none',label='CMIP6')
plt.scatter(-50, -50,marker=markers['CMIP5'][0],s=30,color='k',linewidths=1,edgecolors='k',label='CMIP5')
plt.scatter(-50, -50,marker=markers['nonCMIP'][0],s=30,color='k',linewidths=1,edgecolors='k',label='non-CMIP')
# Multi-model means
plt.scatter(-50, -50,marker=avemarkers['CMIP6'][0],s=75,color='k',linewidths=1,edgecolors='k',facecolors='none',label='CMIP6')
plt.scatter(-50, -50,marker=avemarkers['CMIP5'][0],s=75,color='k',linewidths=1,edgecolors='k',facecolors='none',label='CMIP5')
plt.scatter(-50, -50,marker=avemarkers['nonCMIP'][0],s=75,color='k',linewidths=1,edgecolors='k',facecolors='none',label='non-CMIP')
leg = plt.legend(edgecolor='None',facecolor='None',markerfirst=False,fontsize=9)
plt.show()



