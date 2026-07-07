# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/snow/Snow_NA_CORDEX_GWLs.ipynb

# %% cell 4
# Specify the path to the Global warming levels csv file.
GWL_csv = '/path/CMIP5_Atlas_WarmingLevels.csv'

# %% cell 5
import csv

# %% cell 6
GWL_dict = dict()
i = 0
with open(GWL_csv) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
    for row in spamreader:
        #print(i)
        print(row)
        model = row[0]
        print(model)
        GWL_dict[model] = dict()
        if i==0:
            colnames = row
        j = 1
        for elt in row[1:17]:
            #print(j)
            print (elt)
            GWL_dict[model][colnames[j]] = row[j]
            j = j + 1
        i = i + 1

# %% cell 8
import glob

# %% cell 9
list_of_files = glob.glob('[insert the path to the yearly files output by snow_NA_CORDEX.sh]') # File names will be of the form NAM-22_MOHC_HadGEM2-ES_r1i1p1_GERICS-REMO2015_26_snw100seas_1980-2100_remo22grid.nc
list_of_files

# %% cell 10
import os

# %% cell 11
GWL_dict.keys()

# %% cell 12
#model_scenario_GWL.nc

output_rootdir = '/div/amoc/archive/ciles/IPCC_FGD/snow/NA_CORDEX/GWLs'
files_per_GWL = dict()
for GWL in ['1.5','2','3','4']:
    files_per_GWL[GWL] = list()

for wfile in list_of_files:
    #print os.path.basename(wfile)
    filename = os.path.basename(wfile)
    wmodel = (filename.split('_')[2]+'_'+filename.split('_')[3])
    scenario = filename.split('_')[5]
    RCM = filename.split('_')[4]
    domain=filename.split('_')[0]
    if wmodel in GWL_dict:
        print ('We have : ', wmodel)
        #print (GWL_dict[wmodel])
        for GWL in ['1.5','2','3','4']:
            if scenario=='26': GWL_scenario = GWL+'_rcp26'
            if scenario=='85': GWL_scenario = GWL+'_rcp85'
            
            # --> file nc
            # --> period
            central_year = GWL_dict[wmodel][GWL_scenario]
            if central_year not in ['NA','9999']:
                outfilename = output_rootdir +'/'+ domain+'_'+ wmodel+'_'+ RCM +'_'+scenario+'_GWL'+GWL+'_snw100seas_remo22grid.nc'
                start_year = str( int(central_year)-9 )
                end_year = str( int(central_year)+10 )
                cmd = 'cdo timavg -selyear,'+start_year+'/'+end_year+' '+wfile+' '+outfilename
                #print (cmd)
                os.system(cmd)
                files_per_GWL[GWL].append(outfilename) 
    else:
        print ('We dont have GWL info for ',wmodel)

# %% cell 13
#testing
files_per_GWL['1.5']
