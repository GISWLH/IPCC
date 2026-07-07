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

CAMMAC=${CAMMAC:-/home/ssenesi/CAMMAC}
export CAMMAC=$(cd $CAMMAC; pwd)

# Create a local working directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname


# Create input parameters file 
cat <<EOF >fig.yaml

figure_title           : "Multi-model seasonal mean evapotranspiration percentage change (2081-2100 vs 1995-2014)"
auto_title_prefix      : Seasonal
#
figure_name            : Fig8-17
version                : ""
scheme                 : AR6S
sign_threshold         : 0.8
#
variable               : evspsbl
table                  : Amon
field_type             : means_rchange
derivation_label       : plain
custom_plot            : {  "units": "mm/d" }
#
included_models        : null 
excluded_models        : []
variability_models     : null
variability_excluded_models : []
variability_sampling_args   : { shift: 100, nyears: 20, number: 10, house_keeping: False, compute: True, detrend: True }
#
seasons                : [ DJF, JJA ]  
experiments            : [ ssp126, ssp245, ssp585 ] 
proj_period            : "2081-2100"
ref_experiment         : historical
ref_period             : "1995-2014"  
#
use_cached_proj_fields : True
write_cached_proj_fields : True
drop_old_figures       : False
print_statistics       : True
#
outdir                 : ./figures
cache_dir              : ./cache
figure_details         : { page_width : 2450,  page_height : 3444,  insert_width : 1800, pt : 48,  ybox : 133,  y : 52, font :  Liberation-Sans}
common_grid            : "r360x180"
figure_mask            : null

plot_for_each_model    : []
ranges : 
           reference   : { scale : 24*3600 , units : mm/d, min : 0 , max : 5 , delta : 0.5 }
           projection  : { scale : 24*3600 , units : mm/d, min : 0 , max : 5 , delta : 0.5 }
           change      : { scale : 24*3600 , units : mm/d, min : -2.5 , max : 2.5 , delta : 0.5 }
           rchange     : { min : -100. , max : 100., delta : 10. }
           variability : { scale : 24*3600 , units : mm/d, min : 0 , max : 0.25 , delta : 0.2 }

do_test                : ${1:-False}
EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters 
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours=12 $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_map_3SSPs_2seasons.ipynb fig.yaml $jobname $output $commons
