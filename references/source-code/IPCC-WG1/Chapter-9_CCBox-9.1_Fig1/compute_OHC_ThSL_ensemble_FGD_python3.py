# coding=utf-8
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import matplotlib
import pickle
import csv


def extract_period(yrs, series, fyr=1900.5, lyr=2009.5):
    """
    This function extracts a subsection of a timeseries on the basis of specified first and last years
    inputs:
        * yrs    = time coordinate in years
        * series = input timeseries
        * fyr    = first year of sub-period
        * lyr    = last year of sub-period
    outputs:
        * subyrs    = years corresponding to sub-section timeseries
        * subseries = sub-section of input timeseries
    """
    subi = np.where((yrs >= fyr) & (yrs <= lyr))[0]  # Index for sub-section
    subseries = series[subi].copy()
    subyrs = yrs[subi]
    return subyrs, subseries

def runningmean(yrs, series, window=3):
    """
    This function applies a running-mean smoothing to OHC timerseries in order to reduce the effect
    of sampling noise. The default is to use a 3-yr window, following Domingues et al (2008) and AR6
    Chapter 2.
    :param yrs: input time coordinate in years
    :param series: input timeseries
    :param window: the length of the window for running-mean
    :return: timeseries with running-mean applied, with same length as original timeseries
    """
    newseries = series.copy()
    # First extract the non-NaN values into a sub-array
    nmsgi = np.isfinite(series)
    subseries = series[nmsgi]
    subyrs    = yrs[nmsgi]
    # Perform the runnning mean..
    weights = np.repeat(1.0, window)/window
    rmseries = np.convolve(subseries, weights, 'same') # Preserve original series length (end effects visible)
    rmseries[0] = subseries[0] # Make sure the start and end points are identical to original series (avoid edge effects)
    rmseries[-1] = subseries[-1]
    # Reinstate the rmseries into the parent array copy..
    newseries[nmsgi] = rmseries
    return newseries

def compute_OHC_ThSL_regression(ohc_dict, thsl_dict, layer='0-700m',
                                names=['Pur10', 'Dom08', 'Lev12', 'Ish17']):
    """
    This function computes a regression coefficient between OHC change and ThSL so that
    timeseries of OHC change can be converted into timeseries of ThSL change, when ThsL is not available.
    :param ohc_dict: Input dictionary of OHC timeseries
    :param thsl_dict: Input dictionary of ThSL timeseries
    :param layer: String to determine the depth layer used
    :param names: A list of product names from which to compute the regressions
    :return: the mean regression value computed from all available products..
    """
    nvals = len(names)  # Number of regression estimates
    depths = ohc_dict['depths']
    zi = np.where(depths == layer)[0][0]  # Depth index
    reg_vals = np.empty(nvals)  #  Array for regression values
    reg_vals[:] = np.NaN
    deg = 1.  # Degree of polynomial to fit

    colors = ['tab:red', 'tab:blue', 'tab:orange', 'tab:purple', 'tab:pink',
              'tab:olive', 'tab:cyan']

    for nn, name in enumerate(names):
        try:
            series1 = ohc_dict[name][zi, :]
            series2 = thsl_dict[name][zi, :]
            idx = np.isfinite(series1) & np.isfinite(series2)
            slope, offset = np.polyfit(series1[idx], series2[idx], deg)
            plt.plot(series1, series2, label=name, marker='x', markersize=10,
                     linewidth=0.0, color=colors[nn], fillstyle='none')
            plt.plot(series1, series1 * slope + offset, color=colors[nn],
                     linewidth=2.0)
            reg_vals[nn] = slope
        except:
            None
    ax = plt.gca()
    ymin, ymax = ax.get_ylim()
    xmin, xmax = ax.get_xlim()
    for nn, name in enumerate(names):
        if np.isfinite(reg_vals[nn]):
            text = str(np.round(reg_vals[nn], decimals=5)) + ' mm / ZJ'
            color = colors[nn]
            x = 0.6 * xmax
            y = 0.1 * ymin + 0.2 * nn * ymin
            plt.text(x, y, text, color=color)
    mean_val = np.nanmean(reg_vals)
    text = str(np.round(mean_val, decimals=5)) + ' mm / ZJ'
    plt.text(x, 0.9 * ymin, text, color='k')
    plt.title(layer + ' regression OHC vs ThSL')
    plt.xlabel('OHC Change (ZJ)')
    plt.ylabel('ThSL Change (mm)')
    plt.legend(frameon=False)
#    plt.show()
    plt.close()
    # Return the mean regression value:
    return mean_val

#-----------------------------------------
# Set output files/dirs for plots/data..
#-----------------------------------------
plotdir = '/Users/matt/python/ar6/src/notebooks/FGD/plots/'
savedir  = '/Users/matt/python/ar6/src/notebooks/FGD/data/'

pltstr = 'AR6_FGD_OHC_ThSL_ensemble' # First part of plot filename

pickle_file1 = 'AR6_OHC_ensemble_FGD.pickle'
csv_file1 = 'AR6_OHC_ensemble_FGD.csv'
pickle_file2 = 'AR6_ThSL_ensemble_FGD.pickle'
csv_file2 = 'AR6_ThSL_ensemble_FGD.csv'

#-----------------------------
# Read in data / dictionaries..
#-----------------------------

datadir = '/Users/matt/Data/AR6/Domingues/FGD/'
matfile = 'AR6_GOHC_GThSL_timeseries_MDP_2021-01-20.mat'
matdata = scipy.io.loadmat(datadir + matfile)

yrs = matdata['time_yr'][0] + 0.5 # Express time coordinate as year mid-points..
depths = []  # Define empty list for depths..
for array in matdata['dep']:
#    depth_string = string.strip(str(array[0][0]))
    depth_string = str(array[0][0]).strip()
    depths.append(depth_string.replace(" ", "")) # Remove all white space
depths = np.array(depths)
# depths = ['0-300m' '0-700m' '700-2000m' '>2000m' 'Full-depth' '0-2000m']

# Product names in *.mat file (as of 11/09/2020)
#['Bagg19', 'CARS09', 'CORAv5.2', 'CSIRO', 'Cheng17', 'Desb17', 'Dom08', 'Dom08-I', 'Dom08-L',
# 'EN4', 'GCOS20', 'IPRC', 'ISAS-15', 'Ish17', 'JAMSTEC', 'KvS011', 'LEGOS', 'Lev12', 'NOC',
# 'PMEL', 'Pur10', 'Res19', 'Scripps', 'Su20', 'Zan19']

hc_data = matdata['hc_global']
hc_e_data = matdata['hc_e_global']
th_data = matdata['th_global']
th_e_data = matdata['th_e_global']

ohc_dict = {} # Define an empty dictionary for OHC / ThsL and their errors
ohc_err_dict = {}
thsl_dict = {}
thsl_err_dict = {}

for ii, array in enumerate(matdata['fname']):
#    name = string.strip(str(array[0][0]))
    name = str(array[0][0]).strip()
    ohc_dict[name] = hc_data[ii, :, :]
    ohc_err_dict[name] = hc_e_data[ii, :, :]
    thsl_dict[name] = th_data[ii, :, :]
    thsl_err_dict[name] = th_e_data[ii, :, :]

# Build the depth information into the dictionaries
ohc_dict['depths'] = depths
ohc_err_dict['depths'] = depths
thsl_dict['depths'] = depths
thsl_err_dict['depths'] = depths

ohc_dict['units'] = 'ZJ'
ohc_err_dict['units'] = 'ZJ (1-sigma)'
thsl_dict['units'] = 'mm'
thsl_err_dict['units'] = 'mm (1-sigma)'
ohc_dict['baseline_period'] = '1995-2014'
thsl_dict['baseline_period'] = '1995-2014'

###############################
# NOTE - as of 13.01.2020 Catia has changed the string for Ishii from 'Ish17' to 'Ish17v7.3'.
# Simplest fix is to copy the data into a dictionary entry with the old name..
if matfile in ['AR6_GOHC_GThSL_timeseries_MDP_2021-01-13.mat', 'AR6_GOHC_GThSL_timeseries_MDP_2021-01-20.mat']:
    ohc_dict['Ish17'] = ohc_dict['Ish17v7.3']
    ohc_err_dict['Ish17'] = ohc_err_dict['Ish17v7.3']
    thsl_dict['Ish17'] = thsl_dict['Ish17v7.3']
    thsl_err_dict['Ish17'] = thsl_err_dict['Ish17v7.3']
###############################

color_dict = {'Cheng17':'tab:purple',
           'Dom08':'tab:blue',
           'EN4':'tab:red',
           'Ish17':'tab:green',
           'Lev12':'tab:orange',
           'Zan19':'tab:cyan',
           'PMEL':'tab:pink'}

# Define ensemble members for each vertical layer..
ohc_names = {'0-700m':['Dom08', 'Lev12', 'Ish17', 'EN4', 'Cheng17'],
            '700-2000m':['Lev12', 'Ish17', 'Cheng17']}

# Subset of products with ThSL estimate available for each vertical layer..
thsl_names = {'0-700m':['Dom08', 'Lev12', 'Ish17'],
            '700-2000m':['Lev12', 'Ish17']}

# Dictionaries for ensemble assessments of OHC and ThSl change..
ensm_ohc_dict = {}
ensm_thsl_dict = {}
ensm_ohc_dict['units'] = 'ZJ'
ensm_ohc_dict['error units'] = 'ZJ (1-sigma)'
ensm_thsl_dict['units'] = 'mm'
ensm_thsl_dict['error units'] = 'mm (1-sigma)'
ensm_ohc_dict['baseline period'] = '1995-2014'
ensm_thsl_dict['baseline period'] = '1995-2014'

#-----------------------------
#-----------------------------


#-----------------------------
# Generate and plot the ensemble..
#-----------------------------

byr1=1995.5 # Set basline period used in AR6 and extract indices
byr2=2014.5
bindex = np.where((yrs >= byr1) & (yrs <= byr2))[0]


# Generate array of years common to all ensemble members
core_yrs = np.arange(1971.5, 2018.5 + 1, 1.0) # Generate at timeseries of years from 1971.5 to 2018.5

fyr = core_yrs[0]
lyr = core_yrs[-1]

for layer in ['0-700m', '700-2000m']:
    plotfile1 = pltstr+'_structural_uncertainty_'+layer+'.png'
    plotfile2 = pltstr+'_internal_uncertainty_'+layer+'.png'

    zi = np.where(depths == layer)[0][0]
    names = ohc_names[layer]
    nprod = len(names)

    for nn, name in enumerate(names):
        series1 = ohc_dict[name][zi, :].copy()
        eseries1 = ohc_err_dict[name][zi, :].copy()
        if name in thsl_names[layer]:
            series2 = thsl_dict[name][zi, :].copy()
            eseries2 = thsl_err_dict[name][zi, :].copy()
        else:
            ohc2thsl = compute_OHC_ThSL_regression(ohc_dict, thsl_dict, layer=layer)
            print(layer, ' ohc2thsl = ', ohc2thsl)
            series2 = series1 * ohc2thsl # Convert OHC to ThSL using mean regression coefficient from available products
            eseries2 = eseries1 * ohc2thsl

        # Apply common baseline period..
        series1 -= series1[bindex].mean()
        series2 -= series2[bindex].mean()

        if name == 'Cheng17':
            print('Apply Cheng17 error scaling..')
            eseries1 = eseries1 * (1.0 / 1.645)  # Convert 90% confidence interval to 1-sigma errors
            # NOTE: don't scale eseries2, because it is already dependent on eseries1!

        series1 = runningmean(yrs, series1)  # Apply 3-year running mean as per Domingues et al.
        eseries1 = runningmean(yrs, eseries1)
        series2 = runningmean(yrs, series2)  # Apply 3-year running mean as per Domingues et al.
        eseries2 = runningmean(yrs, eseries2)

        subyrs1, subseries1 = extract_period(yrs, series1, fyr=fyr, lyr=lyr)
        subyrs1, subeseries1 = extract_period(yrs, eseries1, fyr=fyr, lyr=lyr)
        subyrs2, subseries2 = extract_period(yrs, series2, fyr=fyr, lyr=lyr)
        subyrs2, subeseries2 = extract_period(yrs, eseries2, fyr=fyr, lyr=lyr)

        if (layer == '0-700m') & (name == 'Dom08'):
            ensm_ohc_dict['ocean_' + layer] = subseries1 - subseries1[0] # Input Domingues et al (2008) as central estimate for 0-700m layer
            ensm_thsl_dict['ocean_' + layer] = subseries2 - subseries2[0]
            ensm_ohc_dict['yrs'] = subyrs1
            ensm_thsl_dict['yrs'] = subyrs2

        if (layer == '700-2000m') & (name == 'Ish17'):
            ensm_ohc_dict['ocean_' + layer] = subseries1 - subseries1[0]  # Input Ishii et al (2017) as central estimate for 700-2000m layer
            ensm_thsl_dict['ocean_' + layer] = subseries2 - subseries2[0]

        if nn == 0:  # Setup matrix for ensemble..
            nyrs = len(subseries1)
            ensm1 = np.zeros((nprod, nyrs))
            ensm_error1 = np.zeros((nprod, nyrs))
            ensm2 = np.zeros((nprod, nyrs))
            ensm_error2 = np.zeros((nprod, nyrs))
            ensm1[nn, :] = subseries1
            ensm_error1[nn, :] = subeseries1
            ensm2[nn, :] = subseries2
            ensm_error2[nn, :] = subeseries2
        else:
            ensm1[nn, :] = subseries1
            ensm_error1[nn, :] = subeseries1
            ensm2[nn, :] = subseries2
            ensm_error2[nn, :] = subeseries2

    # Compute ensemble statistics for OHC:
    ensm_mean1   = np.nanmean(ensm1, axis=0).copy()
    struct_err1  = np.nanstd(ensm1, axis=0).copy()
    map_err1     = np.nanmax(ensm_error1, axis=0).copy()
    total_err1   = np.sqrt(np.square(struct_err1) + np.square(map_err1)).copy()
    ensm_ohc_dict['ocean_' + layer + '_error'] = total_err1

    # Compute ensemble statistics for ThSL:
    ensm_mean2   = np.nanmean(ensm2, axis=0).copy()
    struct_err2  = np.nanstd(ensm2, axis=0).copy()
    map_err2     = np.nanmax(ensm_error2, axis=0).copy()
    total_err2   = np.sqrt(np.square(struct_err2) + np.square(map_err2)).copy()
    ensm_thsl_dict['ocean_' + layer + '_error'] = total_err2

    plt.figure()
    f = plt.gcf()
    f.set_size_inches(12.0, 6.0)
    matplotlib.rcParams['font.size'] = 11

    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    for nn, name in enumerate(names):
        color = color_dict[name]
        series1 = ensm1[nn, :]
        series2 = ensm2[nn, :]
        ax1.plot(core_yrs, series1, color=color, label=name)
        ax2.plot(core_yrs, series2, color=color, label=name)
    # plt.plot(gcos_yrs, gcos_series, 'k--', label='GCOS')
    ax1.plot(core_yrs, ensm_mean1, 'k', linewidth=2.0, label='Ens_Mean')
    ax1.fill_between(core_yrs, ensm_mean1 - struct_err1 * 1.645, ensm_mean1 + struct_err1 * 1.645,
                     facecolor='gray', alpha=0.5, edgecolor='None', label='90% C.I.')
    ax2.plot(core_yrs, ensm_mean2, 'k', linewidth=2.0, label='Ens_Mean')
    ax2.fill_between(core_yrs, ensm_mean2 - struct_err2 * 1.645, ensm_mean2 + struct_err2 * 1.645,
                     facecolor='gray', alpha=0.5, edgecolor='None', label='90% C.I.')
    ax1.set_title('OHC Structural Uncertainty ' + layer)
    ax1.set_ylabel('OHC Anomaly (ZJ)')
    ax1.legend(prop={'size': 10}, frameon=False, ncol=1)
    ax2.set_title('ThSL Structural Uncertainty ' + layer)
    ax2.set_ylabel('Sea Level Anomaly (ZJ)')
    ax2.legend(prop={'size': 10}, frameon=False, ncol=1)

    print("Saving file: ", plotdir + plotfile1)
    plt.savefig(plotdir + plotfile1, dpi=300)
    plt.show()

    plt.figure()
    f = plt.gcf()
    f.set_size_inches(12.0, 6.0)
    matplotlib.rcParams['font.size'] = 11

    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    for nn, name in enumerate(names):
        color = color_dict[name]
        series1 = ensm_error1[nn, :]
        series2 = ensm_error2[nn, :]
        ax1.plot(core_yrs, series1 * 1.645, color=color, label=name)
        ax2.plot(core_yrs, series2 * 1.645, color=color, label=name)

    ax1.fill_between(core_yrs, np.zeros_like(map_err1), map_err1 * 1.645,
                     facecolor='gray', alpha=0.5, edgecolor='None')
    ax1.plot(core_yrs, map_err1 * 1.645, 'k:', linewidth=2.0, label='Mapping Error')
    ax2.fill_between(core_yrs, np.zeros_like(map_err2), map_err2 * 1.645,
                     facecolor='gray', alpha=0.5, edgecolor='None')
    ax2.plot(core_yrs, map_err2 * 1.645, 'k:', linewidth=2.0, label='Mapping Error')

    ax1.set_title('OHC Mapping Uncertainty ' + layer)
    ax1.set_ylabel('90% C.I. OHC Error (ZJ)')
    ax1.legend(prop={'size': 10}, frameon=False, ncol=1)
    ax2.set_title('ThSL Mapping Uncertainty ' + layer)
    ax2.set_ylabel('90% C.I. Sea Level Error (mm)')
    ax2.legend(prop={'size': 10}, frameon=False, ncol=1)
    print("Saving file: ", plotdir + plotfile2)
    plt.savefig(plotdir + plotfile2, dpi=300)
    plt.show()

#-----------------------------
#-----------------------------

#---------------------------------------------------------------------------
# Incorporate estimate of sub-2000m trends based on Purkey and Johson (2010)
# and Desbruyeres et al (2016)
#---------------------------------------------------------------------------

# Load from Catia's *.mat file
zi = np.where(depths == '>2000m')[0][0]
ohc = ohc_dict['Pur10'][zi, :]
ohc_err = ohc_err_dict['Pur10'][zi, :] * (1./1.645) # Convert to 1 standard error from 90% C.I.
thsl = thsl_dict['Pur10'][zi, :]
thsl_err = thsl_err_dict['Pur10'][zi, :] * (1./1.645) # Convert to 1 standard error from 90% C.I.
# Convert NaN values to 0.0
msgi = np.isnan(ohc)
ohc[msgi] = 0.0
msgi = np.isnan(ohc_err)
ohc_err[msgi] = 0.0
msgi = np.isnan(thsl)
thsl[msgi] = 0.0
msgi = np.isnan(thsl_err)
thsl_err[msgi] = 0.0

subyrs1, subseries1 = extract_period(yrs, ohc, fyr=fyr, lyr=lyr)
subyrs1, subeseries1 = extract_period(yrs, ohc_err, fyr=fyr, lyr=lyr)
subyrs2, subseries2 = extract_period(yrs, thsl, fyr=fyr, lyr=lyr)
subyrs2, subeseries2 = extract_period(yrs, thsl_err, fyr=fyr, lyr=lyr)

ensm_ohc_dict['ocean_2000-6000m'] = subseries1
ensm_ohc_dict['ocean_2000-6000m_error'] = subeseries1
ensm_thsl_dict['ocean_2000-6000m'] = subseries2
ensm_thsl_dict['ocean_2000-6000m_error'] = subeseries2

ensm_ohc_dict['ocean_Full-depth'] = ensm_ohc_dict['ocean_0-700m'] + ensm_ohc_dict['ocean_700-2000m'] + ensm_ohc_dict['ocean_2000-6000m']
ensm_ohc_dict['ocean_Full-depth_error'] = ensm_ohc_dict['ocean_0-700m_error'] + ensm_ohc_dict['ocean_700-2000m_error'] + ensm_ohc_dict['ocean_2000-6000m_error']

ensm_thsl_dict['ocean_Full-depth'] = ensm_thsl_dict['ocean_0-700m'] + ensm_thsl_dict['ocean_700-2000m'] + ensm_thsl_dict['ocean_2000-6000m']
ensm_thsl_dict['ocean_Full-depth_error'] = ensm_thsl_dict['ocean_0-700m_error'] + ensm_thsl_dict['ocean_700-2000m_error'] + ensm_thsl_dict['ocean_2000-6000m_error']

#-------------------------------------------------
# Write the OHC ensemble to CSV / *.pickle file..
#-------------------------------------------------

ohc_0to700m = ensm_ohc_dict['ocean_0-700m']
ohc_700to200m = ensm_ohc_dict['ocean_700-2000m']
ohc_below2000m = ensm_ohc_dict['ocean_2000-6000m']
ohc_total = ensm_ohc_dict['ocean_Full-depth']

ohc_err_0to700m = ensm_ohc_dict['ocean_0-700m_error']
ohc_err_700to200m = ensm_ohc_dict['ocean_700-2000m_error']
ohc_err_below2000m = ensm_ohc_dict['ocean_2000-6000m_error']
ohc_err_total = ensm_ohc_dict['ocean_Full-depth_error']

with open(savedir + csv_file1, mode='w') as CSV_file:
    OHC_writer = csv.writer(CSV_file, delimiter=',',
                             quoting=csv.QUOTE_MINIMAL)
    OHC_writer.writerow(['Changes in global ocean heat content in Zettajoules (ZJ) ' +
                          'relative to the 1971 average.'])
    OHC_writer.writerow(['Year',
                          'Central Estimate 0-700m',
                          '0-700m Uncertainty (1-sigma)',
                          'Central Estimate 700-2000m',
                          '700-2000m Uncertainty (1-sigma)',
                          'Central Estimate >2000m',
                          '>2000m Uncertainty (1-sigma)',
                          'Central Estimate Full-depth',
                          'Full-depth Uncertainty (1-sigma)'])

    for yy, yr in enumerate(core_yrs):
        OHC_writer.writerow([yr,
        ohc_0to700m[yy],
        ohc_err_0to700m[yy],
        ohc_700to200m[yy],
        ohc_err_700to200m[yy],
        ohc_below2000m[yy],
        ohc_err_below2000m[yy],
        ohc_total[yy,],
        ohc_err_total[yy,]])

print("SAVING:"+savedir+csv_file1)

ohc_dict = {'ensm_ohc_dict':ensm_ohc_dict}

print("SAVING:"+savedir+pickle_file1)
pickle.dump( ohc_dict, open( savedir+pickle_file1, "wb" ) )
#-------------------------------------------------
#-------------------------------------------------

#-------------------------------------------------
# Write the ThSL ensemble to CSV / *.pickle file..
#-------------------------------------------------

thsl_0to700m = ensm_thsl_dict['ocean_0-700m']
thsl_700to200m = ensm_thsl_dict['ocean_700-2000m']
thsl_below2000m = ensm_thsl_dict['ocean_2000-6000m']
thsl_total = ensm_thsl_dict['ocean_Full-depth']

thsl_err_0to700m = ensm_thsl_dict['ocean_0-700m_error']
thsl_err_700to200m = ensm_thsl_dict['ocean_700-2000m_error']
thsl_err_below2000m = ensm_thsl_dict['ocean_2000-6000m_error']
thsl_err_total = ensm_thsl_dict['ocean_Full-depth_error']

with open(savedir + csv_file2, mode='w') as CSV_file:
    ThSL_writer = csv.writer(CSV_file, delimiter=',',
                             quoting=csv.QUOTE_MINIMAL)
    ThSL_writer.writerow(['Changes in global thermal expansion (mm) ' +
                          'relative to the 1971 average.'])
    ThSL_writer.writerow(['Year',
                          'Central Estimate 0-700m',
                          '0-700m Uncertainty (1-sigma)',
                          'Central Estimate 700-2000m',
                          '700-2000m Uncertainty (1-sigma)',
                          'Central Estimate >2000m',
                          '>2000m Uncertainty (1-sigma)',
                          'Central Estimate Full-depth',
                          'Full-depth Uncertainty (1-sigma)'])

    for yy, yr in enumerate(core_yrs):
        ThSL_writer.writerow([yr,
        thsl_0to700m[yy],
        thsl_err_0to700m[yy],
        thsl_700to200m[yy],
        thsl_err_700to200m[yy],
        thsl_below2000m[yy],
        thsl_err_below2000m[yy],
        thsl_total[yy,],
        thsl_err_total[yy,]])

print("SAVING:"+savedir+csv_file2)

thsl_dict = {'ensm_thsl_dict':ensm_thsl_dict}

print("SAVING:"+savedir+pickle_file2)
pickle.dump( thsl_dict, open( savedir+pickle_file2, "wb" ) )
#-------------------------------------------------
#-------------------------------------------------
