# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/SM_satellites/Compute_CMIP6_time_averages_GWLs_on_regional_averages_MathiasHauser.ipynb

# %% cell 3
import xarray as xr
import glob, os
import numpy as np
import csv

# %% cell 5
def retrieve_AR6regions():

    regions_filename='/home/jservon/Chapter12_IPCC/scripts/ATLAS/reference-regions/IPCC-WGI-reference-regions-v4_coordinates.csv'

    # -- Store the informations by region in the 'regions' dictionary
    regions = dict()
    with open(regions_filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
        for row in spamreader:
            #if row[0]==region_name:
            print row[2]
            regions[row[2]]=row[3]
    #
    return regions
regions = retrieve_AR6regions()

# %% cell 8
# -- List all the files and retrieve the models and realization
# -- Extract the period and compute the average => cdo timavg -seldate
# -- 
exp_list = [
    dict(experiment='historical',
         period = '1995-2014'),
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2041-2060'),
]

# %% cell 9
models_per_exp = dict()
regional_averages = dict()
regional_averages_for_diff = dict()
for exp in exp_list:
    
    scenario = exp['experiment']
    period = exp['period']
    start_year = period.split('-')[0]
    end_year = period.split('-')[1]
    clim_period = scenario+'_'+period
    
    models_per_exp[clim_period] = dict()
    #regional_averages[clim_period] = dict()
    #regional_averages_for_diff[clim_period] = dict()
    
    #for long_region_name  in regions:
    #    regional_averages[clim_period][regions[long_region_name]] = []
    #    regional_averages_for_diff[clim_period][regions[long_region_name]] = []
    #
    # -- Get the list of files for the experiment / clim_period
    search_pattern = '/data/jservon/IPCC/mrso/tmp_20210225/data.iac.ethz.ch/IPCC_AR6/for_ch12/cmip6/mrso/sm_annmean_reg_ave_ar6/sm_annmean_reg_ave_ar6_mrso_Lmon_*_'+scenario+'_*.nc'
    lof = glob.glob(search_pattern)
    list_of_models = []
    list_of_files = []
    for wfile in lof:

        # -- Extract period and compute average
        outdir = '/data/jservon/IPCC/mrso/averages_over_periods/'
        # -- Create the output filename
        ncfilename = os.path.basename(wfile)
        outfilename = outdir+ncfilename.replace('.nc','_clim-'+start_year+'-'+end_year+'.nc')
        dum = ncfilename.split('_')
        wmodel = dum[7]
        models_per_exp[clim_period][wmodel] = outfilename
        
        # -- Select the period and compute the time average with cdo
        cmd = 'cdo timavg -selyear,'+start_year+'/'+end_year+' '+wfile+' '+outfilename
        #os.system(cmd)

# %% cell 10
models_per_exp['historical_1995-2014'].keys()

# %% cell 11
# Pour chaque scenario futur, il me faut l'équivalent historical

# Boucle sur les scenarios futurs

# %% cell 12
# Sauvegarder les resultats en bruts en difference

# %% cell 14
for exp in ['historical_1995-2014',
            'ssp126_2041-2060',
            'ssp126_2081-2100',
            'ssp585_2041-2060',
            'ssp585_2081-2100']:
    regional_averages[exp] = dict()
    for long_region_name in regions:
        regional_averages[exp][regions[long_region_name]] = []
    # -- For each future clim period, we loop on all the models availables
    for model in models_per_exp[exp]:
        # -- Raw values
        # ------------------------------------------------------------------
        # -- Get the data with Xarray for the future time slice
        wfile_exp = models_per_exp[exp][model]
        dum = xr.open_dataset(wfile_exp)
        dat = dum['mrso']
        region_names = list(dum['names'].values)

        # -- Loop on the regional averages available in the file
        for region_name in region_names:
            if region_name in regions:
                shortname = regions[region_name]
                ind = region_names.index(region_name)
                value = float(dat[0][ind].values)
                regional_averages[exp][shortname].append( value )

# %% cell 15
## Gather the data to compute the differences model by model

# %% cell 16
# -- Loop on the time periods
for exp in ['ssp126_2041-2060', 'ssp126_2081-2100','ssp585_2041-2060','ssp585_2081-2100']:
    regional_averages_for_diff[exp] = dict()
    regional_averages_for_diff[exp+'_historical_1995-2014'] = dict()
    for long_region_name in regions:
        regional_averages_for_diff[exp][regions[long_region_name]] = []
        regional_averages_for_diff[exp+'_historical_1995-2014'][regions[long_region_name]] = []


    # -- Differences
    # ------------------------------------------------------------------
    # -- For each future clim period, we loop on all the models availables
    for model in models_per_exp[exp]:
        # -- And if the model is also available for baseline, we keep going
        if model in models_per_exp['historical_1995-2014']:
            wfile_baseline = models_per_exp['historical_1995-2014'][model]
            wfile_exp = models_per_exp[exp][model]

            # -- Get the data with Xarray for the future time slice
            dum = xr.open_dataset(wfile_exp)
            dat = dum['mrso']
            region_names = list(dum['names'].values)

            # -- Loop on the regional averages available in the file
            for region_name in region_names:
                if region_name in regions:
                    shortname = regions[region_name]
                    ind = region_names.index(region_name)
                    value = float(dat[0][ind].values)
                    regional_averages_for_diff[exp][shortname].append( value )            

            # -- Get the data for the baseline
            dum = xr.open_dataset(wfile_baseline)
            dat = dum['mrso']
            region_names = list(dum['names'].values)

            # -- Short name
            for region_name in region_names:
                if region_name in regions:
                    shortname = regions[region_name]
                    ind = region_names.index(region_name)
                    value = float(dat[0][ind].values)
                    regional_averages_for_diff[exp+'_historical_1995-2014'][shortname].append( value )

# %% cell 17
regional_averages_for_diff['ssp126_2041-2060_historical_1995-2014']

# %% cell 19
GWL_csv = '/home/jservon/Chapter12_IPCC/scripts/ATLAS/warming-levels/CMIP6_Atlas_WarmingLevels.csv'

GWL_dict = dict()
i = 0
with open(GWL_csv) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
    for row in spamreader:
        print row
        model = row[0]#.split('_')[0]
        print model
        GWL_dict[model] = dict()
        if i==0:
            colnames = row
        j = 1
        for elt in row[1:len(row)]:
            print elt
            GWL_dict[model][colnames[j]] = row[j]
            j = j + 1
        i = i + 1

# %% cell 20
list_of_GWLs = ['1.5','2','3','4']

#files_per_GWL = dict()
#for GWL in ['1.5','2']:
#    files_per_GWL[GWL] = dict()
req_dict = dict(project='CMIP6',
                table='Amon'
               )

models_per_GWL = dict()
for GWL in list_of_GWLs:
    models_per_GWL[GWL] = dict()
    #regional_averages[GWL] = dict()
    #regional_averages[GWL+'_historical_1995-2014'] = dict()
    #for long_region_name  in regions:
    #    regional_averages[GWL][regions[long_region_name]] = []
    #    #regional_averages[GWL+'_historical_1995-2014'][regions[long_region_name]] = []

        
#
#Pour Chaque GWL, je garde le model_realization_scenario dans lequel je mets le path vers le fichier
for scenario in ['26','85']:

    if scenario=='26': req_scenario = 'ssp126'
    if scenario=='85': req_scenario = 'ssp585'

    search_pattern = '/data/jservon/IPCC/mrso/tmp_20210225/data.iac.ethz.ch/IPCC_AR6/for_ch12/cmip6/mrso/sm_annmean_reg_ave_ar6/sm_annmean_reg_ave_ar6_mrso_Lmon_*_'+req_scenario+'_*.nc'
    lof = glob.glob(search_pattern)
    for wfile in lof:
        dum = os.path.basename(wfile).split('_')
        wmodel = dum[7]
        wrealization = dum[9]
        print wmodel, wrealization
        wmodel_realization = wmodel+'_'+wrealization
        if wmodel_realization in GWL_dict:
            print 'We have : ', wmodel_realization
            print GWL_dict[wmodel_realization]
            for GWL in list_of_GWLs:
                if scenario=='26': GWL_scenario = GWL+'_ssp126'
                if scenario=='85': GWL_scenario = GWL+'_ssp585'

                # --> file nc
                # --> period
                central_year = GWL_dict[wmodel_realization][GWL_scenario]
                if central_year not in ['NA','9999']:
                    start_year = str( int(central_year)-9 )
                    end_year = str( int(central_year)+10 )
                #
                ncfilename = os.path.basename(wfile)
                outfilename = outdir+ncfilename.replace('.nc','_clim-GWL'+GWL+'.nc')
                cmd = 'cdo timavg -selyear,'+start_year+'/'+end_year+' '+wfile+' '+outfilename
                #os.system(cmd)
                
                models_per_GWL[GWL][wmodel_realization+'_'+scenario] = outfilename

# %% cell 22
for GWL in list_of_GWLs:
    regional_averages[GWL] = dict()
    for long_region_name in regions:
        regional_averages[GWL][regions[long_region_name]] = []
    # -- For each future clim period, we loop on all the models availables
    for model in models_per_GWL[GWL]:
        # -- Raw values
        # ------------------------------------------------------------------
        # -- Get the data with Xarray for the future time slice
        wfile_exp = models_per_GWL[GWL][model]
        dum = xr.open_dataset(wfile_exp)
        dat = dum['mrso']
        region_names = list(dum['names'].values)

        # -- Loop on the regional averages available in the file
        for region_name in region_names:
            if region_name in regions:
                shortname = regions[region_name]
                ind = region_names.index(region_name)
                value = float(dat[0][ind].values)
                regional_averages[GWL][shortname].append( value )

# %% cell 24
for GWL in list_of_GWLs:
    print 'GWL = ', GWL
    regional_averages_for_diff[GWL] = dict()
    regional_averages_for_diff[GWL+'_historical_1995-2014'] = dict()
    for long_region_name in regions:
        regional_averages_for_diff[GWL][regions[long_region_name]] = []
        regional_averages_for_diff[GWL+'_historical_1995-2014'][regions[long_region_name]] = []
    
    for model in models_per_GWL[GWL]:
        wmodel = model.split('_')[0]
        if wmodel in models_per_exp['historical_1995-2014']:
            wfile_baseline = models_per_exp['historical_1995-2014'][wmodel]
            wfile_exp = models_per_GWL[GWL][model]
            
            # -- Get the data with Xarray
            dum = xr.open_dataset(wfile_exp)
            dat = dum['mrso']
            region_names = list(dum['names'].values)

            # -- Short name
            for region_name in region_names:
                if region_name in regions:
                    shortname = regions[region_name]
                    ind = region_names.index(region_name)
                    value = float(dat[0][ind].values)
                    regional_averages_for_diff[GWL][shortname].append( value )            

            # -- Get the data with Xarray
            dum = xr.open_dataset(wfile_baseline)
            dat = dum['mrso']
            region_names = list(dum['names'].values)

            # -- Short name
            for region_name in region_names:
                if region_name in regions:
                    shortname = regions[region_name]
                    ind = region_names.index(region_name)
                    value = float(dat[0][ind].values)
                    regional_averages_for_diff[GWL+'_historical_1995-2014'][shortname].append( value )

# %% cell 26
quantiles_dict = dict()
for clim_period in regional_averages:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages[clim_period]:
        print clim_period, region_name
        if regional_averages[clim_period][region_name]:
            dat = np.array(regional_averages[clim_period][region_name])
            q10 = np.quantile(dat, 0.1)
            q50 = np.quantile(dat, 0.5)
            q90 = np.quantile(dat, 0.9)
            quantiles_dict[clim_period][region_name] = [q10, q50, q90]
import json
ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/SM_satellites/'+ensemble+'_SM_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 27
quantiles_dict = dict()
for clim_period in regional_averages_for_diff:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_for_diff[clim_period]:
        print clim_period, region_name
        if regional_averages_for_diff[clim_period][region_name]:
            if 'historical_1995-2014' not in clim_period:
                baseline = np.array(regional_averages_for_diff[clim_period+'_historical_1995-2014'][region_name])
                dat = np.array(regional_averages_for_diff[clim_period][region_name])
                q10 = np.quantile(dat-baseline, 0.1)
                q50 = np.quantile(dat-baseline, 0.5)
                q90 = np.quantile(dat-baseline, 0.9)
                quantiles_dict[clim_period][region_name] = [q10, q50, q90]
import json
ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/SM_satellites/'+ensemble+'_SM_diff_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 28
quantiles_dict = dict()
for clim_period in regional_averages_for_diff:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_for_diff[clim_period]:
        print clim_period, region_name
        if regional_averages_for_diff[clim_period][region_name]:
            if 'historical_1995-2014' not in clim_period:
                baseline = np.array(regional_averages_for_diff[clim_period+'_historical_1995-2014'][region_name])
                dat = np.array(regional_averages_for_diff[clim_period][region_name])
                q10 = np.quantile(((dat-baseline)/baseline)*100, 0.1)
                q50 = np.quantile(((dat-baseline)/baseline)*100, 0.5)
                q90 = np.quantile(((dat-baseline)/baseline)*100, 0.9)
                quantiles_dict[clim_period][region_name] = [q10, q50, q90]
import json
ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/SM_satellites/'+ensemble+'_SM_diff_perc2020_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)
