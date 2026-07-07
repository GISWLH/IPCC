#GF 06/01/2021
#script for Figure 2.29

setwd("c:/users/glf1u08/Desktop/RScript/OA IPCC")

#files needed
Plio.pH<-read.table (file="Plio.pH.txt", header=TRUE) #Pliocene 
Sos.GR<-read.table (file="Sos.GR.txt", header = TRUE) #Neogene
Anag20<-read.table (file="Anag2020.txt", header=TRUE) #Eocene
BATS<-read.table (file ="BATS.txt", header = TRUE) #Modern
HOTS<-read.table (file = "HOTS.txt", header = TRUE) #Modern
modern<-read.table (file="global_modernpH.txt", header=TRUE) #modern averages
Shao<-read.table (file="Shao.txt", header =TRUE) #deglacial & Holocene

#panel a
par (mfrow=c(1,1)) 
par(mar=c(5,5, 1, 4))
par (oma=c(1,1,1,1))

plot (Sos.GR$Age.myr, Sos.GR$pH50 , yaxt="n", xaxt="n", xlab="", ylab="", cex.axis = 0.8, col="blue", pch=1, las=1, type="n", xlim=c(65,0), ylim=c(7.4, 8.35), cex=0.6)
axis (1, at=(seq(0, 65, by=10)),padj=-1, cex.axis=0.8, tck=-0.025)
axis (2, at=(seq(7.5, 8.5, by=0.2)),hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
text (64, 7.45, "(a)")
title (xlab="Age (Myr bp)", line=1.4, cex.lab=1)
title (ylab="pH", line=2, cex.lab=1)

text (58, 7.43, "PETM", cex = 0.6)

polygon(c(Sos.GR$Age.myr,rev(Sos.GR$Age.myr)),c(Sos.GR$pH2.5, rev(Sos.GR$pH97.5)),col=rgb (53, 165, 197, max=255, alpha = 125), border="NA")
lines (Sos.GR$Age.myr, Sos.GR$pH50, col=rgb (53, 165, 197, max=255), lwd=1)

polygon(c(Anag20$Age,rev(Anag20$Age)),c(Anag20$pH-Anag20$sd2.do, rev(Anag20$pH+Anag20$sd2.up)),col=rgb (53, 165, 197, max=255, alpha = 125), border="NA")
lines (Anag20$Age, Anag20$pH, col=rgb (53, 165, 197, max=255))

points (0, 8.052, pch=16, col=rgb (170, 24 , 24, max=255), cex=1.5) #2018 global mean

points (c(53, 49), c(8.3, 8.3), lwd=1, pch =".", cex=2) #EECO
points (c(16.9, 14.7), c(8.3, 8.3), lwd=1, pch =".", cex=2) #MCO
points (c(3.3, 3.0), c(8.3, 8.3), lwd=1, pch =".", cex=2) #panel b

#panel b
par (mfrow=c(1,1)) 
par(mar=c(5,12.8, 1, 4))
par (oma=c(1,1,1,1))

plot (Plio.pH$Age.myr, Plio.pH$pH50, type="n", yaxt="n", xaxt="n", cex=0.6, col="blue", ylim=c(7.9, 8.35), xlim=c(3.5, 0), xlab="", ylab="")
axis (1, at=(seq(0, 3.5, by=0.5)),padj=-1, cex.axis=0.8, tck=-0.025)
axis (2, at=(seq(7.9, 8.3, by=0.1)),hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
text (3.4, 7.925, "(b)")
title (xlab="Age (Myr bp)", line=1.4, cex.lab=1)
title (ylab="pH", line=2, cex.lab=1)

points (0, 8.05, pch=16, col=rgb (170, 24 , 24, max=255), cex=1.5) #2018 global mean

polygon(c(Plio.pH$Age.myr,rev(Plio.pH$Age.myr)),c(Plio.pH$pH2.5, rev(Plio.pH$pH97.5)),col=rgb (53,165,197, max=255, alpha = 125), border=NA)
lines (Plio.pH$Age.myr, Plio.pH$pH50, col=rgb (53,165,197, max=255))

points (c(3.3, 3.0), c(8.3, 8.3), lwd=1, pch =".", cex=2) #MPWP
points (c(0.129, 0.116), c(7.9, 7.9), lwd=1, pch =".", cex=2) #panel c

#Panel c
par (mfrow=c(1,1))
par(mar=c(5,18.5, 1, 4))
par (oma=c(1,1,1,1))

plot (Plio.pH$Age.myr, Plio.pH$pH50, type="n", yaxt="n", xaxt="n", cex=0.6, col="blue", ylim=c(7.9, 8.35), xlim=c(26, 0), xlab="", ylab="")
axis (1, at=(seq(0, 26, by=2)),padj=-1, cex.axis=0.8, tck=-0.025)
axis (4, at=(seq(7.9, 8.3, by=0.1)),hadj=0, cex.axis=0.8, tck=-0.025, las=1)
text (2, 7.925, "(c)")
title (ylab="pH", line=2, cex.lab=1)

points (0, 8.05, pch=16, col=rgb (170, 24 , 24, max=255), cex=1.5) #2018 global mean

polygon(c(Shao$Age,rev(Shao$Age)),c(Shao$pH+Shao$pH.er.2se, rev(Shao$pH-Shao$pH.er.2se)),col=rgb (53, 165, 197, max=255, alpha = 125), border=NA)
lines (Shao$Age, Shao$pH, col=rgb (53, 165, 197, max=255))

points (c(6.5, 5.5), c(8.3, 8.3), lwd=1, pch =".", cex=2) #MH
points (c(26.5, 19.5), c(7.9, 7.9), lwd=1, pch =".", cex=2) #LGM
points (c(18, 11), c(7.9, 7.9), lwd=1, pch =".", cex=2) #LDT

#panel d
par (mfrow=c(1,1)) 
par(mar=c(5,5, 1, 4))
par (oma=c(1,1,1,1))

plot (BATS$year, BATS$pH, col=rgb (8, 46, 114, max=255), ylim=c(8.025, 8.15), type="n", xlab="", ylab="", xaxt="n", yaxt="n", xlim=c(1980,2020))
axis (1, at=(seq(1900, 2020, by=5)),padj=-1, cex.axis=0.8, tck=-0.025)
axis (2, at=(seq(8.0, 8.15, by=0.025)),hadj=0.8, cex.axis=0.8, tck=-0.025, las=1)
text (2019, 8.03, "(d)")
title (xlab="Date AD", line=1.4, cex.lab=1)
title (ylab="pH", line=2, cex.lab=1)

lines (BATS$year, BATS$pH, col=rgb (8, 46, 114, max=255))#dark_cat #5
lines (HOTS$year, HOTS$pH, col=rgb (236, 156, 46, max=255))#dark_cat #6

polygon(c(modern$date,rev(modern$date)),c(modern$CMEMS.pH+(2*modern$CMEMS.pHer.1s), rev(modern$CMEMS.pH-(2*modern$CMEMS.pHer.1s))),col=rgb (221, 84, 46, max=255, alpha = 125), border=NA)#dark_cat #1
lines (modern$date, modern$CMEMS.pH, col=rgb (221, 84, 46, max=255), lwd=1)

polygon(c(modern$date,rev(modern$date)),c(modern$Ocean_Soda.pH+(2*modern$Ocean_Soda.pHer.1s), rev(modern$Ocean_Soda.pH-(2*modern$Ocean_Soda.pHer.1s))),col=rgb (128, 54, 168, max=255, alpha = 125), border=NA)#dark_cat #1
lines (modern$date, modern$Ocean_Soda.pH, col=rgb (128, 54, 168, max=255), lwd=1)

text (1985, 8.125, "BATS", col=rgb (8, 46, 114, max=255))
text (2000, 8.075, "HOT", col=rgb (236, 156, 46, max=255))
text (2010, 8.1, "Global_CMEMS", col="#E00000")
text (2010, 8.05, "Global_OceanSoda", col=rgb (128, 54, 168, max=255))
text (2018, 8.01, "(d)", col="black")

