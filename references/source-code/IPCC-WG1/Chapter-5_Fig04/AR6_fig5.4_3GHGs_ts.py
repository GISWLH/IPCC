# coding: shift-JIS
#
# Purpose:
#   Plot timeseries of CO2, CH4, N2O cocentrations and their growth rates. Requires "Process_data.py"
#   Calculate the total as well as increasing and decreasing grt. This Fig 5.4 of Chapter 5 of AR6
# Prepared by: Naveen Chandra (naveennegi@jamstec.go.jp) and Prabir Patra (prabir@jamstec.go.jp)
###########################################

import os, sys, glob
import numpy as np
from math import *
from pylab import *
from scipy import stats
from matplotlib import lines
from matplotlib.ticker import AutoMinorLocator

#from scipy import optimize
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import Process_data
import ccgfilt_mod

p1  = './data/co2_sio/scripps_stn_data/' # co2 direct measuremets
p2  = './data/ch4_all/' # ch4 direct measuremets
p3  = './data/n2o_all/out_p01/' # ch4 direct measuremets

# lawDomeIce core (AD)
p4  = './data/lawDomeIceCore_data/co2_data.txt'
p5  = './data/lawDomeIceCore_data/ch4_data.txt'
p6  = './data/lawDomeIceCore_data/n2o_data.txt'

#EPA Dome data (800 kyr$^{-1}$ BC): VOSTOCK
p7  = './data/lawDomeIceCore_data/Ch2_ice_core.txt' # Updated icecore data
p8  = './data/lawDomeIceCore_data/edc_ch4_2008.txt'
p9  = './data/lawDomeIceCore_data/edc_n2o_2008.txt'

p10 = './data/'

###################################################
#************** Defined variables *****************
####################################################

syr = 1970
eyr = 2020
dum_yr  = np.arange(syr, eyr, 1)#; CO2 yarly mean

# Stations for plotting direct observations
stn = np.array(['ALT','MLO','SPO'])

# Fitting the data
CO2stn = Process_data.StnCO2read(p1, dum_yr, stn)
CH4stn = Process_data.StnCH4read(p2, dum_yr, stn)
N2Ostn = Process_data.StnN2Oread(p3, dum_yr, stn)

# Store all the data in an array
ff = []
ff.append([CO2stn,CH4stn, N2Ostn])
stn_dat = np.array(ff)

# Read data
ice_dat   = Process_data.IceDatRead(p4, p5, p6)
vos_dat   = Process_data.VosDatRead(p7, p8, p9)
wdc_dat   = Process_data.WdcDatRead(p10)

LLGHG_dat = Process_data.LLGHGDatRead(p10)
#print(LLGHG_dat)

# Paleo growth rate
co2_grt = np.zeros(3); ch4_grt = np.zeros(3); n2o_grt = np.zeros(3)
co2_std = np.zeros(3); ch4_std = np.zeros(3); n2o_std = np.zeros(3)

co2_grt[0] = 0.01 # Avg growth rate
co2_grt[1] = 2.87 # Avg rise rate
co2_grt[2] = 1.96 # Avg fall rate

co2_std[0] = 0.0 # Avg growth rate
co2_std[1] = 1.49 # Avg rise rate
co2_std[2] = 1.53 # Avg fall rate

ch4_grt[0] = 0.01 # Avg growth rate
ch4_grt[1] = 13.9 # Avg rise rate
ch4_grt[2] = 7.7 # Avg fall rate

ch4_std[0] = 0.0 # Avg growth rate
ch4_std[1] = 10.3 # Avg rise rate
ch4_std[2] = 5.8 # Avg fall rate

n2o_grt[0] = 0.02 # Avg growth rate
n2o_grt[1] = 1.13 # Avg rise rate
n2o_grt[2] = 1.15 # Avg fall rate

n2o_std[0] = 0.0 # Avg growth rate
n2o_std[1] = 0.90 # Avg rise rate
n2o_std[2] = 0.96 # Avg fall rate

grt = np.zeros(3); std = np.zeros(3)
#grt[0] = 0.96 # CO2 -ppm/yr
#grt[1] = 7.8 # CH4 - ppb/yr
#grt[2] = 0.45 # N2O - ppb/yr
#std[0] = 0.79
#std[0] = 5.26
#std[0] = 0.29

def IplotProp(ax,j, iylab, ixlim, iylim_l, iylim_h, bbox_to_anchor):
     ''' Define properties for inset plot'''
     axx = inset_axes(ax, borderpad=1, width="80%", height="110%", loc=2, bbox_to_anchor=bbox_to_anchor, bbox_transform=ax.transAxes)
     axx.patch.set_facecolor('white')
     axx.patch.set_alpha(0.0)
     axx.tick_params(axis='both', pad=1, length=1.2, width=0.5, colors='k', labelsize=3.9)
     axx.spines['right'].set_visible(False)
     axx.spines['top'].set_visible(False)
     plt.setp(axx.spines.values(), linewidth=0.5)
     plt.xlim(ixlim[0], ixlim[1])
     plt.ylabel(iylab[j], fontsize=3.5, labelpad=1)
     plt.ylim(iylim_l[j], iylim_h[j])
     plt.setp(axx.get_yticklabels(),  visible = True)
     plt.setp(axx.get_xticklabels(),  visible = False)
     return axx

#************************************************************************
             # Plotting will start from here
print('plotting starts')
#************************************************************************

plt.close()
plt.clf()
print('plotting starts')

col1 = ['forestgreen','darkorange','c','lightpink','mediumvioletred','forestgreen'] # direct obs
col = ['Silver','palevioletred','darkslateblue','limegreen','mediumvioletred','forestgreen']

ylab = ['(ppm)', '(ppb)','(ppb)']
xlab = ['Year, BCE', 'Year, CE','Year, CE']
tit  = ['(a) Atmospheric CO$_2$ concentration', '(b) Atmospheric CH$_4$ concentration', '(c) Atmospheric N$_2$O concentration']
iylab   = ['(ppm kyr$^{-1}$)', '(ppb kyr$^{-1}$)', '(ppb kyr$^{-1}$)'] # Y-label for bar plots
iylab1   = ['(ppm yr$^{-1}$)', '(ppb yr$^{-1}$)', '(ppb yr$^{-1}$)'] # Y-label for bar plots
iylim_h = [1.0, 14, 1]  #1900-2018 Bar's y-axis range, used below 400 lines
iylim_l = [0, 0, 0]
iylim1_h = [1, 11, 1]
iylim1_l = [0, 0, 0]
sym   = ['^', '^', '^', '^']
msize = [0.5, 0.5, 0.5]
mwdth = [0.3, 0.3, 0.3]
barwidth = 0.28 # set width of bar
#xbar = [2012, 2012.5, 2013]
xbar = [2013, 2012, 2012.5]
print('definitions made')

for k in range(3):
 for j in range(3):
   if k<1:
     ax1 = subplot2grid((3,4), (j,k), colspan=2) # Set starting index to the top left cell
     ax1.spines['right'].set_visible(False)
   else:
     ax1 = subplot2grid((3,4), (j,k+1))
     ax1.spines['left'].set_visible(False)

   ################################################################
   #**************** Set plot properties ************************
   #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   ax1.tick_params(axis='both', pad=1, length=1, width=0.4, colors='k', labelsize=4.5)
   plt.setp(ax1.spines.values(), linewidth=0.5)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)

   # Change the x axis line colour
   if k ==1:
     ax1.spines['bottom'].set_color('firebrick')
     ax1.tick_params(axis='x', colors='firebrick')
     ax1.xaxis.label.set_color('firebrick')
     ax1.title.set_color('firebrick')

   if k >1:
     ax1.spines['bottom'].set_color('navy')
     ax1.tick_params(axis='x', colors='navy')
     ax1.xaxis.label.set_color('navy')

   if k ==0:
     ax1.spines['bottom'].set_color('k')
     ax1.tick_params(axis='x', colors='k')
     ax1.xaxis.label.set_color('k')

   #+++++++++++++++++++++++++++++++++++++++++++++++
   #********** Data source name and arrow *********
   #+++++++++++++++++++++++++++++++++++++++++++++++
   if j==0 and k ==0:
      plt.text(950, 445, tit[j], fontsize =5, color = 'k', fontweight ='normal')
      ax1.text(400, 512, 'EPICA Dome C',
               style='normal', size =4,
               ha="center", va="center")

      ax1.annotate("",
            xy=(800, 490), xycoords='data',
            xytext=(0, 490), textcoords='data',
            arrowprops=dict(arrowstyle='<->, head_length=0.2, head_width=0.1', linewidth=0.4,
                            connectionstyle="arc3"), annotation_clip=False)

   if j==0 and k ==1:
      ax1.text(1250, 512, 'Law Dome Ice Core',
               style='normal', size =4,
               ha="center", va="center")

      ax1.annotate("",
            xy=(-150, 490), xycoords='data',
            xytext=(2750, 490), textcoords='data',
            arrowprops=dict(arrowstyle='<->, head_length=0.2, head_width=0.1', linewidth=0.4,
                            connectionstyle="arc3"), annotation_clip=False)

   if j==0 and k ==2:
      ax1.text(1988, 512, 'Ambient Air',
               style='normal', size =4,
               ha="center", va="center")
      ax1.annotate("",
            xy=(1945, 490), xycoords='data',
            xytext=(2030, 490), textcoords='data',
            arrowprops=dict(arrowstyle='<->, head_length=0.2, head_width=0.1', linewidth=0.4,
                            connectionstyle="arc3"), annotation_clip=False)

   if j==1 and k ==0:
      plt.text(950, 2080, tit[j], fontsize =5, fontweight ='normal', color = 'k')

   if j==2 and k ==0:
      plt.text(950, 362, tit[j], fontsize =5, fontweight ='normal', color = 'k')

   # +++++++++++++++++++++++++++++++++++++++++++++++++++ 
   # ********* x, y tick labels and limits ***********
   # +++++++++++++++++++++++++++++++++++++++++++++++++++

   if j == 0 :#CO2
     plt.ylim(150, 420)
     ax1.set_yticks(np.arange(200, 421, 100))

   if j == 1 :#CH4
     plt.ylim(300, 1950)
     ax1.set_yticks(np.arange(300, 1951, 500))

   if j == 2 :#N2O
     plt.ylim(200, 350)
     ax1.set_yticks(np.arange(200, 351, 50))

   if k == 0:
     plt.xlim(800, 0)
     ax1.set_xticks(np.arange(800,  1, -200 ))
     ax1.set_xticklabels(('800k', '600k', '400k', '200k'))

   if k == 1:
     plt.xlim(0, 1900)
     ax1.set_xticks(np.arange(0, 1901, 1000 ))

   if k> 1:
     plt.xlim(1900, 2020)
     ax1.set_xticks(np.arange(1900, 2021, 40 ))

   if (j>= 0 and k == 0): # y-lab
      plt.ylabel(ylab[j], fontsize=4.5, labelpad=3)

   if (j== 2 and k>= 0): # x-lab
      plt.xlabel(xlab[k], fontsize=4.5, labelpad=3)

   if (k ==0): # y-tick labels
      plt.setp(ax1.get_yticklabels(), visible =True)

   else:
      plt.setp(ax1.get_yticklabels(), visible =False)

   #if j == 2: # x-tick labels

   if j>= 0: # x-tick labels
      plt.setp(ax1.get_xticklabels(), visible =True)
   else:
      plt.setp(ax1.get_xticklabels(), visible =False)

   if k>0:
    plt.setp(ax1.yaxis.get_ticklines(), 'markersize', 0.0)
    plt.setp(ax1.yaxis.get_ticklines(), 'markeredgewidth', 0.0)

   #********************************************
   #++++++ Plotting will start from here +++++++
   #++++++++++++++++++++++++++++++++++++++++++++

   if k == 0: # Vostock: -800 - 0 kY [BC]
     vos = vos_dat[0][j]
     ax1.plot(vos[:,0], vos[:,1], linestyle='-',linewidth=0, marker =sym[j], markersize=msize[j], markeredgewidth=mwdth[j], color = 'k', alpha=1.0)

   if k == 1: # # 0 - 2000 yr$^{-1}$
     ice = ice_dat[0][j]
     id1 = np.where(ice[:,0]<1750)
     ax1.plot(ice[id1,0], ice[id1,1], linestyle='-',linewidth=0, marker =sym[j], markersize=msize[j], markeredgewidth=mwdth[j], color = 'k', alpha=1.0)
     ax1.plot(LLGHG_dat[:,0], LLGHG_dat[:,j+1], linewidth=0, marker = sym[j], markersize=msize[j], markeredgewidth=mwdth[j], color = 'k', alpha=1.0)

   if k == 2: # ice core and station
     #++++++++++++++++++++++++
     ice = ice_dat[0][j]
     id1 = np.where(ice[:,0]<1750)
     ax1.plot(ice[id1,0], ice[id1,1], linestyle='-',linewidth=0, marker =sym[j], markersize=msize[j], markeredgewidth=mwdth[j], color = 'k', alpha=1.0)
     ax1.plot(LLGHG_dat[:,0], LLGHG_dat[:,j+1], linewidth=0, marker = sym[j], markersize=msize[j], markeredgewidth=mwdth[j], color = 'k', alpha=1.0)

     ixlim = [2011.5, 2013.5]
     ax2 = IplotProp(ax1,j, iylab, ixlim,  iylim_l, iylim_h, bbox_to_anchor=(1.16,0.3,1.0,0.9))

     #********************************************************
     #***********Inset bar graph for growth rate 800k-0 ++++++++++++

     for m in range(3): # Bars for growth rate

        if j ==0: # CO2
          ax2.bar(xbar[m], co2_grt[m], yerr = co2_std[m], align='center',  width=barwidth, alpha=1.0, ecolor='black', color = col[0], error_kw=dict(lw=0.4, capsize=1, capthick=0.5))
          plt.ylim([0, 4.5])
          ax2.set_yticks([0, 4, 2])

          if m==0:
            plt.text(2012.6, -1.6, 'Mean rate', fontsize=3, rotation=60)
            plt.text(2011.57, -1.4, 'Rise rate', fontsize=3, rotation=60)
            plt.text(2012.1, -1.4, 'Fall rate', fontsize=3, rotation=60)
            plt.text(2014.1, -1.5, 'Mean rate', fontsize=3, rotation=60)

        if j ==1: # CH4
          ax2.bar(xbar[m], ch4_grt[m], yerr = ch4_std[m], align='center',  width=barwidth, alpha=1.0, ecolor='black', color = col[0], error_kw=dict(lw=0.3, capsize=1, capthick=0.5))
          plt.ylim([0, 25])
          ax2.set_yticks([0, 24, 12])

          if m==0:
            plt.text(2012.6, -8.7, 'Mean rate', fontsize=3, rotation=60)
            plt.text(2011.57, -7.9, 'Rise rate', fontsize=3, rotation=60)
            plt.text(2012.1, -7.8, 'Fall rate', fontsize=3, rotation=60)
            plt.text(2014.1, -8.3, 'Mean rate', fontsize=3, rotation=60)

        if j ==2: # N2O
          ax2.bar(xbar[m], n2o_grt[m], yerr = n2o_std[m], align='center',  width=barwidth, alpha=1.0, ecolor='black', color = col[0], error_kw=dict(lw=0.4, capsize=1, capthick=0.5))
          plt.ylim([0, 2.2])
          ax2.set_yticks([0, 2.0, 1])

          if m ==0:
            plt.text(2012.6, -0.8, 'Mean rate', fontsize=3, rotation=60)
            plt.text(2011.57, -0.7, 'Rise rate', fontsize=3, rotation=60)
            plt.text(2012.1, -0.65, 'Fall rate', fontsize=3, rotation=60)
            plt.text(2014.1, -0.8, 'Mean rate', fontsize=3, rotation=60)

     #++++++++++++++++++++++++
     #********************************************************
     #***********Inset bar graph for growth rate 2011-2012 ++++++++++++

     ixlim = [2011, 2012]
     ax3 = IplotProp(ax1,j, iylab1, ixlim, iylim_l, iylim_h, bbox_to_anchor=(2.22,0.3,0.4,0.9))

     # Growth rate for recent period
     id1 = np.where(LLGHG_dat[:,0]>1899)[0]
     xp, yp, grt1, std1 = [], [], [], []
     xp  = LLGHG_dat[id1,0]
     yp = LLGHG_dat[id1,j+1]
     filt = ccgfilt_mod.ccgFilter(xp,yp)
     fit_trend = filt.getGrowthRateValue(xp)

     # Average and std for 1990-2019
     grt1 = np.nanmean(fit_trend)
     std1 = np.nanstd(fit_trend)
     print(grt1,std1)

     plt.xlim(2011, 2012)
     ax3.bar(2011.5, grt1, yerr = std1, align='center',  width=barwidth, alpha=0.5, ecolor='black', color = 'darkslateblue', error_kw=dict(lw=0.3, capsize=1, capthick=0.5))

     #ax3.bar(2011.5, grt[j],  width=0.25, alpha=1.0,  color = col[1])

     if j ==0:
       plt.ylim(0, 2)
       ax3.set_yticks([0, 2, 1])
       plt.setp(ax3.get_yticklabels(), visible =True)
       plt.text(2011.0, 2.2, '1900-2019', fontsize=3.5, rotation=0)
       plt.text(2009.5, 2.6, 'Growth Rates', fontsize=4, fontweight='normal', rotation=0)
       plt.text(2008.5, 2.2, '800k-0k', fontsize=3.5, rotation=0)

     if j ==1:
       ax3.set_yticks([0, 12, 6])
       plt.setp(ax3.get_yticklabels(), visible =True)

     if j ==2:
        ax3.set_yticks([0, 1, 1])
        plt.setp(ax3.get_yticklabels(), visible =True)

subplots_adjust(left=None, bottom=0.25, right=0.52, top=0.75, wspace=0.08, hspace=0.4)

#left  = 0.125  # the left side of the subplots of the figure
#right = 0.9    # the right side of the subplots of the figure
#bottom = 0.1   # the bottom of the subplots of the figure
#top = 0.9      # the top of the subplots of the figure
#wspace = 0.2   # the amount of width reserved for blank space between subplots,
               # expressed as a fraction of the average axis width
#hspace = 0.2   # the amount of height reserved for white space between subplots,
               # expressed as a fraction of the average axis height

#------------------------------------------------------------------
# Save figure
#----------------------------------------------------------------

#plt.savefig('p04_3GHGs_ts.png', format='png',dpi=1200, bbox_inches='tight')
plt.savefig('p04_3GHGs_ts.pdf', format='pdf', bbox_inches='tight')
plt.close()

print('Done')    

