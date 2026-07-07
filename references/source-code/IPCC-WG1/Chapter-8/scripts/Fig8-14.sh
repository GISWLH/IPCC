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

# Create a working directory specific to this figure. It will hold cached data and figures
figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname


# Create input parameters file 
cat <<EOF >fig.yaml

figure_name              : Fig8-14  
figure_title             : "Multi-model seasonal mean precipitation percentage change for SSP2-4.5 (2081-2100 vs 1995-2014)"  
scheme                   : AR6S
sign_threshold           : 0.8
auto_title_prefix        : Seasonal 
outdir                   :  ./figures 
version                  : "_test" 

variable                 : pr 
derivation_label         : plain         
table                    : Amon 
field_type               : means_rchange  

seasons                  : [ DJF , MAM ,  JJA ,  SON ]  
experiment               :  ssp245 
proj_period              : "2081-2100"
ref_experiment           :  historical 
ref_period               : "1995-2014"  

included_models          : null
excluded_models          : []

use_cached_proj_fields   : True
write_cached_proj_fields : True
drop_old_figures         : False
print_statistics         : True

cache_dir                :  ./cache 
figure_details           : { page_width : 2450, page_height : 3444,  insert_width : 1600, pt : 50,  ybox : 133, y : 52 , font :  Liberation-Sans}
common_grid              :  r360x180 

figure_mask              : null
variability_sampling_args : { house_keeping : True, compute : True, detrend : True, shift : 100, nyears : 20, number : 10}

do_test                  : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters 
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours="06" $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_4seasons.ipynb fig.yaml $jobname $output $commons
