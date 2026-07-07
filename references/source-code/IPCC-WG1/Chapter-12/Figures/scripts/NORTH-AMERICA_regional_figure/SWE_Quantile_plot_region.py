# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/NORTH-AMERICA_regional_figure/SWE_Quantile_plot_region.ipynb

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

# %% cell 4
mask = 'mask14'

# %% cell 6
library(rjson)

# %% cell 8
# -- List of regions for AFRICA
continent_regions = c('NWN','NEN','WNA','CNA','ENA','NCA')

regions_by_continent = list(
    NAM = c('NWN','NEN','WNA','CNA','ENA','NCA')
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

# %% cell 10
clim_periods = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late', '1.5','2','4')

ensemble = 'CMIP6'
json_file = paste(CWD,'/../../data/Figure_12.10/',ensemble,'_NORTH-AMERICA_snw_',mask,'_AR6_regional_averages.json',sep='')
json_data <- fromJSON(paste(readLines(json_file), collapse=""))

for (clim_period in names(json_data)){
    if (clim_period=='85_1995_2014'){ wclim_period='modern' }
    if (clim_period=='85_2041_2060'){ wclim_period='8.5_mid' }
    if (clim_period=='85_2081_2099'){ wclim_period='8.5_late' }
    if (clim_period=='26_2041_2060'){ wclim_period='2.6_mid' }
    if (clim_period=='26_2081_2099'){ wclim_period='2.6_late' }
    if (clim_period=='1.5'){ wclim_period='1.5' }
    if (clim_period=='2'){ wclim_period='2' }
    if (clim_period=='3'){ wclim_period='3' }
    if (clim_period=='4'){ wclim_period='4' }
    for (region_name in names(json_data[[clim_period]])){
        if (json_data[[clim_period]][[region_name]][1] == -99999){
            vals = c(NA,NA,NA)
        }else{
            vals = json_data[[clim_period]][[region_name]]
        }
        all_regions[[region_name]][[ensemble]][[wclim_period]][['vals']] = vals
    }
}

# %% cell 11
all_regions[['CNA']][['CMIP6']][['modern']][['vals']]
#json_data[['85_1995_2014']][['CNA']][1]

# %% cell 13
clim_periods = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late', '1.5','2','4')

ensemble = 'CMIP5'
json_file = paste(CWD,'/../../data/Figure_12.10/',ensemble,'_NORTH-AMERICA_snw_',mask,'_AR6_regional_averages.json',sep='')
json_data <- fromJSON(paste(readLines(json_file), collapse=""))

for (clim_period in names(json_data)){
    if (clim_period=='85_1995_2014'){ wclim_period='modern' }
    if (clim_period=='85_2041_2060'){ wclim_period='8.5_mid' }
    if (clim_period=='85_2081_2099'){ wclim_period='8.5_late' }
    if (clim_period=='26_2041_2060'){ wclim_period='2.6_mid' }
    if (clim_period=='26_2081_2099'){ wclim_period='2.6_late' }
    if (clim_period=='1.5'){ wclim_period='1.5' }
    if (clim_period=='2'){ wclim_period='2' }
    if (clim_period=='3'){ wclim_period='3' }
    if (clim_period=='4'){ wclim_period='4' }
    for (region_name in names(json_data[[clim_period]])){
        if (json_data[[clim_period]][[region_name]][1] == -99999){
            vals = c(NA,NA,NA)
        }else{
            vals = json_data[[clim_period]][[region_name]]
        }
        all_regions[[region_name]][[ensemble]][[wclim_period]][['vals']] = vals
    }
}

# %% cell 14
all_regions[['CNA']][['CMIP5']][['modern']][['vals']]

# %% cell 15
names(json_data)

# %% cell 17
ensemble = 'CORDEX'
wensemble = paste('NAM-22_',ensemble,sep='')
json_file = paste(CWD,'/../../data/Figure_12.10/',wensemble,'_NORTH-AMERICA_snw_',mask,'_AR6_regional_averages.json',sep='')
json_data <- fromJSON(paste(readLines(json_file), collapse=""))

for (clim_period in names(json_data)){
    if (clim_period=='85_1995_2014'){ wclim_period='modern' }
    if (clim_period=='85_2041_2060'){ wclim_period='8.5_mid' }
    if (clim_period=='85_2081_209*'){ wclim_period='8.5_late' }
    if (clim_period=='26_2041_2060'){ wclim_period='2.6_mid' }
    if (clim_period=='26_2081_209*'){ wclim_period='2.6_late' }
    if (clim_period=='1.5'){ wclim_period='1.5' }
    if (clim_period=='2'){ wclim_period='2' }
    if (clim_period=='3'){ wclim_period='3' }
    if (clim_period=='4'){ wclim_period='4' }
    for (region_name in names(json_data[[clim_period]])){
        if (json_data[[clim_period]][[region_name]][1] == -99999){
            vals = c(NA,NA,NA)
        }else{
            all_regions[[region_name]][[ensemble]][[wclim_period]][['vals']] = json_data[[clim_period]][[region_name]]
        }
    }
}

# %% cell 20
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

# %% cell 21
"barplot_satellite_chap12"=function(data, title, ylabel, do_ylab='TRUE', do_xlab='TRUE', mar=c(4,3,2.5,1)){
    #
    # -- Names
    ensembles = c('CORDEX','CMIP5','CMIP6')
    GWLs = c('1.5','2','4')
    scenarios = c('modern', '2.6_mid', '8.5_mid', '2.6_late', '8.5_late')
    nhorizons = length(GWLs)+length(scenarios)
        
    ylim = c(0,100)
    
    # -- position on the x axis of the ensembles
    xpos = c(1,2,3, 4.5, 6, 7, 8, 9)
    xvert = c(1.5,2.5,3.5,5.5,7.5)
    inner_margin = 0.5
    xlim = c(1-inner_margin, max(xpos)+inner_margin)
    general_cex=1.3
    par(cex=general_cex+0.3)
    par(mar=mar)
    plot(1:nhorizons, rep(NA, nhorizons), col='white', ylim=ylim, xlim=xlim,
         xaxt='n', yaxt='n', xlab='', ylab='', xaxs="i", yaxs='i', font=2)#
    par(cex=general_cex)
    mtext(ylabel, 2, font=2, line=2.2, cex=general_cex)
    par(xpd=NA)
    par(font=2)
    
    for (yval in seq(0,100,by=20)){
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
    yvals = seq(0,100, by=20)
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
    vline[1] = ylim[1] - (ylim[2]-ylim[1])*0.25
    if (do_xlab=='TRUE'){
        for (v in xvert){lines(c(v,v),vline,type='l', lwd=1)}
    }else{
        for (v in xvert){lines(c(v,v),ylim,type='l')}
    }

    if (do_xlab=='TRUE'){
        cex_text = 1.8
        bline = ylim[1] - 0.3*(ylim[2]-ylim[1])
        #
        # -- Labels GWLs
        GWLs_range = c(0.5,3.2)
        btext = ylim[1] - 0.5*(ylim[2]-ylim[1])
        lines(c(0.5,3.2), c(bline,bline), type='l', lwd=3)
        text(mean(GWLs_range),btext,expression("GWL"), font=1, adj=c(0.5,0), cex=cex_text*0.9)

        btext2 = ylim[1] - 0.15*(ylim[2]-ylim[1])
        adj_ts = c(0.5,0.5)
        adj_gwl = c(0.5,0.5)
        text(0.8,btext2,"1.5", cex=cex_text, font=1, adj=adj_gwl)
        text(2,btext2,"2", cex=cex_text, font=1, adj=adj_gwl)
        text(3,btext2,"4", cex=cex_text, font=1, adj=adj_gwl)

        # -- Labels time slices = modern, mid-term, long-term
        xmodern = 4.5
        xmid = 6.5
        xlate = 8.5
        text(xmodern,btext2, "r.past", font=1, cex=cex_text, adj=adj_ts)#, srt=90
        text(xmid,btext2, "mid.", font=1, cex=cex_text, adj=adj_ts)
        text(xlate,btext2, "long.", font=1, cex=cex_text, adj=adj_ts)

        time_slices = c(3.6,9.3)
        lines(time_slices, c(bline,bline), type='l', lwd=3)
        text(mean(time_slices),btext,"Time slices", font=1, adj=c(0.5,0), cex=cex_text*0.9)
    }#end if do_ylab

}

# %% cell 22
"draw_legend_box_hor"=function(data, mar=c(0,0,0,0)){

    par(mar=mar)
    plot(0:1,0:1,col='white',xaxt='n',yaxt='n', xlab='', ylab='')#, bty='n')
    text(-0.02,0.88, "Legend", font=2, cex=2, adj=0)
    linewidth = 0.07
    lwd=13
    xcol1 = 0.2
    ycol1 = 0.48
    space_between_cols = linewidth*1.5
    space_between_lines = 0.2
    ycol = ycol1
    xensemble = xcol1 - 0.05
    xensemble = xcol1 - 0.05
    cex_text = 1.7
    cex_title = 1.9
    for (ensemble in c('CMIP6','CMIP5','CORDEX')){
        xcol = xcol1
        text(xensemble, ycol, ensemble, font=2, cex=cex_text, adj=1)
        for (GWL in c('1.5','2','4')){
            lines(c(xcol,xcol+linewidth), c(ycol, ycol), type='l', lwd=lwd, col=data[[ensemble]][[GWL]][['color']])
            if (ensemble=='CMIP6'){
                if (GWL=='1.5'){ tmplab = expression('+1.5'*degree*C) }
                if (GWL=='2'){ tmplab = expression('+2'*degree*C) }
                if (GWL=='4'){ tmplab = expression('+4'*degree*C) }
                text(mean(c(xcol,xcol+linewidth)), ycol1+space_between_lines, tmplab, font=2, cex=cex_text)
                if (GWL=='1.5'){
                    text(xcol, ycol1+space_between_lines*2.2, 'GWL', font=2, cex=cex_title, adj=0)
                }
            }
            xcol = xcol + space_between_cols
        }
        ycol = ycol - space_between_lines
    }

    xcol1 = 0.55
    ycol = ycol1
    xensemble = xcol1 - 0.05
    xensemble = xcol1 - 0.05
    for (ensemble in c('CMIP6','CMIP5','CORDEX')){
        xcol = xcol1
        for (time_slice in c('modern','2.6_late','8.5_late')){
            if (time_slice=='modern'){ tmplab = 'r.past' }
            if (time_slice=='2.6_late'){ tmplab = '2.6' }
            if (time_slice=='8.5_late'){ tmplab = '8.5' }
            lines(c(xcol,xcol+linewidth), c(ycol, ycol), type='l', lwd=lwd, col=data[[ensemble]][[time_slice]][['color']])
            if (ensemble=='CMIP6'){
                text(mean(c(xcol,xcol+linewidth)), ycol1+space_between_lines, tmplab, font=1, cex=cex_text)
            }
            if (time_slice=='modern'){
                text(xcol, ycol1+space_between_lines*2.2, 'RCPs/SSPs', font=2, cex=cex_title, adj=0)
            }
            xcol = xcol + space_between_cols
        }
        ycol = ycol - space_between_lines
    }
        ycol = ycol - space_between_lines
    
    yline = 0.5
    ypos = 0.5
    ylen = 0.3
    xx = 0.9
    lines(c(xx,xx),c(ypos-ylen,ypos+ylen), type='l', lwd=lwd/2, col='black')
    points(xx,ypos, pch=16, cex=2.2)
    text(xx+0.02,ypos+(ylen*1.1), expression(paste(90^th,"p")), font=1, cex=cex_text,adj=0)
    text(xx+0.02,ypos-(ylen*1.1), expression(paste(10^th,"p")), font=1, cex=cex_text,adj=0)
    text(xx+0.02,ypos, "median", font=1, cex=cex_text, adj=0)
    
}

# %% cell 23
region = 'NORTH-AMERICA'


figname = paste(CWD,'/../../figs/Figure_12.10/panel_d_',region,'_SWE_',mask,'_boxplot.png',sep='')
png(figname, width=900,height=1100)
mat=rbind(
c(1,2),
c(3,4),
c(5,0),
c(6,6)
)

continent_regions = c('NWN','NEN','WNA','CNA','ENA')

layout(mat, heights=c(1,1,1.35,0.7), widths=c(1.2,1))
i = 1
for (subregion in continent_regions){
    mar = c(1,1,2.5,1)
    
    if (subregion %in% c('NWN','WNA','ENA')){
        do_ylab='TRUE'
        mar[2]=4
    }else{
        do_ylab='FALSE'
    }#
    if (subregion %in% c('ENA','CNA')){
        do_xlab='TRUE'
        #mar[1] = 5 # -- bottom margin
    }else{
        do_xlab='FALSE'
    }#
    if (subregion %in% c('ENA')){mar[1] = 5}

    plot_title = subregion
    ylab = ''
    barplot_satellite_chap12(all_regions[[subregion]],plot_title, ylab, mar=mar, do_ylab=do_ylab, do_xlab=do_xlab)
    
    i = i + 1
}
draw_legend_box_hor(all_regions[[subregion]],mar=c(0,0,3,0))
dev.off()

# %% cell 24
library("IRdisplay")
display_png(file=figname)

# %% cell 26
figname = paste(CWD,'/../../figs/Figure_12.10/panel_d_',region,'_SWE_',mask,'_boxplot.pdf',sep='')
pdf(figname, width=9*1.4,height=11*1.4)
mat=rbind(
c(1,2),
c(3,4),
c(5,0),
c(6,6)
)

continent_regions = c('NWN','NEN','WNA','CNA','ENA')

layout(mat, heights=c(1,1,1.35,0.7), widths=c(1.2,1))
i = 1
for (subregion in continent_regions){
    mar = c(1,1,2.5,1)
    
    if (subregion %in% c('NWN','WNA','ENA')){
        do_ylab='TRUE'
        mar[2]=4
    }else{
        do_ylab='FALSE'
    }#
    if (subregion %in% c('ENA','CNA')){
        do_xlab='TRUE'
        #mar[1] = 5 # -- bottom margin
    }else{
        do_xlab='FALSE'
    }#
    if (subregion %in% c('ENA')){mar[1] = 5}

    plot_title = subregion
    ylab = ''
    barplot_satellite_chap12(all_regions[[subregion]],plot_title, ylab, mar=mar, do_ylab=do_ylab, do_xlab=do_xlab)
    
    i = i + 1
}
draw_legend_box_hor(all_regions[[subregion]],mar=c(0,0,3,0))
dev.off()
