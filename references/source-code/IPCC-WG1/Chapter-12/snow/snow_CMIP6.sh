#!/bin/bash

# Processes CMIP6 snow data for Figures 12.9d and 12.10d in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 12
# Calculates the mean number of days per year with snow depth greater than 100 ml (100 kg per m^2) snow water equivalent (SWE100) over the northern hemisphere snow season (November to March - since the data are only shown for Europe and North America) for the the periods 1995-2014 (recent past), 2041-2060 (mid-term) and 2081-2099 (long term (2100 is excluded since data exist for only the first 2 months of the 2100 snow season)).


#Steps
#- Read in and concatenate each simulation to generate one file covering 1980-2100 for both scenarios (using historical simulations for 1980-2014 and SSP1-2.6 or SSP5-8.5 for 2015-2100)
#- calculate the snow index
#- regrid the data
#- calculate means over the 20 year time periods listed above


# Inputs:
#- CMIP6 historical, ssp126 and ssp585 daily snw variable
#- sftlf (land area fraction) files
# This program calls the Atlas' regridding script (remappeR_v2.cdo.sh) and uses the file "destination_mask_1.nc4" as the target grid. This regridding script conservatively remaps land and ocean separately and then interpolates between the two. For CMIP6 the target grid is a regular 1 degree lon-lat grid.

# This code was run on the DKRZ machine Mistral
# Created by Carley Iles (carley.iles@cicero.oslo.no)

module load nco
module load cdo

tempp='insert path to folder for temporary files'
snowdir='insert path to folder in which to keep the processed data'
landmasks='insert path to folder with sftlf files'

mkdir ${snowdir}/cmip6
mkdir ${snowdir}/cmip6/regridded
mkdir ${snowdir}/cmip6/regridded/yearly
mkdir ${snowdir}/cmip6/regridded/time_periods


scenariolist="26 85"

mlistCMIP6="CanESM5 EC-Earth3 GFDL-ESM4 IPSL-CM6A-LR MRI-ESM2-0 NESM3 UKESM1-0-LL MPI-ESM1-2-HR MIROC6 BCC-CSM2-MR ACCESS-CM2 AWI-CM-1-1-MR HadGEM3-GC31-LL HadGEM3-GC31-MM INM-CM4-8 INM-CM5-0 MIROC-ES2L MPI-ESM1-2-LR"

rm ${tempp}*.nc


for  m in $mlistCMIP6 ; do
echo $m

rm ${tempp}/*.nc

if [ $m = "CanESM5" ]
then
echo $m
echo "processing CanESM5"

# concatenate data into one file for 1980-2100 for each scenario

cdo selyear,1980/2014 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/day/snw/gn/v20190429/snw_day_CanESM5_historical_r1i1p1f1_gn_18500101-20141231.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/CCCma/CanESM5/ssp126/r1i1p1f1/day/snw/gn/v20190429/snw_day_CanESM5_ssp126_r1i1p1f1_gn_20150101-21001231.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/CCCma/CanESM5/ssp585/r1i1p1f1/day/snw/gn/v20190429/snw_day_CanESM5_ssp585_r1i1p1f1_gn_20150101-21001231.nc ${tempp}/snow_85.nc


elif [ $m = "EC-Earth3" ]
then
echo $m
echo "processing EC-Earth3"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_198* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_199* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_20* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp126/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_ssp126_r1i1p1f1_gr*.nc ${tempp}/snow_26.nc

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_198* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_199* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/EC-Earth-Consortium/EC-Earth3/historical/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_historical_r1i1p1f1_gr_20* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/EC-Earth-Consortium/EC-Earth3/ssp585/r1i1p1f1/day/snw/gr/v20200310/snw_day_EC-Earth3_ssp585_r1i1p1f1_gr_*.nc ${tempp}/snow_85.nc


elif [ $m = "GFDL-CM4" ]
then
echo $m
echo "processing GFDL-CM4"

# ssp126 not available
ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-CM4/historical/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-CM4_historical_r1i1p1f1_gr1_19700101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-CM4/historical/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-CM4_historical_r1i1p1f1_gr1_19900101-20091231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-CM4/historical/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-CM4_historical_r1i1p1f1_gr1_20100101-20141231.nc ${tempp}/snow_present_prelim.nc

cdo selyear,1980/2014 ${tempp}/snow_present_prelim.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/NOAA-GFDL/GFDL-CM4/ssp585/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-CM4_ssp585_r1i1p1f1_gr1_*.nc ${tempp}/snow_85.nc

rm ${tempp}/snow_present_prelim.nc


elif [ $m = "GFDL-ESM4" ]
then
echo $m
echo "processing GFDL-ESM4"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/day/snw/gr1/v20190726/snw_day_GFDL-ESM4_historical_r1i1p1f1_gr1_19700101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/day/snw/gr1/v20190726/snw_day_GFDL-ESM4_historical_r1i1p1f1_gr1_19900101-20091231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/day/snw/gr1/v20190726/snw_day_GFDL-ESM4_historical_r1i1p1f1_gr1_20100101-20141231.nc ${tempp}/snow_present_prelim.nc

cdo selyear,1980/2014 ${tempp}/snow_present_prelim.nc ${tempp}/snow_present.nc


ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp126/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-ESM4_ssp126_r1i1p1f1_gr1_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp585/r1i1p1f1/day/snw/gr1/v20180701/snw_day_GFDL-ESM4_ssp585_r1i1p1f1_gr1_*.nc ${tempp}/snow_85.nc

rm ${tempp}/snow_present_prelim.nc


elif [ $m = "IPSL-CM6A-LR" ]
then
echo $m
echo "processing IPSL-CM6A-LR"

cdo selyear,1980/2014 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/IPSL/IPSL-CM6A-LR/historical/r1i1p1f1/day/snw/gr/v20180803/snw_day_IPSL-CM6A-LR_historical_r1i1p1f1_gr_18500101-20141231.nc ${tempp}/snow_present.nc

# this next step sorts out the time dimension which had some issues otherwise
cdo selyear,2015/2100 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp126/r1i1p1f1/day/snw/gr/v20190903/snw_day_IPSL-CM6A-LR_ssp126_r1i1p1f1_gr_20150101-21001231.nc ${tempp}/snow_future26.nc

#same
cdo selyear,2015/2100 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp585/r1i1p1f1/day/snw/gr/v20190903/snw_day_IPSL-CM6A-LR_ssp585_r1i1p1f1_gr_20150101-21001231.nc ${tempp}/snow_future85.nc

ncrcat -h ${tempp}/snow_present.nc ${tempp}/snow_future26.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc ${tempp}/snow_future85.nc ${tempp}/snow_85.nc

rm ${tempp}/snow_future26.nc
rm ${tempp}/snow_future85.nc


elif [ $m = "MRI-ESM2-0" ]
then
echo $m
echo "processing MRI-ESM2-0"


cdo selyear,1980/1999 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MRI/MRI-ESM2-0/historical/r1i1p1f1/day/snw/gn/v20190603/snw_day_MRI-ESM2-0_historical_r1i1p1f1_gn_19500101-19991231.nc ${tempp}/snow_prelim26.nc

ncrcat -h ${tempp}/snow_prelim26.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MRI/MRI-ESM2-0/historical/r1i1p1f1/day/snw/gn/v20190603/snw_day_MRI-ESM2-0_historical_r1i1p1f1_gn_20000101-20141231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MRI/MRI-ESM2-0/ssp126/r1i1p1f1/day/snw/gn/v20191108/snw_day_MRI-ESM2-0_ssp126_r1i1p1f1_gn_20150101-20641231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MRI/MRI-ESM2-0/ssp126/r1i1p1f1/day/snw/gn/v20191108/snw_day_MRI-ESM2-0_ssp126_r1i1p1f1_gn_20650101-21001231.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_prelim26.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MRI/MRI-ESM2-0/historical/r1i1p1f1/day/snw/gn/v20190603/snw_day_MRI-ESM2-0_historical_r1i1p1f1_gn_20000101-20141231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MRI/MRI-ESM2-0/ssp585/r1i1p1f1/day/snw/gn/v20191108/snw_day_MRI-ESM2-0_ssp585_r1i1p1f1_gn_20150101-20641231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MRI/MRI-ESM2-0/ssp585/r1i1p1f1/day/snw/gn/v20191108/snw_day_MRI-ESM2-0_ssp585_r1i1p1f1_gn_20650101-21001231.nc ${tempp}/snow_85.nc

rm ${tempp}/snow_prelim26.nc


elif [ $m = "NESM3" ]
then
echo $m
echo "processing NESM3"

cdo selyear,1980/2014 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/NUIST/NESM3/historical/r1i1p1f1/day/snw/gn/v20190812/snw_day_NESM3_historical_r1i1p1f1_gn_19800101-20141231.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/NUIST/NESM3/ssp126/r1i1p1f1/day/snw/gn/v20190806/snw_day_NESM3_ssp126_r1i1p1f1_gn_* ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/NUIST/NESM3/ssp585/r1i1p1f1/day/snw/gn/v20190811/snw_day_NESM3_ssp585_r1i1p1f1_gn_* ${tempp}/snow_85.nc



elif [ $m = "UKESM1-0-LL" ]
then
echo $m
echo "processing UKESM1-0-LL"

cdo selyear,1980/2014 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MOHC/UKESM1-0-LL/historical/r1i1p1f2/day/snw/gn/v20190627/snw_day_UKESM1-0-LL_historical_r1i1p1f2_gn_19500101-20141230.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MOHC/UKESM1-0-LL/ssp126/r1i1p1f2/day/snw/gn/v20190708/snw_day_UKESM1-0-LL_ssp126_r1i1p1f2_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MOHC/UKESM1-0-LL/ssp585/r1i1p1f2/day/snw/gn/v20190726/snw_day_UKESM1-0-LL_ssp585_r1i1p1f2_gn_*.nc ${tempp}/snow_85.nc


elif [ $m = "BCC-CSM2-MR" ]
then
echo $m
echo "processing BCC-CSM2-MR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/BCC/BCC-CSM2-MR/historical/r1i1p1f1/day/snw/gn/v20181114/snw_day_BCC-CSM2-MR_historical_r1i1p1f1_gn_19620101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/BCC/BCC-CSM2-MR/historical/r1i1p1f1/day/snw/gn/v20181114/snw_day_BCC-CSM2-MR_historical_r1i1p1f1_gn_19900101-20141231.nc ${tempp}/snow_presentprelim.nc

cdo selyear,1980/2014 ${tempp}/snow_presentprelim.nc ${tempp}/snow_present.nc

rm ${tempp}/snow_presentprelim.nc


ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp126/r1i1p1f1/day/snw/gn/v20190312/snw_day_BCC-CSM2-MR_ssp126_r1i1p1f1_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp585/r1i1p1f1/day/snw/gn/v20190308/snw_day_BCC-CSM2-MR_ssp585_r1i1p1f1_gn_*.nc ${tempp}/snow_85.nc



elif [ $m = "MIROC6" ]
then
echo $m
echo "processing MIROC6"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_historical_r1i1p1f1_gn_19800101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_historical_r1i1p1f1_gn_19900101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_historical_r1i1p1f1_gn_20000101-20091231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_historical_r1i1p1f1_gn_20100101-20141231.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MIROC/MIROC6/ssp126/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_ssp126_r1i1p1f1_gn* ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MIROC/MIROC6/ssp585/r1i1p1f1/day/snw/gn/v20191016/snw_day_MIROC6_ssp585_r1i1p1f1_gn* ${tempp}/snow_85.nc


elif [ $m = "MPI-ESM1-2-HR" ]
then
echo $m
echo "processing MPI-ESM1-2-HR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-HR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-HR_historical_r1i1p1f1_gn_198* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-HR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-HR_historical_r1i1p1f1_gn_199* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-HR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-HR_historical_r1i1p1f1_gn_20* ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/DKRZ/MPI-ESM1-2-HR/ssp126/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-HR_ssp126_r1i1p1f1_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/DKRZ/MPI-ESM1-2-HR/ssp585/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-HR_ssp585_r1i1p1f1_gn_*.nc ${tempp}/snow_85.nc


elif [ $m = "ACCESS-CM2" ]
then
echo $m
echo "processing ACCESS-CM2"

ncrcat -h /work/dicad/cmip6-prod/data4freva/model/global/cmip6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/day/snw/gn/v20191108/snw_day_ACCESS-CM2_historical_r1i1p1f1_gn_*.nc ${tempp}/snow_present_part1.nc

cdo selyear,1980/2014 ${tempp}/snow_present_part1.nc ${tempp}/snow_present.nc
rm ${tempp}/snow_present_part1.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-prod/data4freva/model/global/cmip6/ScenarioMIP/CSIRO-ARCCSS/ACCESS-CM2/ssp126/r1i1p1f1/day/snw/gn/v20191108/snw_day_ACCESS-CM2_ssp126_r1i1p1f1_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-prod/data4freva/model/global/cmip6/ScenarioMIP/CSIRO-ARCCSS/ACCESS-CM2/ssp585/r1i1p1f1/day/snw/gn/v20191108/snw_day_ACCESS-CM2_ssp585_r1i1p1f1_gn_*.nc ${tempp}/snow_85.nc

elif [ $m = "AWI-CM-1-1-MR" ]
then
echo $m
echo "processing AWI-CM-1-1-MR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/AWI/AWI-CM-1-1-MR/historical/r1i1p1f1/day/snw/gn/v20181218/snw_day_AWI-CM-1-1-MR_historical_r1i1p1f1_gn_198*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/AWI/AWI-CM-1-1-MR/historical/r1i1p1f1/day/snw/gn/v20181218/snw_day_AWI-CM-1-1-MR_historical_r1i1p1f1_gn_199*.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/AWI/AWI-CM-1-1-MR/historical/r1i1p1f1/day/snw/gn/v20181218/snw_day_AWI-CM-1-1-MR_historical_r1i1p1f1_gn_20*.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/AWI/AWI-CM-1-1-MR/ssp126/r1i1p1f1/day/snw/gn/v20190529/snw_day_AWI-CM-1-1-MR_ssp126_r1i1p1f1_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/AWI/AWI-CM-1-1-MR/ssp585/r1i1p1f1/day/snw/gn/v20190529/snw_day_AWI-CM-1-1-MR_ssp585_r1i1p1f1_gn_*.nc ${tempp}/snow_85.nc


elif [ $m = "HadGEM3-GC31-LL" ]
then
echo $m
echo "processing HadGEM3-GC31-LL"

cdo selyear,1980/2014 /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MOHC/HadGEM3-GC31-LL/historical/r1i1p1f3/day/snw/gn/v20190624/snw_day_HadGEM3-GC31-LL_historical_r1i1p1f3_gn_19500101-20141230.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_HadGEM3-GC31-LL_ssp126_r1i1p1f3_gn*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/bk1088/ciles/snow/extra_simulations/snw_day_HadGEM3-GC31-LL_ssp585_r1i1p1f3_gn*.nc ${tempp}/snow_85.nc


elif [ $m = "HadGEM3-GC31-MM" ]
then
echo $m
echo "processing HadGEM3-GC31-MM"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/day/snw/gn/v20191207/snw_day_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_198* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/day/snw/gn/v20191207/snw_day_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_199* /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/day/snw/gn/v20191207/snw_day_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_20* ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /mnt/lustre02/work/bk1088/ciles/snow/extra_simulations/snw_day_HadGEM3-GC31-MM_ssp126_r1i1p1f3_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /mnt/lustre02/work/bk1088/ciles/snow/extra_simulations/snw_day_HadGEM3-GC31-MM_ssp585_r1i1p1f3_gn_*.nc ${tempp}/snow_85.nc


elif [ $m = "INM-CM4-8" ]
then
echo $m
echo "processing INM-CM4-8"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/INM/INM-CM4-8/historical/r1i1p1f1/day/snw/gr1/v20190530/snw_day_INM-CM4-8_historical_r1i1p1f1_gr1_19500101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/INM/INM-CM4-8/historical/r1i1p1f1/day/snw/gr1/v20190530/snw_day_INM-CM4-8_historical_r1i1p1f1_gr1_20000101-20141231.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/INM/INM-CM4-8/ssp126/r1i1p1f1/day/snw/gr1/v20190603/snw_day_INM-CM4-8_ssp126_r1i1p1f1_gr1_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/INM/INM-CM4-8/ssp585/r1i1p1f1/day/snw/gr1/v20190603/snw_day_INM-CM4-8_ssp585_r1i1p1f1_gr1_*.nc ${tempp}/snow_85.nc


elif [ $m = "INM-CM5-0" ]
then
echo $m
echo "processing INM-CM5-0"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/INM/INM-CM5-0/historical/r1i1p1f1/day/snw/gr1/v20190610/snw_day_INM-CM5-0_historical_r1i1p1f1_gr1_19500101-19991231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/INM/INM-CM5-0/historical/r1i1p1f1/day/snw/gr1/v20190610/snw_day_INM-CM5-0_historical_r1i1p1f1_gr1_20000101-20141231.nc ${tempp}/snow_present_part1.nc

cdo selyear,1980/2014 ${tempp}/snow_present_part1.nc ${tempp}/snow_present.nc

rm ${tempp}/snow_present_part1.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/INM/INM-CM5-0/ssp126/r1i1p1f1/day/snw/gr1/v20190619/snw_day_INM-CM5-0_ssp126_r1i1p1f1_gr1_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/INM/INM-CM5-0/ssp585/r1i1p1f1/day/snw/gr1/v20190724/snw_day_INM-CM5-0_ssp585_r1i1p1f1_gr1_*.nc ${tempp}/snow_85.nc


elif [ $m = "MIROC-ES2L" ]
then
echo $m
echo "processing MIROC-ES2L"

ncrcat -h /mnt/lustre02/work/bk1088/ciles/snow/extra_simulations/snw_day_MIROC-ES2L_historical_r1i1p1f2_gn*.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /mnt/lustre02/work/bk1088/ciles/snow/extra_simulations/snw_day_MIROC-ES2L_ssp126_r1i1p1f2_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /mnt/lustre02/work/bk1088/ciles/snow/extra_simulations/snw_day_MIROC-ES2L_ssp585_r1i1p1f2_gn_*.nc ${tempp}/snow_85.nc


elif [ $m = "MPI-ESM1-2-LR" ]
then
echo $m
echo "processing MPI-ESM1-2-LR"

ncrcat -h /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_19700101-19891231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_19900101-20091231.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_20100101-20141231.nc ${tempp}/snow_present_part1.nc

cdo selyear,1980/2014 ${tempp}/snow_present_part1.nc ${tempp}/snow_present.nc

rm ${tempp}/snow_present_part1.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp126/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-LR_ssp126_r1i1p1f1_gn_*.nc ${tempp}/snow_26.nc

ncrcat -h ${tempp}/snow_present.nc /work/dicad/cmip6-dicad/data4freva/model/global/cmip6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r1i1p1f1/day/snw/gn/v20190710/snw_day_MPI-ESM1-2-LR_ssp585_r1i1p1f1_gn_*.nc ${tempp}/snow_85.nc


fi

	for sc in $scenariolist ; do
	echo $sc

		
		# mark with ones for days with more than 100 kg per m squared snow
		cdo gec,100 ${tempp}/snow_${sc}.nc ${tempp}/snw100_${sc}.nc

		# make monthly totals of days >100 kg per m
		cdo monsum ${tempp}/snw100_${sc}.nc ${tempp}/snw100mon_${sc}_$m.nc

		# make seasonal totals for the NH snow season (nov-march)
		cdo timselsum,5,10,7 ${tempp}/snw100mon_${sc}_$m.nc ${snowdir}/cmip6/${m}_${sc}_snw100seas_1980-2100.nc

		
		# remapping
		if [ $m = "EC-Earth3" ] # There was a problem with EC-Earth3's landmask, so use normal conservative remapping
		then
			cdo remapcon,/work/bk1088/ciles/grids/destination_mask_1.nc4 ${snowdir}/cmip6/${m}_${sc}_snw100seas_1980-2100.nc ${snowdir}/cmip6/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.1deg.nc


		else

		# regrid the data using the Atlas script
			. remappeR_v2.cdo.sh ${snowdir}/cmip6/${m}_${sc}_snw100seas_1980-2100.nc ${snowdir}/cmip6/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.1deg.nc $landmasks/sftlf_fx_${m}_*.nc /work/bk1088/ciles/grids/destination_mask_1.nc4 1


		fi
			
		# calculate 20 year means for the time periods defined above

		# first select the 20 year period
		cdo selyear,1995/2014 ${snowdir}/cmip6/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.1deg.nc ${tempp}/${m}_${sc}_snw100seas_1995_2014.1deg.nc
		# Then calculate the 20 year mean
		cdo timmean ${tempp}/${m}_${sc}_snw100seas_1995_2014.1deg.nc ${snowdir}/cmip6/regridded/time_periods/${m}_${sc}_snw100seas_1995_2014_MEAN.1deg.nc
		rm ${tempp}/${m}_${sc}_snw100seas_1995_2014.1deg.nc


		cdo selyear,2041/2060 ${snowdir}/cmip6/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.1deg.nc ${tempp}/${m}_${sc}_snw100seas_2041_2060.1deg.nc
		cdo timmean ${tempp}/${m}_${sc}_snw100seas_2041_2060.1deg.nc ${snowdir}/cmip6/regridded/time_periods/${m}_${sc}_snw100seas_2041_2060_MEAN.1deg.nc
		rm ${tempp}/${m}_${sc}_snw100seas_2041_2060.1deg.nc



		cdo selyear,2081/2099 ${snowdir}/cmip6/regridded/yearly/${m}_${sc}_snw100seas_1980-2100.1deg.nc ${tempp}/${m}_${sc}_snw100seas_2081_2099.1deg.nc
		cdo timmean ${tempp}/${m}_${sc}_snw100seas_2081_2099.1deg.nc ${snowdir}/cmip6/regridded/time_periods/${m}_${sc}_snw100seas_2081_2099_MEAN.1deg.nc
		rm ${tempp}/${m}_${sc}_snw100seas_2081_2099.1deg.nc



	done

rm ${tempp}/*.nc

done


