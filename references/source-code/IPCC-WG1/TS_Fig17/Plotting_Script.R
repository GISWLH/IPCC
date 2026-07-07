library(extrafont)

makeTransparent<-function(someColor, alpha=100)
{
  newColor<-col2rgb(someColor)
  apply(newColor, 2, function(curcoldata){rgb(red=curcoldata[1], green=curcoldata[2],
                                              blue=curcoldata[3],alpha=alpha, maxColorValue=255)})
}

col_red<-rgb(222/255,45/255,38/255,0.8)
col_red_trans<-rgb(222/255,45/255,38/255,0.3)
col_blue<-rgb(49/255,130/255,189/255,0.8)
col_grey<-'grey'
col_bg_bars<-'grey90'
bg_panel1<-"transparent"
bg_panel2<-"transparent"
bg_panel3<-"blanchedalmond"

panel_a_data<-read.csv('panel_a.csv')
panel_b_data<-read.csv('panel_b.csv')
panel_c_data<-read.csv('panel_c.csv')

load('bgc_feedbacks.Rdata')


#Some constants
jmax<-3 #mean, min & max of range
of<-0.5 #0.9offset for bars
wd<-0.5 #width of bars
ds<-0.5 #0.7 #scaling constant for bars
#Panel #1: ES feedbacks
imax_panel1<-6          # number of feedbacks
xmax_panel1=3           # feedback range
xmin_panel1=-5         # feedback range
#Panel #2: Non-CO2 BGC and BGP
imax_panel2<-6          # number of feedbacks
xmin_panel2<-(-0.5)     # feedback range  
xmax_panel2<-0.5*3/5    # feedback range
#Panel #3: CO2 feedbacks
imax_panel3<-4          # number of feedbacks
xmax_panel3=3           # feedback range   
xmin_panel3=-5          # feedback range

#Set up data matrix and names for Panel #1 
panel1_names<-c()
panel1_data<-array(NA,c(imax_panel1,jmax)); 

index<-0
panel1_names<-c(expression(paste(bold('Total '))),panel1_names)
panel1_data[imax_panel1-index,1:3]<-as.numeric(panel_a_data[1,2:4])
index<-index+1
  
panel1_names<-c(expression(paste('Planck ')),panel1_names)
panel1_data[imax_panel1-index,]<-as.numeric(panel_a_data[2,2:4])
index<-index+1
  
#panel1_names<-c(expression(paste('WV+LR')),panel1_names)
panel1_names<-c(expression(paste('Water vapour and lapse rate')),panel1_names)
panel1_data[imax_panel1-index,]<-as.numeric(panel_a_data[3,2:4])
index<-index+1
  
panel1_names<-c(expression(paste('Surface albedo')),panel1_names)
panel1_data[imax_panel1-index,]<-as.numeric(panel_a_data[4,2:4])
index<-index+1
  
panel1_names<-c(expression(paste('Clouds')),panel1_names)
panel1_data[imax_panel1-index,]<-as.numeric(panel_a_data[5,2:4])
index<-index+1
  
panel1_names<-c(expression(paste('')),panel1_names)
panel1_data[imax_panel1-index,]<-as.numeric(panel_a_data[6,2:4])
index<-index+1
  
#Set-up data matrix and names for panel 2
panel2_data_PF<-panel2_data<-array(NA,c(imax_panel2,jmax));panel2_names<-c()
  
index<-0
panel2_names<-c(expression(paste(bold('Total'),' (without permafrost feedback)')),panel2_names)
panel2_data[imax_panel1-index,]<-as.numeric(panel_b_data[1,2:4])
index<-index+1
  
panel2_names<-c(expression(paste(CH[4],' source response to climate')),panel2_names)
panel2_data[imax_panel2-index,]<-as.numeric(panel_b_data[2,2:4])
panel2_data_PF[imax_panel2-index,]<-as.numeric(panel_b_data[3,2:4])
index<-index+1  
  
panel2_names<-c(expression(paste('atm. ',CH[4],' lifetime response to climate')),panel2_names)
panel2_data[imax_panel2-index,]<-as.numeric(panel_b_data[4,2:4])
index<-index+1
  
panel2_names<-c(expression(paste(N[2],'O source response to climate')),panel2_names)
panel2_data[imax_panel2-index,]<-as.numeric(panel_b_data[5,2:4])
index<-index+1
  
panel2_names<-c(expression(paste('Other non-',CO[2],' biogeochemical')),panel2_names)
panel2_data[imax_panel2-index,]<-as.numeric(panel_b_data[6,2:4])
index<-index+1
  
panel2_names<-c(expression(paste('Biogeophysical')),panel2_names)
panel2_data[imax_panel2-index,]<-as.numeric(panel_b_data[7,2:4])
index<-index+1
  
# Setup data matrix and names for Carbon-Cycle Feedbacks
panel3_data_PF<-panel3_data<-array(NA,c(imax_panel3,jmax))
panel3_names<-c()
  
index<-0
panel3_names<-c(expression(paste('Land carbon response to ',CO[2])),panel3_names)
panel3_data[imax_panel3-index,]<-as.numeric(panel_c_data[1,2:4])
index<-index+1
  
panel3_names<-c(expression(paste('Ocean carbon response to ',CO[2])),panel3_names)
panel3_data[imax_panel3-index,]<-as.numeric(panel_c_data[2,2:4])
index<-index+1
  
panel3_names<-c(expression(paste('Land carbon response to ',climate)),panel3_names)
panel3_data[imax_panel3-index,]<-as.numeric(panel_c_data[3,2:4])
panel3_data_PF[imax_panel3-index,]<-as.numeric(panel_c_data[4,2:4])
index<-index+1  
  
panel3_names<-c(expression(paste('Ocean carbon response to ',climate)),panel3_names)
panel3_data[imax_panel3-index,]<-as.numeric(panel_c_data[5,2:4])
  
#split bars into positive and negative feedbacks (for color coding)
  panel1_posfb<-panel1_negfb<-panel1_data[,1]
  panel1_negfb[panel1_negfb>=0]<-NA
  panel1_posfb[panel1_posfb<0]<-NA
  panel2_posfb<-panel2_negfb<-panel2_data[,1]
  panel2_negfb[panel2_negfb>=0]<-NA
  panel2_posfb[panel2_posfb<0]<-NA  
  panel2_posfb_PF<-panel2_data_PF[,1]
  panel2_posfb_PF[panel2_posfb_PF<0]<-NA 
  panel3_posfb<-panel3_negfb<-panel3_data[,1]
  panel3_negfb[panel3_negfb>=0]<-NA
  panel3_posfb[panel3_posfb<0]<-NA  
  panel3_posfb_PF<-panel3_data_PF[,1]
  panel3_posfb_PF[panel3_posfb_PF<0]<-NA 

#open figure file  
  outputformat<-'pdf'  
  if(outputformat=='pdf') {loadfonts(device="pdf");pdf('./AR6_TS_Figure17.pdf',height=7,width=7,family ='Arial Narrow')}
  if(outputformat=='png') png('./AR6_TS_Figure17.png',height=7,width=7,units='in',res=300,bg='white',family='Arial Narrow')
  if(outputformat=='svg') svg('./AR6_TS_Figure17.svg',height=7,width=7,family='Arial Narrow')
  if(outputformat=='eps') postscript('./AR6_TS_Figure17.eps',height=7,width=7,family='Arial Narrow')
  
  mat<-matrix(c(rep(1,7),rep(2,6),rep(3,5)),ncol=1)
  layout(mat)
  par(mai=c(0.3,1.7,0.7,1.2),mgp=c(1.5,0.2,0),xpd=NA)
  
  # Panel A: ECS relevant climate feedbacks
  # make plot frame with gray alternating bars, ticks and a zero line
  mc<-barplot(c(rep(c(0,5.4),3)),width=1,space=0,
              horiz = T,xlim=c(xmin_panel1,xmax_panel1),ylim=c(-0.5,5.8),
              border=NA,col=col_bg_bars,
              las=1,names.arg=NA,
              xaxt='n',
              xlab=expression(paste('climate feedback parameter (W ',m^{-2},' ',degree,C^{-1},')')))
  barplot(c(rep(c(0,xmin_panel1),3)),width=1,space=0,horiz = T,border=NA,col=col_bg_bars,add=TRUE,xaxt='n')
  axis(1,tck=1,at=c(xmin_panel1,seq(-3.5,xmax_panel1,0.5)),col.ticks='grey')
  axis(1,tck=0.025,at=seq(xmin_panel1,xmax_panel1,0.1),lab=NA,col.ticks='grey')
  lines(c(0,0),c(-0.8,6),lwd=1,col='black')
  
  #add panel title
  mtext('(a) Feedbacks in the Climate System',3,4,padj = 1,adj=0,cex=0.8)
  
  #add feedback labels to left of plot
  text(x=xmin_panel1-0.05,y=mc,panel1_names,las=1,adj=1)
  text(x=xmin_panel1-0.05,y=mc[1],expression(paste('Biogeophysical and')),las=1,adj=1)
  text(x=xmin_panel1-0.05,y=mc[1]-0.5,expression(paste('non-',CO[2],' biogeochemical')),las=1,adj=1)
  text(x=xmin_panel1-0.05,y=mc[1]-1.0,expression(paste('(',bold('Total'),' from panel (b))')),las=1,adj=1)
  
  #add data
  barplot(panel1_posfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel1-1)),width=wd,
          border='black',col=col_red)
  barplot(panel1_negfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel1-1)),width=wd,
          border='black',col=col_blue)
  #add very likely range
  arrows(panel1_data[,2],mc,panel1_data[,3],mc,angle=90,len=0.02,code=3,lwd=2)  
  
  #add mean and very likely range as text to the left 
  text(4.5,6.5,expression(paste('Mean [',italic('very likely'),' range]',sep='')),adj=0.5,col='black')
  text(y=mc,x=4.5,paste(format(round(panel1_data[,1]*100)/100),' [',format(round(panel1_data[,2]*100)/100),' to ',format(round(panel1_data[,3]*100)/100),']',sep=''))
  
  #add arrows
  arrows(0,6.3,-3.5,6.3,col=col_blue,angle=45,code=2,len=0.06,lwd=3)
  text(-3.5/2,7.3,expression(paste(bold('Negative feedbacks'),' diminish the')),adj=0.5,col=col_blue)
  text(-3.5/2,6.8,'initial climate response to radiative forcing',adj=0.5,col=col_blue)
  arrows(0,6.3,3.5,6.3,col=col_red,angle=45,code=2,len=0.06,lwd=3)
  text(3.5/2,7.3,expression(paste(bold('Positive feedbacks'),' amplify the')),adj=0.5,col=col_red)
  text(3.5/2,6.8,'initial climate response to radiative forcing',adj=0.5,col=col_red)
  
  
  #Panel B: Other bgc bgp feedbacks
  #add background color
  par(mai=c(0.4,1.7,0.4,1.2),mgp=c(1.5,0.2,0),xpd=NA)
  plot.new()
  rect(par("usr")[1],par("usr")[3],par("usr")[2],par("usr")[4],col = bg_panel2,border=NA)
  par(new=T)
  # make plot frame with gray alternating bars, ticks and a zero line
  mc<-barplot(c(rep(c(0,0.615),imax_panel2/2)),width=1,space=0,
              horiz = T,xlim=c(xmin_panel2,xmax_panel2),ylim=c(0,5.8),
              border=NA,col=col_bg_bars,
              las=1,names.arg=panel2_names,
              xaxt='n',
              xlab=expression(paste('climate feedback parameter (W ',m^{-2},' ',degree,C^{-1},')')))
  barplot(c(rep(c(0,xmin_panel2),imax_panel2/2),0),width=1,space=0,horiz = T,border=NA,col=col_bg_bars,add=TRUE,xaxt='n')
  axis(1,tck=1,at=c(xmin_panel2,round(seq(-0.3,xmax_panel2,0.1)*10)/10),col.ticks='grey')
  axis(1,tck=0.025,at=seq(xmin_panel2,xmax_panel2,0.01),lab=NA,col.ticks='grey')
  lines(c(0,0),c(-0.2,6.),lwd=1,col='black')
  lines(c(0.2,0.2),c(4.2,4.8),lwd=2,col='white')
  lines(c(0.3,0.3),c(4.2,4.8),lwd=2,col='white')
  
  #add title
  mtext(expression(paste('(b) Biogeophysical and non-',CO[2],' Biogeochemical Climate Feedbacks')),3,1.5,padj = 1,adj=0,cex=0.8)
  
  #add data
  barplot(panel2_posfb_PF,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel2-1)),width=wd,
          border='black',col=col_red_trans)  
  barplot(panel2_posfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel2-1)),width=wd,
          border='black',col=col_red)
  barplot(panel2_negfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel2-1)),width=wd,
          border='black',col=col_blue)
  #add very likely range
  idx<-c(1,2,3,4,6)
  arrows(panel2_data[idx,2],mc[idx],panel2_data[idx,3],mc[idx],angle=90,len=0.02,code=3,lwd=2)  
  arrows(panel2_data[5,2],mc[5]+0.1,panel2_data[5,3],mc[5]+0.1,angle=90,len=0.02,code=3,lwd=2)  
  arrows(panel2_data_PF[5,2],mc[5]-0.1,panel2_data_PF[5,3],mc[5]-0.1,angle=90,len=0.02,code=3,lwd=2,col='grey10') 
  
  #add mean and 5-95% range as text to the left   
  text(0.51,6.5,'Mean [5-95% range]',adj=0.5,col='black')
  text(y=mc,x=0.51,paste(format(round(panel2_data[,1]*100)/100),' [',
                         format(round(panel2_data[,2]*100)/100),' to ',
                         format(round(panel2_data[,3]*100)/100),']',sep=''))
  
  legend(xy.coords(x=0.15,y=mc[5]+(mc[6]-mc[5])/2),
         leg=c('permafrost feedback'),
         pch=c(-1),
         density=c(NA),
         border=c('black'),
         fill=c(col_red_trans),
         bg='transparent',
         bty='o',box.col='transparent')
  
  
  #Panel C: carbon-cycle climate feedbacks
  #add background color
  par(mai=c(0.6,1.7,0.3,1.2),mgp=c(1.5,0.2,0),xpd=NA)
  plot.new()

  par(new=T)
  ylimit<-3.9
  # make plot frame with gray alternating bars, ticks and a zero line
  mc<-barplot(c(rep(c(0,5.4),imax_panel3/2)),width=1,space=0,
              horiz = T,xlim=c(xmin_panel3,xmax_panel3),ylim=c(0,ylimit),
              border=NA,col=col_bg_bars,
              las=1,names.arg=panel3_names,
              xaxt='n',
              xlab=expression(paste('climate feedback parameter (W ',m^{-2},' ',degree,C^{-1},')')))
  barplot(rep(c(0,xmin_panel3),floor(imax_panel3/2)),width=1,space=0,horiz = T,border=NA,col=col_bg_bars,add=TRUE,xaxt='n')
  barplot(rep(c(xmin_panel3,0),floor(imax_panel3/2)),width=1,space=0,horiz = T,border=NA,col=bg_panel3,add=TRUE,xaxt='n')
  barplot(rep(c(5.4,0),floor(imax_panel3/2)),width=1,space=0,horiz = T,border=NA,col=bg_panel3,add=TRUE,xaxt='n')
  
  axis(1,tck=1,at=c(xmin_panel3,seq(-3.5,xmax_panel3,0.5)),col.ticks='grey')
  axis(1,tck=0.025,at=seq(xmin_panel3,xmax_panel3,0.1),lab=NA,col.ticks='grey')
  lines(c(1.5,1.5),c(1.1,1.9),lwd=2,col=col_bg_bars)
  lines(c(2.0,2.0),c(1.1,1.9),lwd=2,col=col_bg_bars)
  lines(c(2.5,2.5),c(1.1,1.9),lwd=2,col=col_bg_bars)
  lines(c(3,3),c(1.1,1.9),lwd=2,col=col_bg_bars)
  lines(c(0,0),c(-0.1,4.0),lwd=1,col='black')
  
  #add title
  mtext(expression(paste('(c) Carbon-Cycle Climate Feedbacks')),3,1.5,padj = 1,adj=0,cex=0.8)
  
  barplot(panel3_posfb_PF,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel3-1)),width=wd,
          border='black',col=col_red_trans)  
  barplot(panel3_posfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel3-1)),width=wd,
          border='black',col=col_red)
  barplot(panel3_negfb,add=TRUE,xaxt='n',
          horiz = T,space=c(of,rep(ds/wd,imax_panel3-1)),width=wd,
          border='black',col=col_blue)
  
  arrows(panel3_data[c(1,3,4),2],mc[c(1,3,4)],panel3_data[c(1,3,4),3],mc[c(1,3,4)],angle=90,len=0.02,code=3,lwd=2)  
  arrows(panel3_data[2,2],mc[2]+0.1,panel3_data[2,3],mc[2]+0.1,angle=90,len=0.02,code=3,lwd=2)  
  arrows(panel3_data_PF[2,2],mc[2]-0.1,panel3_data_PF[2,3],mc[2]-0.1,angle=90,len=0.02,code=3,lwd=2,col='grey10')  
  
  legend(xy.coords(x=1.3,y=mc[2]+(mc[3]-mc[2])/2),
         leg=c('permafrost feedback'),
         pch=c(-1),
         density=c(NA),
         border=c('black'),
         fill=c(col_red_trans),
         bg='transparent',
         bty='o',box.col='transparent')
  
  text(4.5,4.5,'Mean [5-95% range]',adj=0.5,col='black')
  for (i in c(1,3,4)) {
    text(y=mc[i],x=4.5,paste(format(round(panel3_data[i,1]*100)/100),' [',format(round(panel3_data[i,2]*100)/100),' to ',format(round(panel3_data[i,3]*100)/100),']',sep=''))
  }
  text(y=mc[2,],x=4.5,paste(format(round(panel3_data_PF[2,1]*100)/100),' [',format(round(panel3_data_PF[2,2]*100)/100),' to ',format(round(panel3_data_PF[2,3]*100)/100),']',sep=''))
  
  dev.off()
  if(outputformat=='pdf')  embedFonts('foo.pdf','pdfwrite','./AR6_TS_Figure_17.pdf')
  