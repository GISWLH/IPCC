# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/regional-scatter-plots_Figure-Atlas-13_R.ipynb

# %% cell 3
library(repr)
# Change plot size 
options(repr.plot.width=14, repr.plot.height=6)

# %% cell 6
library(magrittr)
library(httr)
library(lattice)
library(latticeExtra)
library(gridExtra)

# %% cell 8
source("../datasets-aggregated-regionally/scripts/computeDeltas.R")
source("../datasets-aggregated-regionally/scripts/computeFigures.R")
source("../datasets-aggregated-regionally/scripts/computeOffset.R")

# %% cell 10
scatter.seasons <- list(1:12, c(12, 1, 2), 6:8)
ref.period <- 1995:2014
area <- "landsea"
regions <- c("world")
cordex.domain <- FALSE
xlim <- c(-2, 12)
ylim <- c(-2, 7)

# %% cell 12
fig_landsea <- computeFigures(regions = regions,
                      cordex.domain = cordex.domain,
                      area = area, 
                      ref.period = ref.period, 
                      scatter.seasons = scatter.seasons,
                      xlim = xlim,
                      ylim = ylim)

# %% cell 14
do.call("grid.arrange", c(fig_landsea, top =  area))

# %% cell 18
outfilename <- sprintf("ATvsAP_%s_%s_cordex:%s_baseperiod:%s.pdf",
  paste(regions, collapse = "-"), area, cordex.domain, paste(range(ref.period), collapse = "-")
)

pdf(outfilename, width = (length(scatter.seasons)+1)*5*0.85, height = length(regions)*5*0.85)
  do.call("grid.arrange", fig_landsea)
dev.off()

# %% cell 19
outfilename

# %% cell 21
area <- "land"

# %% cell 22
fig_land <- computeFigures(regions = regions,
                      cordex.domain = cordex.domain,
                      area = area, 
                      ref.period = ref.period, 
                      scatter.seasons = scatter.seasons,
                      xlim = xlim,
                      ylim = ylim)

# %% cell 23
do.call("grid.arrange", c(fig_land, top =  area))

# %% cell 25
outfilename <- sprintf("ATvsAP_%s_%s_cordex:%s_baseperiod:%s.pdf",
  paste(regions, collapse = "-"), area, cordex.domain, paste(range(ref.period), collapse = "-")
)

pdf(outfilename, width = (length(scatter.seasons)+1)*5*0.85, height = length(regions)*5*0.85)
  do.call("grid.arrange", fig_land)
dev.off()

# %% cell 27
sessionInfo()
