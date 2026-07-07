#!/bin/bash

# Generates data for a panel for figure BoxTS-12 in the IPCC Working
# Group I Contribution to the Sixth Assessment Report Technical
# Summary. The panel shows rate of change of precipitation and runoff
# with warming, for the extratropics

# It also needs a dictionnary of available CMIP6 datasets versions; a
# version of such a dictionnary is provided in sibling directory
# data/, and is valid for the data available on the ESPRI platform.

# Creator : Stéphane Sénési stejase@laposte.net
# Version date : 20210328

# This script needs CAMMAC - see https://cammac.readthedocs.io/.

# It actually launches one of its notebooks (see last line), feeding
# it with some parameter values, through CAMMAC utility job_pm.sh
# Parameters are explained in CAMMAC doc for the launched notebbok

CAMMAC=${CAMMAC:-/data/ssenesi/CAMMAC}
export CAMMAC=$(cd $CAMMAC; pwd)

# Create a working sub-directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}
wdir=${figname/_figure}
mkdir -p $wdir
cd $wdir

# Create input parameters file 
cat <<EOF >fig.yaml

version            : ""

variables          : [ [ pr , mean ], [ prw , mean ], [ pr , std ], [ mrro , mean ], [ mrro , std ] ]
stats_list         : [  mean ,  ens , nq5 , nq95 ]

hybrid_seasons  : 
    extra_annual : [  [NH , ANN ] , [SH , ANN ] ]  
latitude_limit     : 30.
SH_latitude_limit  : 60.

scenarios          : [  ssp585 ,  ssp245 , ssp126  ]

ref_experiment     : historical 
ref_period         : "1850-1900" 
proj_period        : "2000-2099"

option             : direct 
max_warming        : 5. 
min_warming        : 1.5
warming_step       : 0.25
window_half_size   : 10  

included_models    : {}  
excluded_models    : 
   mrro: [ CAMS-CSM1-0, IITM-ESM ]  # CAMS : outlier for variability, IITM : no mrro
   pr:   [ IITM-ESM ]  
   prw:  [ IITM-ESM,  CMCC-CM2-HR4, CMCC-CM2-SR5, FIO-ESM-2-0 ] # According to range check  

outdir             :  ./changes 

do_test            : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours=12 $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_hybrid_seasons_dT.ipynb fig.yaml $jobname $output $commons
