# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/EUROPE_regional_figure/Q100_Quantile_plot_region.ipynb

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

# %% cell 3
CWD = getwd()

# %% cell 5
library(rjson)

# %% cell 7
# -- List of regions for AFRICA
continent_regions = c('NEU','WCE','MED')

regions_by_continent = list(
    EUR_MaskDesert = c('NEU','WCE','MED')
    #CAM = c('NCA')
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

# %% cell 9
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

# %% cell 11
ensemble = 'CMIP6'

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    # -- Recent past raw value
    clim_period = 'modern_raw'
    wclim_period='ssp585_1995-2014'
    if (continent=='EUR_MaskDesert'){
        wcontinent='EUR'
    }else{
        wcontinent=continent
    }
    metrics_filename = paste(CWD,'/../../data/Figure_12.9/Q100_',ensemble,'/Q100_',wclim_period,'.nc_',wcontinent,'.txt',sep='')
    print(paste('Raw values :', metrics_filename))
    res_metrics_by_AR6region = metrics_reader(metrics_filename)
    for (region_name in names(res_metrics_by_AR6region)){
        all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
    }
     
    # -- Differences for future time periods and GWLs
    for (clim_period in c('2.6_mid', '8.5_mid', '2.6_late', '8.5_late','1.5','2','4')){
        if (clim_period=='2.6_mid'){ wclim_period='ssp126_mid' }
        if (clim_period=='2.6_late'){ wclim_period='ssp126_far' }
        if (clim_period=='8.5_mid'){ wclim_period='ssp585_mid' }
        if (clim_period=='8.5_late'){ wclim_period='ssp585_far' }
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
        
        metrics_filename = paste(CWD,'/../../data/PERCENTILES_CHANGE_DIVDRA_ABSOLUTE/percentiles_',ensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
}#end for continent

# %% cell 13
ensemble = 'CMIP5'

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    # -- Recent past raw value
    clim_period = 'modern_raw'
    wclim_period='rcp85_1995-2014'
    if (continent=='EUR_MaskDesert'){
        wcontinent='EUR'
    }else{
        wcontinent=continent
    }
    metrics_filename = paste(CWD,'/../../data/Figure_12.9/Q100_',ensemble,'/Q100_',wclim_period,'.nc_',wcontinent,'.txt',sep='')
    print(paste('Raw values :', metrics_filename))
    res_metrics_by_AR6region = metrics_reader(metrics_filename)
    for (region_name in names(res_metrics_by_AR6region)){
        all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
    }
     
    # -- Differences for future time periods and GWLs
    for (clim_period in c('2.6_mid', '8.5_mid', '2.6_late', '8.5_late','1.5','2','4')){
        if (clim_period=='2.6_mid'){ wclim_period='rcp26_mid' }
        if (clim_period=='2.6_late'){ wclim_period='rcp26_far' }
        if (clim_period=='8.5_mid'){ wclim_period='rcp85_mid' }
        if (clim_period=='8.5_late'){ wclim_period='rcp85_far' }
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
        
        metrics_filename = paste(CWD,'/../../data/PERCENTILES_CHANGE_DIVDRA_ABSOLUTE/percentiles_',ensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
}#end for continent

# %% cell 15
ensemble = 'CORDEX'
wensemble = paste(ensemble,'-core',sep='')

for (continent in names(regions_by_continent)){
    print(paste(continent,'==> '))
    print(regions_by_continent[[continent]])
    
    # -- Recent past raw value
    clim_period = 'modern_raw'
    wclim_period='rcp85_1995-2014'
    if (continent=='EUR_MaskDesert'){
        wcontinent='EUR'
    }else{
        wcontinent=continent
    }
    metrics_filename = paste(CWD,'/../../data/Figure_12.9/Q100_',wensemble,'/Q100_',wclim_period,'.nc_',wcontinent,'.txt',sep='')
    print(paste('Raw values :', metrics_filename))
    res_metrics_by_AR6region = metrics_reader(metrics_filename)
    for (region_name in names(res_metrics_by_AR6region)){
        all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
    }
     
    # -- Differences for future time periods and GWLs
    for (clim_period in c('2.6_mid', '8.5_mid', '2.6_late', '8.5_late','1.5','2','4')){
        if (clim_period=='2.6_mid'){ wclim_period='rcp26_mid' }
        if (clim_period=='2.6_late'){ wclim_period='rcp26_far' }
        if (clim_period=='8.5_mid'){ wclim_period='rcp85_mid' }
        if (clim_period=='8.5_late'){ wclim_period='rcp85_far' }
        if (clim_period=='1.5'){ wclim_period='1.5' }
        if (clim_period=='2'){ wclim_period='2.0' }
        if (clim_period=='4'){ wclim_period='4.0' }
        
        metrics_filename = paste(CWD,'/../../data/PERCENTILES_CHANGE_DIVDRA_ABSOLUTE/percentiles_',wensemble,'/',wclim_period,'_',continent,'.txt',sep='')
        print(metrics_filename)
        res_metrics_by_AR6region = metrics_reader(metrics_filename)
        for (region_name in names(res_metrics_by_AR6region)){
            all_regions[[region_name]][[ensemble]][[clim_period]][['vals']] = res_metrics_by_AR6region[[region_name]]
        }
    }#end for clim_period
    
    
}#end for continent

# %% cell 17
for (region_name in continent_regions){
    ensemble = 'CMIP6'
    all_regions[[region_name]][[ensemble]][['modern_raw']][['color']] = 'black'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue4'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'red'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue4'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'red'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'darkorchid4'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'darkorange'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'tan4'

    ensemble = 'CMIP5'
    all_regions[[region_name]][[ensemble]][['modern_raw']][['color']] = 'grey40'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue3'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'lightcoral'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue3'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'lightcoral'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'darkorchid3'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'sandybrown'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'peachpuff4'

    ensemble = 'CORDEX'
    all_regions[[region_name]][[ensemble]][['modern_raw']][['color']] = 'grey60'
    all_regions[[region_name]][[ensemble]][['2.6_mid']][['color']] = 'dodgerblue'
    all_regions[[region_name]][[ensemble]][['8.5_mid']][['color']] = 'lightpink'
    all_regions[[region_name]][[ensemble]][['2.6_late']][['color']] = 'dodgerblue'
    all_regions[[region_name]][[ensemble]][['8.5_late']][['color']] = 'lightpink'
    all_regions[[region_name]][[ensemble]][['1.5']][['color']] = 'mediumpurple1'
    all_regions[[region_name]][[ensemble]][['2']][['color']] = 'navajowhite2'
    all_regions[[region_name]][[ensemble]][['4']][['color']] = 'peachpuff3'
}#end for region_name

# %% cell 19
"vert_scale"=function(val, ylim){
    return( (val - ylim[1]) / (ylim[2] - ylim[1]) )
}

"barplot_satellite_chap12"=function(data, title, ylabel, do_xlab='TRUE',
                                    do_ylab_raw='TRUE', do_ylab_diff='TRUE', mar=c(4,3,2.5,1)){
    #
    # -- Names
    ensembles = c('CORDEX','CMIP5', 'CMIP6')
    GWLs = c('1.5','2','4')
    scenarios = c('2.6_mid', '8.5_mid', '2.6_late', '8.5_late')
    nhorizons = length(GWLs)+length(scenarios)
    
    ylim_base = c(0,1)
    ylim_raw = c(0,0.8)
    ylim_diff = c(-0.15,0.1)
        
    ylim = ylim_base
    
    # -- position on the x axis of the ensembles
    # RP, GWL 1.5, 2, 4, mid, long
    xpos = c(1, 2,3,4, 5,6, 7,8)
    xvert = c(1.5, 2.5,3.5,4.5, 6.5)
    inner_margin = 0.5
    xlim = c(1-inner_margin, max(xpos)+inner_margin)
    general_cex=1.3
    par(cex=general_cex)
    par(mar=mar)
    plot(1:nhorizons, rep(NA, nhorizons), col='white', ylim=ylim, xlim=xlim,
         xaxt='n', yaxt='n', xlab='', ylab='', xaxs="i", yaxs='i', font=2)
    mtext(ylabel, 2, font=2, line=2.2, cex=general_cex)
    #     cex.axis=1.2, cex.lab=1.5, font=2)
    par(xpd=NA)
    par(font=2)
    
    # -- Add horizontal lines for raw values
    #for (yval in vert_scale(seq(0,1.4,by=0.2), ylim_raw)){
    #    lines(c(xlim[1],xvert[1]),rep(yval,2),type='l', lty=2)
    #}
    
    # -- Add horizontal lines for diff
    for (yval in vert_scale(c(-0.1,0,0.1), ylim_diff)){
        lines(c(xvert[1],xlim[2]),rep(yval,2),type='l', lty=2)
    }
    
    delta = 0.24 # - space between CMIP6/CMIP5/CORDEX
    
    # -- Plot data
    # -- Plot baseline
    i = 1
    for (horizon in c('modern_raw',GWLs, scenarios)){
        j = xpos[i] - delta
        for (ensemble in ensembles){
            print(paste(horizon, ensemble))
            if (horizon=='modern_raw'){
                dat = vert_scale(data[[ensemble]][[horizon]][['vals']], ylim_raw)
            }else{
                dat = vert_scale(data[[ensemble]][[horizon]][['vals']], ylim_diff)
            }
            print(dat)
            if (is.null(dat)){dat = c(NA,NA,NA)}
            col = data[[ensemble]][[horizon]][['color']]
            lines(rep(j,2), c(dat[1],dat[3]), type='l', col=col, lwd=4)
            points(j, dat[2], cex=1.5, pch=16, col=col)
            j = j + delta
        }
        i = i + 1
    }

    
    # -- Y axis raw
    yvals = seq(0,0.8,by=0.2)
    dumyvals = vert_scale(yvals, ylim_raw)
    ylabels = yvals
    par(cex=2.4)
    axis(2, at=dumyvals, labels=rep('',length(yvals)))
    if (do_ylab_raw=='TRUE'){
        axis(2, pos=0.75, at=dumyvals, tick='FALSE', labels=ylabels, las=1)
    }
    par(cex=general_cex)
    
    # -- Y axis Differences
    yvals = c(-0.1,0,0.1)
    dumyvals = vert_scale(yvals, ylim_diff)
    ylabels = yvals
    par(cex=2.2)
    axis(4, at=dumyvals, labels=rep('',length(yvals)))
    if (do_ylab_diff=='TRUE'){
        axis(4, pos=xlim[2]-0.25, at=dumyvals, labels=ylabels, las=1, tick='FALSE')
    }
    par(cex=general_cex)
    

    # -- X axis
    if (do_xlab=='FALSE'){
        axis(1, at=xvert, labels=rep('',length(xvert)))
    }
    # -- Title
    mtext(title,3, font=2, cex=3, line=0.5)

    bline = ylim[1] - 0.22*(ylim[2]-ylim[1])
    #
    # -- X axis
    if (do_xlab=='FALSE'){
        axis(1, at=xvert, labels=rep('',length(xvert)))
    }

    # -- Vertical lines
    vline = ylim
    vline[1] = ylim[1] - (ylim[2]-ylim[1])*0.16
    if (do_xlab=='TRUE'){
        for (v in xvert){lines(c(v,v),vline,type='l', lwd=1)}
    }else{
        for (v in xvert){lines(c(v,v),ylim,type='l')}
    }
    # Make a thicker line to separate r.past from the rest
    vline = ylim
    v = xvert[1]
    lines(c(v,v),vline,type='l', lwd=3)
    
    if (do_xlab=='TRUE'){
        cex_text = 1.8
        bline = ylim[1] - 0.2*(ylim[2]-ylim[1])
        #
        # -- Labels GWLs
        GWLs_range = c(1.5,4.35)
        btext = ylim[1] - 0.3*(ylim[2]-ylim[1])
        lines(GWLs_range, c(bline,bline), type='l', lwd=3)
        text(mean(GWLs_range),btext,expression("GWL"), font=1, cex=cex_text*0.9)

        btext2 = ylim[1] - 0.10*(ylim[2]-ylim[1])
        text(1,btext2-0.12,"r.past.", cex=cex_text, font=1, srt=90, adj=c(0.5,0.5))
        text(2,btext2,"1.5", cex=cex_text, font=1, adj=c(0.5,0.5))#, srt=90
        text(3,btext2,"2", cex=cex_text, font=1, adj=c(0.5,0.5))#, srt=90
        text(4,btext2,"4", cex=cex_text, font=1, adj=c(0.5,0.5))#, srt=90

        # -- Labels time slices = modern, mid-term, long-term
        xmodern = 4.5
        xmid = 5.5
        xlate = 7.5
        text(xmid,btext2, "mid.", font=1, cex=cex_text, adj=c(0.5,0.5))#, srt=90
        text(xlate,btext2, "long.", font=1, cex=cex_text, adj=c(0.5,0.5))#, srt=90

        time_slices = c(4.65,8.5)
        lines(time_slices, c(bline,bline), type='l', lwd=3)
        text(mean(time_slices),btext,"Time slices", font=1, cex=cex_text)
    }#end if do_ylab
    
    
}

# %% cell 20
region = 'EUROPE'


figname = paste(CWD,'/../../figs/Figure_12.9/panel_c_',region,'_Q100_boxplot.png',sep='')
png(figname, width=900,height=650)
mat=rbind(
        c(1,0),
        c(2,3)
    )


layout(mat, heights=c(1,1.35), widths=c(1,1))
i = 1
for (subregion in continent_regions){
    mar = c(1,1,2.5,1)
    if (subregion %in% c('NEU','WCE')){
        do_ylab_raw='TRUE'
        mar[2]=4
    }else{
        do_ylab_raw='FALSE'
    }#
    if (subregion %in% c('MED')){
        do_ylab_diff='TRUE'
        mar[4]=4
    }else{
        do_ylab_diff='FALSE'
    }#
    if (subregion %in% c('NEU')){ do_ylab_diff='TRUE' }
    if (subregion %in% c('WCE','MED')){
        do_xlab='TRUE'
        mar[1] = 5.5 # -- bottom margin
    }else{
        do_xlab='FALSE'
    }#
    plot_title = subregion
    ylab = ''
    barplot_satellite_chap12(all_regions[[subregion]],plot_title, ylab, mar=mar, do_xlab=do_xlab,
                             do_ylab_raw=do_ylab_raw, do_ylab_diff=do_ylab_diff)
    
    i = i + 1
}

dev.off()

# %% cell 21
library("IRdisplay")
display_png(file=figname)

# %% cell 23
figname = paste(CWD,'/../../figs/Figure_12.9/panel_c_',region,'_Q100_boxplot.pdf',sep='')
pdf(figname, width=9*1.4,height=6.5*1.4)
mat=rbind(
        c(1,0),
        c(2,3)
    )


layout(mat, heights=c(1,1.35), widths=c(1,1))
i = 1
for (subregion in continent_regions){
    mar = c(1,1,2.5,1)
    if (subregion %in% c('NEU','WCE')){
        do_ylab_raw='TRUE'
        mar[2]=4
    }else{
        do_ylab_raw='FALSE'
    }#
    if (subregion %in% c('MED')){
        do_ylab_diff='TRUE'
        mar[4]=4
    }else{
        do_ylab_diff='FALSE'
    }#
    if (subregion %in% c('NEU')){ do_ylab_diff='TRUE' }
    if (subregion %in% c('WCE','MED')){
        do_xlab='TRUE'
        mar[1] = 5.5 # -- bottom margin
    }else{
        do_xlab='FALSE'
    }#
    plot_title = subregion
    ylab = ''
    barplot_satellite_chap12(all_regions[[subregion]],plot_title, ylab, mar=mar, do_xlab=do_xlab,
                             do_ylab_raw=do_ylab_raw, do_ylab_diff=do_ylab_diff)
    
    i = i + 1
}

dev.off()
