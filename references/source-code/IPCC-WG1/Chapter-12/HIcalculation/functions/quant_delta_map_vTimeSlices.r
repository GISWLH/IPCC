#Function that applies bias correction using quantile delta mapping (QDM) for different time slices
#Input:
#  - model_grid: Model name (string)
#  - fname_OBS: File name of heat stress indicator for reference dataset for bias correction (string)
#  - fname_MOD: File name of heat stress indicator for model dataset (string)
#  - dir_data: Folder where data are stored (string)
#  - folder_out: Output folder (string)
#  - var_name: Name of variable to be bias corrected (string)
#  - time_ref: Vector indicating reference period (2-element vector)
#  - time_app: Vector indicating application period (2-element vector)
#  - time_mod: Vector indicating the whole time period for which data is present in fname_MOD (2 element vector)
#  - DOYs: Number of days per year (string)
#  - mask_land: Flag that indicates if only the land gridponts or all gridpoints should be included (bool)
quant_delta_map_vTimeSlices <- function(model_grid, fname_OBS, fname_MOD, dir_data, folder_out, var_name, time_ref, time_app, time_mod, DOYs=365, mask_land=TRUE) {

    #Load libraries
    .libPaths(c("/uio/kant/div-cicero-u1/clems/R/x86_64-conda_cos6-linux-gnu-library/3.5", .libPaths()))
    library(MBC)
    library(ncdf4)
    library(doParallel)
    library(feather)

    #Define file names
    f_name_YEARS_MOD  <- paste0(dir_data, 'CMIP6/CMIP6_merged/', toString(time_mod[1]), '-', toString(time_mod[2]), '_dates_YEARS_', toString(DOYs), '.csv')
    f_name_MONTHS_MOD <- paste0(dir_data, 'CMIP6/CMIP6_merged/', toString(time_mod[1]), '-', toString(time_mod[2]), '_dates_MONTHS_', toString(DOYs), '.csv')
    f_name_YEARS_ERA  <- paste0(dir_data, 'ERA5/ERA5_regrid/', toString(time_ref[1]), '-', toString(time_ref[2]), '_dates_YEARS_365.csv')
    f_name_MONTHS_ERA <- paste0(dir_data, 'ERA5/ERA5_regrid/', toString(time_ref[1]), '-', toString(time_ref[2]), '_dates_MONTHS_365.csv')
    fname_gridsel     <- paste('/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Land_sea_masks/Land_without_Antarctica_', model_grid, '.nc', sep="")

    #Read years and months
    YR_MOD <- read.csv(file=f_name_YEARS_MOD, header=FALSE, sep=",")
    MN_MOD <- read.csv(file=f_name_MONTHS_MOD, header=FALSE, sep=",")
    YR_ERA <- read.csv(file=f_name_YEARS_ERA, header=FALSE, sep=",")
    MN_ERA <- read.csv(file=f_name_MONTHS_ERA, header=FALSE, sep=",")

    #Select data for reference and application periods
    sel_ref_OBS <- YR_ERA>=time_ref[1] & YR_ERA<=time_ref[2]
    sel_ref_MOD <- YR_MOD>=time_ref[1] & YR_MOD<=time_ref[2]
    sel_app_MOD <- YR_MOD>=time_app[1] & YR_MOD<=time_app[2]

    #Get months in reference and application periods
    mon_ref_ERA  <- MN_ERA[sel_ref_OBS]
    mon_ref_MOD  <- MN_MOD[sel_ref_MOD]
    mon_app_MOD  <- MN_MOD[sel_app_MOD]

    #Create indices for selecting right time for NetCDF files
    sta_ref_OBS = c(1, 1, which(sel_ref_OBS)[1])
    sta_ref_MOD = c(1, 1, which(sel_ref_MOD)[1])
    sta_app_MOD = c(1, 1, which(sel_app_MOD)[1])
    len_ref_OBS = c(-1, -1, sum(sel_ref_OBS))
    len_ref_MOD = c(-1, -1, sum(sel_ref_MOD))
    len_app_MOD = c(-1, -1, sum(sel_app_MOD))

    #Open data sets
    nc_OBS <- nc_open(fname_OBS)
    nc_MOD <- nc_open(fname_MOD)

    #Read data
    data_OBS_ref <- ncvar_get(nc_OBS, var_name, start=sta_ref_OBS, count=len_ref_OBS)
    data_MOD_ref <- ncvar_get(nc_MOD, var_name, start=sta_ref_MOD, count=len_ref_MOD)
    data_MOD_app <- ncvar_get(nc_MOD, var_name, start=sta_app_MOD, count=len_app_MOD)

    #Close NetCDFs
    nc_close(nc_OBS)
    nc_close(nc_MOD)

    #Create indicex for all grid points, on which to carry out the analysis
    if (mask_land==TRUE) {

        #Read which grid cells to consider
        nc_gridsel   <- nc_open(fname_gridsel)
        data_gridsel <- ncvar_get(nc_gridsel, "selection")
        vec_gridsel  <- as.vector(data_gridsel) #Convert to vector
        nc_close(nc_gridsel)

        #Select land grid points
        ind = which(data_gridsel==1, arr.ind = T)
        N   = dim(ind)[1]

    } else {

        #Select all grid points
        data_gridsel = matrix(data=TRUE, nrow=dim(data_MOD_app)[1], ncol=dim(data_MOD_app)[2])
        ind = which(data_gridsel==TRUE, arr.ind = T)
        N   = dim(ind)[1]

    }
    
    #Define number of cores for parallel computing
    registerDoParallel(cores=40)

    #Write time selection to file
    sel_time = sel_app_MOD
    path = paste0(folder_out, 'Time_selection.feather')
    write_feather(as.data.frame(sel_time), path)

    #Loop over all selected grid points
    foreach(n=1:N) %dopar% {
    # for (n in 1:N) {

        #Select data on grid point   
        OBSref <- data_OBS_ref[ind[n,1], ind[n,2], ]
        MODref <- data_MOD_ref[ind[n,1], ind[n,2], ]
        MODapp <- data_MOD_app[ind[n,1], ind[n,2], ]

        #Create data frame for output
        QDM <- vector(,len_app_MOD[3]) * NA

        #Loop over all months
        for(i in 1:12) {

            #Select data
            selR_ERA <- mon_ref_ERA==(i%%12 + 12*(i%%12==0))
            selR_MOD <- mon_ref_MOD==(i%%12 + 12*(i%%12==0))
            selA_MOD <- mon_app_MOD==(i%%12 + 12*(i%%12==0))

            #Select data for quantile mapping calibration
            OBS_R <- OBSref[selR_ERA]
            MOD_R <- MODref[selR_MOD]
            MOD_A <- MODapp[selA_MOD]

            #Check for NaNs
            out_corr <- rep(NA, length(MOD_A))
            ch1 <- !is.nan(OBS_R)
            ch2 <- !is.nan(MOD_R)
            ch3 <- !is.nan(MOD_A)

            #Perform QDM if data is not NaN
            if (!(sum(ch1)==0 | sum(ch2)==0 | sum(ch3)==0)) {

                QDM_out <- QDM(OBS_R[ch1], MOD_R[ch2], MOD_A[ch3], ratio=FALSE, n.tau=50)

                #Consider NaNs in output
                out_corr[ch3] <- QDM_out$mhat.p 
                QDM[selA_MOD]  <- out_corr #Save in data frame
             }       

        }
        
        #Write to file
        path = paste0(folder_out, 'Grid_', toString(ind[n,1]), '_', toString(ind[n,2]), '_data.feather')
        write_feather(as.data.frame(QDM), path)
        
    }
        
    #Overwrite big data sets to make them smaller (in case they would not be deleted from cache)
    data_OBS_ref <- 0
    data_MOD_ref <- 0
    data_MOD_app <- 0

}