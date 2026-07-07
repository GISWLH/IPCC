'''
Script to read in REgional mean values and produce time series 
of future changes in PM2.5 concentrations in different CMIP6
Scenarios

Created on Jan 6, 2020

@author: sturnock
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.lines as mlines

DATA_DIR    = '/home/h06/sturnock/Python/UKESM_cmip6/AR6_reg_mean_txt_files/'
PLOT_DIR    = '/net/home/h06/sturnock/Python/UKESM_cmip6/Images_multi_mods/IPCC_figs/'
SCEN        = ['ssp126','ssp245','ssp370','ssp370-lowNTCF','ssp370-lowNTCFCH4','ssp585']
PLOT_LAB    = ['ssp126','ssp245','ssp370','ssp370-lowSLCF-highCH4','ssp370-lowSLCF-lowCH4','ssp585']

CP          = 'PM2pt5'
MICRO       = r'$\mathregular{\mu}$' # micro (mu) symbol
CP_LAB      = '$\mathregular{PM_{2.5}}$'
UNITS_LAB   = '('+MICRO+'g $\mathregular{m^{-3}}$)'

YEARS_ALL = [2017,2022,2027,2032,2037,2042,2047,2052,2057,2062,2067,2072,2077,2082,2087,2092,2097]

# Use AR6 Regional Definitions
AR6_REGS        = ['Africa','Asia-Pacific Developed','Eastern Asia','Europe','Eurasia','Latin America and Carribean','Middle East','North America','Southern Asia','South-East Asia and Developing Pacific']
AR6_REG_NUMS    = [3       ,7                       ,10            ,2       ,6        ,5                            ,8            ,9              ,1              ,4]
AR6_REG_COLS    = ['wheat' ,'purple'                ,'red'         ,'blue'  ,'darkorange','maroon'                  ,'cyan'       ,'gold'         ,'plum'         ,'lightgreen']

#########################################

#----------------------------------------------------------------------

def read_base_mod(fname):
    '''
    read in CMIP6 model 2005-14 baseline values
    '''
    reg_data_out = np.zeros((len(AR6_REGS)+1)) # annual multi-model mean values
    reg_data_sd  = np.zeros((len(AR6_REGS)+1)) # standard deviation of multi-model mean
    print(reg_data_out.shape)
    
    with open(fname) as fp:
        
        data_lines = fp.read().splitlines() # read all lines of file into list and strip /n from end of line and also white space
        #regional header line
        hd_line_sp = data_lines[0].split(',')
        reg_header = hd_line_sp[3:]
        print( reg_header)
        
        for (iln,line) in enumerate(data_lines[1:]): #for each line in file
            line_sp = line.split(',')
            if iln == 0: reg_data_out[:] = line_sp[3:] # first data line is multi-model mean values
            if iln == 1: reg_data_sd[:] = line_sp[3:]  # 2nd line is standard deviation values
    
    return reg_data_out, reg_data_sd, reg_header

#----------------------------------------------------------------------

def read_fut_mod(fname,scn_in,yrs_in):
    '''
    read in CMIP6 model 2005-14 baseline values
    '''
    reg_data_out = np.zeros((len(scn_in),len(yrs_in),len(AR6_REGS)+1)) # annual multi-model mean values
    print(reg_data_out.shape)
    
    with open(fname) as fp:
        data_lines = fp.read().splitlines() # read all lines of file into list and strip /n from end of line and also white space
        #regional header line
        hd_line_sp = data_lines[0].split(',')
        reg_header = hd_line_sp[2:]
        print( reg_header)
        
        for iscn,scn in enumerate(scn_in):
            print('Get data for {}'.format(scn))
            iyr = 0
            for (iln,line) in enumerate(data_lines[1:]): #for each line in file
                line_sp = line.split(',')
                #print(line_sp)
                cur_scn = line_sp[1]
                #print(cur_scn)
                #print(iyr)
                
                #if line.startswith(scn):
                if cur_scn == scn:
                    reg_data_out[iscn,iyr,:] = line_sp[2:]
                    #print (reg_data_out[iscn,iyr,:])
                    iyr += 1       
    
    return reg_data_out, reg_header
        
#----------------------------------------------------------------------

def plot_fut_timeseries_fig_no_loc(mod_surf,mod_sd,reg_names,mod_surf_abs,mod_surf_abs_sd):
    '''
    Produce time series figure of future changes in CMIP6 scenarios across different regions
    '''
    fig = plt.figure()
    plt.subplots_adjust(bottom=0.05,left=0.07,top=0.945,right=0.93,wspace=0.15,hspace=0.3)
    
    # Set up major and minor tick spacings
    xmajorLocator = MultipleLocator(20)
    xminorLocator = MultipleLocator(10)
    ymajorLocator = MultipleLocator(5)
    yminorLocator = MultipleLocator(1)
    
    # Use IPCC colour scheme and transparency values
    colors_scn_mod     = [(29.0/255.0,51.0/255.0,84.0/255.0),(234.0/255.0,221.0/255.0,61.0/255.0),(242.0/255.0,17.0/255.0,17.0/255.0),(242.0/255.0,17.0/255.0,17.0/255.0),(242.0/255.0,17.0/255.0,17.0/255.0),(132.0/255.0,11.0/255.0,34.0/255.0)]
    colors_scn_mod_fc  = colors_scn_mod
    alpha_fac          = [0.2,0.2,0.2,0.2,0.2,0.2]
    
    #['Africa','Asia-Pacific Developed','Eastern Asia','Europe','Eurasia','Latin America and Carribean','Middle East','North America',
    #'Southern Asia','South-East Asia and Developing Pacific']
    # Change order of Above to
    #plot_ind = [13,15,3,1,2,4,14,0,7,11,8]
    plot_ind = [5,11,3,1,2,4,6,0,7,10,9]
    
    yrs_all_str_lab = [' ','2020','2040','2060','2080','2100']
    
    print(len(reg_names))
    
    for ireg,reg in enumerate(reg_names):
        
        if (reg == 'North Pole') or (reg == 'South Pole'):# or (reg == 'Ocean'):
            # Do not plot these regions
            print('## DO NOT PLOT REGION {} ##'.format(reg))
        
        else:
            # set up plot for other regions
            print('plot {} region'.format(reg))
            
            cur_plot_ind = plot_ind[ireg]+1
            print(cur_plot_ind)
            ax = plt.subplot(3,4,cur_plot_ind)
            
            # Change axis width 
            for axis in ['top','bottom','left','right']:
                ax.spines[axis].set_linewidth(0.5)
            
            # Now plot up time series for each scenario within a region
            for iscn,scn in enumerate(SCEN):
                print('Plot up scenario {}'.format(scn))
                cur_data = mod_surf[iscn,:,ireg]
                y_err_dwn = cur_data-mod_sd[iscn,:,ireg]
                y_err_up  = cur_data+mod_sd[iscn,:,ireg]
                print(len(YEARS_ALL))
                print(cur_data.shape)
                
                ln_style='-'
                if scn == 'ssp370-lowNTCF': 
                    # Change linestyle for this scenario to dashed
                    ln_style = '--'
                    # set data with zeros to NaNs in ssp370-lowNTCF
                    zero_ind = np.where(cur_data == 0.0) # find out where data not available for lowNTCF scenario
                    #print(zero_ind)
                    cur_data[zero_ind[0]] = float(np.nan)
                    y_err_dwn[zero_ind[0]] = float(np.nan)
                    y_err_up[zero_ind[0]] = float(np.nan)
                    #print(cur_data)
                
                if scn == 'ssp370-lowNTCFCH4': ln_style = ':'
                # Plot up time series line using mean values and shading using standard deviation
                ax.plot(np.hstack((2014,YEARS_ALL)), np.hstack((0,cur_data)), color = colors_scn_mod[iscn], linewidth=0.8,linestyle=ln_style, zorder=3)
                ax.fill_between(np.hstack((2014,YEARS_ALL)),np.hstack((0,y_err_dwn)),np.hstack((0,y_err_up)),alpha=alpha_fac[iscn], facecolor=colors_scn_mod_fc[iscn],antialiased=True,zorder=2)
                
                # PLot up zero line to represent 2015 starting point
                zero_pnts = np.zeros(len(YEARS_ALL)+1)
                plt.plot(np.hstack((2014,YEARS_ALL)), zero_pnts, color='0.5', linestyle=':', linewidth =0.75,zorder=1,alpha=0.75)
            
            # Sort out formatting for each regional plot
            if reg == 'South-East Asia and Developing Pacific':
                reg_plot = 'South-East Asia\n and Developing Pacific'
            else:
                reg_plot = reg
            if (cur_plot_ind == 1) or (cur_plot_ind == 4):
                print('Do not plot title yet')
            else:
                plt.title(reg_plot,fontsize=6.5)#,color=h2_reg_col_plt[ireg]) # plot up regional title
            
            plt.minorticks_on() 
            plt.xticks(rotation=15)
            
            # Plot on regional mean value in 2015 (+/- S.D.)    
            cur_reg_val = mod_surf_abs[ireg]#[:,0,ireg]   # year 2015 values across all scenarios
            cur_reg_sd  = mod_surf_abs_sd[ireg]#[:,0,ireg]
            
            ax.text(0.05,0.925,'{:.1f} +/- {:.1f}'.format(cur_reg_val,cur_reg_sd),transform=ax.transAxes,fontsize=5.5) 
            
            plt.tick_params(axis='y',left='on',right='on',labelsize=6,which='major',direction='out',length=2,width=0.5)#,width=1)
            plt.tick_params(axis='y',left='on',right='on',which='minor',direction='out',length=1,width=0.5)#,width=0.5)
            plt.tick_params(axis='x',labelsize=6,which='both')#,direction='inout')
            plt.tick_params(axis='x',top='off',which='both')
            plt.tick_params(axis='x',bottom='on',which='major',direction='out',length=3)#,width=0.)
            plt.tick_params(axis='x',bottom='on',which='minor',direction='out')#,width=1)
            
            if (cur_plot_ind == 4) or (cur_plot_ind == 8) or (cur_plot_ind == 12) or (cur_plot_ind == 16) or (cur_plot_ind == 20): 
                # Turn on right hand yaxis labels for plots on right hand side
                plt.tick_params(labelright='on',labelsize=6)
                ax.yaxis.set_label_position("right")
                plt.ylabel('{}'.format(UNITS_LAB),fontsize=6.5) # plot up units on y-axis
                if (cur_plot_ind == 4):
                    # plot up y-axis title in horizontal at top of figure
                    #plt.ylabel('Change in {}'.format(CP_LAB),fontsize=6,rotation=0)
                    #ax.yaxis.set_label_coords(0.9,1.02) # set label to be above y-axis
                    ax.text(0.5,1.026,'Change in surface {}'.format(CP_LAB),transform=ax.transAxes,fontsize=5.8) # plot y-axis title
                    ax.text(0.3,1.13,reg,transform=ax.transAxes,fontsize=7) # move regional title along
            
            if (cur_plot_ind == 1) or (cur_plot_ind == 5) or (cur_plot_ind == 9) or (cur_plot_ind == 13) or (cur_plot_ind == 14) or (cur_plot_ind == 17):
                # Turn on left hand yaxis labels for plots on left hand side
                plt.tick_params(labelleft='on',labelsize=6)
                ax.yaxis.set_label_position("left")
                plt.ylabel('{}'.format(UNITS_LAB),fontsize=6.5) # plot up units on y-axis
                if (cur_plot_ind == 1):
                    # plot up y-axis title in horizontal at top of figure
                    #plt.ylabel('Change in {}'.format(CP_LAB),fontsize=6,rotation=0)
                    #ax.yaxis.set_label_coords(-0.1,1.02) # set label to be above y-axis
                    ax.text(-0.33,1.026,'Change in surface {}'.format(CP_LAB),transform=ax.transAxes,fontsize=5.8) # plot y-axis title
                    ax.text(0.2,1.13,reg,transform=ax.transAxes,fontsize=7) # move regional title along
                    
            else:
                # for all other axis turn off labelling
                plt.tick_params(labelleft='off')  
            
            #if (cur_plot_ind == 17) or (cur_plot_ind == 18) or (cur_plot_ind == 19) or (cur_plot_ind == 20):
            if (cur_plot_ind == 5) or (cur_plot_ind == 10) or (cur_plot_ind == 11) or (cur_plot_ind == 12) or (cur_plot_ind == 13):
                # plot up x axis labels for only bottom plots
                ax.set_xticklabels(yrs_all_str_lab,fontsize=5.5)
            else:
                # do not plot x axis labels on any other plots
                plt.tick_params(labelbottom='off') 
           
               
            # plot grid lines onto plot
            plt.grid(True,which='major',axis='y',linewidth=0.5,color='0.75',linestyle=':',alpha=0.5)
            
            # Set limits of x and y axis
            #plt.ylim(-17,15)
            plt.ylim(-15,12)
            plt.xlim(2014,2100)
            
            # Set spacing of tick labels
            ax.xaxis.set_major_locator(xmajorLocator)
            ax.xaxis.set_minor_locator(xminorLocator)
            ax.yaxis.set_major_locator(ymajorLocator)
            ax.yaxis.set_minor_locator(yminorLocator)
            
    # Set up legends to put onto plots
    
    # Scenario Labels
    all_lines = []#line_2]
    for iscn,scn in enumerate(SCEN):
        ln_style='-'
        if (scn == 'ssp370-lowNTCF'):  ln_style = '--'
        if (scn == 'ssp370-lowNTCFCH4'): ln_style = ':'
        all_lines.append(mlines.Line2D([], [], color=colors_scn_mod[iscn],linestyle=ln_style, linewidth=1.25, label=PLOT_LAB[iscn]))
    
    labels = [h.get_label() for h in all_lines] 
    
    fig.legend(handles=all_lines, labels=labels, loc=(0.04,0.075),fontsize=7,frameon=False,ncol=1)
    #fig.legend(handles=all_lines, labels=labels, loc=(0.325,0.7),fontsize=6,frameon=False,ncol=3)
    
    # Save figure
    plt.savefig(PLOT_DIR+'Ann_mean_2015_2100_surf_{}_resp_all_CMIP6_5_fut_scns_over_all_regions_CMIP6_multi_model_mean_AR6_regs_no_loc_plot_NTCFCH4_V1_ALL_MODS_ONLY.pdf'.format(CP),orientation='landscape') #print out plot to file
    plt.close("all")    
            
#########################################

if __name__ == '__main__':
        
    print('Read in precomputed Regional mean data')
    # read in pre-computed surface PM2.5 averaged over world regions from multiple CMIP6 models over 2005-2014
    print('read in the 2005-14 annual mean values')
    base_fname = 'Surf_PM2pt5_data_05_14_mean_for_IPCC_figure_V1_5mods.csv'#5mods.csv'
    ann_mod_mean_05_14_mn, ann_mod_mean_05_14_sd, reg_header_05_14 = read_base_mod(DATA_DIR+base_fname)
    print(ann_mod_mean_05_14_mn)
    print(ann_mod_mean_05_14_sd)
    
    print('read in the future surface response values')
    # read in pre-computed surface PM2.5 averaged over world regions from multiple CMIP6 models as change in future
    fut_fname = 'Surf_PM2pt5_data_fut_mean_for_IPCC_figure_V1_5mods.csv'#5mods.csv'
    ann_mod_mean_fut_mn, reg_header_fut = read_fut_mod(DATA_DIR+fut_fname,SCEN,YEARS_ALL)
    print(ann_mod_mean_fut_mn[-1,-1,:])
    
    print('read in the future surface response Standard deviation values values')
    # read in pre-computed standard deviation in surface PM2.5 averaged over world regions from multiple CMIP6 models in future years
    fut_sd_fname = 'Surf_PM2pt5_SD_data_fut_mean_for_IPCC_figure_V1_5mods.csv'#_5mods.csv'
    ann_mod_mean_fut_sd, reg_header_fut_sd = read_fut_mod(DATA_DIR+fut_sd_fname,SCEN,YEARS_ALL)
    print(ann_mod_mean_fut_sd[-1,-1,:])
     
    ####################################
    
    print('Plot up future changes in surface PM2.5 across different world regions from CMIP6 models')
    # produce time series figure of future changes in surface O3 across different scenarios without location map
    plot_fut_timeseries_fig_no_loc(ann_mod_mean_fut_mn,ann_mod_mean_fut_sd,reg_header_fut,ann_mod_mean_05_14_mn,ann_mod_mean_05_14_sd)
       
    print('Fin')
    
    
