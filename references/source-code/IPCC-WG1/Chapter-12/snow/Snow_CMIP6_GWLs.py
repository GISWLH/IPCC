# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/snow/Snow_CMIP6_GWLs.ipynb

# %% cell 4
# Specify the path to the Global warming levels csv file.
GWL_csv = '/path/CMIP6_Atlas_WarmingLevels.csv'

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
        model = row[0].split('_')[0]
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
list_of_files = glob.glob('[insert the path to the yearly files output by snow_CMIP6.sh]') # File name will be of the form AWI-CM-1-1-MR_85_snw100seas_1980-2100.1deg.nc
list_of_files

# %% cell 10
import os

# %% cell 11
GWL_dict.keys()

# %% cell 12

output_rootdir = '[insert path to directory in which to output the data]'
files_per_GWL = dict()
for GWL in ['1.5','2','3','4']:
    files_per_GWL[GWL] = list()

for wfile in list_of_files:
    #print os.path.basename(wfile)
    filename = os.path.basename(wfile)
    wmodel = filename.split('_')[0]
    scenario = filename.split('_')[1]
    if wmodel in GWL_dict:
        print ('We have : ', wmodel)
        #print (GWL_dict[wmodel])
        for GWL in ['1.5','2','3','4']:
            if scenario=='26': GWL_scenario = GWL+'_ssp126'
            if scenario=='85': GWL_scenario = GWL+'_ssp585'
            
            # --> file nc
            # --> period
            central_year = GWL_dict[wmodel][GWL_scenario]
            if central_year not in ['NA','9999']:
                outfilename = output_rootdir +'/'+ wmodel+'_'+scenario+'_'+GWL+'.nc'
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
