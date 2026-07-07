# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/wind_satellites/Prepare_CORDEX_files_for_regional_averages.ipynb

# %% cell 2
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 4
# -- Function to split a multi-member file in individual files
# -- Uses Xarray
def split_ensemble_file(ensemble_file, output_pattern, variable):
    if not os.path.isdir(os.path.dirname(output_pattern)):
        os.makedirs(os.path.dirname(output_pattern))
    import xarray as xr
    dat = xr.open_dataset(ensemble_file)[variable]
    for member in dat.member:
        member_name = str(member.values)
        print member_name
        outfilename = output_pattern+member_name+'.nc'
        if not os.path.isfile(outfilename):
            print 'Save '+outfilename
            member_dat = dat.loc[:,member_name,:,:]
            member_dat.to_netcdf(outfilename)
        else:
            print outfilename+' already exists'

# %% cell 5
variable='wind'
CORDEX_domains = [
    # -- Africa
    'AFR',
    # -- AustralAsia
    'AUS',
    # -- Central America
    'CAM',
    # -- North America
    'NAM',
    # -- South America
    'SAM',
    # -- Asia
    'EAS',
    'WAS',
    'SEA',
    # -- Europe
    #'EUR-11',
    
]
# -- Compute the annual sums
exp_list = [
    dict(experiment='historical',
         years = range(1971,2006)),
    dict(experiment='rcp85',
         years = range(2006,2101)),
    dict(experiment='rcp26',
         years = range(2006,2101))
]
for CORDEX_domain in CORDEX_domains:
    for exp_dict in exp_list:
        years = exp_dict['years']
        experiment = exp_dict['experiment']
        for year in years:
            wfile = '/data/jservon/IPCC/wind/CORDEX_wind/CORDEX-'+CORDEX_domain+'_'+experiment+'_sfcWind/'+CORDEX_domain+'-22_'+experiment+'_'+variable+'_'+str(year)+'.nc4'
            output_pattern = '/data/jservon/IPCC/wind/CORDEX_individual_models/CORDEX-'+CORDEX_domain+'_'+experiment+'_'+variable+'_'+str(year)+'_'
            split_ensemble_file(wfile, output_pattern, variable)
#

# %% cell 6
!ls /data/jservon/IPCC/tx35/bias_corrected/CORDEX-EAS_rcp85_tx35isimip/EAS-22_rcp85_tx35isimip_*
