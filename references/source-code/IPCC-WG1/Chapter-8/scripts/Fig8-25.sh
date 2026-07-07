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

figure_name               : Fig8-27
do_test                   : False
version                   : "" 
scheme                    : AR6S
sign_threshold            : 0.8
title                     : "Effect on precipitation of first versus second 2 degrees of global warming (vs 1850-1900)"
outdir                    :  ./figures 

variable                  :  pr      
table                     :  Amon          
variable_transformation   :  plain         
seasons                   : [ DJF , JJA ]  
experiment                :  ssp585 
first_delta               : 2.0         
second_delta              : 4.0         
proj_period               : "2015-2099" 
ref_experiment            :  historical 
ref_period                : "1850-1900" 
window_half_size          : 10          
field_type                : rmean     
threshold                 : 0.1/(24*3600) 

included_models           : null
excluded_models           : [ ]
with_variability          : True 
variability_models        : null
variability_excluded_models : []

plot_args                 : 
                   color  :  AR6_Precip_12
                   colors : "-80. -40. -20. -10. -5. 0 5. 10. 20. 40. 80. "

figure_details            : { page_width : 2450, page_height : 3444,  insert_width : 2000, pt : 60,  ybox : 133, y : 40, font :  Liberation-Sans}
common_grid               : "r360x180"
variability_sampling_args : { house_keeping : True, compute : True, detrend : True, shift : 100, nyears : 20, number : 10}
#

do_test                   : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

$CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_path_dependance.ipynb fig.yaml $jobname $output $commons

