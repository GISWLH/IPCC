# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/linear-trends_R.ipynb

# %% cell 4
options(java.parameters = "-Xmx8g")
library(loadeR)
library(transformeR)
library(visualizeR) # spatialPlot
library(geoprocessoR)
library(climate4R.indices) # linearTrend

# %% cell 6
library(magrittr)
library(sp)
library(RColorBrewer)
library(rgdal) # readOGR

# %% cell 9
regs <- get(load("../reference-regions/IPCC-WGI-reference-regions-v4_R.rda")) %>% as("SpatialPolygons")

# %% cell 11
regs.area <- c("NWN", "NEN", "WNA", "CNA","ENA","NCA") # North America regions

# %% cell 13
regs <- regs[regs.area]
plot(regs)

# %% cell 15
coast <- readOGR("auxiliary-material/WORLD_coastline.shp")

# %% cell 17
UDG.datasets()$OBSERVATIONS

# %% cell 19
lonLim <- c(168.0, -50)
latLim <- c(2.2, 85)

# %% cell 21
years <- 1980:2014

# %% cell 24
var <- "pr"

# %% cell 31
grid <- loadGridData("auxiliary-material/W5E5_NorthAmerica_pr_1980-2014_yearly.nc4", var = "pr")

# %% cell 34
grid <- setGridProj(grid = grid, proj = proj4string(regs))

# %% cell 36
spatialPlot(climatology(grid),
            at = seq(0, 10, 1), 
            set.min = 0,
            set.max = 10,
            backdrop.theme = "coastline",
            col.regions = brewer.pal(n = 9, "BuPu") %>% colorRampPalette(),
            main = paste0("Climatology of total precipitation (W5E5, ", min(years), "-", max(years), ") - mm/day"),
            sp.layout = list(
                list(regs, first = FALSE, lwd = 0.6),
                list("sp.text", coordinates(regs), names(regs), first = FALSE, cex = 1)
))

# %% cell 38
grid %<>% overGrid(regs)

# %% cell 40
spatialPlot(climatology(grid),
            at = seq(0, 10, 1), 
            set.min = 0,
            set.max = 10,
            backdrop.theme = "coastline",
            col.regions = brewer.pal(n = 9, "BuPu") %>% colorRampPalette(),
            main = paste0("Climatology of total precipitation (W5E5, ", min(years), "-", max(years), ") - mm/day"),
            sp.layout = list(
                list(regs, first = FALSE, lwd = 0.6),
                list("sp.text", coordinates(regs), names(regs), first = FALSE, cex = 1)
))

# %% cell 42
trendGrid <- linearTrend(grid) %>% subsetGrid(var = "b")

# %% cell 46
spatialPlot(trendGrid, 
            col.regions = brewer.pal(n = 9, "BrBG") %>% colorRampPalette(),
            at = seq(-0.1, 0.1, 0.01), 
            set.min = -0.1,
            set.max = 0.1,
            main = paste("Linear trends of the annual total precipitaion (mm/day) - W5E5"),
            sp.layout = list(  
            list(regs, first = FALSE, lwd = 0.6),
            list(coast, col = "gray50", first = FALSE, lwd = 0.6),  
            list("sp.text", coordinates(regs), names(regs), first = FALSE, cex = 1)
))

# %% cell 48
pvalGrid <- linearTrend(grid) %>% subsetGrid(var = "pval")
pvalGrid <- binaryGrid(pvalGrid, threshold = 0.1, condition = "GT")

# %% cell 50
spatialPlot(pvalGrid)

# %% cell 52
mask <- binaryGrid(climatology(grid),condition = "GE", threshold = 0, values = c(NA,1))
pvalGrid <- gridArithmetics(pvalGrid, mask)

# %% cell 53
spatialPlot(pvalGrid)

# %% cell 55
hatching.lines <- lapply(c("45","-45"), FUN = function(angle) {
  c(map.hatching(clim = climatology(pvalGrid), 
                 threshold = 0.5, 
                 condition = "GE", 
                 density = 4,
                 angle = angle, coverage.percent = 50,
                 upscaling.aggr.fun = list(FUN = "mean", na.rm = TRUE)
  ), 
  "which" = 1, lwd = 0.5)
})

# %% cell 57
spatialPlot(trendGrid, 
            col.regions = brewer.pal(n = 9, "BrBG") %>% colorRampPalette(),
            at = seq(-0.1, 0.1, 0.01), 
            set.min = -0.1,
            set.max = 0.1,
            main = paste("Linear trend of total precipitation (mm/day) - W5E5"),
            sp.layout = list(
              hatching.lines[[1]],
              hatching.lines[[2]],  
              list(regs, first = FALSE, lwd = 0.6),
              list(coast, col = "gray50", first = FALSE, lwd = 0.6),  
              list("sp.text", coordinates(regs), names(regs), first = FALSE, cex = 1)
            )
)

# %% cell 59
grid.regs <- lapply(names(regs), function(r) overGrid(grid, regs[r]))

# %% cell 61
spatialPlot(climatology(grid.regs[["NWN"]]), 
            col.regions = brewer.pal(n = 9, "BuPu") %>% colorRampPalette()
)

# %% cell 63
spatial.mean <- function(grid) aggregateGrid(grid, aggr.spatial = list(FUN = "mean", na.rm = TRUE)) %>% scaleGrid(type = "center")
grid.anom <- lapply(grid.regs, spatial.mean)

# %% cell 65
names(grid.anom)

# %% cell 67
trend.val <- lapply(1:length(grid.anom), FUN = function(x) {
    aux <- linearTrend(grid.anom[[x]]) %>% subsetGrid(var = "b")
    round(aux$Data[1], digits = 3)
})
names(grid.anom) <- sprintf("%s (%g mm/day/yr)", names(grid.anom), trend.val)

# %% cell 68
names(grid.anom)

# %% cell 69
temporalPlot(grid.anom,
               xyplot.custom = list(
                 main = "Precipitation anomaly time series (mm/day)", ylim=c(-0.65, 0.65)
               ))

# %% cell 71
sessionInfo()
