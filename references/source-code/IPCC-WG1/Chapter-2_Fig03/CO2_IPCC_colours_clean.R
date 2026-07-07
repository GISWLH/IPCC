#GF 11/11/2020
#Code for Figure 2.3

setwd("")

#Data input
#gas
ice<-read.table (file="ice_core.txt", header=TRUE)

#boron
sos<-read.table (file="Sosdian.txt", header=TRUE) #from Sosdian et al. 2018 
Eleni<-read.table (file ="Anagnostou.txt", header = TRUE)# from Anagnostou et al. 2020
PP<-read.table (file="Plio_Pleisto_Final.txt", header=TRUE) #compiled from De la Vega et al., 2020, Bartoli et al., 2011; Chalk et al. 2017; Hoenisch et al. 2009; Dyez et al., 2018; Raitzsch et al. 2018 

#d13C
Stoll<-read.table (file="Stoll.txt", header=TRUE)
wit<-read.table (file="wit.txt", header=TRUE)
AlkComp<-read.table (file="Alkenone compilation.txt", header=TRUE)

#other
Phan<-read.table (file="PhanCO2F.txt", header=TRUE) # no PSol <200 ppm; taken from Royer compilation June 2015.  if no age error = 4% if land, = 0.001 if marine.  
PhanCO2sm<-read.table (file="PhanCO2sm.exp.txt", header=TRUE)

#geological 4
agePhan<-Phan$Age
CO2Phan<-Phan$CO2
CO2Phan.er<-Phan$er
agePhan.er<-Phan$Age.er/2
method<-Phan$method

par (mfrow=c(1,1)) #desktop plotting
par(mar=c(3,4, 0.1, 1.2))
par (oma=c(8,1,0.1,2))


#panel (c)
plot (ice$age, ice$CO2, col="black", xlim=c(3500, 0), xaxt="n", cex.axis=0.8, yaxt="n", ylim=c(150, 500), type="l", las=1, xlab ="Age (kyr bp)", ylab="", lwd=1)
axis (1, at=(seq(0, 3500, by=250)),padj=-1, cex.axis=0.8, tck=-0.025)
axis (2, at=(seq(150, 500, by=100)),hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
lines (c(0,0), c(280, 410))
text (3500, 180, "(c)")
title (xlab="Age (kyr bp)", line=1.5, cex.lab=0.8)
title (ylab="CO2 (ppm)", line=2.5, cex.lab=0.8)

text (700, 300, "Ant.Ice Core", col="black", cex=0.8)
text (1500, 400, "d11B-foraminifera", col=rgb (84,146,205, max=255), cex=0.8)
text (2500, 160, "d13C-alkenones", col=rgb (128,128,128, max=255), cex=0.8)

arrows (Stoll$Age*1e3,Stoll$Co2.d, Stoll$Age*1e3,Stoll$Co2.up, code=3, angle=90, length=0.015,lwd=0.8, col=rgb (191, 191, 191, max=255))
points (Stoll$Age*1e3, Stoll$CO2, pch=21, col=rgb (128, 128, 128, max=255), bg=rgb (191, 191, 191, max=255), cex=0.6)


arrows (PP$Age[PP$Study=="Hoenisch2009"],PP$CO2do[PP$Study=="Hoenisch2009"], PP$Age[PP$Study=="Hoenisch2009"],PP$CO2up[PP$Study=="Hoenisch2009"], code=3, angle=90, length=0.015,lwd=0.8, col=rgb (84,146,205, max=255, alpha=100))
points (PP$Age[PP$Study=="Hoenisch2009"], PP$CO2[PP$Study=="Hoenisch2009"], col=rgb (84,146,205, max=255, alpha=100), pch=16, cex=0.6)

arrows (PP$Age[PP$Study=="Raitzsch2018"],PP$CO2do[PP$Study=="Raitzsch2018"], PP$Age[PP$Study=="Raitzsch2018"],PP$CO2up[PP$Study=="Raitzsch2018"], code=3, angle=90, length=0.015,lwd=0.8, col=rgb (84,146,205, max=255, alpha=100))
points (PP$Age[PP$Study=="Raitzsch2018"], PP$CO2[PP$Study=="Raitzsch2018"], col=rgb (84,146,205, max=255, alpha=100), pch=15, cex=0.6)

arrows (PP$Age[PP$Study=="Bartoli2011"],PP$CO2do[PP$Study=="Bartoli2011"], PP$Age[PP$Study=="Bartoli2011"],PP$CO2up[PP$Study=="Bartoli2011"], code=3, angle=90, length=0.015,lwd=0.8, col=rgb (84,146,205, max=255, alpha=100))
points (PP$Age[PP$Study=="Bartoli2011"], PP$CO2[PP$Study=="Bartoli2011"], col=rgb (84,146,205, max=255, alpha=100), pch=15, cex=0.6)

polygon(c(PP$Age[PP$Study=="Dyez2018"],rev(PP$Age[PP$Study=="Dyez2018"])),c(PP$CO2do[PP$Study=="Dyez2018"], rev(PP$CO2up[PP$Study=="Dyez2018"])),col=rgb (84,146,205, max=255, alpha = 125), border=NA)
lines (PP$Age[PP$Study=="Dyez2018"], PP$CO2[PP$Study=="Dyez2018"], col=rgb (84,146,205, max=255))

polygon(c(PP$Age[PP$Study=="Chalk2017.LP"],rev(PP$Age[PP$Study=="Chalk2017.LP"])),c(PP$CO2do[PP$Study=="Chalk2017.LP"], rev(PP$CO2up[PP$Study=="Chalk2017.LP"])),col=rgb (84,146,205, max=255, alpha = 125), border=NA)
lines (PP$Age[PP$Study=="Chalk2017.LP"], PP$CO2[PP$Study=="Chalk2017.LP"], col=rgb (84,146,205, max=255))

polygon(c(PP$Age[PP$Study=="Chalk2017.MPT"],rev(PP$Age[PP$Study=="Chalk2017.MPT"])),c(PP$CO2do[PP$Study=="Chalk2017.MPT"], rev(PP$CO2up[PP$Study=="Chalk2017.MPT"])),col=rgb (84,146,205, max=255, alpha = 125), border=NA)
lines (PP$Age[PP$Study=="Chalk2017.MPT"], PP$CO2[PP$Study=="Chalk2017.MPT"], col=rgb (84,146,205, max=255))

polygon(c(PP$Age[PP$Study=="DelaVega2020"],rev(PP$Age[PP$Study=="DelaVega2020"])),c(PP$CO2do[PP$Study=="DelaVega2020"], rev(PP$CO2up[PP$Study=="DelaVega2020"])),col=rgb (84,146,205, max=255, alpha = 125), border=NA)
lines (PP$Age[PP$Study=="DelaVega2020"], PP$CO2[PP$Study=="DelaVega2020"], col=rgb (84,146,205, max=255))

lines (ice$age, ice$CO2, col="black")
lines (c(3300, 3000), c(500, 500)) #MPWP
lines (c(1200, 800), c(500,500)) #MPT

#####
####panel  (b) 
####

plot (ice$age, ice$CO2, col="red", xlim=c(58, 0), ylim=c(150, 2500), yaxt="n", cex.axis=0.8, xaxt="n", type="n", las=1, xlab ="Age (Myr bp)", ylab="", lwd=1)
axis (1, at=(seq(0, 58, by=5)),padj=-1, cex.axis=0.8,  tck=-0.025)
axis (2, at=(seq(0, 3000, by=500)), labels = FALSE, hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
axis (2, at=(seq(0, 3000, by=500)), labels = TRUE, hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
text (58, 250, "(b)")

title (xlab="Age (Myr)", line=1.5, cex.lab=0.8)
title (ylab="CO2 (ppm)", line=2.5, cex.lab=0.8)


arrows (wit$Ma,wit$pCO2_L1., wit$Ma, wit$pCO2_U1., code=3, angle=90, length=0.015,lwd=0.8, col=rgb (223,194,125, max=255, alpha=100))
arrows (wit$Ma_L,wit$pCO2, wit$Ma_U, wit$pCO2, code=3, angle=90, length=0.015,lwd=0.8, col=rgb (223,194,125, max=255, alpha=100))
polygon(c(sos$Age,rev(sos$Age)),c(sos$CO2.2.5*1e6, rev(sos$CO2.97.5*1e6)),col=rgb (84, 146, 205, max=255, alpha=125), border=NA)
polygon(c(Eleni$age,rev(Eleni$age)),c(Eleni$CO2+Eleni$CO2up, rev(Eleni$CO2-Eleni$CO2do)),col=rgb (84, 146, 205, max=255, alpha=125), border=NA)

points (wit$Ma, wit$pCO2, pch=16, col=rgb (196, 121, 0, max=255, alpha=200), cex=0.5)

points (sos$Age, sos$CO2.50*1e6, pch=16, col=rgb (84,146,205, max=255, alpha=200), cex=0.5)
lines (sos$Age, sos$CO2.50*1e6, col=rgb (84,146,205, max=255, alpha=200))

lines (Eleni$age, Eleni$CO2, col=rgb (84,146,205, max=255))
points (Eleni$age, Eleni$CO2, col=rgb (84,146,205, max=255, alpha=200), pch=16, cex=0.6)

arrows (AlkComp$Age,AlkComp$pCO2_min, AlkComp$Age, AlkComp$pCO2_max, code=3, angle=90, length=0.015,lwd=0.8, col=rgb (191, 191, 191, max=255))
points (AlkComp$Age, AlkComp$pCO2, pch=21, col=rgb (128, 128, 128, max=255), bg=rgb (191, 191, 191, max=255), cex=0.6)

text (40, 400, "d13C-alkenone", col=rgb (128,128,128, max=255), cex=0.8)
text (30, 2000, "d11B-foraminifera", col=rgb (84,146,205, max=255), cex=0.8)
text (20, 1000, "d13C-phytane", col=rgb (196, 121, 0, max=255), cex=0.8)

lines (c(53, 49), c(2500, 2500), lwd=1) #EECO
lines (c(16.9, 14.7), c(2500, 2500)) #MCO
lines (c(3.3, 3.0), c(2500, 2500)) #MPWP
points (55.8, 2500, pch=".") #PETM

#####
#####Panel (a) 
#####

plot (ice$age, ice$CO2, col="red", xlim=c(450, 0), ylim=c(0, 3000), yaxt="n", type="n", las=1, xlab ="Age (Myr bp)", ylab="", lwd=1, cex.axis=0.8, xaxt="n")
axis (1, at=(seq(0, 450, by=50)),padj=-1, tck=-0.025, cex.axis=0.8)
axis (2, at=(c(0, 1000,2000,3000,4000)), labels = FALSE, hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
axis (2, at=(c(0, 1000,2000,3000,4000)), labels = TRUE, hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
text (450, 2800, "(a)")

points (AlkComp$Age, AlkComp$pCO2, pch=21, col=rgb (128, 128, 128, max=255), bg=rgb (191, 191, 191, max=255), cex=0.6)

points (sos$Age, sos$CO2.50*1e6, pch=1, col=rgb (84,146,205, max=255, alpha=200), cex=0.6)

points (Eleni$age, Eleni$CO2, col=rgb (84,146,205, max=255, alpha=200), pch=1, cex=0.6)

points (agePhan[method=="Stomata"], CO2Phan[method=="Stomata"], col=rgb(178, 178, 178, max=255, alpha=200), pch=15,cex=0.6)
points (agePhan[method=="psols"], CO2Phan[method=="psols"], col=rgb(0, 52, 102, max=255, alpha=60), pch=4,cex=0.6)
points (wit$Ma, wit$pCO2, pch=1, col=rgb(196, 121, 0, max=255), cex=0.6)

polygon(c(PhanCO2sm$age,rev(PhanCO2sm$age)),c(PhanCO2sm$lw68, rev(PhanCO2sm$up68)),col=rgb(223, 237, 195, max=255, alpha=200), border=NA)
polygon(c(PhanCO2sm$age,rev(PhanCO2sm$age)),c(PhanCO2sm$lw95, rev(PhanCO2sm$up95)),col=rgb(223, 237, 195, max=255, alpha=100), border=NA)
lines (PhanCO2sm$age, PhanCO2sm$pmaxCO2, col=rgb(0,79,0, max=255), lwd=2)

text (300, 2500, "d13C-paleosols", col=rgb(0, 52, 102, max=255), cex=0.8)
text (130, 350, "stomata", col=rgb(178, 178, 178, max=255), cex=0.8)

title (xlab="Age (Myr)", line=1.5, cex.lab=0.8)
title (ylab="CO2 (ppm)", line=2.5, cex.lab=0.8)

