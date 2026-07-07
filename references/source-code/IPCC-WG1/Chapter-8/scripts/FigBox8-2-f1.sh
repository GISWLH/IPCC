#!/bin/bash

# Generates a Figure in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 8
# The figure number is the basename of this very file

# Creator : Stéphane Sénési stejase@laposte.net
# Version date : 20210328

# It also needs a dictionnary of available CMIP6 datasets versions; a
# version of such a dictionnary is provided in sibling directory
# data/, and is valid for the data available on the ESPRI platform.

# This script needs CAMMAC - see https://cammac.readthedocs.io/.

# It actually launches one of its notebooks (see last line), feeding
# it with some parameter values, through CAMMAC utility job_pm.sh
# Parameters are explained in CAMMAC doc for the launched notebbok

CAMMAC=${CAMMAC:-/data/ssenesi/CAMMAC}
export CAMMAC=$(cd $CAMMAC; pwd)

# Create a working directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname


cat <<EOF >fig.yaml

figure_name        :  Box8-2_Fig1 
outdir             :  ./figures 
version            : ""
scheme             : AR6S
sign_threshold     : 0.8

title              : null

variable           :  pr 
#threshold          : 0.1/(24*3600) # 0.1 mm/day, in SI
threshold          :  null
table              :  Amon 
derivation         :  seasonality 

experiments        :  [ ssp126 , ssp245 , ssp585 ] 
proj_period        :  "2081-2100"
ref_experiment     :  historical 
ref_period         :  "1995-2014"
ssp_for_ref        :  ssp585  
season             :  ANN 
field_type         :  mean_change 
excluded_models    : []  
included_models    : null

custom_plot        : { min : -0.2, max : 0.2,  delta : 0.04,  color : AR6_Temp_12 }

use_cached_proj_fields : True
write_cached_proj_fields : True
drop_old_figures       : True
use_cached_ref_field   : True
cache_dir              : ./cache

figure_details     : { page_width : 2450,  page_height : 2450, insert_width : 2400,  pt : 55,  ybox : 133, y : 40, font :  Liberation-Sans}
common_grid        :  r360x180 
variab_sampling_args : { house_keeping : True, compute : True, detrend : True, shift : 100, nyears : 20, number : 10}

do_test                   : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

$CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_3SSPs_plus_ref.ipynb fig.yaml $jobname $output $commons

