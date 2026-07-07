#!/bin/bash

# Generates DJF panel for figure 8-21 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 8

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

#dirname=${figname/-DJF/} 
dirname=${figname} 
mkdir -p $dirname
cd $dirname


cat <<EOF >fig.yaml

figure_name               : Fig8-21-DJF
version                   : ""   
manual_title              : null
outdir                    :  ./figures 

variable                  :  P-E      
table                     :  Amon          
variable_transformation   :  plain 
season                    :  DJF
experiment                :  ssp585 

ref_experiment            :  historical 
ref_period                : "1850-1900" 
proj_period               : "2015-2099" 
warming                   : 3.0         
window_half_size          : 10          

field_type                :  mean
threshold                 : null

included_models           : null
excluded_models           : [ ACCESS-ESM1-5, EC-Earth3-Veg, EC-Earth3 ]

plot_args : 
  color : AR6_Precip_12 
  min   : -1
  max   : 1 
  delta : 0.2 

clim_contours             : [ ] 
figure_details            : { page_width : 2450, page_height : 3444,  insert_width : 2000, pt : 60,  ybox : 133, y : 40, font :  Liberation-Sans}
common_grid               :  r360x180 

do_test                   : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

$CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_1var_at_WL_1SSP_with_clim.ipynb fig.yaml $jobname $output $commons

