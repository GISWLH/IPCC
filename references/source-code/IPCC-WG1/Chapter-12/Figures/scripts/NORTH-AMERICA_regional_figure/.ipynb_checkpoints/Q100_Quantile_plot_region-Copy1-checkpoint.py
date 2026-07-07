# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/NORTH-AMERICA_regional_figure/.ipynb_checkpoints/Q100_Quantile_plot_region-Copy1-checkpoint.ipynb

# %% cell 2
ensembles = c('CORDEX', 'CMIP5', 'CMIP6')
GWLs = c('1.5','2','4')
scenarios = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')

data = list()
for (ensemble in ensembles){
    data[[ensemble]] = list()
    for (GWL in GWLs){
        data[[ensemble]][[GWL]] = list()
    }
    for (scenario in scenarios){
        data[[ensemble]][[scenario]] = list()
    }

}

# %% cell 4
library(rjson)

# %% cell 6
# -- List of regions for AFRICA
continent_regions = c('NWN','NEN','WNA','CNA','ENA','NCA','CAR')

regions_by_continent = list(
    NAM = c('NWN','NEN','WNA','CNA','ENA'),
    CAM = c('NCA','CAR')
    )


all_regions = list()
GWLs = c('1.5','2','4')
scenarios = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')

for (region_name in continent_regions){
    all_regions[[region_name]] = list()
    for (ensemble in c('CMIP6','CMIP5','CORDEX')){
        all_regions[[region_name]][[ensemble]] = list()
        for (GWL in GWLs){
            all_regions[[region_name]][[ensemble]][[GWL]] = list()
        }#end for GWL
        for (scenario in scenarios){
            all_regions[[region_name]][[ensemble]][[scenario]] = list()
        }#end for scenario
    }#end for ensemble
}#end for region_name

# %% cell 8
"metrics_reader"=function(metrics_filename){
    
    # -- Read the metrics file provided by Fabio
    lines=readLines(file(metrics_filename,open="r"))
    dat = c()
    for (elt in lines){
        tmp = gsub(' ','', elt)
        dat = c(dat, tmp)
    }#end for elt
    # -- Each region has 4 lines => the number of regions is the length / 4
    nregions = length(dat)/4
    # -- Store the results in res
    res = list()
    for (i in 1:nregions){
        # -- Calculate the index of the region name
        startind = (i-1)*4 + 1
        resname = dat[startind]
        print(resname)
        p10 = as.numeric(dat[startind+1])
        median = as.numeric(dat[startind+2])
        p90 = as.numeric(dat[startind+3])
        print(c(p10,median,p90))
        res[[resname]] = c(p10, median, p90)
    }
    return(res)
}

# %% cell 10
ensemble = 'CMIP6'

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    for (clim_period in c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')){
        if (clim_period=='modern'){ wclim_period='ssp585_1995-2014' }
        if (clim_period=='2.6_mid'){ wclim_period='ssp126_2041-2060' }
        if (clim_period=='2.6_late'){ wclim_period='ssp126_2080-2099' }
        if (clim_period=='8.5_mid'){ wclim_period='ssp585_2041-2060' }
        if (clim_period=='8.5_late'){ wclim_period='ssp585_2080-2099' }
        
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',ensemble,'/Q100_',wclim_period,'.nc_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period

    for (clim_period in c('1.5','2','4')){
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
    
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',ensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
    
}#end for continent

# %% cell 12
ensemble = 'CMIP5'

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    for (clim_period in c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')){
        if (clim_period=='modern'){ wclim_period='rcp85_1995-2014' }
        if (clim_period=='2.6_mid'){ wclim_period='rcp26_2041-2060' }
        if (clim_period=='2.6_late'){ wclim_period='rcp26_2080-2099' }
        if (clim_period=='8.5_mid'){ wclim_period='rcp85_2041-2060' }
        if (clim_period=='8.5_late'){ wclim_period='rcp85_2080-2099' }
        
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',ensemble,'/Q100_',wclim_period,'.nc_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period

    for (clim_period in c('1.5','2','4')){
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
    
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',ensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
    
}#end for continent

# %% cell 14
ensemble = 'CORDEX'
wensemble = paste(ensemble,'-core',sep='')

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    for (clim_period in c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')){
        if (clim_period=='modern'){ wclim_period='rcp85_1995-2014' }
        if (clim_period=='2.6_mid'){ wclim_period='rcp26_2041-2060' }
        if (clim_period=='2.6_late'){ wclim_period='rcp26_2080-2099' }
        if (clim_period=='8.5_mid'){ wclim_period='rcp85_2041-2060' }
        if (clim_period=='8.5_late'){ wclim_period='rcp85_2080-2099' }
        
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',wensemble,'/Q100_',wclim_period,'.nc_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period

    for (clim_period in c('1.5','2','4')){
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
    
        metrics_filename = paste('/home/jservon/Chapter12_IPCC/data/Figure_12.10/Q100_',wensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
    
}#end for continent

# %% cell 16
for (region_name in continent_regions){
    ensemble = 'CMIP6'
    all_regions[[region_name]][[ensemble]][['modern']][['color']] = 'black'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue4'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'red'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue4'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'red'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'darkorchid4'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'darkorange'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'tan4'

    ensemble = 'CMIP5'
    all_regions[[region_name]][[ensemble]][['modern']][['color']] = 'grey40'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue3'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'lightcoral'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue3'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'lightcoral'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'darkorchid3'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'sandybrown'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'peachpuff4'

    ensemble = 'CORDEX'
    all_regions[[region_name]][[ensemble]][['modern']][['color']] = 'grey60'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'lightpink'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'lightpink'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'mediumpurple1'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'navajowhite2'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'peachpuff3'
}#end for region_name

# %% cell 18
"barplot_satellite_chap12"=function(data, title, ylabel, do_ylab='TRUE', do_xlab='TRUE', mar=c(4,3,2.5,1)){
    #
    # -- Names
    ensembles = c('CORDEX','CMIP5','CMIP6')
    GWLs = c('1.5','2','4')
    scenarios = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')
    nhorizons = length(GWLs)+length(scenarios)
        
    ylim = c(0,2.5)
    
    # -- position on the x axis of the ensembles
    xpos = c(1,2,3, 4.5, 6, 7, 8, 9)
    xvert = c(1.5,2.5,3.5,5.5,7.5)
    inner_margin = 0.5
    xlim = c(1-inner_margin, max(xpos)+inner_margin)
    general_cex=1.3
    par(cex=general_cex+0.3)
    par(mar=mar)
    plot(1:nhorizons, rep(NA, nhorizons), col='white', ylim=ylim, xlim=xlim,
         xaxt='n', yaxt='n', xlab='', ylab='', xaxs="i", font=2)#
    par(cex=general_cex)
    mtext(ylabel, 2, font=2, line=2.2, cex=general_cex)
    par(xpd=NA)
    par(font=2)
    
    for (yval in seq(0,2.5,by=0.5)){
        lines(xlim,rep(yval,2),type='l', lty=2)
    }

    delta = 0.22 # - space between CMIP6/CMIP5/CORDEX
    # -- Plot data
    i = 1
    for (horizon in c(GWLs, scenarios)){
        j = xpos[i] - delta
        for (ensemble in ensembles){
            print(paste(horizon, ensemble))
            dat = data[[ensemble]][[horizon]][['vals']]
            if (is.null(dat)){dat = c(NA,NA,NA)}
            col = data[[ensemble]][[horizon]][['color']]
            lines(rep(j,2), c(dat[1],dat[3]), type='l', col=col, lwd=4)
            points(j, dat[2], cex=1.5, pch=16, col=col)
            j = j + delta
        }
        i = i + 1
    }
    
    # -- Y axis
    par(cex=2.5)
    yvals = seq(0,2.5,by=0.5)
    ylabels = yvals
    dumyvals = yvals
    if (do_ylab=='TRUE'){
        par(cex=2.6)
        axis(2, at=dumyvals, labels=ylabels, las=1)
        par(cex=general_cex)
    }else{
        axis(2, at=dumyvals, labels=FALSE)#labels=rep(NA,length(dumyvals)))
    }
    par(cex=general_cex)
    
    
    # -- X axis
    if (do_xlab=='FALSE'){
        axis(1, at=xvert, labels=rep('',length(xvert)))
    }
    # -- Title
    mtext(title,3, font=2, cex=3, line=0.5)
    
    # -- Vertical lines    
    vline = ylim
    vline[1] = ylim[1] - (ylim[2]-ylim[1])*0.33
    if (do_xlab=='TRUE'){
        for (v in xvert){lines(c(v,v),vline,type='l', lwd=1)}
    }else{
        for (v in xvert){lines(c(v,v),ylim,type='l')}
    }

    if (do_xlab=='TRUE'){
        cex_text = 1.8
        bline = ylim[1] - 0.41*(ylim[2]-ylim[1])
        #btext2 = ylim[1] - 0.33*(ylim[2]-ylim[1])
        #
        # -- Labels GWLs
        GWLs_range = c(0.5,3.2)
        btext = ylim[1] - 0.54*(ylim[2]-ylim[1])
        lines(c(0.5,3.2), c(bline*0.9,bline*0.9), type='l', lwd=3)
        text(mean(GWLs_range),btext,expression("GWL"), font=1, adj=c(0.5,0), cex=cex_text*0.9)

        btext2 = ylim[1] - 0.22*(ylim[2]-ylim[1])
        adj_ts = c(0.5,0.5)
        adj_gwl = c(0.5,0.5)
        text(1,btext2,"1.5", cex=cex_text, font=1, srt=90, adj=adj_gwl)
        text(2,btext2,"2", cex=cex_text, font=1, srt=90, adj=adj_gwl)
        text(3,btext2,"4", cex=cex_text, font=1, srt=90, adj=adj_gwl)

        # -- Labels time slices = modern, mid-term, long-term
        xmodern = 4.5
        xmid = 6.5
        xlate = 8.5
        text(xmodern,btext2, "r.past", font=1, cex=cex_text, srt=90, adj=adj_ts)
        text(xmid,btext2, "mid.", font=1, cex=cex_text, srt=90, adj=adj_ts)
        text(xlate,btext2, "long.", font=1, cex=cex_text, srt=90, adj=adj_ts)

        time_slices = c(3.6,9.3)
        lines(time_slices, c(bline,bline), type='l', lwd=3)
        text(mean(time_slices),btext,"Time slices", font=1, adj=c(0.5,0), cex=cex_text*0.9)
    }#end if do_ylab

}

# %% cell 19
region = 'NORTH-AMERICA'

figname = paste('/home/jservon/Chapter12_IPCC/figs/Figure_12.10/',region,'_Q100_boxplot.png',sep='')
png(figname, width=900,height=1050)
mat = t(matrix(1:9,3,3))
mat=rbind(
c(1,2,0),
c(3,4,5),
c(6,7,8)
)

layout(mat, heights=c(1,1,1.2), widths=c(1.2,1,1))
i = 1
for (subregion in continent_regions){    
    mar = c(1,1,2,0)
    if (subregion %in% c('NWN','WNA','NCA')){
        do_ylab='TRUE'
        mar[2]=4
    }else{
        do_ylab='FALSE'
    }#
    if (subregion %in% c('NCA','CAR')){
        do_xlab='TRUE'
        mar[1] = 5 # -- bottom margin
    }else{
        do_xlab='FALSE'
    }#
    plot_title = subregion
    ylab = ''
    barplot_satellite_chap12(all_regions[[subregion]],plot_title, ylab, mar=mar, do_ylab=do_ylab, do_xlab=do_xlab)
    
    i = i + 1
}
dev.off()

# %% cell 20
library("IRdisplay")
display_png(file=figname)
