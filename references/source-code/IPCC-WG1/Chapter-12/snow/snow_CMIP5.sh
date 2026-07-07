#!/bin/sh

# Processes CMIP5 snow data for Figures 12.9d and 12.10d in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 12
# Calculates the mean number of days per year with snow depth greater than 100 ml (100 kg per m^2) snow water equivalent (SWE100) over the northern hemisphere snow season (November to March - since the data are only shown for Europe and North America) for the the periods 1995-2014 (recent past), 2041-2060 (mid-term) and 2081-2099 (long term (2100 is excluded since data exist for only the first 2 months of the 2100 snow season)).


#Steps
#- Read in and concatenate each simulation to generate one file covering 1980-2100 for both scenarios (using historical simulations for 1980-2005 and RCP2.6 or RCP8.5 for 2006-2100)
#- calculate the snow index
#- regrid the data
#- calculate means over the 20 year time periods listed above


# Inputs:
#- CMIP5 historical, RCP2.6 and RCP8.5 daily snw variable
#- sftlf (land area fraction) files
# This program calls the Atlas' regridding script (remappeR_v2.cdo.sh) and uses the file "destination_mask_2.nc4" as the target grid. This regridding script conservatively remaps the land and ocean separately and then interpolates between the two. For CMIP5 the target grid is a regular 2 degree lon-lat grid.

# This code was run on the DKRZ machine Mistral
# Created by Carley Iles (carley.iles@cicero.oslo.no)

module load nco
module load cdo

tempp='insert path to folder for temporary files'
snowdir='insert path to folder in which to keep the processed data'
landmasks='insert path to folder with sftlf files'

mkdir ${snowdir}/cmip5
mkdir ${snowdir}/cmip5/regridded
mkdir ${snowdir}/cmip5/regridded/yearly
mkdir ${snowdir}/cmip5/time_periods


scenariolist="26 85"

mlistCMIP5="bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 CNRM-CM5 CSIRO-Mk3-6-0 FGOALS-g2 GFDL-CM3 GFDL-ESM2G GFDL-ESM2M HadGEM2-CC HadGEM2-ES inmcm4 MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 MRI-ESM1 NorESM1-M"


rm  ${tempp}/*.nc

for  m in $mlistCMIP5 ; do
echo $m

rm  ${tempp}/*.nc

if [ $m = "bcc-csm1-1" ]
then
echo $m
echo "processing bcc-csm1-1"

# concatenate data into one file for 1980-2100 for each scenario

cdo selyear,1980/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1/historical/day/landIce/day/r1i1p1/v1/snw/snw_day_bcc-csm1-1_historical_r1i1p1_19500101-20121231.nc  ${tempp}/concat_snw_presentshort.nc

ncrcat -h  ${tempp}/concat_snw_presentshort.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1/rcp26/day/landIce/day/r1i1p1/v20120705/snw/snw_day_bcc-csm1-1_rcp26_r1i1p1_20060101-20991231.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/concat_snw_presentshort.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1/rcp85/day/landIce/day/r1i1p1/v20120705/snw/snw_day_bcc-csm1-1_rcp85_r1i1p1_20060101-20991231.nc  ${tempp}/snow_85.nc

rm  ${tempp}/concat_snw_presentshort.nc


elif [ $m = "bcc-csm1-1-m" ]
then
echo $m
echo "processing bcc-csm1-1-m"

cdo selyear,1980/1999 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1-m/historical/day/landIce/day/r1i1p1/v20120709/snw/snw_day_bcc-csm1-1-m_historical_r1i1p1_19750101-19991231.nc  ${tempp}/concat_snw_presentshort1.nc

cdo selyear,2000/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1-m/historical/day/landIce/day/r1i1p1/v20120709/snw/snw_day_bcc-csm1-1-m_historical_r1i1p1_20000101-20121231.nc  ${tempp}/concat_snw_presentshort2.nc

ncrcat -h   ${tempp}/concat_snw_presentshort1.nc  ${tempp}/concat_snw_presentshort2.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1-m/rcp26/day/landIce/day/r1i1p1/v20120910/snw/snw_day_bcc-csm1-1-m_rcp26_r1i1p1_*.nc  ${tempp}/snow_26.nc

ncrcat -h   ${tempp}/concat_snw_presentshort1.nc  ${tempp}/concat_snw_presentshort2.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BCC/bcc-csm1-1-m/rcp85/day/landIce/day/r1i1p1/v20130411/snw/snw_day_bcc-csm1-1-m_rcp85_r1i1p1_*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/concat_snw_presentshort1.nc
rm  ${tempp}/concat_snw_presentshort2.nc


elif [ $m = "BNU-ESM" ]
then
echo $m
echo "processing BNU-ESM"

cdo selyear,1980/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BNU/BNU-ESM/historical/day/landIce/day/r1i1p1/v20120504/snw/snw_day_BNU-ESM_historical_r1i1p1_19500101-20051231.nc  ${tempp}/snw_present.nc

ncrcat -h  ${tempp}/snw_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BNU/BNU-ESM/rcp26/day/landIce/day/r1i1p1/v20120503/snw/snw_day_BNU-ESM_rcp26_r1i1p1_20060101-21001231.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snw_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/BNU/BNU-ESM/rcp85/day/landIce/day/r1i1p1/v20120504/snw/snw_day_BNU-ESM_rcp85_r1i1p1_20060101-21001231.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snw_present.nc 


elif [ $m = "CanESM2" ]
then
echo $m
echo "processing CanESM2"

cdo selyear,1980/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CCCma/CanESM2/historical/day/landIce/day/r1i1p1/v20120618/snw/snw_day_CanESM2_historical_r1i1p1_19790101-20051231.nc  ${tempp}/snw_present.nc

ncrcat -h  ${tempp}/snw_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CCCma/CanESM2/rcp26/day/landIce/day/r1i1p1/v20120618/snw/snw_day_CanESM2_rcp26_r1i1p1_20060101-21001231.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snw_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CCCma/CanESM2/rcp85/day/landIce/day/r1i1p1/v20120407/snw/snw_day_CanESM2_rcp85_r1i1p1_20060101-21001231.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snw_present.nc


elif [ $m = "CNRM-CM5" ]
then
echo $m
echo "processing CNRM-CM5"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_20*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/rcp26/day/land/day/r1i1p1/v20121001/snw/snw_day_CNRM-CM5_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/day/land/day/r1i1p1/v20120530/snw/snw_day_CNRM-CM5_historical_r1i1p1_20*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CNRM-CERFACS/CNRM-CM5/rcp85/day/land/day/r1i1p1/v20121001/snw/snw_day_CNRM-CM5_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc


elif [ $m = "CSIRO-Mk3-6-0" ]
then
echo $m
echo "processing CSIRO-Mk3-6-0"

cdo selyear,1980/1989 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/day/landIce/day/r1i1p1/v20110518/snw/snw_day_CSIRO-Mk3-6-0_historical_r1i1p1_19700101-19891231.nc  ${tempp}/snow_present_short.nc

ncrcat -h  ${tempp}/snow_present_short.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/day/landIce/day/r1i1p1/v20110518/snw/snw_day_CSIRO-Mk3-6-0_historical_r1i1p1_19900101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/rcp26/day/landIce/day/r1i1p1/v20110518/snw/snw_day_CSIRO-Mk3-6-0_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snow_present_short.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/day/landIce/day/r1i1p1/v20110518/snw/snw_day_CSIRO-Mk3-6-0_historical_r1i1p1_19900101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/rcp85/day/landIce/day/r1i1p1/v20110518/snw/snw_day_CSIRO-Mk3-6-0_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snow_present_short.nc


elif [ $m = "FGOALS-g2" ]
then
echo $m
echo "processing FGOALS-g2"

ncrcat -h /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_198*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_199*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_20*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc 

ncrcat -h /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_198*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_199*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_historical_r1i1p1_20*.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_FGOALS-g2_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc 

elif [ $m = "GFDL-CM3" ]
then
echo $m
echo "processing GFDL-CM3"

# rcp 2.6 not available

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-CM3/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-CM3_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-CM3/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-CM3_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-CM3/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-CM3_historical_r1i1p1_2*.nc /work/bk1088/ciles/snow/GFDL-CM3/snw_day_GFDL-CM3_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc 


elif [ $m = "GFDL-ESM2G" ] 
then
echo $m
echo "processing GFDL-ESM2G"

cdo selyear,1980 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_19760101-19801231.nc  ${tempp}/snowtemp.nc

ncrcat -h  ${tempp}/snowtemp.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_2*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/rcp26/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snowtemp.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_historical_r1i1p1_2*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2G/rcp85/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2G_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snowtemp.nc


elif [ $m = "GFDL-ESM2M" ] 
then
echo $m
echo "processing GFDL-ESM2M"

cdo selyear,1980 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_19760101-19801231.nc  ${tempp}/snowtemp.nc

ncrcat -h  ${tempp}/snowtemp.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_2*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/rcp26/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snowtemp.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/historical/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_historical_r1i1p1_2*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NOAA-GFDL/GFDL-ESM2M/rcp85/day/landIce/day/r1i1p1/v20110601/snw/snw_day_GFDL-ESM2M_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snowtemp.nc


elif [ $m = "HadGEM2-CC" ]
then
echo $m
echo "processing HadGEM2-CC"

# rcp 2.6 not available
cdo selyear,1980/1984 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-CC/historical/day/landIce/day/r1i1p1/v20110930/snw/snw_day_HadGEM2-CC_historical_r1i1p1_19791201-19841130.nc  ${tempp}/snow1980.nc

ncrcat -h  ${tempp}/snow1980.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-CC/historical/day/landIce/day/r1i1p1/v20110930/snw/snw_day_HadGEM2-CC_historical_r1i1p1_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-CC/historical/day/landIce/day/r1i1p1/v20110930/snw/snw_day_HadGEM2-CC_historical_r1i1p1_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-CC/historical/day/landIce/day/r1i1p1/v20110930/snw/snw_day_HadGEM2-CC_historical_r1i1p1_2*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-CC/rcp85/day/landIce/day/r1i1p1/v20120531/snw/snw_day_HadGEM2-CC_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snow1980.nc


elif [ $m = "HadGEM2-ES" ]
then
echo $m
echo "processing HadGEM2-ES"

cdo selyear,1980/1989 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/historical/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc  ${tempp}/snow1980.nc

ncrcat -h   ${tempp}/snow1980.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/historical/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_historical_r1i1p1_19891201-19991130.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/historical/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/rcp26/day/landIce/day/r1i1p1/v20120405/snw/snw_day_HadGEM2-ES_rcp26_r1i1p1_2*.nc  ${tempp}/snow_26.nc

ncrcat -h   ${tempp}/snow1980.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/historical/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_historical_r1i1p1_19891201-19991130.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/historical/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_historical_r1i1p1_19991201-20051130.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MOHC/HadGEM2-ES/rcp85/day/landIce/day/r1i1p1/v20111212/snw/snw_day_HadGEM2-ES_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snow1980.nc


elif [ $m = "inmcm4" ]
then
echo $m
echo "processing inmcm4"

# rcp 2.6 not available

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/INM/inmcm4/historical/day/land/day/r1i1p1/v20110323/snw/snw_day_inmcm4_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/INM/inmcm4/historical/day/land/day/r1i1p1/v20110323/snw/snw_day_inmcm4_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/INM/inmcm4/historical/day/land/day/r1i1p1/v20110323/snw/snw_day_inmcm4_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/INM/inmcm4/rcp85/day/land/day/r1i1p1/v20110323/snw/snw_day_inmcm4_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc


elif [ $m = "MIROC5" ]
then
echo $m
echo "processing MIROC5"

cdo selyear,2000/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/historical/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_historical_r1i1p1_20000101-20091231.nc  ${tempp}/concat_snw_presentshort.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/historical/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/historical/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_historical_r1i1p1_19900101-19991231.nc  ${tempp}/concat_snw_presentshort.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/rcp26/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_rcp26_r1i1p1_20*.nc  ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/historical/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/historical/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_historical_r1i1p1_19900101-19991231.nc  ${tempp}/concat_snw_presentshort.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC5/rcp85/day/landIce/day/r1i1p1/v20111124/snw/snw_day_MIROC5_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/concat_snw_presentshort.nc


elif [ $m = "MIROC-ESM" ]
then
echo $m
echo "processing MIROC-ESM"

cdo selyear,1980/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM/historical/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM_historical_r1i1p1_19500101-20051231.nc  ${tempp}/snow_present.nc

ncrcat -h  ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM/rcp26/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM_rcp26_r1i1p1_20060101-21001231.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM/rcp85/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snow_present.nc


elif [ $m = "MIROC-ESM-CHEM" ]
then
echo $m
echo "processing MIROC-ESM-CHEM"

cdo selyear,1980/2005 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM-CHEM/historical/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM-CHEM_historical_r1i1p1_19500101-20051231.nc  ${tempp}/snow_present.nc

ncrcat -h  ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM-CHEM/rcp26/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM-CHEM_rcp26_r1i1p1_20060101-21001231.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MIROC/MIROC-ESM-CHEM/rcp85/day/landIce/day/r1i1p1/v20111129/snw/snw_day_MIROC-ESM-CHEM_rcp85_r1i1p1_20060101-21001231.nc  ${tempp}/snow_85.nc

rm  ${tempp}/snow_present.nc


elif [ $m = "MPI-ESM-LR" ] 
then
echo $m
echo "processing MPI-ESM-LR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/rcp26/day/landIce/day/r1i1p1/v20111014/snw/snw_day_MPI-ESM-LR_rcp26_r1i1p1_20*.nc  ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/historical/day/landIce/day/r1i1p1/v20111006/snw/snw_day_MPI-ESM-LR_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-LR/rcp85/day/landIce/day/r1i1p1/v20111014/snw/snw_day_MPI-ESM-LR_rcp85_r1i1p1_20*.nc  ${tempp}/snow_85.nc


elif [ $m = "MPI-ESM-MR" ] 
then
echo $m
echo "processing MPI-ESM-MR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/rcp26/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_rcp26_r1i1p1_20*.nc  ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/historical/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MPI-M/MPI-ESM-MR/rcp85/day/landIce/day/r1i1p1/v20120503/snw/snw_day_MPI-ESM-MR_rcp85_r1i1p1_20*.nc  ${tempp}/snow_85.nc


elif [ $m = "MRI-CGCM3" ]
then
echo $m
echo "processing MRI-CGCM3"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/rcp26/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_rcp26_r1i1p1_20*.nc   ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/historical/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-CGCM3/rcp85/day/landIce/day/r1i1p1/v20111019/snw/snw_day_MRI-CGCM3_rcp85_r1i1p1_20*.nc   ${tempp}/snow_85.nc


elif [ $m = "MRI-ESM1" ] 
then
echo $m
echo "processing MRI-ESM1"

# rcp 2.6 not available
ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-ESM1/historical/day/landIce/day/r1i1p1/v20130307/snw/snw_day_MRI-ESM1_historical_r1i1p1_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-ESM1/historical/day/landIce/day/r1i1p1/v20130307/snw/snw_day_MRI-ESM1_historical_r1i1p1_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/MRI/MRI-ESM1/historical/day/landIce/day/r1i1p1/v20130307/snw/snw_day_MRI-ESM1_historical_r1i1p1_20000101-20051231.nc /work/bk1088/ciles/snow/GFDL-CM3/snw_day_MRI-ESM1_rcp85_r1i1p1_2*.nc  ${tempp}/snow_85.nc


elif [ $m = "NorESM1-M" ]
then
echo $m
echo "processing NorESM1-M"

cdo selyear,1980/1999 /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NCC/NorESM1-M/historical/day/landIce/day/r1i1p1/v20110901/snw/snw_day_NorESM1-M_historical_r1i1p1_19500101-19991231.nc  ${tempp}/snow_present_short.nc

ncrcat -h  ${tempp}/snow_present_short.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NCC/NorESM1-M/historical/day/landIce/day/r1i1p1/v20110901/snw/snw_day_NorESM1-M_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NCC/NorESM1-M/rcp26/day/landIce/day/r1i1p1/v20110901/snw/snw_day_NorESM1-M_rcp26_r1i1p1_20*.nc  ${tempp}/snow_26.nc

ncrcat -h  ${tempp}/snow_present_short.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NCC/NorESM1-M/historical/day/landIce/day/r1i1p1/v20110901/snw/snw_day_NorESM1-M_historical_r1i1p1_20000101-20051231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip5/output1/NCC/NorESM1-M/rcp85/day/landIce/day/r1i1p1/v20110901/snw/snw_day_NorESM1-M_rcp85_r1i1p1_20*.nc  ${tempp}/snow_85.nc


fi



# get rid of the extra dimension for GFDL models
if [ $m = "GFDL-CM3" ] || [ $m = "GFDL-ESM2M" ] || [ $m = "GFDL-ESM2G" ]
then


ncks -C -O -x -v average_DT  ${tempp}/snow_26.nc  ${tempp}/snw26_simp.nc
ncks -C -O -x -v average_DT  ${tempp}/snow_85.nc  ${tempp}/snw85_simp.nc


# mark with ones for days with more than 100 kg per m squared
cdo gec,100  ${tempp}/snw26_simp.nc  ${tempp}/snw100_26.nc
cdo gec,100  ${tempp}/snw85_simp.nc  ${tempp}/snw100_85.nc


else

# mark with ones for days with more than 100 kg per m squared
cdo gec,100  ${tempp}/snow_26.nc  ${tempp}/snw100_26.nc
cdo gec,100  ${tempp}/snow_85.nc  ${tempp}/snw100_85.nc


fi


# make monthly totals of days >100
cdo monsum  ${tempp}/snw100_26.nc  ${tempp}/snw100mon_26_$m.nc
cdo monsum  ${tempp}/snw100_85.nc  ${tempp}/snw100mon_85_$m.nc

# make seasonal totals for the NH snow season (nov-march)
cdo timselsum,5,10,7  ${tempp}/snw100mon_26_$m.nc  ${snowdir}/cmip5/${m}_26_snw100seas_1980-2100.nc
cdo timselsum,5,10,7  ${tempp}/snw100mon_85_$m.nc  ${snowdir}/cmip5/${m}_85_snw100seas_1980-2100.nc


	for sc in $scenariolist ; do
	echo $sc

		# regrid the data using the Atlas script
		. remappeR_v2.cdo.sh ${snowdir}/cmip5/${m}_${sc}_snw100seas_1980-2100.nc ${snowdir}/cmip5/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.2deg.nc $landmasks/sftlf_fx_${m}_*.nc /work/bk1088/ciles/grids/destination_mask_2.nc4 1
			
		# calculate 20 year means for the time periods defined above
		# first select the 20 year period
		cdo selyear,1995/2014 ${snowdir}/cmip5/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.2deg.nc  ${tempp}/${m}_${sc}_snw100seas_1995_2014.2deg.nc
		# Then calculate the 20 year mean
		cdo timmean  ${tempp}/${m}_${sc}_snw100seas_1995_2014.2deg.nc ${snowdir}/cmip5/regridded/time_periods/${m}_${sc}_snw100seas_1995_2014_MEAN.2deg.nc
		rm  ${tempp}/${m}_${sc}_snw100seas_1995_2014.2deg.nc


		cdo selyear,2041/2060 ${snowdir}/cmip5/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.2deg.nc  ${tempp}/${m}_${sc}_snw100seas_2041_2060.2deg.nc
		cdo timmean  ${tempp}/${m}_${sc}_snw100seas_2041_2060.2deg.nc ${snowdir}/cmip5/regridded/time_periods/${m}_${sc}_snw100seas_2041_2060_MEAN.2deg.nc
		rm  ${tempp}/${m}_${sc}_snw100seas_2041_2060.2deg.nc


		cdo selyear,2081/2099 ${snowdir}/cmip5/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.2deg.nc  ${tempp}/${m}_${sc}_snw100seas_2081_2099.2deg.nc
		cdo timmean  ${tempp}/${m}_${sc}_snw100seas_2081_2099.2deg.nc ${snowdir}/cmip5/regridded/time_periods/${m}_${sc}_snw100seas_2081_2099_MEAN.2deg.nc
		rm  ${tempp}/${m}_${sc}_snw100seas_2081_2099.2deg.nc

	done

rm  ${tempp}/*.nc

done

