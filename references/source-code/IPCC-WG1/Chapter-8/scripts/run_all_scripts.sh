#!/bin/bash

# Just run (almost) all scripts from its dir (normally $CAMMAC/scripts),

# If arg#1 is set, run them with with flag 'True' for letting
# them do only a small (reduced size) test

# The job is done in batch mode by the scripts, so there is no way
# to check the results in same script; we need to run another script
# for that

# Those scripts dedicated to the plot phase only (which name have "_figure") are not run 

CAMMAC=${CAMMAC?must set it, e.g. to /data/ssenesi}
CLIMAF=${CLIMAF?must set it, e.g. to /home/ssenesi.climaf_installs/running_climaf}

refdir=$(cd $(dirname $0); pwd)
scripts=$(cd $refdir ; ls Fig*sh Tab*sh | grep -v _figure)

echo Running that scripts : $scripts

# arg#1 = True means : just a test case (reduced size)
[ "$1" ] && flag='True'

# arg#2 for choosing ESPRI ciclad environment 
if [ "$2" == "C3" ] ; then
    export ENV_PM=$CAMMAC/jobs/job_env_ciclad_python3.sh
elif [ "$2" == "C2" ] ; then
    export ENV_PM=$CAMMAC/jobs/job_env_ciclad.sh
else :
    export ENV_PM="" # Use CAMMAC default
fi

# Run scripts
$CAMMAC/jobs/basic.sh ssp585 JJAS KS 0.9 pr
for script in $scripts ; do
    $refdir/$script $flag
done
