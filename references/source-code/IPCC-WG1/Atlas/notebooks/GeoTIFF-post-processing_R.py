# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/GeoTIFF-post-processing_R.ipynb

# %% cell 4
library(transformeR)
library(loadeR)
library(loadeR.2nc)
library(geoprocessoR)
library(visualizeR)
library(RColorBrewer)
library(sp)
library(rgdal)

# %% cell 6
map <- readGDAL("auxiliary-material/CMIP5 - Mean temperature (T) Change deg C - Long Term (2081-2100) RCP 8.5 1986-2005 - Annual (mean of 29 models).tiff")

# %% cell 8
delta <- sgdf2clim(map)

# %% cell 10
spatialPlot(delta, backdrop.theme = "coastline")

# %% cell 12
mask <- loadGridData("../reference-grids/land_sea_mask_2degree.nc4", var = "sftlf")
mask.land <- binaryGrid(mask, condition = "GT", threshold = 0.999, values = c(NA, 1))

# %% cell 14
delta.masked <- gridArithmetics(delta, mask.land, operator = "*")
spatialPlot(delta.masked, backdrop.theme = "coastline", rev.colors = TRUE)

# %% cell 16
delta.EU <- subsetGrid(delta.masked, lonLim = c(-30, 65), latLim = c(28, 75))
spatialPlot(delta.EU, backdrop.theme = "coastline", rev.colors = TRUE)

# %% cell 18
regions <- get(load("../reference-regions/IPCC-WGI-reference-regions-v4_R.rda"))
regions <- as(regions, "SpatialPolygons")
proj4string(regions) <- CRS("+init=epsg:4326")

# %% cell 20
delta.masked <- projectGrid(delta.masked, proj4string(regions))

# %% cell 22
regionnames <- c("NEU", "WCE", "EEU", "MED")

# %% cell 24
# Overly with reference regions
delta.masked.regs <- overGrid(delta.masked, regions[regionnames], subset = TRUE)

spatialPlot(delta.masked.regs,
            color.theme = "RdBu", 
            rev.colors = TRUE,
            strip = FALSE,
            as.table = TRUE,
            backdrop.theme = "coastline",
            sp.layout = list(list(regions, first = FALSE)),
            par.settings = list(axis.line = list(col = "transparent")),
            main =  list("CMIP5_DELTA_CHANGE",
                         cex = 0.7),
            at = seq(-10, 10, 1),
            set.max = 10,
            set.min = -10)

# %% cell 26
reg.averages <- sapply(regionnames, function(i){
      reg <- overGrid(delta.masked, regions[i])
      grid <- aggregateGrid(reg, aggr.spatial = list(FUN = "mean", na.rm = TRUE), weight.by.lat = TRUE)
      grid$Data
})

# %% cell 27
reg.averages

# %% cell 29
sessionInfo()
