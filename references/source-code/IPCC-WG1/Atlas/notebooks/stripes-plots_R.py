# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/stripes-plots_R.ipynb

# %% cell 4
library(magrittr)
library(httr)
library(lattice)
library(latticeExtra)
library(RColorBrewer)

# %% cell 6
source("../datasets-aggregated-regionally/scripts/computeStripes.R")

# %% cell 10
computeStripes(project = "CMIP6", 
               var = "pr",
               experiment = "ssp585",
               season = 1:12,
               area = "land",
               region = "world",
               cordex.domain = NULL,
               brewer.pal.name = "Blues",
               rev.colors = TRUE)

# %% cell 12
computeStripes(project = "CMIP6", 
               var = "tas",
               experiment = "ssp585",
               season = 1:12,
               area = "land",
               region = "world",
               cordex.domain = NULL,
               brewer.pal.name = "RdBu",
               rev.colors = TRUE,
               main = list("Stripes of mean temperature for CMIP6", cex = 1.5),
               colorkey = list(width = 2))

# %% cell 14
computeStripes(project = "CMIP6", 
               var = "tas",
               experiment = "ssp585",
               season = 1:12,
               area = "sea",
               region = "MED",
               cordex.domain = NULL,
               brewer.pal.name = "RdBu",
               rev.colors = TRUE)

# %% cell 16
computeStripes(project = "CORDEX", 
               var = "tas",
               experiment = "rcp85",
               season = 6:8,
               area = "land",
               region = "MED",
               cordex.domain = "AFR",
               brewer.pal.name = "RdGy",
               rev.colors = TRUE)

# %% cell 17
sessionInfo()
