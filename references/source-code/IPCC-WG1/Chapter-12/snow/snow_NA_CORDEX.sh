#!/bin/bash

# Processes CMIP6 snow data for Figures 12.10 b,d in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 12
# Calculates the mean number of days per year with snow depth greater than 100 ml (100 kg per m^2) snow water equivalent (SWE100) over the northern hemisphere snow season (November to March - since the data are only shown for North America) for the the periods 1995-2014 (recent past), 2041-2060 (mid-term) and 2081-2099 (long term (2100 is excluded since data exist for only the first 2 months of the 2100 snow season. When simulations end in 2099 then 2099 is also excluded)).


#Steps
#- Read in and concatenate each simulation to generate one file covering 1980-2100 for both scenarios (using historical simulations for 1980-2005 and RCP2.6 or RCP-8.5 for 2006-2100)
#- calculate the snow index
#- regrid the data conservatively to the 0.22 degree rotated REMO2015 grid
#- calculate means over the 20 year time periods listed above


# Inputs:
#- CORDEX data for North America at 0.22 and 0.44 degrees,historical, RCP2.6 and RCP8.5 daily snw variable

# This code was run on the DKRZ machine Mistral
# Created by Carley Iles (carley.iles@cicero.oslo.no)


module load nco
module load cdo

tempp='insert path to folder for temporary files'
snowdir='insert path to folder in which to keep the processed data'

mkdir ${snowdir}/NA_CORDEX
mkdir ${snowdir}/NA_CORDEX/regridded
mkdir ${snowdir}/NA_CORDEX/regridded/time_periods


CORDEXlist="NAM-22_MOHC_HadGEM2-ES_r1i1p1_ISU-RegCM4-v4.4 NAM-22_MPI-M_MPI-ESM-LR_r1i1p1_ISU-RegCM4-v4.4 NAM-22_NOAA_GFDL-GFDL-ESM2M_r1i1p1_ISU-RegCM4-v4.4 NAM-22_MOHC_HadGEM2-ES_r1i1p1_GERICS-REMO2015 NAM-22_MPI-M_MPI-ESM-LR_r1i1p1_GERICS-REMO2015 NAM-22_NCC_NorESM1-M_r1i1p1_GERICS-REMO2015 NAM-44_ICHEC_EC-EARTH_r3i1p1_DMI-HIRHAM5"

scenariolist="26 85"

rm ${tempp}/*.nc

for m in $CORDEXlist ; do

echo $m

rm ${tempp}/*.nc

if [ $m = "NAM-22_MOHC_HadGEM2-ES_r1i1p1_ISU-RegCM4-v4.4" ]
then
echo $m
echo "processing NAM-22_MOHC-HadGEM2-ES_r1i1p1_ISU-RegCM4-v4.4"

cdo selyear,1981/2005 /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_MOHC-HadGEM2-ES_rcp85_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_85_${m}.nc
rm ${tempp}/snow_present.nc
# only goes to 2099


elif [ $m = "NAM-22_MPI-M_MPI-ESM-LR_r1i1p1_ISU-RegCM4-v4.4" ]
then
echo $m
echo "processing NAM-22_MPI-M-MPI-ESM-LR_r1i1p1_ISU-RegCM4-v4.4"

cdo selyear,1981/2005 /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_85_${m}.nc
rm ${tempp}/snow_present.nc


elif [ $m = "NAM-22_NOAA_GFDL-GFDL-ESM2M_r1i1p1_ISU-RegCM4-v4.4" ]
then
echo $m
echo "processing NAM-22_NOAA-GFDL-GFDL-ESM2M_r1i1p1_ISU-RegCM4-v4.4"

cdo selyear,1981/2005 /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_NOAA-GFDL-GFDL-ESM2M_historical_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_present.nc

ncrcat -h ${tempp}/snow_present.nc /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-22_NOAA-GFDL-GFDL-ESM2M_rcp85_r1i1p1_ISU-RegCM4_v4.4.nc ${tempp}/snow_85_${m}.nc
rm ${tempp}/snow_present.nc
#only goes to 2099


elif [ $m = "NAM-22_MOHC_HadGEM2-ES_r1i1p1_GERICS-REMO2015" ]
then
echo $m
echo "processing NAM-22_MOHC-HadGEM2-ES_r1i1p1_GERICS-REMO2015"

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/rcp26/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191025/snw_NAM-22_MOHC-HadGEM2-ES_rcp26_r1i1p1_GERICS-REMO2015_v1_day_* ${tempp}/snow_26_${m}.nc

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051230.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/rcp85/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191029/snw_NAM-22_MOHC-HadGEM2-ES_rcp85_r1i1p1_GERICS-REMO2015_v1_day_* ${tempp}/snow_85_${m}.nc
#only goes to 2099


elif [ $m = "NAM-22_MPI-M_MPI-ESM-LR_r1i1p1_GERICS-REMO2015" ]
then
echo $m
echo "processing NAM-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS-REMO2015"

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/rcp26/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191025/snw_NAM-22_MPI-M-MPI-ESM-LR_rcp26_r1i1p1_GERICS-REMO2015_v1_day_* ${tempp}/snow_26_${m}.nc

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MPI-M-MPI-ESM-LR_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MPI-M-MPI-ESM-LR/rcp85/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191029/snw_NAM-22_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_GERICS-REMO2015_v1_day_*.nc ${tempp}/snow_85_${m}.nc


elif [ $m = "NAM-22_NCC_NorESM1-M_r1i1p1_GERICS-REMO2015" ]
then
echo $m
echo "processing NAM-22_NCC-NorESM1-M_r1i1p1_GERICS-REMO2015"

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/rcp26/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191025/snw_NAM-22_NCC-NorESM1-M_rcp26_r1i1p1_GERICS-REMO2015_v1_day_*.nc ${tempp}/snow_26_${m}.nc

ncrcat -h /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19860101-19901231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19910101-19951231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_19960101-20001231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_NCC-NorESM1-M_historical_r1i1p1_GERICS-REMO2015_v1_day_20010101-20051231.nc /work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/NCC-NorESM1-M/rcp85/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191029/snw_NAM-22_NCC-NorESM1-M_rcp85_r1i1p1_GERICS-REMO2015_v1_day_* ${tempp}/snow_85_${m}.nc


elif [ $m = "NAM-44_ICHEC_EC-EARTH_r3i1p1_DMI-HIRHAM5" ]
then
echo $m
echo "processing NAM-44_ICHEC-EC-EARTH_r3i1p1_DMI-HIRHAM5"

cp /work/bk1088/ciles/snow/extra_simulations/CORDEX_NAM/snw_NAM-44_ICHEC-EC-EARTH_rcp85_r3i1p1_DMI-HIRHAM5_v1_day_1981_2100.nc ${tempp}/snow_85_${m}.nc

fi

	for sc in $scenariolist ; do
	echo $sc

		
		# mark with ones for days with more than 100 kg per m squared snow
		cdo gec,100 ${tempp}/snow_${sc}_${m}.nc ${tempp}/snw100_${sc}.nc


		# make monthly totals of days >100
		cdo monsum ${tempp}/snw100_${sc}.nc ${tempp}/snw100mon_${sc}_$m.nc

		# make seasonal totals for the NH snow season (nov-march)
		cdo timselsum,5,10,7 ${tempp}/snw100mon_${sc}_$m.nc ${snowdir}/NA_CORDEX/${m}_${sc}_snw100seas_1980-2100.nc

		

		# conservatively remap onto the 0.22 degree rotated REMO2015 grid, or else if simulations are already REMO2015 then copy them to the regridded folder
		if [ $m = "NAM-22_MOHC_HadGEM2-ES_r1i1p1_ISU-RegCM4-v4.4" ] || [ $m = "NAM-22_MPI-M_MPI-ESM-LR_r1i1p1_ISU-RegCM4-v4.4" ] || [ $m = "NAM-22_NOAA_GFDL-GFDL-ESM2M_r1i1p1_ISU-RegCM4-v4.4" ] || [ $m = "NAM-44_ICHEC_EC-EARTH_r3i1p1_DMI-HIRHAM5" ]
		then
			cdo remapnn,/work/kd0956/CORDEX/data/cordex/output/NAM-22/GERICS/MOHC-HadGEM2-ES/historical/r1i1p1/GERICS-REMO2015/v1/day/snw/v20191015/snw_NAM-22_MOHC-HadGEM2-ES_historical_r1i1p1_GERICS-REMO2015_v1_day_19810101-19851230.nc ${snowdir}/NA_CORDEX/${m}_${sc}_snw100seas_1980-2100.nc ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc
		else
			cp ${snowdir}/NA_CORDEX/${m}_${sc}_snw100seas_1980-2100.nc ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc
		fi


		# calculate 20 year means for the time periods defined above

		# first select the 20 year period
		cdo selyear,1995/2014 ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc ${tempp}/${m}_${sc}_present.nc
		# Then calculate the 20 year mean
		cdo timmean ${tempp}/${m}_${sc}_present.nc ${snowdir}/NA_CORDEX/regridded/time_periods/${m}_${sc}_snw100seas_1995_2014_remo22grid.nc

		cdo selyear,2041/2060 ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc ${tempp}/${m}_${sc}_midcent.nc
 		cdo timmean ${tempp}/${m}_${sc}_midcent.nc ${snowdir}/NA_CORDEX/regridded/time_periods/${m}_${sc}_snw100seas_2041_2060_remo22grid.nc

		# for the last period some models do not include the year 2100. We exclude the last year as it only contains the first 2 months of the snow season
		if [ $m = "NAM-22_MOHC_HadGEM2-ES_r1i1p1_ISU-RegCM4-v4.4" ] || [ $m = "NAM-22_NOAA_GFDL-GFDL-ESM2M_r1i1p1_ISU-RegCM4-v4.4" ] || [ $m = "NAM-22_MOHC_HadGEM2-ES_r1i1p1_GERICS-REMO2015" ]
		then
			cdo selyear,2081/2098 ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc ${tempp}/${m}_${sc}_farfut.nc
			cdo timmean ${tempp}/${m}_${sc}_farfut.nc ${snowdir}/NA_CORDEX/regridded/time_periods/${m}_${sc}_snw100seas_2081_2098_remo22grid.nc
		else
			cdo selyear,2081/2099 ${snowdir}/NA_CORDEX/regridded/${m}_${sc}_snw100seas_1980-2100_remo22grid.nc ${tempp}/${m}_${sc}_farfut.nc
			cdo timmean ${tempp}/${m}_${sc}_farfut.nc ${snowdir}/NA_CORDEX/regridded/time_periods/${m}_${sc}_snw100seas_2081_2099_remo22grid.nc
		fi

	done

rm ${tempp}/*.nc


done

