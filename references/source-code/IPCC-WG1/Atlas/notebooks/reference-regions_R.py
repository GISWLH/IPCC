# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/reference-regions_R.ipynb

# %% cell 3
library(rgdal)
library(sp)
library(RColorBrewer)

# %% cell 6
tmpdir <- tempdir()
unzip("../reference-regions/IPCC-WGI-reference-regions-v4_shapefile.zip", exdir = tmpdir)
refregions <- readOGR(dsn = tmpdir, layer = "IPCC-WGI-reference-regions-v4")

# %% cell 8
class(refregions)

# %% cell 10
load("../reference-regions/IPCC-WGI-reference-regions-v4_R.rda", verbose = TRUE)

# %% cell 12
refregions <- as(IPCC_WGI_reference_regions_v4, "SpatialPolygons")

# %% cell 14
plot(refregions)

# %% cell 18
temp.dir <- tempdir()
zipfile <- file.path(temp.dir, "world.zip")
download.file(url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/physical/ne_110m_coastline.zip",
              destfile = zipfile)
unzip(zipfile, exdir = temp.dir)

# %% cell 20
coastLines <- readOGR(dsn = temp.dir, layer = "ne_110m_coastline")

# %% cell 21
plot(coastLines)

# %% cell 24
coastLines <- readOGR(dsn = "./auxiliary-material/", layer = "WORLD_coastline")

# %% cell 25
plot(coastLines, col = "grey")
plot(refregions, add = TRUE)
text(x = coordinates(refregions)[ ,1],
     y = coordinates(refregions)[ ,2],
     labels = names(refregions), cex = 0.6)

# %% cell 28
names(names(refregions))

# %% cell 30
newzealand <- refregions["NZ"]
plot(newzealand)
plot(coastLines, col = "grey", add = TRUE)
text(x = coordinates(newzealand)[,1],
     y = coordinates(newzealand)[,2],
     labels = names(newzealand), cex = 1)

# %% cell 32
australasia <- refregions[c("NZ", "SEA", "NAU", "CAU", "EAU", "SAU")]

plot(australasia)
plot(coastLines, col = rgb(0.85,0.85,0.85,0.7), add = TRUE)
text(x = coordinates(australasia)[,1],
    y = coordinates(australasia)[,2],
    labels = names(australasia), cex = 1)

# %% cell 34
library(transformeR)
library(loadeR)
library(visualizeR)
library(geoprocessoR)

# %% cell 36
di <- dataInventory("./auxiliary-material/CMIP6Amon_tas_CanESM5_r1i1p1f1_historical_gn_185001-201412.nc")
str(di)

# %% cell 38
grid1 <- loadGridData(dataset = "./auxiliary-material/CMIP6Amon_tas_CanESM5_r1i1p1f1_historical_gn_185001-201412.nc",
                      var = "tas")

# %% cell 40
grid185001 <- subsetGrid(grid1, years = 1850, season = 1, drop = TRUE)

# %% cell 42
regnameslayer <- list("sp.text", coordinates(refregions), names(refregions))
spatialPlot(grid185001, backdrop.theme = "coastline", 
            color.theme = "RdBu",
            rev.colors = TRUE,
            sp.layout = list(list(refregions, first = FALSE, col = "blue"), regnameslayer))

# %% cell 44
grid1.ann <- aggregateGrid(grid1, aggr.y = list(FUN = "mean", na.rm = TRUE))
spatialPlot(climatology(grid1.ann), backdrop.theme = "coastline", 
            color.theme = "RdBu",
            rev.colors = TRUE,
            main = "Annual mean surface temperature (K)",
            sp.layout = list(list(refregions, first = FALSE, col = "blue"), regnameslayer))

# %% cell 46
proj4string(refregions)

# %% cell 48
grid1.ann <- setGridProj(grid = grid1.ann, proj = proj4string(refregions))

# %% cell 50
grid1.au <- overGrid(grid1.ann, australasia)

# %% cell 51
spatialPlot(climatology(grid1.au), 
            color.theme = "RdBu",
            rev.colors = TRUE,
            sp.layout = list(coastLines, first = FALSE, col = "black"))

# %% cell 53
grid1.au <- overGrid(grid1.ann, australasia, subset = TRUE)

# %% cell 54
spatialPlot(climatology(grid1.au), 
            color.theme = "RdBu",
            rev.colors = TRUE,
            sp.layout = list(coastLines, first = FALSE, col = "black"))

# %% cell 56
temporalPlot(grid1.au, aggr.spatial = list(FUN = "mean", na.rm = TRUE), xyplot.custom = list(ylab = "Annual mean surface temperature (K)"))

# %% cell 59
sessionInfo()
