#
# This script calculates annual atmospheric burden based off pressure levels
#
# Required inputs: molar mixing ratio (4D field)
#                  pressure at tropopause (3D field)
#                  model cell area (2D field)
# ==========================================================================
# Working for burden based on pressure levels:
#
# p = F/A = mg/A, where m = mass of air
# dp = g/A dm ---> dm = A/g dp
# m = A/g (ps_lower - ps_upper), by integration with lower and upper pressure bounds
#
# n = m/M, for a particular species
# n{co}/n{air} = m{co}M{air}/m{air}M{co}, using co as an example
# m{co} = mol_frac * M{co}/M{air} * A/g * (ps_lower - ps_upper), where mol_frac = n{co}/c{air}
# ==========================================================================

import sys
import gc
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import netCDF4 as nc
import pandas as pd


def get_file(path, target):
    """
    Searches through all the files in a given folder, and selects the file
    which contains the target year.
    """
    files = glob.glob(path)
    file_ids = {f: np.arange(
        int(f[-16:-12]), int(f[-9:-5])+1, 1) for f in files}
    searched = [f for f, ids in file_ids.items() if target in ids]
    return searched[0]


def regridder(targetGrid, inputFile, variable):
    """
    targetGrid: path to file with correct grid
    inputFile: path to file with wrong grid
    variable: string variable name
    returns: np array with right grid!
    """
    targetArray = xr.open_mfdataset(targetGrid)
    print(inputFile)
    inputArray = xr.open_mfdataset(inputFile)
    newGrid = inputArray.interp_like(targetArray)
    outputArray = newGrid["ptp"].values
    return outputArray


def calculate_vars(model, ensembles, variables, molarMasses, varPath, tropopausePath, manualAreaPath, otherPaths={"UKESM1-0-LL_phalfPath": None, "UKESM1-0-LL_ztpPath": None, "UKESM1-0-LL_airmassPath": None, "GFDL-ESM4_psPath": None}, MRI_hist=True):
    """
    model = string; model name
    ensembles = stringlist; all "r1i1p1f1" type variants
    variables = stringlist; short labels e.g. 'o3'
    molarMasses = floatlist; molar masses in gmol-1
    varPath = string; Currently hardcoded for BADC
    tropopausePath = string; parent folder for ptp files
    manualAreaPath = string; direct path for areacella file
    otherPaths = dict; other paths required for model-specific ugliness. Add as required.
    """
    # by convention pressure_exclusive is the tropopause burden excluding the region between
    # the upper bound of the tropospheric column and the tropopause pressure
    pressure_excl_burden = pd.DataFrame(index=years, columns=['Year'])
    # optional inclusive burden calc - this is much slower!
    pressure_incl_burden = pd.DataFrame(index=years, columns=['Year'])
    # chemopause-based burden calculation
    chemopause_burden = pd.DataFrame(index=years, columns=['Year'])
    tropMaskArray = []
    for run in ensembles:
        print(run)
        # Load area file
        # First *attempt* to load from /badc, and when that inevitably fails, load from the manual area path
        try:
            area = nc.Dataset(base + "/" + centre + "/" + model + "/" + experiment + "/" + run +
                              "/fx/areacella/gn/latest/areacella_fx_" + model + "_piControl_" + run + "_gn.nc").variables["areacella"][:]
        except:
            print(
                "WARNING: Unable to load areacella from /badc. Checking for manual area input.")
            try:
                area = nc.Dataset(manualAreaPath).variables["areacella"][:]
                print("Successfully loaded areacella from manual input.")
            except:
                try:
                    area = np.load(manualAreaPath)
                    print("Loaded area from generated numpy file.")
                except:
                    raise Exception(
                        "No valid areacella file determined. Check for /badc file or enter manual path to areacella file.")

        for variable, molarMass in zip(variables, molarMasses):
            print(variable, molarMass)
            tempOutputList_excl = []
            tempOutputList_incl = []
            tempOutputList_chmp = []

            # Generate path string for file folder location
            #intermediatePath = varPath + variable + "_AERmon_" + model + "_" + experiment + "_" + run + "_g*"

            # BADC PATH
            intermediatePath = glob.glob(
                varPath + run + "/AERmon/" + variable + "/g*")[0]
            intermediatePath = intermediatePath + "/latest/" + variable + \
                "_AERmon_" + model + "_" + experiment + "_" + run + "_g*"

            # Regrid ptp for MRI only - they provide chemistry and physics on two different grids
            if model == "MRI-ESM2-0":
                targetGridFile = glob.glob(intermediatePath)

                ptpPath = tropopausePath + "/ptp_AERmon_" + \
                    model + "_" + experiment + "_" + run + "_g*"
                print(ptpPath)
                #ptpPath ="/badc/cmip6/data/CMIP6/ScenarioMIP/MRI/MRI-ESM2-0/ssp370/" + run + "/AERmon/ptp/gn/latest/ptp_AERmon_MRI-ESM2-0_ssp370_" + run + "_gn_201501-210012.nc"
                ptp = regridder(targetGridFile, ptpPath, "ptp")

            for yr in years:
                # Generate path to molar fraction data
                path = get_file(intermediatePath, yr)
                # Convert year to index by subtracting the first year of the dataset
                year = yr - int(path[-16:-12])

                # Lazy load variable file
                dataset = nc.Dataset(path)

                # Generate trop mask
                if model == "UKESM1-0-LL":
                    # UKESM use phalf to load in pressure levels at boundaries
                    # phalf[0:85] is the lowerBound, and phalf[1:86] is the upperBound

                    phalf = otherPaths["UKESM1-0-LL_phalfPath"] + \
                        "phalf_AERmon_" + model + "_" + experiment + "_" + run + "_g*"
                    phalf = get_file(phalf, yr)
                    phalf = nc.Dataset(
                        phalf).variables["phalf"][year*12:year*12 + 12, ...]

                    lowerBound = phalf[:, 0:85, :, :]
                    upperBound = phalf[:, 1:86, :, :]

                    # Logical check
                    if upperBound[0, 0, 0, 0] > lowerBound[0, 0, 0, 0]:
                        raise Exception(
                            "Upper pressure bound exceeds lower pressure bound. Check order of bnds.")

                    dp = lowerBound - upperBound

                    tropPath = tropopausePath + "/ptp_AERmon_" + \
                        model + "_" + experiment + "_" + run + "_g*"
                    tropPath = get_file(tropPath, yr)
                    tropPressure = nc.Dataset(
                        tropPath).variables["ptp"][year*12:year*12 + 12, ...]
                    tropMask = upperBound > tropPressure[:, None, :, :]

                elif model == "CESM2-WACCM":
                    # Extract p0, surfacePressure, aBnds, and bBnds
                    # Calculate gridbox pressure bounds using a*p0 + b*surfacePressure
                    p0 = dataset.variables["p0"][:]
                    surfacePressure = dataset.variables["ps"][year *
                                                              12:year*12 + 12, :, :]
                    aBnds = dataset.variables["a_bnds"][:]
                    bBnds = dataset.variables["b_bnds"][:]

                    # Note: upperBound should have a lower pressure than lowerBound
                    upperBound = (aBnds[:, 0]*p0)[None, :, None, None] + bBnds[:,
                                                                               0][None, :, None, None]*surfacePressure[:, None, :, :]
                    lowerBound = (aBnds[:, 1]*p0)[None, :, None, None] + bBnds[:,
                                                                               1][None, :, None, None]*surfacePressure[:, None, :, :]
                    # Logical check
                    if upperBound[0, 0, 0, 0] > lowerBound[0, 0, 0, 0]:
                        raise Exception(
                            "Upper pressure bound exceeds lower pressure bound. Check order of bnds.")

                    dp = lowerBound - upperBound  # This is used for discrete integration

                    # Load in model tropPressure
                    # Compare to lower pressure bound, returning True for all levels with a pressure higher than the tropopause
                    tropPath = tropopausePath + "/ptp_AERmon_" + \
                        model + "_" + experiment + "_" + run + "_g*"
                    tropPath = get_file(tropPath, yr)
                    tropPressure = nc.Dataset(
                        tropPath).variables["ptp"][year*12:year*12 + 12, ...]
                    tropMask = upperBound > tropPressure[:, None, :, :]

                elif model == "GFDL-ESM4":
                    # GFDL doesn't have the surface pressure in the metadata so we have to laod it in separately (WHY?)
                    try:
                        psPath = otherPaths["GFDL-ESM4_psPath"] + "/ps_AERmon_" + \
                            model + "_" + experiment + "_" + run + "_g*"
                        psPath = get_file(psPath, yr)
                    except:
                        psPath = otherPaths["GFDL-ESM4_psPath"] + "/ps_AERmon_" + \
                            model + "_" + "esm-hist" + "_" + run + "_g*"
                        psPath = get_file(psPath, yr)

                    # Convert year to index by subtracting the first year of the dataset: this is different for Pressure (WHY?)
                    psYear = yr - int(psPath[-16:-12])

                    # Extract surfacePressure, aBnds, and bBnds
                    # Calculate gridbox pressure bounds using a + b*surfacePressure
                    surfacePressure = nc.Dataset(
                        psPath).variables["ps"][psYear*12:psYear*12 + 12, :, :]
                    aBnds = dataset.variables["ap_bnds"][:]
                    bBnds = dataset.variables["b_bnds"][:]

                    # Note: upperBound should have a lower pressure than lowerBound
                    lowerBound = (aBnds[:, 0])[
                        None, :, None, None] + bBnds[:, 0][None, :, None, None]*surfacePressure[:, None, :, :]
                    upperBound = (aBnds[:, 1])[
                        None, :, None, None] + bBnds[:, 1][None, :, None, None]*surfacePressure[:, None, :, :]
                    # Logical check
                    if upperBound.sum() > lowerBound.sum():
                        raise Exception(
                            "Upper pressure bound exceeds lower pressure bound. Check order of bnds.")

                    dp = lowerBound - upperBound  # This is used for discrete integration

                    tropPath = tropopausePath + "ptp_AERmon_" + \
                        model + "_" + experiment + "_" + run + "_g*"
                    tropPath = get_file(tropPath, yr)
                    # Convert year to index by subtracting the first year of the dataset: this is different for tropHeight (WHYYYYYYY?)
                    ptpYear = yr - int(tropPath[-16:-12])
                    tropPressure = nc.Dataset(
                        tropPath).variables["ptp"][ptpYear*12:ptpYear*12 + 12, :, :]
                    tropMask = lowerBound > tropPressure[:, None, :, :]

                elif model == "MRI-ESM2-0":
                    # Extract p0, surfacePressure, aBnds, and bBnds
                    # Calculate gridbox pressure bounds using a*p0 + b*surfacePressure
                    p0 = dataset.variables["p0"][:]
                    surfacePressure = dataset.variables["ps"][year *
                                                              12:year*12 + 12, :, :]
                    aBnds = dataset.variables["a_bnds"][:]
                    bBnds = dataset.variables["b_bnds"][:]

                    # Note: upperBound should have a lower pressure than lowerBound
                    upperBound = (aBnds[:, 1]*p0)[None, :, None, None] + bBnds[:,
                                                                               1][None, :, None, None]*surfacePressure[:, None, :, :]
                    lowerBound = (aBnds[:, 0]*p0)[None, :, None, None] + bBnds[:,
                                                                               0][None, :, None, None]*surfacePressure[:, None, :, :]
                    # Logical check
                    if upperBound[0, 0, 0, 0] > lowerBound[0, 0, 0, 0]:
                        raise Exception(
                            "Upper pressure bound exceeds lower pressure bound. Check order of bnds.")

                    dp = lowerBound - upperBound  # This is used for discrete integration

                    # Load in model tropPressure
                    # Compare to lower pressure bound, returning True for all levels with a pressure higher than the tropopause
                    # FOR HISTORICAL
                    ptpYear = yr - 1850
                    if MRI_hist == False:
                        ptpYear = yr - 2014
                    tropPressure = ptp[ptpYear*12:ptpYear*12 + 12, ...]
                    tropMask = upperBound > tropPressure[:, None, :, :]

                else:
                    raise Exception("Model not added yet!")

                # Extract one year of variable data
                moleFrac = dataset.variables[variable][year *
                                                       12:year*12 + 12, :, :, :]

                # Calculate burden as described at top of program
                mass = moleFrac * (molarMass/28.97) * \
                    area[None, None, :, :] * dp / 9.81

                # Mask using the tropospheric mask
                trop = mass * tropMask
                tropoPause_incl = False
                if tropoPause_incl == True:
                    if model == "CESM2-WACCM":
                        ntimes, nlevs, nlats, nlons = np.shape(moleFrac)
                        extra_mass = np.zeros((ntimes, nlats, nlons))
                        for itime in range(0, ntimes):
                            for ilat in range(0, nlats):
                                for ilon in range(0, nlons):
                                    lev_index = np.argmax(
                                        upperBound[itime, :, ilat, ilon] > tropPressure[itime, ilat, ilon])
                                    extra_frac = (upperBound[itime, lev_index, ilat, ilon] - tropPressure[itime, ilat, ilon]) / (
                                        dp[itime, lev_index-1, ilat, ilon])
                                    extra_mass[itime, ilat, ilon] = mass[itime,
                                                                         lev_index+1, ilat, ilon] * extra_frac
                    else:
                        ntimes, nlevs, nlats, nlons = np.shape(moleFrac)
                        extra_mass = np.zeros((ntimes, nlats, nlons))
                        for itime in range(ntimes):
                            for ilat in range(0, nlats):
                                for ilon in range(0, nlons):
                                    lev_index = np.argmax(
                                        upperBound[itime, :, ilat, ilon] < tropPressure[itime, ilat, ilon])
                                    extra_frac = (tropPressure[itime, ilat, ilon] - upperBound[itime, lev_index, ilat, ilon]) / (
                                        dp[itime, lev_index+1, ilat, ilon])
                                    extra_mass[itime, ilat, ilon] = mass[itime,
                                                                         lev_index+1, ilat, ilon] * extra_frac

                # Set any 0. to np.nan for calculation purposes
                trop[trop == 0.] = np.nan

                # Sum over lev, lat, lon to generate burden timeseries
                burden = np.nansum(trop, axis=(1, 2, 3))
                if tropoPause_incl == True:
                    pressure_inclusive_increment = np.nansum(
                        extra_mass, axis=(1, 2))
                # Annual mean
                burden = np.nanmean(burden)

                if tropoPause_incl == True:
                    pressure_inclusive_burden = np.nanmean(
                        burden+pressure_inclusive_increment)

                if (yr % 5 == 0):
                    print("")
                    print("Year: %s | Burden: %i Tg" % (yr, burden/1e9))
                    if tropoPause_incl == True:
                        print("Year: %s | Burden: %i Tg" %
                              (yr, (pressure_inclusive_burden)/1e9))
                # Append burden to output_list
                tempOutputList_excl.append(burden)

                if tropoPause_incl == True:
                    tempOutputList_incl.append(pressure_inclusive_burden)

                chemoPause = True
                if chemoPause == True:
                    # Mask using the tropospheric mask
                    tropMask = moleFrac <= 150e-9
                    trop = mass * tropMask
                    # Set any 0. to np.nan for calculation purposes
                    trop[trop == 0.] = np.nan
                    # Sum over lev, lat, lon to generate burden timeseries
                    chemopause_burden_tmp = np.nansum(trop, axis=(1, 2, 3))
                    # Annual mean
                    chemopause_burden_tmp = np.nanmean(chemopause_burden_tmp)
                    if (yr % 5 == 0):
                        print("")
                        print("Year: %s | ChemoPause Burden: %i Tg" %
                              (yr, chemopause_burden_tmp/1e9))
                    tempOutputList_chmp.append(chemopause_burden_tmp)

            # Assign the list to the correct location in the Pandas DataFrame
            pressure_excl_burden[run] = tempOutputList_excl

            if tropoPause_incl == True:
                pressure_incl_burden[run] = tempOutputList_incl

            chemopause_burden[run] = tempOutputList_chmp

    if tropoPause_incl:
        return pressure_excl_burden, pressure_incl_burden, chemopause_burden
    else:
        return pressure_excl_burden, chemopause_burden


print("""
__  __ ____  ___      _____ ____  __  __ ____
|  \/  |  _ \|_ _|    | ____/ ___||  \/  |___ \\
| |\/| | |_) || |_____|  _| \___ \| |\/| | __) |  _____ _____
| |  | |  _ < | |_____| |___ ___) | |  | |/ __/  |_____|_____|
|_|  |_|_| \_\___|    |_____|____/|_|  |_|_____|

_     _     _             _           _        _
| |__ (_)___| |_ ___  _ __(_) ___ __ _| |  _ __/ |
| '_ \| / __| __/ _ \| '__| |/ __/ _` | | | '__| |
| | | | \__ \ || (_) | |  | | (_| (_| | | | |  | |
|_| |_|_|___/\__\___/|_|  |_|\___\__,_|_| |_|  |_|"""
      )

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "historical"
ensembles = ["r1i1p1f1"]  # , "r2i1p1f1", "r3i1p1f1", "r4i1p1f1",  "r5i1p1f1"]
centre = "MRI"
model = "MRI-ESM2-0"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(1850, 2015, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/CMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",
                                                                           manualAreaPath=manualAreaPath)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})
pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl_r1.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause_r1.csv")


print("""
__  __ ____  ___      _____ ____  __  __ ____
|  \/  |  _ \|_ _|    | ____/ ___||  \/  |___ \
| |\/| | |_) || |_____|  _| \___ \| |\/| | __) |  _____ _____
| |  | |  _ < | |_____| |___ ___) | |  | |/ __/  |_____|_____|
|_|  |_|_| \_\___|    |_____|____/|_|  |_|_____|

_     _     _             _           _       ____            ____
| |__ (_)___| |_ ___  _ __(_) ___ __ _| |  _ _|___ \      _ __| ___|
| '_ \| / __| __/ _ \| '__| |/ __/ _` | | | '__|__) |____| '__|___ \
| | | | \__ \ || (_) | |  | | (_| (_| | | | |  / __/_____| |   ___) |
|_| |_|_|___/\__\___/|_|  |_|\___\__,_|_| |_| |_____|    |_|  |____/"""
      )

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "historical"
ensembles = ["r2i1p1f1", "r3i1p1f1", "r4i1p1f1",  "r5i1p1f1"]
centre = "MRI"
model = "MRI-ESM2-0"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(1850, 2015, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/gws/nopw/j04/aerchemmip_vol3/users/ptg21/MRI/historical/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",
                                                                           manualAreaPath=manualAreaPath)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})
pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl_r2-r5.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause_r2-r5.csv")


print("""
__  __ ____  ___      _____ ____  __  __ ____
|  \/  |  _ \|_ _|    | ____/ ___||  \/  |___ \\
| |\/| | |_) || |_____|  _| \___ \| |\/| | __) |  _____ _____
| |  | |  _ < | |_____| |___ ___) | |  | |/ __/  |_____|_____|
|_|  |_|_| \_\___|    |_____|____/|_|  |_|_____|

____ ____  ____ __________ ___
/ ___/ ___||  _ \___ /___  / _ \\
\___ \___ \| |_) ||_ \  / / | | |
___) |__) |  __/___) |/ /| |_| |
|____/____/|_|  |____//_/  \___/
""")

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "ssp370"
ensembles = ["r1i1p1f1", "r2i1p1f1",  "r3i1p1f1"]
centre = "MRI"
model = "MRI-ESM2-0"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(2015, 2100, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/ScenarioMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",
                                                                           manualAreaPath=manualAreaPath, MRI_hist=False)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})
pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")


print("""
 ____ _____ ____  __  __ ____    __        ___    ____ ____ __  __
/ ___| ____/ ___||  \/  |___ \   \ \      / / \  / ___/ ___|  \/  |
| |   |  _| \___ \| |\/| | __) |___\ \ /\ / / _ \| |  | |   | |\/| |
| |___| |___ ___) | |  | |/ __/_____\ V  V / ___ \ |__| |___| |  | |
\____|_____|____/|_|  |_|_____|     \_/\_/_/   \_\____\____|_|  |_|

              _     _     _             _           _
             | |__ (_)___| |_ ___  _ __(_) ___ __ _| |
_____ _____  | '_ \| / __| __/ _ \| '__| |/ __/ _` | |
|_____|_____| | | | | \__ \ || (_) | |  | | (_| (_| | |
             |_| |_|_|___/\__\___/|_|  |_|\___\__,_|_|
             """)


baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "historical"
ensembles = ["r1i1p1f1",  "r2i1p1f1",  "r3i1p1f1"]
centre = "NCAR"
model = "CESM2-WACCM"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(1850, 2015, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/CMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")


print("""
 ____ _____ ____  __  __ ____    __        ___    ____ ____ __  __
/ ___| ____/ ___||  \/  |___ \   \ \      / / \  / ___/ ___|  \/  |
| |   |  _| \___ \| |\/| | __) |___\ \ /\ / / _ \| |  | |   | |\/| |
| |___| |___ ___) | |  | |/ __/_____\ V  V / ___ \ |__| |___| |  | |
\____|_____|____/|_|  |_|_____|     \_/\_/_/   \_\____\____|_|  |_|

              ____ ____  ____ __________ ___         _
             / ___/ ___||  _ \___ /___  / _ \   _ __/ |
_____ _____  \___ \___ \| |_) ||_ \  / / | | | | '__| |
|_____|_____|  ___) |__) |  __/___) |/ /| |_| | | |  | |
             |____/____/|_|  |____//_/  \___/  |_|  |_|      
     
     """)

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "ssp370"
ensembles = ["r1i1p1f1"]  # , "r2i1p1f1",  "r3i1p1f1"  ]
centre = "NCAR"
model = "CESM2-WACCM"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(2015, 2100, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/ScenarioMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl_r1.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause_r1.csv")

print("""
  ____ _____ ____  __  __ ____    __        ___    ____ ____ __  __
 / ___| ____/ ___||  \/  |___ \   \ \      / / \  / ___/ ___|  \/  |
| |   |  _| \___ \| |\/| | __) |___\ \ /\ / / _ \| |  | |   | |\/| |
| |___| |___ ___) | |  | |/ __/_____\ V  V / ___ \ |__| |___| |  | |
 \____|_____|____/|_|  |_|_____|     \_/\_/_/   \_\____\____|_|  |_|

               ____ ____  ____ __________ ___        ____        _____
              / ___/ ___||  _ \___ /___  / _ \   _ _|___ \   _ _|___ /
 _____ _____  \___ \___ \| |_) ||_ \  / / | | | | '__|__) | | '__||_ \\
|_____|_____|  ___) |__) |  __/___) |/ /| |_| | | |  / __/  | |  ___) |
              |____/____/|_|  |____//_/  \___/  |_| |_____| |_| |____/
""")

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "ssp370"
ensembles = ["r2i1p1f1", "r3i1p1f1"]
centre = "NCAR"
model = "CESM2-WACCM"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/MRI/areacella_estimated_MRI-ESM2-0_historical.npy"

# Integer years of interest
years = np.arange(2015, 2056, 1)

# Variable name
variables = ["o3"]  # ,"co"]
molarMasses = [47.996]  # ,28.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/ScenarioMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath)
# otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl_r2-r3.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause_r2-r3.csv")


print(""" 
_   _ _  _______ ____  __  __ _
| | | | |/ / ____/ ___||  \/  / |
| | | | ' /|  _| \___ \| |\/| | |  _____ _____
| |_| | . \| |___ ___) | |  | | | |_____|_____|
\___/|_|\_\_____|____/|_|  |_|_|

_     _     _             _           _
| |__ (_)___| |_ ___  _ __(_) ___ __ _| |
| '_ \| / __| __/ _ \| '__| |/ __/ _` | |
| | | | \__ \ || (_) | |  | | (_| (_| | |
|_| |_|_|___/\__\___/|_|  |_|\___\__,_|_|""")

base = "/gws/nopw/j04/aerchemmip_vol3/users/ptg21/o3.tmp/"
baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "historical"
ensembles = [
    "r11i1p1f2", "r16i1p1f2", "r18i1p1f2", "r1i1p1f2", "r3i1p1f2", "r5i1p1f3",
    "r7i1p1f3", "r9i1p1f2", "r10i1p1f2",
    "r12i1p1f2", "r17i1p1f2", "r19i1p1f2", "r2i1p1f2",
    "r4i1p1f2", "r6i1p1f3", "r8i1p1f2"]
centre = "MOHC"
model = "UKESM1-0-LL"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"

# Integer years of interest
years = np.arange(1850, 2015, 1)

# Variable name
# variables = ["ch4","o3"]
# molarMasses = [16.043,47.997]
variables = ["o3"]
molarMasses = [47.997]
pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/CMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath,\
                                                                           otherPaths={"UKESM1-0-LL_phalfPath": baseYMS + "other_data/",\
                                                                                       "UKESM1-0-LL_airmassPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")

# # UKESM1-0-LL ScenarioMIP

print("""
_   _ _  _______ ____  __  __ _
| | | | |/ / ____/ ___||  \/  / |
| | | | ' /|  _| \___ \| |\/| | |  _____ _____
| |_| | . \| |___ ___) | |  | | | |_____|_____|
\___/|_|\_\_____|____/|_|  |_|_|

____ ____  ____ __________ ___
/ ___/ ___||  _ \___ /___  / _ \\
\___ \___ \| |_) ||_ \  / / | | |
___) |__) |  __/___) |/ /| |_| |
|____/____/|_|  |____//_/  \___/
""")

base = "/gws/nopw/j04/aerchemmip_vol3/users/ptg21/o3.tmp/"
baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "ssp370"
ensembles = ["r10i1p1f2", "r12i1p1f2", "r17i1p1f2", "r19i1p1f2", "r2i1p1f2",
             "r4i1p1f2", "r8i1p1f2", "r11i1p1f2", "r16i1p1f2", "r18i1p1f2",
             "r1i1p1f2", "r3i1p1f2", "r9i1p1f2"]
centre = "MOHC"
model = "UKESM1-0-LL"

# Set the manual areacella path if not available on /badc
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"

# Integer years of interest
years = np.arange(2015, 2100, 1)

# Variable name
variables = ["ch4", "o3"]
molarMasses = [16.043, 47.997]
variables = ["o3"]
molarMasses = [47.997]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/ScenarioMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath,\
                                                                           otherPaths={"UKESM1-0-LL_phalfPath": baseYMS + "other_data/",\
                                                                                       "UKESM1-0-LL_airmassPath": baseYMS + "other_data/"})


pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")


# =============================================================================
print("""
 ____ _____ ____  _
/ ___|  ___|  _ \| |
| |  _| |_  | | | | |      _____ _____
| |_| |  _| | |_| | |___  |_____|_____|
\____|_|   |____/|_____|

_   _ ___ ____ _____ ___  ____  ___ ____    _    _
| | | |_ _/ ___|_   _/ _ \|  _ \|_ _/ ___|  / \  | |
| |_| || |\___ \ | || | | | |_) || | |     / _ \ | |
|  _  || | ___) || || |_| |  _ < | | |___ / ___ \| |___
|_| |_|___|____/ |_| \___/|_| \_\___\____/_/   \_\_____|""")
#
baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "historical"
ensembles = ["r1i1p1f1"]
centre = "NOAA-GFDL"
model = "GFDL-ESM4"

# Set the manual areacella path if not available on /badc
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"

# Integer years of interest
years = np.arange(1850, 2015, 1)

# Variable name
variables = ["o3"]  # ,"ch4"]
molarMasses = [47.997]  # ,16.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/CMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath,\
                                                                           otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")

# =============================================================================
print("""
 ____ _____ ____  _                     ____ ____  ____ __________ ___
/ ___|  ___|  _ \| |                   / ___/ ___||  _ \___ /___  / _ \\
| |  _| |_  | | | | |      _____ _____  \___ \___ \| |_) ||_ \  / / | | |
| |_| |  _| | |_| | |___  |_____|_____|  ___) |__) |  __/___) |/ /| |_| |
\____|_|   |____/|_____|               |____/____/|_|  |____//_/  \___/""")

baseYMS = "/gws/nopw/j04/acsis/yms23_1/"
experiment = "ssp370"
ensembles = ["r1i1p1f1"]
centre = "NOAA-GFDL"
model = "GFDL-ESM4"

# Set the manual areacella path if not available on /badc
manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GFDL/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/CESM2/areacella_fx_CESM2-WACCM_historical_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/GISS/areacella_fx_GISS-E2-1-H_piControl_r1i1p1f1_gn.nc"
#manualAreaPath = "/gws/nopw/j04/acsis/yms23_1/emicomp/UKESM/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc"

# Integer years of interest
years = np.arange(2015, 2100, 1)

# Variable name
variables = ["o3"]  # ,"ch4"]
molarMasses = [47.997]  # ,16.01]

pressure_excl_outputDataframe, chemopause_outputDataframe = calculate_vars(model=model,
                                                                           ensembles=ensembles,
                                                                           variables=variables,
                                                                           molarMasses=molarMasses,
                                                                           varPath="/badc/cmip6/data/CMIP6/ScenarioMIP/" + centre + "/" + model + "/" + experiment + "/",\
                                                                           #                                     varPath=baseYMS + "all_conc/",\
                                                                           tropopausePath=baseYMS + "other_data/",\
                                                                           manualAreaPath=manualAreaPath,\
                                                                           otherPaths={"GFDL-ESM4_psPath": baseYMS + "other_data/"})

pressure_excl_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment + "_" + str(
    years[0]) + "-" + str(years[-1]) + "_pressure_excl.csv")
chemopause_outputDataframe.to_csv("data/burdens_" + model + "_" + experiment +
                                  "_" + str(years[0]) + "-" + str(years[-1]) + "_chemopause.csv")
