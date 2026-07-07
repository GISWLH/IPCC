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

# It systematically combines the data processing step and the plot step
# Doing the plot step alone is possible, by launching manually the plot command
# which is displayed in one of the last output cells of the launched notebook

# The documentation for the processed data files (which are passed by the compute
# phase to the plot phase) is available in the data files archived on IPCC/WGI/DMS.

# However, the naming an structure of these NetCDF files is quite
# self-explanatory; just need to know on top of that that NetCDF
# variables have suffixes : mean for multi-model change mean,
# land_mean for multi-model change mean over land,pctl5 and pctl95 for
# multi-model 5 and 95 percentiles, variab5 and variab95 for 5 and 95
# percentiles of the internal variability


CAMMAC=${CAMMAC:-/data/ssenesi/CAMMAC}
export CAMMAC=$(cd $CAMMAC; pwd)

# Create locally a working directory specific to this figure. It will hold cached data
figname=$(basename $0)
figname=${figname/.sh/}

mkdir -p $figname
cd $figname

# Create input parameters file 
cat <<EOF >fig.yaml

title                      : Multi-model zonal mean long-term changes in P, E and P-E
variables                  : [ pr, evspsbl, P-E ]
table                      : Amon
columns                    : "Precipitation|Evaporation|Precip. minus evaporation"
figure_name                : Fig8-13 
version                    : "" 
outdir                     : ./figures

# Data used (data_version_tag is set in commom_parameters.yaml)
included_models            : null      
excluded_models            : { pr : [ IITM-ESM ]  , P-E : [ IITM-ESM ] , evspsbl : [ IITM-ESM ]} 
variability_models         : null
variability_excluded_models : { pr : [ IITM-ESM ] , P-E : [ IITM-ESM ] , evspsbl : [ IITM-ESM ] } 

ref_experiment             : historical
ref_period                 : "1995-2014"
experiments                : [ssp126, ssp245, ssp585] 
projection_period          : "2081-2100"
#
print_statistics           : True
common_grid                : "r360x180"
variability_sampling_args  : { shift: 100, nyears: 20, number: 10, house_keeping: False, compute: True, detrend: True }
check_fixed_fields         : True

do_profiling               : False
do_test                    : ${1:-False}

EOF

# Launch a job in which papermill will execute the notebook, injecting above parameters 
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours=11 $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_zonal_mean.ipynb fig.yaml $jobname $output $commons
