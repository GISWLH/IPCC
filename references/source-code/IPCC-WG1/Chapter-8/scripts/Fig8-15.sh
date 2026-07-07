#!/bin/bash

# Generates a Figure in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 8
# The figure number is the basename of this very file

# Creator : Stéphane Sénési stejase@laposte.net
# Version date : 20210328

# This script needs CAMMAC - see https://cammac.readthedocs.io/.

# It also needs a dictionnary of available CMIP6 datasets versions; a
# version of such a dictionnary is provided in sibling directory
# data/, and is valid for the data available on the ESPRI platform.

# It actually launches one of its notebooks (see last line), feeding
# it with some parameter values, through CAMMAC utility job_pm.sh
# Parameters are explained in CAMMAC doc for the launched notebbok

CAMMAC=${CAMMAC:-/data/ssenesi/CAMMAC}
export CAMMAC=$(cd $CAMMAC; pwd)

# Create a local working directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname

# Create input parameters file 
cat <<"EOF" >fig.yaml

figure_name        : Fig8-16 
scheme             : AR6S
sign_threshold     : 0.8
version            : ""        
title              : "Multi-model annual mean long-term changes in daily precipitation statistics"
outdir             : ./figures

cases              : 
                     ydry    : { derivation : plain  ,  variable : dday ,  table : yr ,  threshold : null, 
                                 plot_args  : {  color : AR6_Evap_12 ,  units : days , 
                                                 colors : "-32 -16 -8 -4 -2 0 2 4 8 16 32",
                                                 focus : land  }}
                     ydrain  : { derivation : plain  ,  variable : drain ,  table : yr ,  threshold : null, 
                                 plot_args : {  color : AR6_Precip_12 ,  units : mm ,  scale : 24.*3600., 
                                                colors : "-2 -1 -0.5 -0.2 -0.1 0 0.1 0.2 0.5 1 2 ",
                                                focus : land } } 

order              : [ ydry, ydrain ]

derived_variables_pattern  : "/data/ssenesi/CMIP6_derived_variables/${variable}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}_${version}_${PERIOD}.nc"
derived_variable_table     : yr

ref_experiment     : historical
experiments        : [ ssp126 , ssp245 , ssp585 ]
ref_period         : "1995-2014"
proj_period        : "2081-2100"
field_type         :  mean_change 
season             :  ANN 

included_models    : null
excluded_models    : [ ]

variability_models : null
variability_excluded_models : [ ]

use_cached_proj_fields   : True
write_cached_proj_fields : True
drop_old_figures         : False
print_statistics         : True

common_grid            : "r360x180"
variab_sampling_args   : { house_keeping : True, compute : True, detrend : True, shift : 100, nyears : 20, number : 10}
cache_dir              :  ./cache 
figure_details         : { page_width : 2450, page_height : 3444,  insert_width : 2400, pt : 55, ybox : 133, y : 40, font :  Liberation-Sans}

do_test                  : ${1:-False}

EOF


# Launch a job in which papermill will execute the notebook, injecting above parameters 
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours=12 $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_3SSPs_2vars.ipynb fig.yaml $jobname $output $commons
