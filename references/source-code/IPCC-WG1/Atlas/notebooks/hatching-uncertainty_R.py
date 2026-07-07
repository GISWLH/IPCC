# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/hatching-uncertainty_R.ipynb

# %% cell 5
library(loadeR)
library(visualizeR)
library(sp)

# %% cell 7
source("../datasets-interactive-atlas/hatching-functions/hatching-functions.R")
source("../datasets-interactive-atlas/hatching-functions/AR6-WGI-hatching.R")

# %% cell 9
di <- dataInventory("auxiliary-material/CMIP6_SAM_historical_JJA_pr_1850-1900_annual.nc")
str(di)

# %% cell 11
ref <- loadGridData("auxiliary-material/CMIP6_SAM_historical_JJA_pr_1850-1900_annual.nc", var = "pr")
delta <- loadGridData("auxiliary-material/CMIP6_SAM_ssp585_JJA_pr_2081-2100_delta.nc", var = "pr")

# %% cell 13
pl.simple.sam <- AR6.WGI.hatching(delta = delta, method = "simple", 
                                  map.hatching.args = list(density = 2, lwd = 1.2), 
                                  color.theme = "BrBG")

# %% cell 14
pl.simple.sam

# %% cell 16
rel.delta <- loadGridData("auxiliary-material/CMIP6_SAM_ssp585_JJA_pr_2081-2100_relative_delta.nc", var = "pr")
pl.simple.sam <- AR6.WGI.hatching(delta = delta, relative.delta = rel.delta, method = "simple", 
                                  map.hatching.args = list(density = 2, lwd = 1.2), 
                                  color.theme = "BrBG", set.max = 50, set.min = -50)

# %% cell 17
pl.simple.sam

# %% cell 19
pl.advanced.sam <- AR6.WGI.hatching(delta = delta, historical.ref = ref, relative.delta = rel.delta, method = "advanced", 
                                  map.hatching.args = list(density = 1, lwd = 0.7), 
                                  color.theme = "BrBG", set.max = 50, set.min = -50)

# %% cell 20
pl.advanced.sam

# %% cell 23
di <- dataInventory("auxiliary-material/CMIP6_historical_JJA_pr_1995-2014.nc")

# %% cell 25
hist <- loadGridData("auxiliary-material/CMIP6_historical_JJA_pr_1995-2014.nc", var = "pr")
scen <- loadGridData("auxiliary-material/CMIP6_ssp585_JJA_pr_2081-2100.nc", var = "pr")

# %% cell 28
delta <- gridArithmetics(climatology(scen), climatology(hist), operator = "-")
ensemble.mean <- function(grid) aggregateGrid(grid, aggr.mem = list(FUN = mean, na.rm = T))
delta.ens <- ensemble.mean(delta)
hist.ens <- ensemble.mean(climatology(hist))
# Relative delta
rel.delta <- gridArithmetics(delta.ens, 
                             hist.ens, 
                             100, 
                             operator = c("/", "*"))

# %% cell 30
spatialPlot(delta, backdrop.theme = "coastline", main = "delta", 
           set.max = 5, set.min = -5, color.theme = "BrBG")

# %% cell 32
spatialPlot(rel.delta, backdrop.theme = "coastline", main = "relative delta", 
           set.max = 60, set.min = -60, color.theme = "BrBG")

# %% cell 35
simple <- aggregateGrid(delta, aggr.mem = list(FUN = agreement, th = 80))
spatialPlot(simple)

# %% cell 37
simple.hatch <- map.hatching(clim = climatology(simple), threshold = "0.5", angle = "-45",
                             condition = "LT", density = 4,  lwd = 0.6,
                             upscaling.aggr.fun = list(FUN = mean))
plot(simple.hatch[[2]])

# %% cell 39
pl.simple <- spatialPlot(rel.delta, 
            color.theme = "BrBG", 
            at = seq(-60, 60, 5), 
            set.max = 60, set.min = -60,
            backdrop.theme = "coastline",
            main = list("Mean delta change", cex = 0.8),
            xlab = list("Period: 2081-2100, Season: JJA", cex = 0.8),
            sp.layout = list(simple.hatch),
            par.settings = list(axis.line = list(col = 'transparent')))
pl.simple

# %% cell 42
sign <- loadGridData("auxiliary-material/CMIP6_ssp585_JJA_pr_2081-2100_signal.nc", var = "pr_signal")

# %% cell 44
advanced1 <- aggregateGrid(sign, aggr.mem = list(FUN = signal.ens1, th = 66))

# %% cell 45
advanced2.aux <- aggregateGrid(sign, aggr.mem = list(FUN = signal.ens2, th = 66))

# %% cell 47
spatialPlot(advanced1, main = "no signal = 0")
spatialPlot(advanced2.aux, main = "no signal = 1")

# %% cell 49
advanced2.aux <- gridArithmetics(advanced2.aux, simple, operator = "+") 
spatialPlot(advanced2.aux)

# %% cell 51
advanced2 <- binaryGrid(advanced2.aux, condition = "GT", threshold = 0)
spatialPlot(advanced2)

# %% cell 53
my.hatching <- function(grid, angle) map.hatching(grid, threshold = 0.8, angle = angle,
                                       condition = "LT", density = 4,  lwd = 0.6,
                                       upscaling.aggr.fun = list(FUN = mean))
advanced1.hatch <- my.hatching(climatology(advanced1), "-45")
advanced2.hatch <- my.hatching(climatology(advanced2),  "45")
advanced2.hatch.bis <- my.hatching(climatology(advanced2), "-45")

# %% cell 54
plot(advanced1.hatch[[2]])
plot(advanced2.hatch[[2]], add = TRUE)
plot(advanced2.hatch.bis[[2]], add = TRUE)

# %% cell 56
pl.advanced <- spatialPlot(rel.delta, 
            color.theme = "BrBG", 
            at = seq(-60, 60, 5), 
            set.max = 60, set.min = -60,
            backdrop.theme = "coastline",
            main = list("Mean delta change", cex = 0.8),
            xlab = list("Period: 2081-2100, Season: JJA", cex = 0.8),
            sp.layout = list(advanced1.hatch, advanced2.hatch, advanced2.hatch.bis),
            par.settings = list(axis.line = list(col = 'transparent')))
pl.advanced

# %% cell 59
sessionInfo()
