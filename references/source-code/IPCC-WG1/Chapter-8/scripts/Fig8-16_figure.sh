#!/bin/bash

# Plot processed data for a Figure in the IPCC Working Group I
# Contribution to the Sixth Assessment Report: Chapter 8

# The figure number is the basename of this very file

# This script should be run after the corresponding compute scripts

# Creator : Stéphane Sénési stejase@laposte.net
# Version date : 20210328

# This script needs CAMMAC - see https://cammac.readthedocs.io/.

# It actually launches one of its notebooks (see last line), feeding
# it with some parameter values, through CAMMAC utility job_pm.sh
# Parameters are explained in CAMMAC doc for the launched notebbok

D=${CAMMAC:-/home/ssenesi/CAMMAC}

# Create a local working dir which is the same as for companion scripts, for getting cached data
figname=$(basename $0)
figname=${figname/.sh/}
wdir=${figname/_figure} 
mkdir -p $wdir
cd $wdir


# Create input parameters file 
cat <<EOF >fig_figure.yaml

version               : ""
figure_name           :  Fig8-15
outdir                :  ./figures 
indir                 :  ./changes    # Location for compute phase outputs
scenario              :   ssp585 
variables             : [ [ mrro ,  mean ],[ pr ,  mean ], [ prw ,  mean ], [ mrro ,  std ], [ pr ,  std ]]
seasons               : [ tropics_JJA , tropics_DJF , extra_summer , extra_winter ]
excluded_models       : { mrro : [  CAMS-CSM1-0  ]}
ensemble_stat         :  nq95  



########################################
# Plot tuning (Ncl/PyNgl conventions)
########################################

layout      : [2,2] 
title       : "Projected water cycle changes as a function of global warming ~Z70~~C~in SSP5-8.5 and over 20-year overlapping periods, starting from [2021-2040], relative to 1850-1900"
yaxis_title : "%% change averaged over land and across %d %s models~Z75~~C~Error bars show 5-95%% percentiles only for extreme GWLs"
xaxis_title : "Global Warming Level (~S~o~N~C) vs. %s"
#
seasons_description : [ "a) Tropics JJA", 
                        "b) Tropics DJF", 
                        "c) Extra-tropics Summer (NH:JJA, SH : DJF)", 
                        "d) Extra-tropics Winter (NH:DJF, SH:JJA)"
                      ]
#
seasons_showing_legend : [ tropics_JJA ]
show_all_error_bars    : False

colors          : { pr  :  firebrick3 ,  huss  :  black ,  prw  :  grey40 ,  mrro  :  blue3 }
#colors          : { pr  :  red ,  huss  :  black ,  prw  :  forestgreen ,  mrro  :  blue }

xyMarkLineModes : { mean  :  MarkLines ,  std  :  MarkLines }
xyDashPatterns  : { mean  :  0,  std : 1 }
xyMarkers       : { mean  : 16,  std : 4 }
xyMarkerSizes   : { mean  : 0.015,  std : 0.01 }

nice            : 
   pr    :  precipitation 
   prw   :  precipitable water 
   mrro  :  runoff 
   std   :  year-to-year variability 
   mean  :  mean 

wks_type        : "eps"                       #-- output type of workstation


EOF

jobname=$figname
output=$figname

# Tell job_pm.sh to use co-located parameters file 
commons=$(cd $(dirname $0); pwd)/common_parameters.yaml
[ ! -f $commons ] && $commons = ""

$D/jobs/job_pm.sh $D/notebooks/change_hybrid_seasons_figure.ipynb fig_figure.yaml $jobname $output $commons
