#!/bin/bash

DATA_DIR=/data/CMIP/curated_ESGF_replica

PMIP3_MODELS="CCSM4 CNRM-CM5 COSMOS-ASO FGOALS-g2 GISS-E2-R IPSL-CM5A-LR MIROC-ESM MPI-ESM-P MRI-CGCM3"
expt_names="lgm-cal-adj midHolocene-cal-adj"

monClim="monClim_"

tracking_ids=()
#Pseudocode repeat for all desired variables. Making sure to select cal-adj or not appropriately
for expt_i in $expt_names
do
  for var_i in "tas_"
  do 
    for mod_i in $PMIP3_MODELS
    do
      in_fils=`ls $DATA_DIR/$mod_i/lgm-cal-adj/$var_i*nc`
      echo $in_fils
      fil_str=${fil##*/}
      fil_str_no_nc=${fil##*/}
      for mm in {1..12}; do
        ncra -O -F -d time,${mm},,12 $in_fils ../netcdfs/clm${mm}.nc
      done
      ncrcat -O ../netcdfs/clm*.nc ../netcdfs/$var_i$monClim$mod_i'_'$expt_i.nc
      rm ../netcdfs/clm*.nc ../netcdfs/*.tmp
      modellist+=($mod_i)
      id=`ncdump -h ../netcdfs/$var_i$monClim$mod_i'_'$expt_i.nc | grep tracking`
      tracking_ids+=(${id:18:36})      
    done
    echo $modellist
    echo $tracking_ids
  done
done
#ncecat line
#ncks line to add model name as dimension
