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

# Create a working directory specific to this figure, based on script name.
# It will hold cached data

figname=$(basename $0)
figname=${figname/.sh/}
mkdir -p $figname
cd $figname

cat <<EOF >fig.yaml

do_compute            : True
do_plot               : True

version               : ""
plot_version          : ""
figure_name           :  Fig8-26 

included_models      : null
excluded_models      : [] 

# Compute parameters
##########################

compute_basins : [ Amazon , Lena, Yangtze , Mississippi, Danube, Niger, Euphrates, Indus, Nile, Parana, Amu-Darya, Mackenzie, "Lake Eyre", Murray ]

variables: 
  - [ mrro , Lmon, mean ]
  - [ mrro , Lmon, std ]

stats_list          : [  mean , nq5 , nq95 , ens ]

ref_experiment      :  historical 
ref_period          : "1850-1900" 

scenarios          : [  ssp585 ,  ssp245 , ssp126  ]
periods_length     : 20
start_year         : 1901
last_year          : 2081  # i.e. last period's begin
step               : 10  # Not necessarily equal to periods_length !
#
outdir             : ./figures
image_format       : eps


# Plot parameters
###################################

plot_basins         : [ Mississippi, Danube, Lena, Amazon, Euphrates, Yangtze, Niger, Indus, Murray ]
plot_variables      : [ [ mrro , Lmon , mean ], [ mrro , Lmon , std ] ]
plot_variable_label :  runoff 
plot_name1          :  mean 
plot_name2          :  variability 

plot_stats          : [ nq5 , mean , nq95 ]
plot_stats_label    : "ensemble mean, 5 and 95 percentiles"

plot_start_year     : 1901
plot_last_year      : 2081
plot_step           : 10

# y-axis range for various basins
minmax :
  Amazon  :     [ -45 , 30 ]
  Lena    :     [ -10 , 70 ]
  Yangtze :     [ -35 , 40 ]
  Mississippi : [ -30 , 45 ]
  Danube  :     [ -35 , 40 ]
  Niger :       [-70 , 160 ]
  Euphrates  :  [ -120 , 80 ]
  Indus  :      [ -45 , 110 ]
  Nile :        [ -100 , 180 ] 
  Parana :      [ -40 , 70 ]
  Mackenzie :   [ -10 , 50 ]
  Amu-Darya :   [ -50 , 80 ]
  Murray  :     [ -70 , 120 ]


basins_file        : $CAMMAC/data/basins/num_bas_ctrip.nc 
basins_key         : { land : -999,  Yangtze : 11 ,  Lena : 8,  Amazon : 1,  Mississippi : 3 , 
                       Danube : 29,  Niger : 9,  Euphrates : 31,  Indus : 20,  Nile : 4,  Parana : 5 , 
                       Amu-Darya :  45,  Mackenzie : 12,  Lake Eyre : 15,  Murray : 17}

do_test             : ${1:-False}

EOF


# Launch a job in which papermill will execute the notebook, injecting above parameters
jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

hours="48" $CAMMAC/jobs/job_pm.sh $CAMMAC/notebooks/change_rate_basins.ipynb fig.yaml $jobname $output $commons

