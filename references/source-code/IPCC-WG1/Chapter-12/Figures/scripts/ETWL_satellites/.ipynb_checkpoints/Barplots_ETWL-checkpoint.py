# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/ETWL_satellites/.ipynb_checkpoints/Barplots_ETWL-checkpoint.ipynb

# %% cell 2
library(rjson)
library("IRdisplay")

# %% cell 3
CWD = getwd()

# %% cell 4
AR6_regions = c('Global','NWN', 'NEN', 'NEU', 'RAR',
'WNA', 'CNA', 'ENA', 'WCE', 'EEU', 'WSB', 'ESB', 'RFE',
'NCA', 'SCA', 'CAR', 'MED', 'WCA', 'ECA', 'TIB', 'EAS',
'NWS', 'NSA', 'SAH', 'WAF', 'CAF', 'NEAF', 'ARP', 'SAS',
'SAM', 'NES', 'WSAF', 'ESAF', 'MDG', 'SEAF', 'SEA', 
'SWS', 'SES', 'SSA', 'NAU', 'CAU', 'EAU', 'SAU', 'NZ')


res = list()
for (scenario in c('RCP85','RCP45')){
    for (horizon in c('2050','2100')){
        json_file = paste(CWD,'/../../data/ETWL/Vousdoukas_ETWL_by_AR6_region_',scenario,'_',horizon,'.json',sep='')
        if (horizon=='2050'){term='mid'}
        if (horizon=='2100'){term='late'}
        wname = paste(scenario,term,sep='_')
        res[[wname]] = list()
        
        json_data <- fromJSON(paste(readLines(json_file), collapse=""))
        for (subregion in AR6_regions){
            res[[wname]][[subregion]] = c(json_data[[subregion]]$q5, json_data[[subregion]]$median, json_data[[subregion]]$q95)
        }#end subregion
    }#end horizon
}#and scenario

json_file = paste(CWD,'/../../data/ETWL/Vousdoukas_ETWL_by_AR6_region_modern.json',sep='')

json_data <- fromJSON(paste(readLines(json_file), collapse=""))
wname='modern'
for (subregion in AR6_regions){
    res[[wname]][[subregion]] = c(json_data[[subregion]]$q5, json_data[[subregion]]$median, json_data[[subregion]]$q95)
}#end subregion

# %% cell 5
regions_filename=paste(CWD,'/../../scripts/ATLAS/reference-regions/IPCC-WGI-reference-regions-v4_coordinates.csv',sep='')
tmp = read.csv(regions_filename, sep=',', header=FALSE)
names_list = list()
for (i in 1:nrow(tmp)){
    names_list[[as.character(tmp[i,3])]] = as.character(tmp[i,4])
}

# %% cell 6
Ebru_file = paste(CWD,'/../../data/Figure_S12.6/Kirezci_ESL.csv',sep='')
test = read.csv(Ebru_file, sep=';')

#;;Present day;Present day;Present day;RCP45 2050;RCP45 2050;RCP45 2050;RCP45 2100;RCP45 2100;RCP45 2100;RCP85 2050;RCP85 2050;RCP85 2050;RCP85 2100;RCP85 2100;RCP85 2100
Ebru_res = list()
Ebru_res[['modern']] = list()
Ebru_res[['RCP45_mid']] = list()
Ebru_res[['RCP45_late']] = list()
Ebru_res[['RCP85_mid']] = list()
Ebru_res[['RCP85_late']] = list()


for (i in 2:nrow(test)){
    region_name = as.character(test[i,1]) # 2!
    if (region_name=='Global'){
        short_name='Global'
    }else{
        short_name = gsub('%','',gsub("[^0-9A-Za-z///' ]","%" , as.character(names_list[[region_name]])))
    }#
    
    print(paste(region_name,short_name))

    # -- Modern
    tmp_q5  = as.numeric(gsub(',','.', as.character(test[i,3])))
    tmp_q50 = as.numeric(gsub(',','.', as.character(test[i,4])))
    tmp_q95 = as.numeric(gsub(',','.', as.character(test[i,5])))
    Ebru_res[['modern']][[short_name]] = c( tmp_q5, tmp_q50, tmp_q95 )
    # -- RCP45_2050
    tmp_q5  = as.numeric(gsub(',','.', as.character(test[i,6])))
    tmp_q50 = as.numeric(gsub(',','.', as.character(test[i,7])))
    tmp_q95 = as.numeric(gsub(',','.', as.character(test[i,8])))
    Ebru_res[['RCP45_mid']][[short_name]] = c( tmp_q5, tmp_q50, tmp_q95 )
    # -- RCP45_2100
    tmp_q5  = as.numeric(gsub(',','.', as.character(test[i,9])))
    tmp_q50 = as.numeric(gsub(',','.', as.character(test[i,10])))
    tmp_q95 = as.numeric(gsub(',','.', as.character(test[i,11])))
    Ebru_res[['RCP45_late']][[short_name]] = c( tmp_q5, tmp_q50, tmp_q95 )
    # -- RCP85_2050
    tmp_q5  = as.numeric(gsub(',','.', as.character(test[i,12])))
    tmp_q50 = as.numeric(gsub(',','.', as.character(test[i,13])))
    tmp_q95 = as.numeric(gsub(',','.', as.character(test[i,14])))
    Ebru_res[['RCP85_mid']][[short_name]] = c( tmp_q5, tmp_q50, tmp_q95 )
    # -- RCP85_2100
    tmp_q5  = as.numeric(gsub(',','.', as.character(test[i,15])))
    tmp_q50 = as.numeric(gsub(',','.', as.character(test[i,16])))
    tmp_q95 = as.numeric(gsub(',','.', as.character(test[i,17])))
    Ebru_res[['RCP85_late']][[short_name]] = c( tmp_q5, tmp_q50, tmp_q95 )

}

# %% cell 7
"ETWL_barplot"=function(res, res2, title, ylab='FALSE', mar=c(3,4,2,0), do_ylab='TRUE', do_xlab='TRUE'){

    # RCP85-RCP45
    general_cex = 1.6
    pcex=1.4
    pcex_w=1.2
    lwdp = 4
    lwd = 3

    color_rcp45='dodgerblue2'
    color_rcp85='firebrick2'

    color = 'dodgerblue2'
    
    par(cex=general_cex)
    par(mar=mar)
    ylim=c(0,6)
    
    xval = 1:7
    plot(xval, rep(0,length(xval)), type='l', col='white', lty=2, lwd=2, ylim=ylim, xlab='',
         ylab='', xaxt='n', yaxt='n', xaxs='i',yaxs='i')
    for (i in c(3,5)){
        lines(rep(i,2),ylim, type='l',col='gray80',lwd=8)
    }
    for (i in c(2,4)){
        lines(c(1,7),rep(i,2), type='l',lty=2, col='gray80',lwd=4)
    }
    # -- X axis
    axis(1, at=c(2,4), labels=c('',''), font=2)
    if (do_xlab=='TRUE'){
        par(cex=2.8)
        axis(1, at=c(2,6), tick='FALSE', labels=c('r.past','long-'), font=1, line=-0.5)
        axis(1, at=c(4), tick='FALSE', labels=c('mid-'), font=1, line=-0.5)
        axis(1, at=c(4,6), tick='FALSE', labels=c('term','term'), font=1, line=0.9)
        par(cex=general_cex)
    }#end
    
    # -- Y axis
    par(cex=3)
    axis(2, at=seq(0,6,by=2), labels = c('','','',''), font=2, las=1)
    if (do_ylab=='TRUE'){ axis(2, at=seq(0,6,by=2), las=1, tick='FALSE', line=-0.4) }
    par(cex=general_cex)
    
    # -- Title
    mtext(title,3, font=2, cex=3.1, line=0.5)#, adj=0)
    if (ylab=='TRUE'){ mtext("Meters",2, font=2, cex=1.5, line=2.5) }
    
    xmod = 2
    xmid = 4
    xlong = 6
    xadj = 0.3


    # -- Modern
    # -------------------------------
    resname = 'modern'
    color = 'black'
    # -- Vousdoukas
    lines(c(xmod-xadj, xmod-xadj), c(res[[resname]][1], res[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmod-xadj, res[[resname]][2], pch=16, col=color, cex=pcex, lwd=lwdp)
    # -- Ebru
    color = 'black'
    lines(c(xmod+xadj, xmod+xadj), c(res2[[resname]][1], res2[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmod+xadj, res2[[resname]][2], pch=16, col='white', cex=pcex_w, lwd=lwdp)
    points(xmod+xadj, res2[[resname]][2], col=color, cex=pcex_w, lwd=lwdp)

    # -- Mid term
    # -------------------------------
    # -- Vousdoukas
    resname = 'RCP85_mid'
    color = color_rcp85
    lines(c(xmid+xadj, xmid+xadj), c(res[[resname]][1], res[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmid+xadj, res[[resname]][2], pch=16, col=color, cex=pcex, lwd=lwdp)

    resname = 'RCP45_mid'
    color = color_rcp45
    lines(c(xmid-2*xadj, xmid-2*xadj), c(res[[resname]][1], res[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmid-2*xadj, res[[resname]][2], pch=16, col=color, cex=pcex, lwd=lwdp)

    # -- Ebru
    resname = 'RCP85_mid'
    color = color_rcp85
    lines(c(xmid+2*xadj, xmid+2*xadj), c(res2[[resname]][1], res2[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmid+2*xadj, res2[[resname]][2], pch=16, col='white', cex=pcex_w, lwd=lwdp)
    points(xmid+2*xadj, res2[[resname]][2], col=color, lwd=lwdp, cex=pcex_w)

    
    resname = 'RCP45_mid'
    color = color_rcp45
    lines(c(xmid-xadj, xmid-xadj), c(res2[[resname]][1], res2[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xmid-xadj, res2[[resname]][2], pch=16, col='white', cex=pcex_w, lwd=lwdp)
    points(xmid-xadj, res2[[resname]][2], lwd=lwdp, col=color, cex=pcex_w)
    
    # -- Late term
    # -------------------------------
    # -- Vousdoukas
    resname = 'RCP85_late'
    color = color_rcp85
    lines(c(xlong+xadj, xlong+xadj), c(res[[resname]][1], res[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xlong+xadj, res[[resname]][2], pch=16, col=color, cex=pcex, lwd=lwdp)

    resname = 'RCP45_late'
    color = color_rcp45
    lines(c(xlong-2*xadj, xlong-2*xadj), c(res[[resname]][1], res[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xlong-2*xadj, res[[resname]][2], pch=16, col=color, cex=pcex, lwd=lwdp)

    # -- Ebru
    resname = 'RCP85_late'
    color = color_rcp85
    lines(c(xlong+2*xadj, xlong+2*xadj), c(res2[[resname]][1], res2[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xlong+2*xadj, res2[[resname]][2], pch=16, col='white', cex=pcex_w, lwd=lwdp)
    points(xlong+2*xadj, res2[[resname]][2], lwd=lwdp, col=color, cex=pcex_w)

    resname = 'RCP45_late'
    color = color_rcp45
    lines(c(xlong-xadj, xlong-xadj), c(res2[[resname]][1], res2[[resname]][3]), type='l', lwd=lwd, col=color)
    points(xlong-xadj, res2[[resname]][2], pch=16, col='white', cex=pcex_w, lwd=lwdp)
    points(xlong-xadj, res2[[resname]][2], lwd=lwdp, col=color, cex=pcex_w)
    
}


"legend_ETWL"=function(mar=c(3,4,2,0)){

    # RCP85-RCP45
    general_cex = 1.7
    pcex=1.6
    lwdp = 4
    lwd = 6

    color='dodgerblue2'
    color_rcp45='dodgerblue2'
    color_rcp85='firebrick2'
    
    par(cex=general_cex)
    par(mar=mar)
    ylim=c(-1000,600)
    xval = 1:5
    plot(0:1, 0:1, type='l', col='white', bty='n',
         lty=2, lwd=2, ylim=c(0,1), xlab='', ylab='', xaxt='n', yaxt='n', xaxs='i')
    
    # -- Title
    text(0.08, 0.9,'Legend', font=2, cex=2.3)#, line=0.5, adj=-1)
    cex_text = 1.8

    cex_lines_points = 1.7
    # -- p5/median/p95
    ymedian = 0.5
    yhalflen = 0.25
    xmedian = 0.15
    xtextadj = 0.02
    lines(c(xmedian, xmedian), c(ymedian-yhalflen,ymedian+yhalflen), type='l', lwd=lwd*cex_lines_points, col='black')
    par(cex=general_cex)
    points(xmedian, ymedian, pch=16, col='black', cex=pcex*1.5, lwd=lwdp*cex_lines_points)
    text(xmedian+xtextadj, ymedian+yhalflen*1.1, expression(paste(95^th,"p")),adj=0, cex=cex_text)
    text(xmedian+xtextadj, ymedian, "Median estimate",adj=0, cex=cex_text)
    text(xmedian+xtextadj, ymedian-yhalflen*1.1, expression(paste(5^th,"p")),adj=0, cex=cex_text)
    par(cex=general_cex)
    
    # -- CMIP5 V - RCP85
    color = color_rcp85
    xrcp85 = 0.38
    lenline = 0.05
    yrcp85 = 0.75
    lines(c(xrcp85, xrcp85+lenline), c(yrcp85,yrcp85), type='l', lwd=lwdp*cex_lines_points, col=color)
    points(xrcp85+(lenline/2), yrcp85, pch=16, col=color, lwd=lwdp*cex_lines_points, cex=pcex*cex_lines_points)
    text(xrcp85+lenline*1.2, yrcp85, "CMIP5_V RCP8.5",adj=0, font=1, cex=cex_text)
    
    space_between_lines = 0.25
    # -- CMIP5 V - RCP45
    color = color_rcp45
    xrcp45 = xrcp85
    yrcp45 = yrcp85 - space_between_lines
    lines(c(xrcp45, xrcp45+lenline), c(yrcp45,yrcp45), type='l', lwd=lwd*cex_lines_points, col=color)
    points(xrcp45+(lenline/2), yrcp45, pch=16, col=color, lwd=lwdp*cex_lines_points, cex=pcex*cex_lines_points)
    text(xrcp45+lenline*1.2, yrcp45, "CMIP5_V RCP4.5",adj=0, font=1, cex=cex_text)

    # -- CMIP5 V - r.past
    color = 'black'
    xrcp45 = xrcp85
    yrcp45 = yrcp45 - space_between_lines
    lines(c(xrcp45, xrcp45+lenline), c(yrcp45,yrcp45), type='l', lwd=lwd*cex_lines_points, col=color)
    points(xrcp45+(lenline/2), yrcp45, pch=16, col=color, lwd=lwdp*cex_lines_points, cex=pcex*cex_lines_points)
    text(xrcp45+lenline*1.2, yrcp45, "CMIP5_V r.past",adj=0, font=1, cex=cex_text)

    
    # -- CMIP5 K - RCP85
    color = color_rcp85
    yrcp85 = 0.75
    xrcp85 = 0.65
    lines(c(xrcp85, xrcp85+lenline), c(yrcp85,yrcp85), type='l', lwd=lwdp*cex_lines_points, col=color)
    points(xrcp85+(lenline/2), yrcp85, pch=16, col='white', lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    points(xrcp85+(lenline/2), yrcp85, col=color, lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    text(xrcp85+lenline*1.2, yrcp85, "CMIP5_K RCP8.5",adj=0, font=1, cex=cex_text)
    
    # -- CMIP5 K - RCP45
    color = color_rcp45
    xrcp45 = 0.65
    yrcp45 = yrcp85 - space_between_lines
    lines(c(xrcp45, xrcp45+lenline), c(yrcp45,yrcp45), type='l', lwd=lwd*cex_lines_points, col=color)
    points(xrcp45+(lenline/2), yrcp45, pch=16, col='white', lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    points(xrcp45+(lenline/2), yrcp45, col=color, lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    text(xrcp45+lenline*1.2, yrcp45, "CMIP5_K RCP4.5",adj=0, font=1, cex=cex_text)

    # -- CMIP5 K - r.past
    color = 'black'
    xrcp45 = 0.65
    yrcp45 = yrcp45 - space_between_lines
    lines(c(xrcp45, xrcp45+lenline), c(yrcp45,yrcp45), type='l', lwd=lwd*cex_lines_points, col=color)
    points(xrcp45+(lenline/2), yrcp45, pch=16, col='white', lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    points(xrcp45+(lenline/2), yrcp45, col=color, lwd=lwdp*cex_lines_points, cex=(pcex-0.2)*cex_lines_points)
    text(xrcp45+lenline*1.2, yrcp45, "CMIP5_K r.past",adj=0, font=1, cex=cex_text)


}

# %% cell 8
#3 lines
#4 columns
#legend is the last
fsize = 2000
outfilename = paste(CWD,'/../../figs/Satellite_barplots/Figure_S12.6_ETWL_satellite.png',sep='')
png(outfilename, width=fsize*1.4,height=fsize)

AR6_regions = c('NWN', 'NEN',        'NEU' ,                'RAR' ,
                'WNA', 'CNA', 'ENA', 'WCE' , 'EEU' , 'WCA' ,        'RFE' ,
                'NCA', 'SCA', 'CAR', 'MED' , 'SAH' , 'ARP' , 'SAS', 'EAS' ,
                'NWS', 'NSA', 'NES', 'WAF' , 'CAF' , 'NEAF',        'SEA',
                'SWS', 'SES', 'SSA', 'WSAF', 'ESAF', 'SEAF', 'MDG' , 
                'Global', 'NAU' , 'CAU' , 'EAU' , 'SAU' , 'NZ')

mat = rbind(
c(1,2,0,3,0,0,4,0),
c(5,6,7,8,9,10,0,11),
c(12,13,14,15,16,17,18,19),
c(20:25,0,26),
c(27:33,0),
c(34,0,0,35,36,37,38,39),
c(40,40,40,40,40,0,0,0)
)

layout(mat,height=c(1,1,1,1,1,1.2,0.8))

ylab = ''
for (i in 1:length(AR6_regions)){
    subregion = AR6_regions[i]
    wres = list()
    wres_Ebru = list()
    for (wname in c('modern','RCP85_mid', 'RCP85_late','RCP45_mid','RCP45_late')){
        wres[[wname]] = res[[wname]][[subregion]]
        wres_Ebru[[wname]] = Ebru_res[[wname]][[subregion]]
    }
    
    if (subregion %in% c('Global','NAU','CAU','EAU','SAU','NZ')){
        do_xlab='TRUE'
        mar=c(3,2,2,0)
    }else{
        do_xlab='FALSE'
        mar=c(1,2,2,0)
    }#

    plot_title = subregion
    do_ylab='TRUE'
    if (subregion=='Legend'){
        legend_ETWL(mar=c(1,2,2,0))
    }else{
        ETWL_barplot(wres, wres_Ebru, subregion, mar=mar, do_ylab=do_ylab, do_xlab=do_xlab)
    }
}
legend_ETWL(mar=c(1,2,1,0))

dev.off()

library("IRdisplay")
display_png(file=outfilename)

# %% cell 11
fsize = 20*1.4
outfilename = paste(CWD,'/../../figs/Satellite_barplots/Figure_S12.6_ETWL_satellite.pdf',sep='')
pdf(outfilename, width=fsize*1.4,height=fsize)

AR6_regions = c('NWN', 'NEN',        'NEU' ,                'RAR' ,
                'WNA', 'CNA', 'ENA', 'WCE' , 'EEU' , 'WCA' ,        'RFE' ,
                'NCA', 'SCA', 'CAR', 'MED' , 'SAH' , 'ARP' , 'SAS', 'EAS' ,
                'NWS', 'NSA', 'NES', 'WAF' , 'CAF' , 'NEAF',        'SEA',
                'SWS', 'SES', 'SSA', 'WSAF', 'ESAF', 'SEAF', 'MDG' , 
                'Global', 'NAU' , 'CAU' , 'EAU' , 'SAU' , 'NZ')

mat = rbind(
c(1,2,0,3,0,0,4,0),
c(5,6,7,8,9,10,0,11),
c(12,13,14,15,16,17,18,19),
c(20:25,0,26),
c(27:33,0),
c(34,0,0,35,36,37,38,39),
c(40,40,40,40,40,0,0,0)
)

layout(mat,height=c(1,1,1,1,1,1.2,0.8))

ylab = ''
for (i in 1:length(AR6_regions)){
    subregion = AR6_regions[i]
    wres = list()
    wres_Ebru = list()
    for (wname in c('modern','RCP85_mid', 'RCP85_late','RCP45_mid','RCP45_late')){
        wres[[wname]] = res[[wname]][[subregion]]
        wres_Ebru[[wname]] = Ebru_res[[wname]][[subregion]]
    }
    
    if (subregion %in% c('Global','NAU','CAU','EAU','SAU','NZ')){
        do_xlab='TRUE'
        mar=c(3,2,2,0)
    }else{
        do_xlab='FALSE'
        mar=c(1,2,2,0)
    }#

    plot_title = subregion
    do_ylab='TRUE'
    if (subregion=='Legend'){
        legend_ETWL(mar=c(1,2,2,0))
    }else{
        ETWL_barplot(wres, wres_Ebru, subregion, mar=mar, do_ylab=do_ylab, do_xlab=do_xlab)
    }
}
legend_ETWL(mar=c(1,2,1,0))

dev.off()
