# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/regional-scatter-plots_R.ipynb

# %% cell 3
library(repr)
# Change plot size
options(repr.plot.width=14, repr.plot.height=12)

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

# %% cell 12
ref.period <- 1995:2014

# %% cell 14
area <- "land"

# %% cell 16
regions <- c("ECA", "EAS");

# %% cell 18
cordex.domain <- "EAS"

# %% cell 20
ylim <- NULL
xlim <- NULL

# %% cell 22
fig <- computeFigures(regions = regions,
                      cordex.domain = cordex.domain,
                      area = area, 
                      ref.period = ref.period, 
                      scatter.seasons = scatter.seasons,
                      xlim = xlim,
                      ylim = ylim)

# %% cell 24
do.call("grid.arrange", fig)

# %% cell 26
outfilename <- sprintf("%s_%s_baseperiod_%s_ATvsAP.pdf",
  cordex.domain, area, paste(range(ref.period), collapse = "-")
)

pdf(outfilename, width = (length(scatter.seasons)+1)*10/2*0.85, height = length(regions)*10/2*0.85)
  do.call("grid.arrange", fig)
dev.off()

# %% cell 28
regions <- c("world")
cordex.domain <- FALSE

fig.w <- computeFigures(regions = regions,
                      cordex.domain = cordex.domain,
                      area = area, 
                      ref.period = ref.period, 
                      scatter.seasons = scatter.seasons,
                      xlim = xlim,
                      ylim = ylim)

# %% cell 29
do.call("grid.arrange", fig.w)

# %% cell 32
project <- "CMIP5" # other options are CMIP6 and CORDEX
experiment <- "rcp85" 
var <- "tas"
season <- 1:12
ref.period <- 1986:2005
periods <- c("1.5", "2", "3", "4") 
area <- "land"
region <- c("NSA", "SES")
cordex.domain <- "SAM"

WL.cmip5 <- computeDeltas(project = project, 
                          var = var, 
                          experiment = experiment, 
                          season = season, 
                          ref.period = ref.period, 
                          periods = periods, 
                          area = area, 
                          region = region, 
                          cordex.domain = cordex.domain)

# %% cell 34
WL.cmip5$SES

# %% cell 36
par(mar=c(4, 4, 0, 15), xpd=TRUE) # make room for the legend
plot(NA, xlim=c(1.5, 4), ylim=c(0,4), xlab = "GWL", ylab = "Temperature change in SES (deg. C)", type = "n")
model.names <- row.names(WL.cmip5$SES)
n.models <- length(model.names)
line.colors <- rainbow(n.models)
gwls <- as.numeric(periods)
for (i in 1:n.models){
    lines(gwls, WL.cmip5$SES[i,], col = line.colors[i])
    points(gwls, WL.cmip5$SES[i,], col = line.colors[i], pch=16)
}
legend("topright", legend=model.names, pch=16, lty=1, col=line.colors, inset=c(-1,0))

# %% cell 38
WL.cmip5.mean <- apply(WL.cmip5$SES, 2, mean, na.rm = T)
plot(gwls, WL.cmip5.mean, type = "b")

# %% cell 40
WL.cmip5.mean <- lapply(WL.cmip5, function(x) apply(x, 2, mean, na.rm = T))

# %% cell 42
df <- data.frame("WL" = gwls, WL.cmip5.mean)
df

# %% cell 44
xyplot(WL~SES + NSA, data = df, 
       xlab = "Regional temperature change (deg. C)", ylab = "GWL",
       type = "b",
       auto.key = TRUE)

# %% cell 46
sessionInfo()
