#!/bin/bash

# Generates Figure BoxTS7-1 in the IPCC Working Group I Contribution
# to the Sixth Assessment Report Technical Summary

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

# Create a working directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname

cat <<EOF >fig.yaml

do_test              : False

figure_name          :  FigTS-7-f1 
outdir               :  ./figures 
version              : ""
scheme               : AR6S
sign_threshold       : 0.8
manual_title         : null  

experiment           :  ssp245 
proj_period          : "2081-2100"

ref_experiment       :  historical 
ref_period           : "1995-2014" 

season               :  ANN         
field_type           :  means_rchange  

z1                     : 0.1/(24*3600) # 0.1 mm/day, in kg m2 s-1
use_cached_proj_fields : True
write_cached_proj_fields : True
drop_old_figures       : False
#
cache_dir            :  ./cache 
variab_sampling_args : { house_keeping : True, compute : True, detrend : True, shift : 100, nyears : 20, number : 10}
figure_details       : { page_width : 2450, page_height : 3444, pt : 48,  ybox : 133, y : 52, insert_width : 700}
common_grid          : "r360x180"
antarctic_mask       : $CAMMAC/data/mask_hide_antarctic_360x180.nc


included_models      : null
excluded_models      : {}
variability_models   : null
variability_excluded_models : {}

do_test              : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours=23 $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_1SSP_4vars.ipynb fig.yaml $jobname $output $commons
