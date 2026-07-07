#********************************************************************************
#!cdat8.2.1 
#
# plotFinal_1panel_mpl.py
#
# Written by Krishna AchutaRao
#
#            13 February 2021
#
# This code just reads in the annual average zostoga for each experiment and model
# (only the de-drifted versions) and plots (using matplotlib) the multi-model-mean
# in a colored line (according to experiment) and the 5-95 envelope based on the
# model weights determined by number of models and realizations. For this, anomalies
# w.r.t 1850-1900 are calculated for each time series is calculated. The obs data is
# read in from a netCDF file that was created by reading in the csv file provided
# by Matt Palmer. This is essentially data from Table 2.6(?) in chapter 2.
#
# This code also computes the delta (change between two specified start and end years)
# for a list of time intervals and rate (delta/number of years in the interval) to be
# written out for use in table 3.2.
#
# Output files:
#    1. Figure files named "Figure_3.29" in .svg, .pdf and .png formats.
#    2. Text file ExperimentsModelsRealizations.txt with a list of experiments, models
#       and individual realizations that go into producing the plot
#    3. Text file DeltasRates_MME_historical.txt with the values of deltas and rates
#
#
# Required to run the code
#    Other than standard CDAT v8.2.1 libraries (Python 3), two other modules are imported:
#    1. UncertaintyFunctions
#    2. zostogaProcessedPlotDataDict
#
#********************************************************************************

import cdms2, genutil, cdutil, numpy, os, cdtime
import matplotlib.pyplot as plt

from UncertaintyFunctions import *
from zostogaProcessedPlotDataDict import plotDataDict

BASE_TIME_UNITS = 'days since 1850-1-1'

DATA_DIR = '../PROCESSED_DATA/zostoga_AnnualMean_dedrifted/'

fyrs = [1901.5, 1901.5, 1971.5, 1993.5, 2006.5, 1850.5]
lyrs = [1990.5, 2014.5, 2014.5, 2014.5, 2014.5, 2014.5]

exp_list = ['hist-nat', 'hist-aer', 'hist-GHG', 'historical']
lines_to_plot_dict = {}

fout1 = open('ExperimentsModelsRealizations.txt', 'w')
fout2 = open('DeltasRates_MME_historical.txt', 'w')

fout1.write ('Output from plotFinal_1panel_mpl.py\n')
fout1.write ('List of experiments, models, realizations used for plotting Figure 3.29.\n')

for exp in exp_list:
    #
    print ('Experiment :', exp)
    fout1.write ('Experiment :%s\n' %exp)
    #
    lines_to_plot_dict[exp] = {}
    #
    mod_list = list(plotDataDict[exp].keys())
    #
    mod_list.sort()
    N_MODS = len(mod_list)
    N_RELS = {}
    #
    # all_models_rels_weights_list will contain weights for every realization of every model
    #
    all_models_rels_weights_list = []
    #
    # all_models_rels_data will contain every realization of every model
    #
    all_models_rels_data = []
    #
    # all_models_avg_list will contain the average of all realizations of a single model
    #
    all_models_avg_list = []  
    #
    # all_models_avg_var_list_to_plot will contain the individual model averages variable for plotting.
    #
    all_models_avg_var_list_to_plot = []
    #
    all_rels_all_models_list_to_plot = []
    #
    delta_dict = {}
    rate_dict = {}
    #
    for mod in mod_list:
        #
        print ('\tModel :', mod)
        fout1.write('\tModel :%s\n' %mod)
        rel_list = plotDataDict[exp][mod].keys()
        N_RELS[mod] = len(rel_list)
        #
        # Create an empty list where all realizations of this model will be appended
        #
        all_rels_data = []
        #
        for rel in rel_list:
            #
            print ('\t\tRealization :', rel)
            fout1.write('\t\tRealization :%s\n' %rel)
            #
            REL_DIR = DATA_DIR + exp + '/' + mod + '/' + rel + '/'
            #
            file = plotDataDict[exp][mod][rel]
            #
            f = cdms2.open(REL_DIR + file)
            x = f('zostoga', time=('1850-1-1', '2014-12-31'))
            #
            x_clim = cdms2.MV2.average(x(time=('1850-1-1', '1900-12-31')))
            #
            x_anom = x - x_clim
            #
            #print '\tUnits:', x.units
            #
            # Change to mm units
            #
            x_anom = x_anom * 1000.
            #
            taxis = x.getTime()
            #
            # Some hoops to go through because of the 360-day calendar in the UK models
            #
            if taxis.calendar == '360_day':
                CAL = cdtime.Calendar360
            elif taxis.calendar == 'noleap':
                CAL = cdtime.NoLeapCalendar
            elif taxis.calendar == 'proleptic_gregorian':
                CAL = cdtime.GregorianCalendar
            else:
                CAL = cdtime.MixedCalendar
            # end of if taxis.calendar == '360_day':
            #
            all_vals = []
            for jj in range(len(taxis)):
                comp = cdtime.reltime(taxis[jj], taxis.units).tocomp(CAL)
                all_vals.append(comp.torel('days since 1850-1-1').value)
            # end of for jj in range(len(taxis)):
            newtaxis = cdms2.createAxis(numpy.array(all_vals))
            newtaxis.units='days since 1850-1-1'
            newtaxis.calendar = cdtime.MixedCalendar
            newtaxis.designateTime()
            #
            x_anom.setAxis(0, newtaxis)
            #
            all_models_rels_data.append(x_anom[:])
            all_rels_data.append(x_anom[:])
            #
            all_rels_all_models_list_to_plot.append(x_anom)
            #
            # Now compute deltas and rates for each time interval for the historical only
            #
            if exp == 'historical':
                #
                for ti in range(len(fyrs)):
                    fyr = int(fyrs[ti])
                    lyr = int(lyrs[ti])
                    xslice = x_anom(time=(str(fyr)+'-1-1', str(lyr)+'-12-31'))
                    xdelta = xslice[-1] - xslice[0]
                    xrate  = xdelta/(lyr-fyr)
                    PERIOD_STR = str(fyr) + '-' + str(lyr)
                    if PERIOD_STR not in list(delta_dict.keys()):
                        delta_dict[PERIOD_STR] = {}
                        rate_dict[PERIOD_STR] = {}
                    # end of if PERIOD_STR not in list(delta_dict.keys()):
                    #
                    if mod not in list(delta_dict[PERIOD_STR].keys()):
                        delta_dict[PERIOD_STR][mod] = []
                        rate_dict[PERIOD_STR][mod] = []
                    # end of if mod not in (delta_dict[PERIOD_STR].keys())
                    #
                    delta_dict[PERIOD_STR][mod].append(xdelta)
                    rate_dict[PERIOD_STR][mod].append(xrate)
                    #
                # end of for ti in range(len(fyrs)):
            # end of if exp == 'historical':
            f.close()
            del x
            del x_clim
            #
        # end of for rel in rel_list:
        #
        # Compute weights and append to weights list
        #
        this_model_weights = N_RELS[mod]*[1.0/(N_RELS[mod] * N_MODS)]
        for j in range(len(this_model_weights)):
            all_models_rels_weights_list.append(this_model_weights[j])
        # end of for j in range(len(this_model_weights)):
        #
        # Compute model average
        #
        one_model_avg = numpy.average(numpy.array(all_rels_data), axis=0)        
        all_models_avg_list.append(one_model_avg)
        one_model_avg = cdms2.createVariable(one_model_avg, axes=[taxis], id ='zostoga')
        all_models_avg_var_list_to_plot.append(one_model_avg)
        #
    # end of for mod in mod_list[:1]:
    all_models_avg = numpy.average(numpy.array(all_models_avg_list), axis=0)
    #
    #
    # Make the list of values from all models and realizations into an array
    #
    all_models_rels_data = numpy.array(all_models_rels_data)
    #
    # Make the list of weights from all models and realizations into an array
    #
    all_models_rels_weights = numpy.array(all_models_rels_weights_list)
    #
    # Compute the 5-95 %ile range
    #
    low, high = percentileFunction(all_models_rels_data, all_models_rels_weights)
    #
    p05_var = cdms2.createVariable(low, axes=[newtaxis], id = 'p05')
    p95_var = cdms2.createVariable(high, axes=[newtaxis], id = 'p95')
    mmm = cdms2.createVariable(all_models_avg,  axes=[newtaxis], id = 'mmm')
    #
    lines_to_plot_dict[exp]['mmm'] = mmm
    lines_to_plot_dict[exp]['p05'] = p05_var
    lines_to_plot_dict[exp]['p95'] = p95_var
    #
    # Now calculate the multimodel mean and 5-95 range for the deltas and rates - only for historical
    #
    if exp == 'historical':
        #
        mmm_delta_rate_dict = {}
        #
        for ti in range(len(fyrs)):
            fyr = int(fyrs[ti])
            lyr = int(lyrs[ti])
            mmmslice = mmm(time=(str(fyr)+'-1-1', str(lyr)+'-12-31'))
            mmmdelta = mmmslice[-1] - mmmslice[0]
            mmmrate  = mmmdelta/(lyr-fyr)
            PERIOD_STR = str(fyr) + '-' + str(lyr)
            mmm_delta_rate_dict[PERIOD_STR] = {}
            mmm_delta_rate_dict[PERIOD_STR]['delta'] = mmmdelta
            mmm_delta_rate_dict[PERIOD_STR]['rate'] = mmmrate
        # end of for ti in range(len(fyrs)):
        #
        print ('Experiment: ', exp)
        print ('Units: delta in mm; rate in mm/year')
        #
        fout2.write ('Experiment: %s\n' %exp)
        fout2.write ('Units: delta in mm; rate in mm/year\n')
        #
        for period in list(delta_dict.keys()):
            delta_model_list = []
            rate_model_list = []
            for model in list(delta_dict[period].keys()):
                delta_model_list.append(delta_dict[period][model])
                rate_model_list.append(rate_dict[period][model])
            # end of for model in list(delta_dict[period].keys()):
            #
            # First get a flat version of these lists to use in the 5-95% calculations
            #
            flat_delta_model_list = flatten_list(delta_model_list)
            flat_rate_model_list = flatten_list(rate_model_list)
            #
            # Now calculate the 5-95% with the weights that have been calculated
            #
            low_delta, high_delta = oneDimFunction(numpy.array(flat_delta_model_list), all_models_rels_weights)
            low_rate, high_rate = oneDimFunction(numpy.array(flat_rate_model_list), all_models_rels_weights)
            #
            # Now calculate the mean of each model's deltas and rates and the overall MMM delta and rate
            #
            delta_mmm = mmm_list(delta_model_list)
            rate_mmm = mmm_list(rate_model_list)
            #
            print ('Period:', period, 'delta using MMM time series: %5.3f, Mean delta: %5.3f 5-95 Range: (%5.3f, %5.3f)' %(mmm_delta_rate_dict[period]['delta'],delta_mmm, low_delta, high_delta))
            print ('Period:', period, ' rate using MMM time series: %5.3f, Mean  rate: %5.3f 5-95 Range: (%5.3f, %5.3f)' %(mmm_delta_rate_dict[period]['rate'],rate_mmm, low_rate, high_rate))
            print ('\n')
            #
            fout2.write ('Period: %s, delta using MMM time series: %5.3f, Mean delta: %5.3f 5-95 Range: (%5.3f, %5.3f)\n' %(period, mmm_delta_rate_dict[period]['delta'],delta_mmm, low_delta, high_delta))
            fout2.write ('Period: %s, rate using MMM time series: %5.3f, Mean  rate: %5.3f 5-95 Range: (%5.3f, %5.3f)\n' %(period, mmm_delta_rate_dict[period]['rate'],rate_mmm, low_rate, high_rate))
        # end of for period in list(delta_dict.keys()):
    # end of if exp == 'historical':
# end of for exp in exp_list[:1]:


#
# Prepare the observations 
#
y = lines_to_plot_dict['historical']['mmm']
y_clim_20 = cdms2.MV2.average(y(time=('1995-1-1', '2014-12-31')))
y_clim_50 = cdms2.MV2.average(y(time=('1850-1-1', '1900-12-31')))
climatology_correction = y_clim_20 - y_clim_50
#print ('y_clim_20 = ', y_clim_20, 'y_clim_50 = ', y_clim_50, 'Correction = ', climatology_correction)
#
fobs = cdms2.open('../OBS/ThSL_Observed_AR6_FGD_Assessment_Timeseries.nc')
ThSL = fobs('ThSL')
obstaxis = ThSL.getTime()
#
# zero between 1995-2014 and then add historical mmm based correction to sero between 1850-1900
#
ThSL_clim = cdms2.MV2.average(ThSL(time=('1995-1-1', '2014-12-31')))
obs_ThSL = ThSL - ThSL_clim + climatology_correction 
obs_ThSL_1sigma = fobs('ThSL_1sigma')
#
# Make into variables
#
high = obs_ThSL + 1.645 * obs_ThSL_1sigma
low = obs_ThSL - 1.645 * obs_ThSL_1sigma
p05_Obs = cdms2.createVariable(low, axes=[obstaxis], id = 'p05')
p95_Obs = cdms2.createVariable(high, axes=[obstaxis], id = 'p95')
#
# Put them into the dictionary
#
lines_to_plot_dict['Obs'] = {}
lines_to_plot_dict['Obs']['mmm'] = obs_ThSL
lines_to_plot_dict['Obs']['p05'] = p05_Obs
lines_to_plot_dict['Obs']['p95'] = p95_Obs

exp_list.append('Obs')

fout1.close()
fout2.close()


#********************************************************************************
#
# Plotting starts here
#
"""
experiments=['historical','hist-GHG','hist-aer','hist-nat']

cols=numpy.array([[196,121,0],[178,178,178],[0,52,102],[0,79,0]])/256.

shade_cols=numpy.array([[204,174,113],[191,191,191],[67,147,195],[223,237,195])/256.
"""

EXP_COLOR = {'historical': [196,121,0],
             'hist-nat'  : [0,79,0],
             'hist-aer'  : [0,52,102],
             'hist-GHG'  : [178,178,178],
             'Obs'       : [0, 0, 0]
             }
EXP_SHADING = {'historical': [204,174,113],
               'hist-nat'  : [223,237,195],
               'hist-aer'  : [67,147,195],
               'hist-GHG'  : [191,191,191],
               'Obs'       : [0, 0, 0]
               }
EXP_LEGEND = {'historical': 'Anthropogenic + Natural',
              'hist-nat'  : 'Natural',
              'hist-aer'  : 'Aerosols',
              'hist-GHG'  : 'Greenhouse Gases',
              'Obs'       : 'Observed'
              }


#
# Define the plot geometry
#
width_in_inches = 8
height_in_inches = 4
fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches))
#
# Set the x and y ranges for data
#
plt.xlim([182., 63000.])
plt.ylim([-100, 120])
#
# Turn off the top and right side axis spines
#
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#
# Plot the hatched grey rectangle to represent the climatology period
#
rect = plt.Rectangle((182.,-100.), 18444., 220., facecolor='white', edgecolor='lightgrey', alpha=0.4, hatch='////')
ax.add_patch(rect)
#
# Plot the text annotation for climatology period
#
plt.text((182.+18444.)/2, -85, 'Reference Period', fontsize='medium', ha='center')
plt.text((182.+18444.)/2, -95, '(1850-1900)', fontsize='small', ha='center')
#
# Set the tick mark locations
#
ax.set_xticks([3652.0, 10957.0, 18262.0, 25566.0, 32871.0, 40176.0, 47481.0, 54786.0, 62091.0])
ax.set_xticklabels(['1860', '1880', '1900', '1920', '1940', '1960', '1980', '2000', '2020'])


#
# Now for the actual data plotting!
#
for exp in exp_list[::-1]:
    #
    y = lines_to_plot_dict[exp]['mmm']
    x = y.getAxis(0)
    y1 = lines_to_plot_dict[exp]['p05']             
    y2 = lines_to_plot_dict[exp]['p95']
    #
    ax.plot(x[:], y.compressed(), '-', color=raw_to_perc_rgb(EXP_COLOR[exp]), label=EXP_LEGEND[exp])
    ax.fill_between(x[:], y1.compressed(), y2.compressed(), color=raw_to_perc_rgb(EXP_SHADING[exp]), linewidth=0, alpha=0.3)
    #
# end of for exp in exp_list:
#
#
# Set the legend box location and style
#
leg = ax.legend(bbox_to_anchor=(0.35, 0.6, 0.5, .102), frameon=False, ncol=1, title='', handlelength=0,
                fontsize='medium', title_fontsize='large', handletextpad=0.2)

for nt, txt in enumerate(leg.get_texts()):
    col = leg.legendHandles[nt].get_color()
    txt.set_color(col)

#
# Set the plot title
#
ax.set_title('Simulated and observed global mean sea level change due to thermal expansion')
#
# Set the axis labels
#
plt.xlabel("Year")
plt.ylabel("Thermosteric Sea Level Change (mm)")

#
# Show the plot
#
plt.show(block=False)


#
# Save the figure as a pdf & svg
#
plt.savefig('../FIGS/Figure_3.29.png')
plt.savefig('../FIGS/Figure_3.29.pdf')
plt.savefig('../FIGS/Figure_3.29.svg')


