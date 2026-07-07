#! /bin/bash
datanc=$1
outfile=$2
masknc=$3
maskdestnc=$4
nobinarymask=$5

function usage(){
  echo
  echo "Usage: $(basename $0) data_file.nc outfilename data_file_mask.nc destination_mask.nc"
  echo
  echo "Conservative remapping for land and sea points"
  echo
}
if test ${#} -lt 3; then
  usage
  exit
fi
LSMASK=1
# Make input landmask binary
#cd /oceano/gmeteo/WORK/PROYECTOS/2018_IPCC/data/CMIP6/mask_and_refGrid

if [ $nobinarymask == 1 ]; then
 echo "mask values are in %, and goes goes from 0 to 100%"
 cdo mulc,0.01  ${masknc} tmp_maskland.nc
 cdo -setrtoc,-1,0.999,0 -setrtoc,0.999,2,1 tmp_maskland.nc maskland.nc
 cdo mulc,-1 -setrtoc,0.001,2,0 -setrtoc,-1,0.001,-1 tmp_maskland.nc masksea.nc

 rm tmp_maskland.nc
else
 echo "mask values are binary, and goes goes from 0 to 1"
 cdo -setrtoc,-1,0.999,0 -setrtoc,0.999,2,1 ${masknc} maskland.nc
 cdo mulc,-1 -setrtoc,0.001,2,0 -setrtoc,-1,0.001,-1 ${masknc} masksea.nc
fi

  cdo div ${datanc} -setctomiss,0 maskland.nc land.nc
  cdo div ${datanc} -setctomiss,0 masksea.nc sea.nc

#cdo -setrtoc,50,200,1 -setrtoc,-50,90,0 ${masknc} maskland.nc
#cdo -setrtoc,50,200,0 -setrtoc,-50,90,1 ${masknc} masksea.nc
# Sharp change at 0.5 land fraction
# cdo -setrtoc,-1,0.5,0 -setrtoc,0.5,2,1 ${masknc} maskland.nc
# cdo mulc,0.5 -setmisstoc,1 -setrtoc,-0.5,0.5,2 maskland.nc masksea.nc
# Global destination grid (from cdo)
#cdo -f nc4 topo orogdest.nc
#cdo setrtoc,-20000,20000,1 -setrtomiss,-20000,0 orogdest.nc ${maskdestnc}
#if test "${LSMASK}" -eq 1; then


  #Creating weights
  cdo -P 4 gencon,${maskdestnc} -seltimestep,1 ${datanc} weights.nc
  cdo -P 4 gencon,${maskdestnc} land.nc weight_land.nc
  cdo -P 4 gencon,${maskdestnc} sea.nc  weight_sea.nc

  #Remap
  cdo remap,${maskdestnc},weight_land.nc land.nc landr.nc
  cdo remap,${maskdestnc},weight_sea.nc sea.nc sear.nc
  cdo ifthenelse -setmisstoc,0 ${maskdestnc} landr.nc sear.nc merged.nc

  # Fill the gaps with unconstrained remapping (doremap preferred option)
  cdo setmisstoc,1 -setrtoc,-9999999,9999999,0 merged.nc gaps.nc
  cdo remap,${maskdestnc},weights.nc ${datanc} unconstrained.nc
  cdo ifthenelse gaps.nc unconstrained.nc merged.nc ${outfile}


  # Fill the gaps by nearest neigbours
#  cdo setmisstonn landr.nc landrfilled.nc
#  cdo setmisstonn sear.nc searfilled.nc
#  cdo ifthenelse -setmisstoc,0 ${maskdestnc} landrfilled.nc searfilled.nc ${outfile}
#else
#  cdo remap,${maskdestnc},weights.nc ${datanc} ${outfile}
#fi
rm gaps.nc land.nc landr.nc maskland.nc masksea.nc merged.nc sea.nc sear.nc unconstrained.nc weights.nc weight_land.nc weight_sea.nc
