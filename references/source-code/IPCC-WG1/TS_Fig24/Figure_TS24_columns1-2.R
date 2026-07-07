# THIS SCRIPT REPRODUCES COLUMNS 1 AND 2 OF FIGURE TS.24 (IPCC-WGI AR6).
# THIS SCRIPT USES LIBRARIES FROM THE climate4R FRAMEWORK (Iturbide et al. 2019). Go to https://github.com/SantanderMetGroup/climate4R for installation and other information. 
# THIS SCRIPT USES MATERIAL FROM THE IPCC-WGI/Atlas GitHub repository (DOI:10.5281/zenodo.5171760; clone or download: https://github.com/IPCC-WG1/Atlas).
# AUTHOR: Maialen Iturbide Martínez de Albéniz

# Load climate4R libraries for data loading, changing spatial projection and creating map figures ----------------------------------------------------------------
library(loadeR)
library(geoprocessoR)
library(visualizeR)

# Load other libraries related to the management of spatial data and graphics visualization
# (use functions install.packages("name_of_the_package") or devtools::install_github("cran/name_of_the_package") to install them) ----------------------------------
library(RColorBrewer)
library(rgdal)
library(smoothr)
library(gridExtra)

# Directory containing the data (changed by the user) ------------------------------------------------------------------------------------------------------------
data.dir <- "final_data/"

# Auxiliary data for map drawing (clone or download: https://github.com/IPCC-WG1/Atlas) --------------------------------------------------------------------------
regions <- get(load("MyDirectory/Atlas/reference-regions/IPCC-WGI-reference-regions-v4_R.rda"))
coast <- coast <- readOGR("MyDirectory/Atlas/notebooks/auxiliary-materialWORLD_coastline.shp")
world.contour <- SpatialPolygons(list(Polygons(list(Polygon(matrix(c(-180, -180, 180, 180, -180, -90, 90, 90, -90, -90), ncol = 2))), ID = "A")))
proj4string(world.contour) <- proj4string(coast)
world.contour <- densify(world.contour, max_distance = 0.44)

# Create file names objects
change.files <- c("CMIP5_TX35_rcp26_2041-2060_rel.to-1995-2014.nc", "CMIP5_TX35_rcp26_2081-2100_rel.to-1995-2014.nc",
                  "CMIP5_TX35_rcp85_2041-2060_rel.to-1995-2014.nc", "CMIP5_TX35_rcp85_2081-2100_rel.to-1995-2014.nc",
                  "CMIP6_TX35_ssp126_2041-2060_rel.to-1995-2014.nc", "CMIP6_TX35_ssp126_2081-2100_rel.to-1995-2014.nc",
                  "CMIP6_TX35_ssp585_2041-2060_rel.to-1995-2014.nc", "CMIP6_TX35_ssp585_2081-2100_rel.to-1995-2014.nc")
uncertainty.files <- c("CMIP5_TX35_rcp26_2041-2060_rel.to-1995-2014_model_agreement.nc", "CMIP5_TX35_rcp26_2081-2100_rel.to-1995-2014_model_agreement.nc",
                       "CMIP5_TX35_rcp85_2041-2060_rel.to-1995-2014_model_agreement.nc", "CMIP5_TX35_rcp85_2081-2100_rel.to-1995-2014_model_agreement.nc",
                       "CMIP6_TX35_ssp126_2041-2060_rel.to-1995-2014_model_agreement.nc", "CMIP6_TX35_ssp126_2081-2100_rel.to-1995-2014_model_agreement.nc",
                       "CMIP6_TX35_ssp585_2041-2060_rel.to-1995-2014_model_agreement.nc", "CMIP6_TX35_ssp585_2081-2100_rel.to-1995-2014_model_agreement.nc")

# Load the data --------------------------------------------------------------------------------------------------------------------------------------------------
change.grids <- lapply(paste0(data.dir, "/", change.files), loadGridData, var = "TX35")
uncertainty.grids <- lapply(paste0(data.dir, "/", uncertainty.files), loadGridData, var = "TX35_uncertainty")

# Change projection to Robinson ----------------------------------------------------------------------------------------------------------------------------------
change.grids.rob <- lapply(change.grids, function(x) warpGrid(x, new.CRS = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
uncertainty.grids.rob <- lapply(uncertainty.grids, function(x) warpGrid(x, new.CRS = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
regions.rob <- spTransform(regions, CRSobj = CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
coast.rob <- spTransform(coast, CRSobj = CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"))
world.contour.rob <- spTransform(world.contour, CRS("+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"))

hatching.density <- c(rep(3, 4), rep(6, 4))
uncertainty.sp <- lapply(1:length(uncertainty.grids.rob), function(x) map.hatching(climatology(uncertainty.grids.rob[[x]]), threshold = 0.8, angle = "45",
                                                                                   condition = "LT", density = hatching.density[x],  lwd = 0.8, col = "grey40",
                                                                                   upscaling.aggr.fun = list(FUN = mean)))


# Set graphic parameters -----------------------------------------------------------------------------------------------------------------------------------------
legend.bins <- c(-30, -5, -1, 1, 5, 15, 30, 45, 60, 75, 100, 150, 200, 250)
coltheme = "RdBu"
revc <- TRUE
color.palette <- colorRampPalette(brewer.pal(coltheme, n = 10))(22)
titles <- c("(a) TX35 for 2041-2060 (RCP2.6) rel. to 1995-2014", "(b) TX35 for 2081-2100 (RCP2.6) rel. to 1995-2014", 
            "(c) TX35 for 2041-2060 (RCP8.5) rel. to 1995-2014", "(d) TX35 for 2081-2100 (RCP8.5) rel. to 1995-2014",
            "(e) TX35 for 2041-2060 (SSP1-2.6) rel. to 1995-2014", "(f) TX35 for 2081-2100 (SSP1-2.6) rel. to 1995-2014",
            "(g) TX35 for 2041-2060 (SSP5-8.5) rel. to 1995-2014", "(h) TX35 for 2081-2100 (SSP5-8.5) rel. to 1995-2014")

# Plot maps ------------------------------------------------------------------------------------------------------------------------------------------------------
p <- lapply(1:length(change.grids.rob), function(i) {
  spatialPlot(change.grids.rob[[i]], backdrop.theme = "coastline",
              col.regions = c(rev(color.palette[c(13, 15)]), "white", rev(color.palette[1:11])),
              at = legend.bins, set.max = max(legend.bins), set.min = min(legend.bins),
              main = list(titles[i], cex = 0.8),
              colorkey = list(width = 1),
              sp.layout = list(list(regions.rob, lwd = 0.9, first = F),
                               list(coast.rob, col = "gray50", lwd = 0.7, first = FALSE),
                               list(world.contour.rob, first = FALSE),
                               uncertainty.sp[[i]]),
              par.settings = list(axis.line = list(col = 'transparent')))
})


# Export figure ---------------------------------------------------------------------------------------------------------------------------------------------------
pdf("FigureTS24-columns1-2.pdf", width = 8, height = 10)
do.call("grid.arrange", c(p[c(1,5,2,6,3,7,4,8)], ncol = 2, as.table = T))
dev.off()





