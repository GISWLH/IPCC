# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/regional-scatter-plots_Figure-Atlas-26_R.ipynb

# %% cell 3
library(repr)
# Change plot size 
options(repr.plot.width=14, repr.plot.height=30)

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
scatter.seasons <- list(c(12, 1, 2), 6:8)
ref.period <- 1995:2014
area <- "land"
regions <- c("NWN","NEN","WNA","CNA","ENA", "NCA")
cordex.domain <- "NAM"
ylim <- NULL
xlim <- NULL

# %% cell 12
fig <- computeFigures(regions = regions,
                      cordex.domain = cordex.domain,
                      area = area, 
                      ref.period = ref.period, 
                      scatter.seasons = scatter.seasons,
                      xlim = xlim,
                      ylim = ylim)

# %% cell 14
do.call("grid.arrange", fig)

# %% cell 18
outfilename <- sprintf("ATvsAP_%s_%s_cordex:%s_baseperiod:%s.pdf",
  paste(regions, collapse = "-"), area, cordex.domain, paste(range(ref.period), collapse = "-")
)

pdf(outfilename, width = (length(scatter.seasons)+1)*5*0.85, height = length(regions)*5*0.85)
  do.call("grid.arrange", fig)
dev.off()

# %% cell 20
sessionInfo()
