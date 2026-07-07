# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/bias-adjustment_R.ipynb

# %% cell 4
library(loadeR) 
library(climate4R.UDG) 
library(transformeR)
library(downscaleR)
library(climate4R.indices)
library(visualizeR)
library(rgdal)

# %% cell 6
lons <- c(-9.25, 3.5)  # Iberian Peninsula
lats <- c(36, 44)   # Iberian Peninsula

season <- 6:8  # June-July-August
years.hist <- 1986:2005
years.rcp <- 2041:2060

dataset.obs <- "W5E5" 
dataset.hist <- "CMIP5_EC-EARTH_r12i1p1_historical"
dataset.rcp <- "CMIP5_EC-EARTH_r12i1p1_rcp85"

# %% cell 14
file.obs <- "auxiliary-material/W5E5_IP_tas-tasmin-tasmax_1986-2005_JJA.nc"
file.hist <- "auxiliary-material/CMIP5_EC-EARTH_r12i1p1_historical_IP_tas-tasmin-tasmax_1986-2005_JJA.nc"
file.rcp <- "auxiliary-material/CMIP5_EC-EARTH_r12i1p1_rcp85_IP_tas-tasmin-tasmax_2041-2060_JJA.nc"

# Loading mean temperature
y.tas <- loadGridData(file.obs, var = "tas")
x.tas <- loadGridData(file.hist, var = "tas")
newdata.tas <- loadGridData(file.rcp, var = "tas")

# Loading minimum temperature
y.tasmin <- loadGridData(file.obs, var = "tasmin")
x.tasmin <- loadGridData(file.hist, var = "tasmin")
newdata.tasmin <- loadGridData(file.rcp, var = "tasmin")

# Loading maximum temperature
y.tasmax <- loadGridData(file.obs, var = "tasmax")
x.tasmax <- loadGridData(file.hist, var = "tasmax")
newdata.tasmax <- loadGridData(file.rcp, var = "tasmax")

# %% cell 16
hist.tas <- interpGrid(x.tas, new.coordinates = getGrid(y.tas), method = "nearest")
hist.tasmin <- interpGrid(x.tasmin, new.coordinates = getGrid(y.tasmin), method = "nearest")
hist.tasmax <- interpGrid(x.tasmax, new.coordinates = getGrid(y.tasmax), method = "nearest")

# %% cell 18
bias.tas <- gridArithmetics(climatology(hist.tas), climatology(y.tas), operator = "-")
bias.tasmax <- gridArithmetics(climatology(hist.tasmax), climatology(y.tasmax), operator = "-")
bias.tasmin <- gridArithmetics(climatology(hist.tasmin), climatology(y.tasmin), operator = "-")

# %% cell 20
spatialPlot(suppressMessages(makeMultiGrid(bias.tas, bias.tasmax, bias.tasmin, skip.temporal.check = TRUE)), 
            backdrop.theme = "coastline", 
            names.attr = c("Mean temperature", "Maximum Temperature", "Minimum Temperature"),
            main = "EC-EARTH biases (degC)", layout = c(1, 3), as.table = TRUE, 
            set.min = -6, set.max = 6, at = seq(-6, 6, 12/20), rev.colors = TRUE)

# %% cell 22
# Observed TX35, year by year
index.obs <- redim(indexGrid(tx = y.tasmax, index.code = "TXth", th = 35, time.resolution = "year"), 
                   drop = TRUE)
# Simulated TX35, year by year
index.raw <- redim(indexGrid(tx = hist.tasmax, index.code = "TXth", th = 35, time.resolution = "year"), 
                   drop = TRUE)

tx35.obs <- climatology(index.obs)  # Mean value
tx35.raw <- climatology(index.raw)  # Mean value
bias.tx35 <- gridArithmetics(tx35.raw, tx35.obs, operator = "-")  # Bias

# %% cell 23
spatialPlot(bias.tx35, backdrop.theme = "coastline", main = "EC-EARTH bias in TX35 (days/year)", 
            set.min = -30, set.max = 30, 
            at = seq(-30, 30, 60/20),
            rev.colors = TRUE)

# %% cell 26
# Range
y.range <- gridArithmetics(y.tasmax, y.tasmin, operator = "-")
x.range <- gridArithmetics(x.tasmax, x.tasmin, operator = "-")
newdata.range <- gridArithmetics(newdata.tasmax, newdata.tasmin, operator = "-")

# Skewness
y.skew <- gridArithmetics(gridArithmetics(y.tas, y.tasmin, operator = "-"), y.range, operator = "/")
x.skew <- gridArithmetics(gridArithmetics(x.tas,x.tasmin, operator = "-"), x.range, operator = "/")
newdata.skew <- gridArithmetics(gridArithmetics(newdata.tas, newdata.tasmin, operator = "-"), 
                                newdata.range, operator = "/")

# %% cell 28
# List of arguments that have to be passed to the "biasCorrection" function when using the ISIMIP3 method
isimip3.args = list(lower_bound = NULL,lower_threshold = NULL, upper_bound = NULL, 
                    upper_threshold = NULL,  randomization_seed =  NULL, 
                    detrend = array(data = TRUE, dim = 1), rotation_matrices = NULL, 
                    n_quantiles = 50, distribution = "normal", 
                    trend_preservation = array(data = "additive", dim = 1), 
                    adjust_p_values = array(data = FALSE, dim = 1), if_all_invalid_use = NULL, 
                    invalid_value_warnings = FALSE)

# Adjusting historical simulations
bc.tas.hist <- biasCorrection(y = y.tas, x = x.tas, newdata = x.tas, "precipitation" = FALSE, 
                         method = "isimip3", isimip3.args = isimip3.args)
# Adjusting future simulations
bc.tas <- biasCorrection(y = y.tas, x = x.tas, newdata = newdata.tas, "precipitation" = FALSE, 
                         method = "isimip3", isimip3.args = isimip3.args)

# %% cell 30
# List of arguments that have to be passed to the "biasCorrection" function when using the ISIMIP3 method
isimip3.range.args = list(lower_bound = 0, lower_threshold = 0.01, upper_bound = NULL, 
                            upper_threshold = NULL, randomization_seed = NULL, 
                            detrend = array(data = FALSE, dim = 1), rotation_matrices =  NULL, 
                            n_quantiles = 50, distribution = "rice", 
                            trend_preservation = array(data = "mixed", dim = 1),
                            adjust_p_values = array(data = FALSE, dim = 1), if_all_invalid_use = NULL, 
                            invalid_value_warnings = FALSE)

# Adjusting historical simulations
bc.range.hist <- biasCorrection(y = y.range, x = x.range, newdata = x.range, "precipitation" = FALSE, 
                                method = "isimip3", isimip3.args = isimip3.range.args)
# Adjusting future simulations                           
bc.range <- biasCorrection(y = y.range, x = x.range, newdata = newdata.range, "precipitation" = FALSE, 
                           method = "isimip3", isimip3.args = isimip3.range.args)

# %% cell 32
# List of arguments that have to be passed to the "biasCorrection" function when using the ISIMIP3 method
isimip3.skew.args  =  list(lower_bound =  c(0), lower_threshold =  c(0.0001), upper_bound =  c(1), 
                           upper_threshold =  c(0.9999), randomization_seed =  NULL,
                           detrend =  array(data  =  FALSE, dim = 1), rotation_matrices =  c(NULL), 
                           n_quantiles = 50, distribution =  c("beta"), 
                           trend_preservation = array(data = "bounded", dim = 1), 
                           adjust_p_values = array(data  =  FALSE, dim = 1), if_all_invalid_use  =  c(NULL),
                           invalid_value_warnings  =  FALSE)

# Adjusting historical simulations
bc.skew.hist <- biasCorrection(y = y.skew, x = x.skew, newdata = x.skew, "precipitation" = FALSE, 
                          method = "isimip3", isimip3.args = isimip3.skew.args)
# Adjusting future simulations
bc.skew <- biasCorrection(y = y.skew, x = x.skew, newdata = newdata.skew, "precipitation" = FALSE, 
                          method = "isimip3", isimip3.args = isimip3.skew.args)

# %% cell 34
# Bias-adjusted historical temperatures
bc.tasmin.hist <- gridArithmetics(bc.tas.hist, gridArithmetics(bc.range.hist, bc.skew.hist, operator = "*"), 
                                  operator = "-")
bc.tasmax.hist <- gridArithmetics(bc.tasmin.hist, bc.range.hist, operator = "+")

# Bias-adjusted future temperatures
bc.tasmin <- gridArithmetics(bc.tas, gridArithmetics(bc.range, bc.skew, operator = "*"), 
                             operator = "-")
bc.tasmax <- gridArithmetics(bc.tasmin, bc.range, operator = "+")

# %% cell 36
# Bias-adjusted TX35 for the historical period, year by year
index.hist <- redim(indexGrid(tx = bc.tasmax.hist, index.code = "TXth", th = 35, 
                              time.resolution = "year"), drop = TRUE)
tx35.hist <- climatology(index.hist)  # Mean value (number of days/year)

# Bias-adjusted TX35 for the future period of interest, year by year
index.rcp <- redim(indexGrid(tx = bc.tasmax, index.code = "TXth", th = 35, 
                             time.resolution = "year"), drop = TRUE)
tx35.rcp <- climatology(index.rcp) # Mean value (number of days/year)

# %% cell 37
spatialPlot(makeMultiGrid(tx35.hist, tx35.rcp, skip.temporal.check = TRUE), backdrop.theme = "coastline", 
            color.them = "Reds", names.attr = c("Historical (1986-2005)","Projected (2041-2060, RCP8.5)"),
            main = "Bias-adjusted TX35 (days/year)", as.table = TRUE, set.min = 0, set.max = 60, at = seq(0,60,5))

# %% cell 39
sessionInfo()
