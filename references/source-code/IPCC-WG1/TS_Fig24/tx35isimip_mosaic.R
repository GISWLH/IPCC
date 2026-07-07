options(java.parameters = "-Xmx8g")
library(loadeR)
library(transformeR)
library(visualizeR)
library(magrittr)
library(geoprocessoR)
library(sp)
library(rgdal)
library(smoothr)
library(RColorBrewer)
library(gridExtra)
consensus <- function(x, th = 80) {
  mp <- mean(x, na.rm = TRUE)
  if (is.na(mp)) {
    1
  } else {
    if (mp > 0) {
      as.numeric(sum(as.numeric(x > 0), na.rm = TRUE) > as.integer(length(x) * th / 100))
    } else if (mp < 0) {
      as.numeric(sum(as.numeric(x < 0), na.rm = TRUE) > as.integer(length(x) * th / 100))
    } else if (mp == 0){
      1
    }
  }
}

### Choose parameters ------------------------------------------------------------------------------
scenario <- "rcp26" # either rcp26 or rcp85
period <- "2041-2060" # either 2041-2060 or 2081-2100
local_path = "Desktop/IPCC/" # path to netCDF data

# set working directory
setwd(local_path)

### Loading the IPCC regions ------------------------------------------------------------------------------
# Coast
coast <- readOGR("WORLD_coastline.shp") # available in https://github.com/IPCC-WG1/Atlas/tree/main/notebooks/auxiliary-material
proj4string(coast) <- CRS("+proj=longlat +datum=WGS84 +no_defs")
coast.rob <- spTransform(coast, CRSobj = CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
# Contour
contour <- SpatialPolygons(list(Polygons(list(Polygon(matrix(c(-180, -180, 180, 180, -180, -90, 90, 90, -90, -90), ncol = 2))), ID = "A")))
proj4string(contour) <- proj4string(coast)
contour <- densify(contour, max_distance = 0.44)
contour.rob <- spTransform(contour, CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"))
# IPCC regs
regs <- get(load("./IPCC-WGI-reference-regions-v4_R.rda")) # available in https://github.com/IPCC-WG1/Atlas/blob/main/reference-regions/IPCC-WGI-reference-regions-v4_R.rda
regs <- as(regs, "SpatialPolygons")
regs.rob <- spTransform(regs, CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))

### Sea-Land Mask (available in https://github.com/IPCC-WG1/Atlas/blob/main/reference-grids/land_sea_mask_05degree.nc4) ------------------------------------------------------------------------------
mask <- loadGridData("land_sea_mask_05degree.nc4", var = "sftlf") %>% binaryGrid(condition = "LT",threshold = 1, values = c(1,NA))

### Loading tx35 .nc files ------------------------------------------------------------------------------
grid <- loadGridData(paste0("./tx35isimip_",scenario,"_",period,"_1995-2014.nc"), var = "tx35isimip")

### Hatching ------------------------------------------------------------------------------
mask2 <- aggregateGrid(grid, aggr.mem = list(FUN = "mean", na.rm = TRUE)) %>% gridArithmetics(mask) %>% binaryGrid(condition = "GT",threshold = -9999, values = c(NA,1)) # to include land-points with NA values, e.g., Arctic or Antarctica; in addition to sea points which are NA
uncer <- aggregateGrid(grid, aggr.mem = list(FUN = consensus, th = 80)) %>% gridArithmetics(mask2)
attr(uncer$xyCoords, "projection") <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
uncer <- warpGrid(climatology(uncer), new.CRS = CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
l <- c(map.hatching(clim = climatology(uncer), 
                    threshold = 0.5, 
                    condition = "GE", 
                    density = 8,
                    angle = "45", coverage.percent = 100,
                    upscaling.aggr.fun = list(FUN = "mean", na.rm = TRUE)
), "which" = 1, lwd = 0.5)

### Compute the ensemble mean and proyect grid to robin ------------------------------------------------------------------------------
grid %<>% aggregateGrid(aggr.mem = list(FUN = "mean", na.rm = TRUE))
grid$Data[which(is.na(grid$Data), arr.ind = TRUE)] <- NA
grid %<>% gridArithmetics(mask)
attr(grid$xyCoords, "projection") <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
grid <- warpGrid(climatology(grid), new.CRS = CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))

### We display the spatial maps ------------------------------------------------------------------------------
spatialPlot(grid, 
            col.regions = c("#808080",rev(brewer.pal(n = 11, "RdBu"))[5:11]) %>% colorRampPalette(),
            at = c(-32,-31,-30,-5,-1,1,5,15,30,45,60,75,100,150,200,250), 
            set.min = -31,set.max = 250,
            main = paste("TX35 for",period,paste0("(",scenario,")"),"rel. to 1995-2014"),
            par.settings = list(axis.line = list(col = 'transparent')),
            sp.layout = list(
              l,  
              list(regs.rob, first = FALSE, lwd = 0.6),
              list(coast.rob, col = "gray50", first = FALSE, lwd = 0.6),
              list(contour.rob, col = "black", first = FALSE, lwd = 0.7)
            ))



