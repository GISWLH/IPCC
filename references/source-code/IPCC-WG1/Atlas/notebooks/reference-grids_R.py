# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/reference-grids_R.ipynb

# %% cell 4
library(loadeR)
library(visualizeR)
library(convertR)

# %% cell 6
# global reference 1º land/sea mask
mask <- loadGridData("../reference-grids/land_sea_mask_1degree.nc4", var = "sftlf")

# %% cell 8
# plotting mask
spatialPlot(mask)

# %% cell 10
# loading global mean temperature
tas <- loadGridData("auxiliary-material/CMIP6Amon_tas_CanESM5_r1i1p1f1_historical_gn_185001-201412.nc", 
                    var = "tas", years = 2000:2010)

# %% cell 12
# plotting climatology
spatialPlot(climatology(tas), backdrop.theme = "coastline", rev.colors = TRUE)

# %% cell 14
attributes(getGrid(tas))$resX
attributes(getGrid(tas))$resY

# %% cell 16
# Note: This cell may take a while to run 
tas.i <- interpGrid(tas, getGrid(mask), method = "bilinear")

# %% cell 17
attributes(getGrid(tas.i))$resX
attributes(getGrid(tas.i))$resY

# %% cell 19
# binary 1º land/sea mask
land <- binaryGrid(mask, condition = "GT", threshold = 0.999, values = c(NA, 1))
spatialPlot(land)

# %% cell 21
masktimes <- rep(list(land), getShape(tas.i, "time"))
mask2apply <- bindGrid(masktimes, dimension = "time")

# %% cell 23
tas.i.land <- gridArithmetics(tas.i, mask2apply, operator = "*")

# final land-only temperature data
spatialPlot(climatology(tas.i.land), rev.colors = TRUE)

# %% cell 25
# monthly time-series (in K)
temporalPlot(tas.i, tas.i.land, x.axis = "index")

# %% cell 27
# monthly time-series (in Celsius degrees)
tas.i.degC <- udConvertGrid(tas.i, new.units = "degC")
tas.i.land.degC <- udConvertGrid(tas.i.land, new.units = "degC")
temporalPlot(tas.i.degC, tas.i.land.degC, x.axis = "index")

# %% cell 29
sessionInfo()
