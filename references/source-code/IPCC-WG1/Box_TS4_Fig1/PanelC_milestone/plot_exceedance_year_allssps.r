##################################################
#
# plot_exceedance_year_allssps.r    19 April 2021
#
# Generates plots of exceedance year uncertainty
# for IPCC AR6 Ch9
#
##################################################

# Directories
main.dir <- "."
script.dir <- main.dir
res.dir <- paste(main.dir, "/data", sep="")
plot.dir <- paste(main.dir, "/figure", sep="")
plotdata.dir <- paste(main.dir, "/Plotted_Data", sep="")

# Options
plot2dev <- TRUE
plottype <- "pdf"
plot.quantiles <- c(0.05,0.17,0.83,0.95)
n.quantiles <- length(plot.quantiles) + 1

# Scenarios
scenarios <- c("ssp119","ssp126", "ssp245","ssp370", "ssp585")
scenarios.names <- list("ssp119"="SSP1-1.9","ssp126"="SSP1-2.6","ssp245"="SSP2-4.5","ssp370"="SSP3-7.0","ssp585"="SSP5-8.5")
ssp.reds <- c(30, 29, 234, 242, 132)
ssp.greens <- c(150, 51, 221, 17, 11)
ssp.blues <- c(132, 84, 61, 17, 34)
scenarios.cols <- rgb(ssp.reds, ssp.greens, ssp.blues, maxColorValue = 255)
n.scenarios <- length(scenarios)

# Years
plot.years <- seq(2000,2300,by=100)
n.years <- length(plot.years)

# Heights
milestones <- c(0.5, 1.0, 1.5, 2.0) # change this to change milestones used
heights <- seq(0.5, 2.0, by=0.5) # leave unchanged this for internal layout purposes
n.heights <- length(heights)

# Workflows
wf.types <- c(paste("wf_", rep(c(1,2,3), times=1), rep(c("f"), each=3), sep=""), "wf_4")
n.wfs <- length(wf.types)

# Pbox names
pbox.workflows <- matrix(c(1,2,3,4,1,2,1,2), ncol=4, byrow=TRUE)
pbox.names <- c("low confidence", "medium confidence")
n.pboxes <- length(pbox.names)

# Variable to hold the plotted data
missing.value <- 9999
plotted.data <- array(missing.value, dim=c(n.scenarios, n.pboxes, n.heights, n.quantiles))

# Libraries, functions, and sourced code
library(ncdf4)
library(colorspace)
source("super_legend.r")

# Colors for each workflow
dist.cols <- c(lighten(scenarios.cols[1], 0.8), scenarios.cols[1], 
               lighten(scenarios.cols[2], 0.8), scenarios.cols[2],
               lighten(scenarios.cols[3], 0.8), scenarios.cols[3],
               lighten(scenarios.cols[4], 0.8), scenarios.cols[4],
               lighten(scenarios.cols[5], 0.8), scenarios.cols[5])  # Use lightend colors for low-confidence processes


# Calculate the x coordinates for the
# background polygons
poly.y <- apply(rbind(heights[-1], heights[-n.heights]),2,mean)
poly.y <- c(heights[1] - (poly.y[1]-heights[1]), 
            poly.y, 
            heights[n.heights] + (heights[n.heights]-poly.y[length(poly.y)]))
poly.width <- diff(poly.y)

# Output file name
out.file <- sprintf("%s/Fig_TS4_1c_milestone.%s", plot.dir, plottype)

# Setup the plot device
if(plot2dev) { pdf(out.file, height=4.0, width=3.0, pointsize=7.5) }
par(mar=c(2.5,2.0,0.7,1.2)+0.1, yaxs="i", xaxs="i")

# Layout the plots
layout(matrix(c(2,1), byrow=T, ncol=1), heights=c(0.1,0.9))

# Start the plot
plot.new()
plot.window(ylim=range(poly.y), xlim=c(2000,2300))
axis(1, at=plot.years[-length(plot.years)], cex.axis=1.1)
axis(1, at=2300, label="2300+", cex.axis=1.1)
poly.cols <- c("gray90", "white")
for(k in 1:length(heights)){
  polygon(y=c(poly.y[k],poly.y[k],poly.y[k+1],poly.y[k+1]),
          x=c(1900,3000,3000,1900), col=poly.cols[(k%%2)+1], border="black")
}
abline(v=seq(2050,2300,by=50), lty=3, col="gray70")
box()

# Loop over the scenarios
for(i in 1:n.scenarios){
  
  # This fit type
  this.scenario <- scenarios[i]
  
  # Loop over the pbox workflows
  for(j in 1:n.pboxes){
    
    if((i != 2) & (i!=5) & j == 1){ next}
    
    # Which workflows are aggregated into this pbox?
    this.pbox.workflows <- pbox.workflows[j,]
    
    # Initialize variables to hold the individual workflow values
    workflow.seg.lengths <- array(NA, dim=c(length(this.pbox.workflows), n.heights, length(plot.quantiles)))
    workflow.dist.median <- array(NA, dim=c(length(this.pbox.workflows), n.heights))
    
    # Loop over these workflows
    for(k in 1:length(this.pbox.workflows)){
      
      # This workflow
      this.workflow <- wf.types[this.pbox.workflows[k]]
      workflow.file <- sprintf("%s/%s_%s_milestone_figuredata.nc", res.dir, this.workflow, this.scenario)
      workflow.nc <- nc_open(workflow.file)
      
      # Get the heights and quantiles
      nc.heights <- ncvar_get(workflow.nc, "heights")
      nc.qs <- ncvar_get(workflow.nc, "quantiles")
      
      # Load the exceedance year data
      dist.data <- ncvar_get(workflow.nc, "exceedance_years")  #[heights, quantiles]
      
      # Determine the height indices
      height.ind <- which(nc.heights %in% (milestones*1000))
      
      # Get the line segment lengths
      workflow.seg.lengths[k,,] <- dist.data[height.ind,-3]
      
      # Get the median
      workflow.dist.median[k,] <- dist.data[height.ind, 3]
      
      # Close the netcdf file
      nc_close(workflow.nc)
    }
    
    # Calculate the pbox values to plot
    seg.lengths <- array(NA, dim=c(n.heights, length(plot.quantiles)))
    low.idx <- which(plot.quantiles < 0.5)
    hi.idx <- which(plot.quantiles > 0.5)
    seg.lengths[,1:length(low.idx)] <- sapply(low.idx, function(x) apply(workflow.seg.lengths[,,x], 2, min))
    seg.lengths[,(length(low.idx)+1):length(plot.quantiles)] <- sapply(hi.idx, function(x) apply(workflow.seg.lengths[,,x], 2, max))
    dist.median <- apply(workflow.dist.median, 2, mean)
    
    # Any value that equals 2300, set to a higher number so it renders off the plot
    seg.lengths[seg.lengths >= 2300] <- missing.value
    dist.median[dist.median >= 2300] <- missing.value
    
    # Store the plotted data
    plotted.data[i,j,,c(1,2,4,5)] <- seg.lengths
    plotted.data[i,j,,3] <- dist.median
    
    # Determine the y coordinate for this distribution
    this.y <- poly.y[-length(poly.y)] + i*(poly.width/(n.scenarios+1))
    
    # Plot the line segments
    segments(y0=this.y, x0=seg.lengths[,2], x1=seg.lengths[,3],
             col=dist.cols[(i-1)*n.pboxes+j], lwd=4.7, lty=1, lend=1)
    if(j == 1){
      segments(y0=this.y, x0=seg.lengths[,1], x1=seg.lengths[,4],
               col=dist.cols[(i-1)*n.pboxes+j], lwd=1.7, lty=1, lend=1)
    }
    
    # Plot the median as a point
    if(j == 2){ 
      points(dist.median, this.y, pch=21, bg=dist.cols[(i-1)*n.pboxes+j], cex=1.35)
    }
    
  }
}

# Apply various labels to the plot --------------------------
# "Year by which..." text 
# rect(2010, heights[n.heights]-0.45*(heights[2]-heights[1]), 2125, heights[n.heights]+0.0*(heights[2]-heights[1]),
#     col="gray90", border=NA)
text(x=2000, y=heights[n.heights]-0.12*(heights[2]-heights[1]), pos=4, cex=1,
     labels=sprintf("Year by which a rise of", heights[n.heights]), font=1)
text(x=2037, y=heights[n.heights]-0.3*(heights[2]-heights[1]), pos=4, cex=1,
     labels=sprintf("above 1995-2014 is expected", heights[n.heights]), font=1)

# Append the height legend in the corners
text(x=2000, y=heights-0.3*(heights[2]-heights[1]), pos=4, cex=1.1,
     labels=sprintf("%0.1f m", milestones), font=2)

# SSP labels
#rect(2160, heights[n.heights-1]+0.3*(heights[2]-heights[1]), 2210, heights[n.heights-1]+0.45*(heights[2]-heights[1]),
#     col="white", border=NA)
#rect(2190, heights[n.heights-1]+0.055*(heights[2]-heights[1]), 2210, heights[n.heights-1]+0.205*(heights[2]-heights[1]),
#     col="white", border=NA)
#rect(2225, heights[n.heights-1]-0.205*(heights[2]-heights[1]), 2275, heights[n.heights-1]-0.055*(heights[2]-heights[1]),
#     col="white", border=NA)

xloc <- c(2245, 2245, 2245, 2245, 2245)
yloc <- c(0,0,0,0,0)
for(i in 1:n.scenarios){
     yloc[i] <- poly.y[1] + i*(poly.width[1]/(n.scenarios+1))
     if (i == 3) {
          text(x=xloc[i], y=yloc[i], pos=4, cex=0.75,
          labels=scenarios.names[i], font=2, col=darken(scenarios.cols[i],.3))

     }
     else { text(x=xloc[i], y=yloc[i], pos=4, cex=0.75,
          labels=scenarios.names[i], font=2, col=scenarios.cols[i]) }
}

# Low confidence text, box, and arrows
#rect(2125, heights[1]+0.10*(heights[2]-heights[1]), 2225, heights[1]+0.45*(heights[2]-heights[1]),
#     col="white", border=NA)
dheights <- heights[2]-heights[1]
text(x=2125, y=yloc[5]+.08*dheights, pos=4, cex=1,
     labels="Low-confidence", font=1, col="gray60")
text(x=2125, y=yloc[5]-.08*dheights, pos=4, cex=1,
     labels="processes included", font=1, col="gray60")

segments(x0=2125, y0=yloc[5]+.12*dheights, x1=2065, 
         cex=0.7,col="gray60")
arrows(x0=2065, y0=yloc[5]+.12*dheights, x1=2065, y1=yloc[5]+.04*dheights,
       cex=0.7,col="gray60", length=0.05)
arrows(x0=2180, y0=yloc[4], y1=yloc[2]+.04*dheights, 
       cex=0.7,col="gray60", length=0.05)

# Start a new plot area for the figure title text
par(mar=c(0,0,0,0), xpd=NA)
plot.new()
plot.window(xlim=c(0,1), ylim=c(0,1))
text(x=0, y=0, pos=4, cex=1.2, font=2,
     labels="        c) Projected timing of sea-level rise milestones")
par(xpd=FALSE)

# Close the plot
if(plot2dev){ dev.off() }

#####################################################################################

# Generate the plotted data files ---------------------------------------------------

# The 5th and 95th percentile for medium-confidence processes are not displayed, nor 
# are the low-confidence medians, so set them to missing
plotted.data[,2,,c(1,5)] <- missing.value
plotted.data[,1,,3] <- missing.value

# Define the dimension variables
height.ncdim <- ncdim_def("height", "meters", milestones)
percentile.ncdim <- ncdim_def("percentile", "", c(plot.quantiles[c(1,2)], 0.5, plot.quantiles[c(3,4)])*100)

# Define the missing value flag
mv <- 9999

# Initialize list for variables
these.vars = vector("list", n.pboxes)

# Loop over the scenarios
for(i in 1:n.scenarios){
  
  # Loop over the pboxes
  for(j in 1:n.pboxes){
    
    # Create the variables for the netcdf file
    these.vars[[j]] <- ncvar_def(gsub(" ", "_", pbox.names[j]), "year", list(height.ncdim, percentile.ncdim), missval = mv)
    
  }
  
  # Create the netcdf file with these variables
  newnc <- nc_create(paste(plotdata.dir, "/FigTS4-1c-milestone_", scenarios[i], "_data.nc", sep=""), these.vars)
  
  # Loop over the pboxes again
  for(j in 1:n.pboxes){
    
    # Append the data to the netcdf file
    ncvar_put(newnc, these.vars[[j]], plotted.data[i,j,,], start=c(1,1), count=c(n.heights, n.quantiles))
    
  }
  
  # Put the additional information into the netcdf file
  ncatt_put(newnc, 0, "title", "Projected timing of sea-level rise milestones under different forcing scenarios")
  ncatt_put(newnc, 0, "units", "year (CE)")
  ncatt_put(newnc, 0, "creator", "Gregory Garner (gregory.garner@rutgers.edu)")
  ncatt_put(newnc, 0, "activity", "IPCC AR6 (Chapter 9)")
  ncatt_put(newnc, 0, "comments", "Data is for panel C (sea-level rise milestones) of Box TS4 Figure 1 in the IPCC Working Group I contribution to the Sixth Assessment Report")
  ncatt_put(newnc, 0, "missing_value_note", "Percentiles that are not shown in this plot (medium-confidence 5th and 95th, low-confidence 50th) and percentiles that extend beyond the projection time horizon (year 2300) have been set to missing.")
  
  # Close the netcdf file
  nc_close(newnc)
  
}

