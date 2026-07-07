# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/global-warming-levels_R.ipynb

# %% cell 4
library(magrittr)

# %% cell 7
source("../warming-levels/scripts/getGWL.R")

# %% cell 9
target <- "EC-EARTH"
modelfiles <- list.files("../datasets-aggregated-regionally/data/CMIP5/CMIP5_tas_landsea", 
                         full.names = TRUE,
                         pattern = target) %>% print()

# %% cell 12
hist.regions <- grep("historical", modelfiles, value = TRUE) %>%
                read.table(header = TRUE, sep = ",", dec = ".", comment.char = "#") 
str(hist.regions)

# %% cell 14
yrs <- hist.regions[["date"]] %>% gsub("-.*", "", .)
hist <- tapply(hist.regions[["world"]], INDEX = yrs, FUN = "mean", na.rm = TRUE)
names(hist) <- unique(yrs)

# %% cell 16
plot(x = as.integer(names(hist)),
     y = hist, 
     ylab = "global tas (degC)", xlab = "year",
     type = "l", col = "blue", las = 1)
grid()
title(paste(target, "historical tas"))

# %% cell 18
rcp85.regions <- grep("rcp85", modelfiles, value = TRUE) %>% 
                 read.table(header = TRUE, sep = ",", dec = ".", comment.char = "#")
yrs <- rcp85.regions[["date"]] %>% gsub("-.*", "", .)
rcp85 <- tapply(rcp85.regions[["world"]], INDEX = yrs, FUN = "mean", na.rm = TRUE)
names(rcp85) <- unique(yrs)

plot(x = as.integer(names(rcp85)),
     y = rcp85, 
     ylab = "global tas (degC)", xlab = "year",
     type = "l", col = "blue", las = 1)
grid()
title(paste(target, "RCP8.5 tas"))

# %% cell 20
tas <- append(hist, rcp85)
plot(x = as.integer(names(tas)),
     y = tas, 
     ylab = "global tas (degC)", xlab = "year",
     type = "l", col = "blue", las = 1)
grid()
abline(v = 2006, col = "red", lty = 2)
title(paste(target, "hist+RCP 8.5 tas"))

# %% cell 22
 gwl_1.5 <- getGWL(data = tas, 
                   base.period = c(1850, 1900),
                   proj.period = c(1971, 2100),
                   window = 20,
                   GWL = 1.5) %>% print()

# %% cell 24
gwl_1.5

# %% cell 26
attr(gwl_1.5, "interval")

# %% cell 28
gwls <- c(1.5, 2, 3, 4)
central.years <- c()
for (i in 1:length(gwls)) {
    central.years[i] <- getGWL(data = tas, 
                               base.period = c(1850, 1900),
                               proj.period = c(1971, 2100),
                               window = 20,
                               GWL = gwls[i]) 
}

# %% cell 30
plot(x = as.integer(names(tas)),
     y = tas, 
     ylab = "global tas (degC)", xlab = "year",
     type = "l", col = "blue", las = 1)
grid()
title(paste(target, "hist+RCP 8.5 tas"))

## Indicate GWLs as vertical lines
colors <- 1:length(gwls)
line.type <- "dashed"
abline(v = central.years, col = colors, lty = line.type)
legend("topleft",title = "GWLs RCP8.5",
       paste0("+", gwls, " degC (", central.years, ")"),
       lty = line.type, col = colors)

# %% cell 33
sessionInfo()
