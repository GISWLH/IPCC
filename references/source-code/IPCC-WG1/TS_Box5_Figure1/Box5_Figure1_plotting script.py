#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy.crs as ccrs


# requires the Iris package. See:
# https://scitools.org.uk/
# https://scitools-iris.readthedocs.io/en/stable/
#
import iris
import iris.plot as iplt

import os
import sys
print("The Python version is %s.%s.%s" % sys.version_info[:3])
print("The Iris version is ", iris.__version__)


'''
returns a numpy array of years from an Iris cube
'''
def get_yr(x):
    yr2=x.coord('time')
    y2=yr2.units.num2date(yr2.points)
    y3=np.array(y2[0].year)
    for ii in range(1,len(y2)):
       y3=np.append(y3,y2[ii].year)
    
    return y3


'''
simple smoother function
'''
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# SSP colours:
col_hist = '#000000'
col_ssp119 = '#1E9684'
col_ssp126 = '#1D3354'
col_ssp245 = '#EADD3D'
col_ssp370 = '#F21111'
col_ssp585 = '#840B22'
col_ssp534 = '#9A6DC9'


# read CMIP6 conc-driven CO2 concentrations
#
y_hist, co2_hist = np.loadtxt('CMIP6_HIST_CO2.dat',skiprows=1).T

y_ssp, co2_ssp119, co2_ssp126, co2_ssp245, co2_ssp534, co2_ssp370, co2_ssp585 = np.loadtxt('CMIP6_SSP_CO2.dat',skiprows=1).T

y_ssp_2300, co2_ssp126_2300, co2_ssp534_2300, co2_ssp585_2300 = np.loadtxt('CMIP6_SSP2300_CO2.dat',skiprows=1).T

# "historical" data runs to 2014 and then SSPs from 2015 - this leaves a gap when plotted as separate lines
# so extend hist data to 2015 so there's no gap in plotting. first year of SSPs is invariant across scenarios to 5 sig.fig.
y_hist = np.append(y_hist, 2015)
co2_hist = np.append(co2_hist, co2_ssp245[0])


# read CMIP6 emission-driven CO2 concentrations
y_e,co2_e_mmm,co2_e_pc5,co2_e_pc95 = np.loadtxt('CMIP6_e-CO2.dat',skiprows=1).T


# create dictionaries for ease of selecting scenarios, colours etc
#
data = dict([('hist', co2_hist),('ssp585', co2_ssp585),
             ('ssp370', co2_ssp370),('ssp534', co2_ssp534), 
             ('ssp245', co2_ssp245), ('ssp126', co2_ssp126),
             ('ssp119', co2_ssp119)])

yr_data = dict([('hist', y_hist), ('ssp119', y_ssp), ('ssp126', y_ssp),
             ('ssp245', y_ssp), ('ssp534', y_ssp), ('ssp370', y_ssp),
             ('ssp585', y_ssp)])

plot_data = dict([('hist', True), ('ssp119', True), ('ssp126', True),
             ('ssp245', True), ('ssp534', True), ('ssp370', True),
             ('ssp585', True)])

col = dict([('hist', col_hist), ('ssp119', col_ssp119), ('ssp126', col_ssp126),
             ('ssp245', col_ssp245), ('ssp534', col_ssp534), ('ssp370', col_ssp370),
             ('ssp585', col_ssp585)])

lab = dict([('hist', 'Historical'), ('ssp119', 'SSP1-1.9'), ('ssp126', 'SSP1-2.6'),
             ('ssp245', 'SSP2-4.5'), ('ssp534', 'SSP5-3.4OS'), ('ssp370', 'SSP3-7.0'),
             ('ssp585', 'SSP5-8.5')])


# CO2 concentrations from MAGICC emiss-driven runs for SSPs
# with grateful acknowledgement to Zebedee Nicholls

'''
MAGICC is maintained and developed by Malte Meinshausen (<malte.meinshausen@unimelb.edu.au>),
Jared Lewis (<jared.lewis@climate-resource.com>) and Zebedee Nicholls (<zebedee.nicholls@climate-energy-college.org>).
If you have any questions about MAGICC's output or would like to use it in a publication, please contact
Malte Meinshausen (<malte.meinshausen@unimelb.edu.au>),
Jared Lewis (<jared.lewis@climate-resource.com>) and Zebedee Nicholls (<zebedee.nicholls@climate-energy-college.org>).
The setup used to generate this data is described extensively in Cross-chapter Box 7.1 and is based on 
Meinshausen et al. [2009](https://doi.org/10.1038/nature08017), [2011](https://doi.org/10.5194/acp-11-1417-2011) and [2020](https://doi.org/10.5194/gmd-13-3571-2020).
'''

co2_ssp119_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp119.nc')[0]
co2_ssp126_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp126.nc')[0]
co2_ssp245_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp245.nc')[0]
co2_ssp534_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp534-over.nc')[0]
co2_ssp370_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp370.nc')[0]
co2_ssp585_magicc = iris.load('MAGICCv7.5.1_atmospheric-co2_esm-ssp585.nc')[0]


# create array of years and multi-model mean, 5-95% ranges
#
magicc_yr = get_yr(co2_ssp126_magicc[0])

magicc_ssp126_mmm = np.mean(co2_ssp126_magicc.data,axis=0)
magicc_ssp126_pc95 = np.percentile(co2_ssp126_magicc.data,95,axis=0)
magicc_ssp126_pc5 = np.percentile(co2_ssp126_magicc.data,5,axis=0)

magicc_ssp119_mmm = np.mean(co2_ssp119_magicc.data,axis=0)
magicc_ssp119_pc95 = np.percentile(co2_ssp119_magicc.data,95,axis=0)
magicc_ssp119_pc5 = np.percentile(co2_ssp119_magicc.data,5,axis=0)

magicc_ssp245_mmm = np.mean(co2_ssp245_magicc.data,axis=0)
magicc_ssp245_pc95 = np.percentile(co2_ssp245_magicc.data,95,axis=0)
magicc_ssp245_pc5 = np.percentile(co2_ssp245_magicc.data,5,axis=0)

magicc_ssp534_mmm = np.mean(co2_ssp534_magicc.data,axis=0)
magicc_ssp534_pc95 = np.percentile(co2_ssp534_magicc.data,95,axis=0)
magicc_ssp534_pc5 = np.percentile(co2_ssp534_magicc.data,5,axis=0)

magicc_ssp370_mmm = np.mean(co2_ssp370_magicc.data,axis=0)
magicc_ssp370_pc95 = np.percentile(co2_ssp370_magicc.data,95,axis=0)
magicc_ssp370_pc5 = np.percentile(co2_ssp370_magicc.data,5,axis=0)


# multi-model, multi-scenario flux data from Liddicoat et al., 2020
# with grateful acknowledgement to Spencer Liddicoat
# https://journals.ametsoc.org/view/journals/clim/aop/JCLI-D-19-0991.1/JCLI-D-19-0991.1.xml
#

# read in calculated fossil-fuel emissions
# combine fgco2 (ocean flux) and nbp (land flux) into a total

# leading dimension is the year, so crop that off to just leave the flux data

fgco2_ssp119 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp119.txt',skiprows=1).T
nbp_ssp119   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp119.txt',skiprows=1).T
emiss_ssp119 = np.loadtxt('ffEmsHistoricalSsp119_GtCyr.txt',skiprows=1).T
flx_ssp119 = nbp_ssp119[1:] + fgco2_ssp119[1:]
emiss_ssp119 = emiss_ssp119[1:]

fgco2_ssp126 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp126.txt',skiprows=1).T
nbp_ssp126   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp126.txt',skiprows=1).T
flx_ssp126 = nbp_ssp126[1:] + fgco2_ssp126[1:]
emiss_ssp126 = np.loadtxt('ffEmsHistoricalSsp126_GtCyr.txt',skiprows=1).T
emiss_ssp126 = emiss_ssp126[1:]

fgco2_ssp245 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp245.txt',skiprows=1).T
nbp_ssp245   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp245.txt',skiprows=1).T
flx_ssp245 = nbp_ssp245[1:] + fgco2_ssp245[1:]
emiss_ssp245 = np.loadtxt('ffEmsHistoricalSsp245_GtCyr.txt',skiprows=1).T
emiss_ssp245 = emiss_ssp245[1:]

fgco2_ssp534 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp534os.txt',skiprows=1).T
nbp_ssp534   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp534os.txt',skiprows=1).T
flx_ssp534 = nbp_ssp534[1:] + fgco2_ssp534[1:]
emiss_ssp534 = np.loadtxt('ffEmsHistoricalSsp534os_GtCyr.txt',skiprows=1).T
emiss_ssp534 = emiss_ssp534[1:]

fgco2_ssp370 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp370.txt',skiprows=1).T
nbp_ssp370   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp370.txt',skiprows=1).T
flx_ssp370 = nbp_ssp370[1:] + fgco2_ssp370[1:]
emiss_ssp370 = np.loadtxt('ffEmsHistoricalSsp370_GtCyr.txt',skiprows=1).T
emiss_ssp370 = emiss_ssp370[1:]

fgco2_ssp585 = np.loadtxt('global_total_FGCO2_GtC_yr_HistoricalSsp585.txt',skiprows=1).T
nbp_ssp585   = np.loadtxt('global_total_NBP_GtC_yr_HistoricalSsp585.txt',skiprows=1).T
flx_ssp585 = nbp_ssp585[1:] + fgco2_ssp585[1:]
emiss_ssp585 = np.loadtxt('ffEmsHistoricalSsp585_GtCyr.txt',skiprows=1).T
emiss_ssp585 = emiss_ssp585[1:]

y = nbp_ssp585[0]

# insert leading 0 as emissions data runs from 1851
emiss_ssp119 = np.insert(emiss_ssp119, 0, 0, axis=1)
emiss_ssp126 = np.insert(emiss_ssp126, 0, 0, axis=1)
emiss_ssp245 = np.insert(emiss_ssp245, 0, 0, axis=1)
emiss_ssp534 = np.insert(emiss_ssp534, 0, 0, axis=1)
emiss_ssp370 = np.insert(emiss_ssp370, 0, 0, axis=1)
emiss_ssp585 = np.insert(emiss_ssp585, 0, 0, axis=1)

flx_mmm = dict([('ssp119', np.mean(flx_ssp119,axis=0)), ('ssp126', np.mean(flx_ssp126,axis=0)),
             ('ssp245', np.mean(flx_ssp245,axis=0)), ('ssp534', np.mean(flx_ssp534,axis=0)), ('ssp370', np.mean(flx_ssp370,axis=0)),
             ('ssp585', np.mean(flx_ssp585,axis=0))])

flx_pc5 = dict([('ssp119', np.percentile(flx_ssp119,5,axis=0)), ('ssp126', np.percentile(flx_ssp126,5,axis=0)),
             ('ssp245', np.percentile(flx_ssp245,5,axis=0)), ('ssp534', np.percentile(flx_ssp534,5,axis=0)), ('ssp370', np.percentile(flx_ssp370,5,axis=0)),
             ('ssp585', np.percentile(flx_ssp585,5,axis=0))])
flx_pc95 = dict([('ssp119', np.percentile(flx_ssp119,95,axis=0)), ('ssp126', np.percentile(flx_ssp126,95,axis=0)),
             ('ssp245', np.percentile(flx_ssp245,95,axis=0)), ('ssp534', np.percentile(flx_ssp534,95,axis=0)), ('ssp370', np.percentile(flx_ssp370,95,axis=0)),
             ('ssp585', np.percentile(flx_ssp585,95,axis=0))])


# get data to 2300 from 4 ESMs (CanESM5, IPSL, UKESM, CESM2):

year,c5_ssp126,c5_ssp534,c5_ssp585 = np.loadtxt('CanESM5_nbp.dat').T
year,i6_ssp126,i6_ssp534,i6_ssp585 = np.loadtxt('IPSL-CM6A-LR_nbp.dat').T
year,uk_ssp126,uk_ssp534,uk_ssp585 = np.loadtxt('UKESM1-0-LL_nbp.dat').T
year,ce2_ssp126,ce2_ssp534,ce2_ssp585 = np.loadtxt('CESM2-WACCM_nbp.dat').T

year,c5_ocn_ssp126,c5_ocn_ssp534,c5_ocn_ssp585 = np.loadtxt('CanESM5_fgco2.dat').T
year,i6_ocn_ssp126,i6_ocn_ssp534,i6_ocn_ssp585 = np.loadtxt('IPSL-CM6A-LR_fgco2.dat').T
year,uk_ocn_ssp126,uk_ocn_ssp534,uk_ocn_ssp585 = np.loadtxt('UKESM1-0-LL_fgco2.dat').T
year,ce2_ocn_ssp126,ce2_ocn_ssp534,ce2_ocn_ssp585 = np.loadtxt('CESM2-WACCM_fgco2.dat').T


flx_2300_ssp126 = [
    [c5_ssp126 + c5_ocn_ssp126],
    [i6_ssp126 + i6_ocn_ssp126],
    [uk_ssp126 + uk_ocn_ssp126],
    [ce2_ssp126 + ce2_ocn_ssp126]
]

flx_2300_ssp534 = [
    [c5_ssp534 + c5_ocn_ssp534],
    [i6_ssp534 + i6_ocn_ssp534],
    [uk_ssp534 + uk_ocn_ssp534],
    [ce2_ssp534 + ce2_ocn_ssp534]
]

flx_2300_ssp585 = [
    [c5_ssp585 + c5_ocn_ssp585],
    [i6_ssp585 + i6_ocn_ssp585],
    [uk_ssp585 + uk_ocn_ssp585],
    [ce2_ssp585 + ce2_ocn_ssp585]
]


data_2300 = dict([('ssp126', flx_2300_ssp126),
             ('ssp534', flx_2300_ssp534),
             ('ssp585', flx_2300_ssp585)])


# calculate multi-model mean and 5-95%
#

ssp126_2300_mmm = np.mean(flx_2300_ssp126,axis=0)[0]
ssp126_2300_pc95 = np.percentile(flx_2300_ssp126,95,axis=0)[0]
ssp126_2300_pc5  = np.percentile(flx_2300_ssp126,5,axis=0)[0]

ssp534_2300_mmm = np.mean(flx_2300_ssp534,axis=0)[0]
ssp534_2300_pc95 = np.percentile(flx_2300_ssp534,95,axis=0)[0]
ssp534_2300_pc5  = np.percentile(flx_2300_ssp534,5,axis=0)[0]

ssp585_2300_mmm = np.mean(flx_2300_ssp585,axis=0)[0]
ssp585_2300_pc95 = np.percentile(flx_2300_ssp585,95,axis=0)[0]
ssp585_2300_pc5  = np.percentile(flx_2300_ssp585,5,axis=0)[0]


# calculate cumulative fluxes from annuals
#

flx_cum_ssp119 = np.cumsum(flx_ssp119, axis=1)
flx_cum_ssp126 = np.cumsum(flx_ssp126, axis=1)
flx_cum_ssp245 = np.cumsum(flx_ssp245, axis=1)
flx_cum_ssp534 = np.cumsum(flx_ssp534, axis=1)
flx_cum_ssp370 = np.cumsum(flx_ssp370, axis=1)
flx_cum_ssp585 = np.cumsum(flx_ssp585, axis=1)

flx_cum_mmm = dict([('ssp119', np.mean(flx_cum_ssp119,axis=0)), ('ssp126', np.mean(flx_cum_ssp126,axis=0)),
             ('ssp245', np.mean(flx_cum_ssp245,axis=0)), ('ssp534', np.mean(flx_cum_ssp534,axis=0)), ('ssp370', np.mean(flx_cum_ssp370,axis=0)),
             ('ssp585', np.mean(flx_cum_ssp585,axis=0))])

flx_cum_pc5 = dict([('ssp119', np.percentile(flx_cum_ssp119,5,axis=0)), ('ssp126', np.percentile(flx_cum_ssp126,5,axis=0)),
             ('ssp245', np.percentile(flx_cum_ssp245,5,axis=0)), ('ssp534', np.percentile(flx_cum_ssp534,5,axis=0)), ('ssp370', np.percentile(flx_cum_ssp370,5,axis=0)),
             ('ssp585', np.percentile(flx_cum_ssp585,5,axis=0))])

flx_cum_pc95 = dict([('ssp119', np.percentile(flx_cum_ssp119,95,axis=0)), ('ssp126', np.percentile(flx_cum_ssp126,95,axis=0)),
             ('ssp245', np.percentile(flx_cum_ssp245,95,axis=0)), ('ssp534', np.percentile(flx_cum_ssp534,95,axis=0)), ('ssp370', np.percentile(flx_cum_ssp370,95,axis=0)),
             ('ssp585', np.percentile(flx_cum_ssp585,95,axis=0))])


# to calculate sink fractions need to account for land use
# so add land-use to top and bottom of the fraction so instead of nbp/fossil, get nep/total-emiss
#

# use the scenarios data
# data from: https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=50

'''
Data is from the SSP scenarios: Riahi, K. et al., 2017, DOI:110.1016/j.gloenvcha.2016.05.009 
For more details see:
SSP1: van Vuuren, D.P. et al., 2017, DOI:10.1016/j.gloenvcha.2016.05.008 
SSP2: Fricko, O. et al., 2017, DOI:10.1016/j.gloenvcha.2016.06.004 
SSP3: Fujimori, S. et al., 2017, DOI:10.1016/j.gloenvcha.2016.06.009 
SSP5: Kriegler, E. et al., 2017, DOI:10.1016/j.gloenvcha.2016.05.015 
Land-use: Popp, A. et al, 2017, DOI:10.1016/j.gloenvcha.2016.2016.10.002
'''

ssp370_LU = [0.959301818, 1.056843235, 0.959464809, 0.862338354, 0.78794353, 0.857603663, 0.831412897, 0.7754469, 0.699528109, 0.724396664]
ssp119_LU = [0.959301818, 0.866072041, 0.101543745, 0.377358673, -0.222296673, -0.406504146, -0.499712372, -0.578721769, -0.606262542, -0.649481884]
ssp126_LU = [0.959301818, 0.866817094, 0.05128979, -0.105763342, -0.479624451, -0.705440587, -0.704718662, -0.664609591, -0.568549256, -0.790646116]
ssp245_LU = [0.959301818, 0.888927545, 0.785832615, 0.590266856, 0.136613758, -0.419976886, -0.603051387, -0.926548596, -1.177396938, -1.309111901]
ssp585_LU = [0.959301818, 1.077187122, 1.240056188, 0.937018695, 0.55990575, 0.038017088, -0.062708387, -0.040323327, -0.135100418, -0.417359264]
ssp534_LU = [0.959301818, 1.077263489, 1.240992571, 0.936726687, 0.75137482, 1.301441248, 0.68207744, 0.246490909, 0.015850909, -0.218427273]

y_LU = [2015,2020,2030,2040,2050,2060,2070,2080,2090,2100]


# historical land-use data created by Julia Pongratz, and available here:
# http://c4mip.net/cmip6-experiments
# c4mip.net/fileadmin/user_upload/c4mip/CMIP6_C4MIP_landuse_emissions.nc.gz

LU_hist = iris.load('/data/users/hadcn/CMIP6_C4MIP_landuse_emissions.nc')[0]

# account for different units and interpolate to annual timesteps
#
y_lu = np.concatenate([np.arange(1850,2015), np.arange(2015,2101,1)])
ssp370_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp370_LU)])
ssp119_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp119_LU)])
ssp126_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp126_LU)])
ssp245_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp245_LU)])
ssp585_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp585_LU)])
ssp534_lu = np.concatenate([LU_hist.data*1e-12, np.interp(np.arange(2015,2101,1), y_LU, ssp534_LU)])


# calculate sink-fraction with LU included
#

flxnep_ssp370 = ssp370_lu + flx_ssp370
flxnep_cum_ssp370 = np.cumsum(flxnep_ssp370, axis=1)
emisstot_cum_ssp370 = np.cumsum(emiss_ssp370 + ssp370_lu, axis=1)
sink_fractot_ssp370 = flxnep_cum_ssp370 / emisstot_cum_ssp370

flxnep_ssp119 = ssp119_lu + flx_ssp119
flxnep_cum_ssp119 = np.cumsum(flxnep_ssp119, axis=1)
emisstot_cum_ssp119 = np.cumsum(emiss_ssp119 + ssp119_lu, axis=1)
sink_fractot_ssp119 = flxnep_cum_ssp119 / emisstot_cum_ssp119

flxnep_ssp126 = ssp126_lu + flx_ssp126
flxnep_cum_ssp126 = np.cumsum(flxnep_ssp126, axis=1)
emisstot_cum_ssp126 = np.cumsum(emiss_ssp126 + ssp126_lu, axis=1)
sink_fractot_ssp126 = flxnep_cum_ssp126 / emisstot_cum_ssp126

flxnep_ssp245 = ssp245_lu + flx_ssp245
flxnep_cum_ssp245 = np.cumsum(flxnep_ssp245, axis=1)
emisstot_cum_ssp245 = np.cumsum(emiss_ssp245 + ssp245_lu, axis=1)
sink_fractot_ssp245 = flxnep_cum_ssp245 / emisstot_cum_ssp245

flxnep_ssp585 = ssp585_lu + flx_ssp585
flxnep_cum_ssp585 = np.cumsum(flxnep_ssp585, axis=1)
emisstot_cum_ssp585 = np.cumsum(emiss_ssp585 + ssp585_lu, axis=1)
sink_fractot_ssp585 = flxnep_cum_ssp585 / emisstot_cum_ssp585

flxnep_ssp534 = ssp534_lu + flx_ssp534
flxnep_cum_ssp534 = np.cumsum(flxnep_ssp534, axis=1)
emisstot_cum_ssp534 = np.cumsum(emiss_ssp534 + ssp534_lu, axis=1)
sink_fractot_ssp534 = flxnep_cum_ssp534 / emisstot_cum_ssp534


sink_fractot_mmm = dict([('ssp119', np.mean(sink_fractot_ssp119,axis=0)), ('ssp126', np.mean(sink_fractot_ssp126,axis=0)),
             ('ssp245', np.mean(sink_fractot_ssp245,axis=0)), ('ssp370', np.mean(sink_fractot_ssp370,axis=0)),
             ('ssp534', np.mean(sink_fractot_ssp534,axis=0)), ('ssp585', np.mean(sink_fractot_ssp585,axis=0))])

sink_fractot_pc5 = dict([('ssp119', np.percentile(sink_fractot_ssp119,5,axis=0)), ('ssp126', np.percentile(sink_fractot_ssp126,5,axis=0)),
             ('ssp245', np.percentile(sink_fractot_ssp245,5,axis=0)), ('ssp370', np.percentile(sink_fractot_ssp370,5,axis=0)),
             ('ssp534', np.percentile(sink_fractot_ssp534,5,axis=0)), ('ssp585', np.percentile(sink_fractot_ssp585,5,axis=0))])

sink_fractot_pc95 = dict([('ssp119', np.percentile(sink_fractot_ssp119,95,axis=0)), ('ssp126', np.percentile(sink_fractot_ssp126,95,axis=0)),
             ('ssp245', np.percentile(sink_fractot_ssp245,95,axis=0)), ('ssp370', np.percentile(sink_fractot_ssp370,95,axis=0)),
             ('ssp534', np.percentile(sink_fractot_ssp534,95,axis=0)), ('ssp585', np.percentile(sink_fractot_ssp585,95,axis=0))])


# beta / gamma maps
# with grateful acknowledgement to Charlie Koven, data used in chpater 5, figure 5.27
#
'''
for data and notebook, see:
https://github.com/ckoven/cmip6_beta_gamma_maps/blob/master/cmip6_beta_gamma_maps.ipynb
doi 10.5281/zenodo.6039693 
'''

cubes = iris.load('carbon_feedback_parameters.nc')

beta  = cubes.extract('beta_ensmean')[0]
gamma = cubes.extract('gamma_ensmean')[0]

beta_agr  = cubes.extract('beta_fraction_sign_agreement')[0]
gamma_agr = cubes.extract('gamma_fraction_sign_agreement')[0]

zon_beta_land_av  = cubes.extract('beta_land_zonalmean_ensmean')[0]
zon_beta_ocn_av  = cubes.extract('beta_ocean_zonalmean_ensmean')[0]
zon_gamma_land_av  = cubes.extract('gamma_land_zonalmean_ensmean')[0]
zon_gamma_ocn_av  = cubes.extract('gamma_ocean_zonalmean_ensmean')[0]

zon_beta_land_std  = cubes.extract('beta_land_zonalmean_ensstd')[0]
zon_beta_ocn_std  = cubes.extract('beta_ocean_zonalmean_ensstd')[0]
zon_gamma_land_std  = cubes.extract('gamma_land_zonalmean_ensstd')[0]
zon_gamma_ocn_std  = cubes.extract('gamma_ocean_zonalmean_ensstd')[0]

for c in [beta, gamma, beta_agr, gamma_agr]:
    c.coord('lat').rename('latitude')
    c.coord('lon').rename('longitude')

beta_levs = np.linspace(-.02,.02,16)
beta_cmap = plt.cm.get_cmap('PiYG')

gamma_levs = np.linspace(-1.2,1.2,16)
gamma_cmap = plt.cm.get_cmap('PiYG')

lat = zon_beta_land_av.coord('lat').points

# plot the figure
#

fig = plt.figure(figsize=(20,30))

spec_1 = gridspec.GridSpec(ncols=4, nrows=4, width_ratios = [1,4,4,1], wspace=0.01)
spec_2 = gridspec.GridSpec(ncols=2, nrows=4, width_ratios = [2,1], wspace=0)

spec_1b = gridspec.GridSpec(ncols=4, nrows=4, width_ratios = [1,2,2,1])

# set all lines to True, but can be configured to select subset
plot_data = dict([('hist', True), ('ssp119', True), ('ssp126', True),
             ('ssp245', True), ('ssp534', True), ('ssp370', True),
             ('ssp585', True)])

# top row
# grid spec positions:

ax1 = fig.add_axes([0.11, .745, .08, .11])
ax4 = fig.add_axes([0.81, .745, .08, .11])

# second row
ax5 = fig.add_subplot(spec_2[1,0])

# third row
ax6 = fig.add_subplot(spec_2[2,0])
ax7 = fig.add_subplot(spec_2[2,1])

#fourth row
ax8 = fig.add_subplot(spec_2[3,0])
ax8b = fig.add_subplot(spec_2[3,1])


# hide various axes, set ticks etc
axes=[ax1,ax4,ax5,ax6,ax7,ax8,ax8b]

for ax in axes:
    ax.tick_params(labelsize=15)
    for z in ['top', 'right']:
        ax.spines[z].set_visible(False)

for ax in [ax4,ax7,ax8b]:
    ax.tick_params(labelsize=15)
    for z in ['left']:
        ax.spines[z].set_visible(False)

ax4.spines['right'].set_visible(True)
ax8b.spines['bottom'].set_visible(False)
        
ax8b.axes.get_yaxis().set_visible(False)
ax8b.axes.get_xaxis().set_visible(False)

ax7.axes.get_yaxis().set_visible(False)

# manual intervention on ticks:
ax1.set_xticks([0,.1,.2])
ax1.set_yticks(np.arange(-90,120,30))

ax4.set_xticks([-20,-10,0,10])
ax4.set_yticks(np.arange(-90,120,30))

ax6.set_yticks(np.arange(-4,16,2))

ax7.set_xticks([2150,2200,2250,2300])

######
#
# panels a-d
#

ax1.plot(zon_beta_land_av.data, lat, 'g')
ax1.plot(zon_beta_ocn_av.data, lat, 'b')
ax1.fill_betweenx(lat,zon_beta_land_av.data-zon_beta_land_std.data, zon_beta_land_av.data+zon_beta_land_std.data,
                  facecolor='g',alpha=0.2)
ax1.fill_betweenx(lat,zon_beta_ocn_av.data-zon_beta_ocn_std.data, zon_beta_ocn_av.data+zon_beta_ocn_std.data,
                  facecolor='b',alpha=0.2)
ax1.set_xlim(-.02,.3)
ax1.set_ylim(-95,95)
ax1.set_title('                  (a, b) Carbon uptake response to CO$_2$', fontsize=20)
ax1.set_xlabel('10$^6$ kg C m$^{-1}$ ppm$^{-1}$', fontsize=16)
ax1.set_ylabel('latitude', fontsize=16)
ax1.text(.15,-30,'Land', color='g', fontsize=14)
ax1.text(.15,-50,'Ocean', color='b', fontsize=14)

ax4.plot(zon_gamma_land_av.data, lat, 'g')
ax4.plot(zon_gamma_ocn_av.data, lat, 'b')
ax4.fill_betweenx(lat,zon_gamma_land_av.data-zon_gamma_land_std.data, zon_gamma_land_av.data+zon_gamma_land_std.data,
                  facecolor='g',alpha=0.2)
ax4.fill_betweenx(lat,zon_gamma_ocn_av.data-zon_gamma_ocn_std.data, zon_gamma_ocn_av.data+zon_gamma_ocn_std.data,
                  facecolor='b',alpha=0.2)
ax4.yaxis.tick_right()
ax4.set_ylim(-95,95)
ax4.set_xlabel('10$^6$ kg C m$^{-1}$ $^o$C$^{-1}$', fontsize=16)

for i in np.arange(-75,100,25):
    ax1.hlines(i, -0.01,0.3, 'gray', alpha=0.2)
    ax4.hlines(i, -20,10, 'gray', alpha=0.2)

    
ax2 = fig.add_subplot(spec_1[0,1], projection = ccrs.Robinson(central_longitude= 0))
coldata = iplt.contourf(beta, beta_levs, cmap = beta_cmap, extend='both')
ax_map = plt.gca()
contour_stipple_lo = iplt.contourf(beta_agr,colors='None',levels=[0,.8],hatches=['////'])

ax_map.coastlines()
ax_map.set_xlim(ax_map.projection.x_limits)
ax_map.set_ylim(ax_map.projection.y_limits)

bar_pos = [0.23, 0.725, 0.26, 0.01]  # [left,bottom,width,height]
bar_orientation = "horizontal"     # or "vertical"  or "none" (to skip)
bar_ticklen  = 0
bar_ticklabs = [-.02,-.01,0,.01,.02]
bar_label    = u"kg C m$^{-2}$ ppm$^{-1}$"

bar2_axes = fig.add_axes(bar_pos)
bar2 = fig.colorbar(coldata, cax=bar2_axes,
                   orientation=bar_orientation,
                   drawedges=False, extend='max')

bar2.ax.tick_params(length=bar_ticklen)
bar2.ax.tick_params(labelsize=15)
bar2.set_ticks(bar_ticklabs)
bar2.set_label(bar_label, fontsize=16) 

ax_map.set_xlim(ax_map.projection.x_limits)
ax_map.set_ylim(ax_map.projection.y_limits)


ax3 = fig.add_subplot(spec_1[0,2], projection = ccrs.Robinson(central_longitude= 0))
coldata = iplt.contourf(gamma, gamma_levs, cmap = gamma_cmap, extend='both')
ax_map = plt.gca()
contour_stipple_lo = iplt.contourf(gamma_agr,colors='None',levels=[0,.8],hatches=['////'])

ax_map.coastlines()
ax_map.set_title('(c,d) Carbon uptake response to climate warming', fontsize=20)

bar_label    = u"kg C m$^{-2}$ $^o$C$^{-1}$"

bar_pos = [0.54, 0.725, 0.26, 0.01]  # [left,bottom,width,height]
bar3_axes = fig.add_axes(bar_pos)
bar_ticklabs = [-1, -.5, 0, .5, 1]

bar3 = fig.colorbar(coldata, cax=bar3_axes,
                   orientation=bar_orientation,
                   drawedges=False, extend='min')

bar3.ax.tick_params(length=bar_ticklen)
bar3.ax.tick_params(labelsize=15)
bar3.set_ticks(bar_ticklabs)
bar3.set_label(bar_label, fontsize=16)


######
#
# panel e
#

xr = [1990,2100]

for i in np.arange(300,1200,100):
    ax5.hlines(i, xr[0], xr[1], 'gray', alpha=0.2)
    
for i in data:
    if plot_data[i]: ax5.plot(yr_data[i], data[i], color=col[i], label=lab[i])

ax5.fill_between(y_e,co2_e_pc5,co2_e_pc95, facecolor=col_ssp585,alpha=0.1, label='emiss-driven')
ax5.fill_between(magicc_yr, magicc_ssp126_pc5, magicc_ssp126_pc95, facecolor=col_ssp126,alpha=0.1)
ax5.fill_between(magicc_yr, magicc_ssp119_pc5, magicc_ssp119_pc95, facecolor=col_ssp119,alpha=0.1)
ax5.fill_between(magicc_yr, magicc_ssp245_pc5, magicc_ssp245_pc95, facecolor=col_ssp245,alpha=0.1)
ax5.fill_between(magicc_yr, magicc_ssp534_pc5, magicc_ssp534_pc95, facecolor=col_ssp534,alpha=0.1)
ax5.fill_between(magicc_yr, magicc_ssp370_pc5, magicc_ssp370_pc95, facecolor=col_ssp370,alpha=0.1)

ax5.legend(fontsize=18, loc='upper left', bbox_to_anchor=(1.1,1))

ax5.set_title('(e) CO$_2$ concentration (ppm)', fontsize=24, loc='left')
ax5.set_xlim(xr[0], xr[1])
ax5.set_ylim(300,1200)

ax5.text(1995,1110,'10', fontsize=18, color=col['ssp585'])

for axes in [ax5,ax6,ax7,ax8]:
    axes.tick_params(labelsize=18)


######
#
# panel f
#

xr2300 = [2100,2300]

for i in flx_mmm:
    if plot_data[i]:
        ax6.plot(y, flx_mmm[i], color=col[i], label=lab[i])

ax6.fill_between(y, flx_pc5['ssp126'], flx_pc95['ssp126'], facecolor=col['ssp126'], alpha=0.1)
ax6.fill_between(y, flx_pc5['ssp370'], flx_pc95['ssp370'], facecolor=col['ssp370'], alpha=0.1)

for i in np.arange(-4,16,2):
    ax6.hlines(i, xr[0],xr[1], 'gray', alpha=0.2)
    ax7.hlines(i, xr2300[0],xr2300[1], 'gray', alpha=0.2)

ax6.hlines(0, xr[0],xr[1], 'k', alpha=0.5)
ax7.hlines(0, xr2300[0],xr2300[1], 'k', alpha=0.5)
ax7.vlines(2100, -10,20, 'k', linestyle='dashed')

ax6.set_ylim(-5,15)
ax7.set_ylim(-5,15)
ax6.set_xlim(xr[0], xr[1])
ax7.set_xlim(xr2300[0], xr2300[1])

ax7.fill_between(year, smooth(ssp126_2300_pc5,5), smooth(ssp126_2300_pc95,5), facecolor=col['ssp126'], alpha=.1)
ax7.plot(year, ssp126_2300_mmm, col['ssp126'])
ax7.plot(year, ssp534_2300_mmm, col['ssp534'])
ax7.plot(year, ssp585_2300_mmm, col['ssp585'])

ax6.set_title('(f) Net land and ocean carbon fluxes (PgC yr$^{-1}$)', fontsize=24, loc='left')

# print number of models used for each scenario/time period
ax6.text(1995,12.5,'5', fontsize=18, color=col['ssp119'])
ax6.text(1998,12.5,'9', fontsize=18, color=col['ssp126'])
ax6.text(2001,12.5,'9', fontsize=18, color=col['ssp245'])
ax6.text(2004,12.5,'9', fontsize=18, color=col['ssp370'])
ax6.text(2007,12.5,'4', fontsize=18, color=col['ssp534'])
ax6.text(2010,12.5,'9', fontsize=18, color=col['ssp585'])

ax7.text(2120,12.5,'simulations extended to 2300 for:', fontsize=16)
ax7.text(2240,10.5,'SSP5-8.5 [4]', fontsize=18, color=col['ssp585'])
ax7.text(2240,9,'SSP5-3.4-OS [4]', fontsize=18, color=col['ssp534'])
ax7.text(2240,7.5,'SSP1-2.6 [4]', fontsize=18, color=col['ssp126'])


######
#
# panel g
#

for i in sink_fractot_mmm:
    if plot_data[i]:
        ax8.plot(y, sink_fractot_mmm[i], color=col[i], label=lab[i])

ax8.fill_between(y, sink_fractot_pc5['ssp126'], sink_fractot_pc95['ssp126'], facecolor=col['ssp126'], alpha=0.1)
ax8.fill_between(y, sink_fractot_pc5['ssp370'], sink_fractot_pc95['ssp370'], facecolor=col['ssp370'], alpha=0.1)

        
for i in np.arange(0,1,.1):
    ax8.hlines(i, xr[0],xr[1], 'gray', alpha=0.2)

ax8.hlines(0, xr[0],xr[1], 'k', alpha=0.5)

ax8.set_xlim(xr[0],xr[1])
ax8.set_ylim(0.25,.75)

ax8.set_title('(g) Sink fraction', fontsize=24, loc='left')
ax8.set_xlabel('Year', fontsize=24)

ax8.text(1995,.31,'5', fontsize=18, color=col['ssp119'])
ax8.text(1998,.31,'9', fontsize=18, color=col['ssp126'])
ax8.text(2001,.31,'9', fontsize=18, color=col['ssp245'])
ax8.text(2004,.31,'9', fontsize=18, color=col['ssp370'])
ax8.text(2007,.31,'4', fontsize=18, color=col['ssp534'])
ax8.text(2010,.31,'9', fontsize=18, color=col['ssp585'])

ax8b.plot([0])
ax8b.set_xlim(0,10)
ax8b.set_ylim(0,10)
ax8b.arrow(1,9,0,-6,color='gray', head_width=.4)
ax8b.text(2,7.8,'At higher CO$_2$ concentrations,', fontsize=18)
ax8b.text(2,7,'land and ocean carbon stores', fontsize=18)
ax8b.text(2,6.2,'take-up a reduced fraction', fontsize=18)
ax8b.text(2,5.4,'of our emissions,', fontsize=18)
ax8b.text(2,4.6,'despite growing larger', fontsize=18)


plt.savefig('TS.5.png')
