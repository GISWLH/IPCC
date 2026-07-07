'''
Function to plot up 2D contour plots of O3 changes at different temperature thresholds
Calculate multi-model mean of data

Created on Oct 5, 2020

@author: sturnock
'''

import iris
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors  #colors
import cartopy.crs as ccrs         #cartopy  

UKESM_DIR   = '/data/users/sturnock/UKESM_cmip6/ensemble_mean/'
CMIP6_DIR   = '/data/users/sturnock/CMIP6_model_output/processed_ESGF/ensemble_mean/'

PLOT_DIR    = '/net/home/h06/sturnock/Python/UKESM_cmip6/Images_multi_mods/IPCC_figs/'#o3_revised/'#no2/'
FUT_SCEN    = 'ssp370SST'#-lowNTCF'#'historical'#'ssp370'#['SSP1_26','SSP2_45','SSP3_70','SSP5_85']
FUT_SCEN_2  = 'ssp370pdSST'#emis'

SIG_PLOT    = True # set to plot up stipling to show model agreement in sign of change (75%)

CP          = 'o3'#'no'#'o3'
CP_LAB      = '$\mathregular{O_{3}}$'#{NO_{2}}$'#{O_{3}}$'
UNITS_LAB   = '(ppb)'
MOD_LIST    = ['UKESM1-0-LL','GISS-E2-1-G','GFDL-ESM4','MRI-ESM2-0']#,'EC-Earth3-AerChem']
#Define temperature threshold years for models above
DEGREE_SIGN = '$^{\circ}$'
# Threshold based on year temperature difference is hit in each model between ssp370SST - ssp370pdSST scenarios
THRES_PLOT  = ['1.0','1.5','2.0','2.5']
THRESHOLDS  = {'UKESM1-0-LL':[2029,2039,2049,2057],
               'GISS-E2-1-G':[2025,2037,2057,2079],
               'GFDL-ESM4':[2045,2061,2073,2093],
               'MRI-ESM2-0':[2040,2056,2070,2087]}#,
#               'EC-Earth3-AerChem':[2036,2057,2065,2070]}

ST_YR_FILE  = '2015'
EN_YR_FILE  = '2099'#'1850'#'2100'

NROWS       = 2#len(THRES_PLOT)+1

# USE HTAP2 Receptor Regions to create 1x1 array to store multi-model data
REG_DIR_PATH = '/data/users/sturnock/HTAP_files/HTAP_regions/v2/'
REG_FNAME = 'regridTo1x1_Template.nc'

# Manually change default hatching properties within MPL
#mpl.rc('hatch', color='0.1', linewidth=0.5)
mpl.rc('hatch', color='grey', linewidth=0.5)
#plt.rcParams.update({'hatch.color': 'grey'})

#########################################

def check_cube_ann(cube):
    '''
    Check to see if cube has bounds and assigns them
    Also calculates area weights
    '''
    #for icube,cube in enumerate(cube_list):
    #Check to see if cube has bounds and if not assign some
    #if not cube.coord('time').has_bounds(): 
    #    print 'Cube does not have time bounds so guessing them'
    #    cube.coord('time').guess_bounds()
    if not (cube.coord('longitude').has_bounds() and cube.coord('latitude').has_bounds()):
        print('Cube does not have lat/lon bounds so guessing them')
        #cube.coord('time').guess_bounds()
        cube.coord('longitude').guess_bounds()
        cube.coord('latitude').guess_bounds()
        
    if cube.coords('Surface Air Pressure'):
        print('Remove surface Air Pressure coordinate')
        cube.remove_coord('Surface Air Pressure')
        
        # Assign monthly category so can perform meaning
        #for cube in cubes_1_list_surf_out: 
        #coord_cat.add_month(cube, 'time', name='month')
        #print cube
        
    # Define lat lon coordinate system for cube
    lat_lon_coord_system = iris.coord_systems.GeogCS(6371229)
    cube.coord('latitude').coord_system = lat_lon_coord_system
    cube.coord('longitude').coord_system = lat_lon_coord_system
             
    # calculate grid_areas for are weighting
    grid_areas = iris.analysis.cartography.area_weights(cube, normalize=False)

    return cube, grid_areas

#------------------------------------------

def flip_lats_2D(data,lats,lons):
    '''
    Check to see if latitude points are from +90 to -90, otherwise flip
    '''
    new_lats = np.zeros(len(lats),dtype='f')
    new_data = np.zeros((len(lats),len(lons)),dtype='f')
    
    
    #print lats[0], lats[-1]
    if lats[0] > lats[-1]:
        print('Flip Lats to be increasing from -90 to 90')
        
        new_lats = np.flipud(lats)
        
        #new_data = np.flipud(data) #This flips all dimensions including levels
        ilat_2 = len(lats)-1
        for ilat in np.arange(len(lats)):
            #print ilat, ilat_2
            
            new_data[ilat,:] =  data[ilat_2,:]
            
            ilat_2 -= 1
            
    else:
        print('No LAT Shift required')
        new_lats[:] = lats[:]
        new_data[:,:] = data[:,:]
    
    #print data[0,-1,0,0], new_data[0,-1,0,0]
    
    return new_data,new_lats     

#-------------------------------------------------------------

#########################################

if __name__ == '__main__':
    
    print('Read in HTAP-2 region codes file for use as 1x1 array')
    #Load HTAP2 regions as cube
    h2_reg_codes_cube = iris.load_cube(REG_DIR_PATH+REG_FNAME)
    h2_reg_codes_cube_2, grid_areas_1x1 = check_cube_ann(h2_reg_codes_cube)
    print(h2_reg_codes_cube_2.summary(shorten=True))
    reg_lats = h2_reg_codes_cube_2.coord('latitude').points
    reg_lons = h2_reg_codes_cube_2.coord('longitude').points
    
    print('H2_CODES',reg_lats[0],reg_lats[-1])
    print('H2_CODES',reg_lons[0],reg_lons[-1])
    
    print('Check to see if Lats need reversing')
    htap_2_region_codes_flp,new_reg_lats = flip_lats_2D(h2_reg_codes_cube_2.data,reg_lats,reg_lons)
    print('H2_CODES',new_reg_lats[0], new_reg_lats[-1])
    print(htap_2_region_codes_flp.shape)
    
    # Create cube with 
    h2_reg_codes_flp_cube = h2_reg_codes_cube_2.copy(data=np.zeros(htap_2_region_codes_flp.shape))
    h2_reg_codes_flp_cube.coord('latitude').points = new_reg_lats[:]
    h2_reg_codes_flp_cube.data[:,:] = htap_2_region_codes_flp[:,:]
    h2_reg_codes_flp_cube, grid_areas_1x1 = check_cube_ann(h2_reg_codes_flp_cube)
    print(h2_reg_codes_flp_cube.summary(shorten=True))
    
    # Array to collate all model data
    all_mod_ann_fut_resp_o3_1x1 = np.zeros((len(MOD_LIST),len(THRES_PLOT),len(reg_lats),len(reg_lons)))
    all_mod_ann_fut_resp_o3_1x1_pos = np.zeros(all_mod_ann_fut_resp_o3_1x1.shape)
    glob_ann_mean_fut_resp      = np.zeros((len(MOD_LIST),len(THRES_PLOT)))
    
    print('Set up plot figure')
    no_mods = 2#len(MOD_LIST)
    # plot up model output as go along (models on y and 2015, 2050, 2100 on x)
    fig, axes = plt.subplots(NROWS,no_mods)
    plt.subplots_adjust(bottom=0.08,left=0.03,top=0.97,right=0.97,wspace=0.05,hspace=0.05)
    
    projection = ccrs.Robinson()
    
    # Difference Colour maps
    cont_levs_diff = [-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]   
    cmap_use_diff = plt.get_cmap('RdBu_r')
    norm_diff = colors.BoundaryNorm(cont_levs_diff, cmap_use_diff.N)
    
    print('Read in individual model data')
    for imod,mod in enumerate(MOD_LIST):
        
        #plt_ind = imod + 1
        print('Read in Surface {} concentrations for {}'.format(CP,mod))
        file_path_use = CMIP6_DIR
        
        fname               = '{}_monthly_annual_seasonal_mean_surf_{}_for_CMIP6_{}_{}_{}_all.nc'.format(mod,CP,FUT_SCEN,ST_YR_FILE,EN_YR_FILE)
        cube_name           = 'annual mean surface {} concentration in {}'.format(CP,FUT_SCEN)
        mod_data_ann_surf_in       = iris.load_cube(file_path_use+fname,cube_name)
        
        check_cube_ann(mod_data_ann_surf_in)
        
        print(mod_data_ann_surf_in.summary(shorten=True))
        
        fname_2     = '{}_monthly_annual_seasonal_mean_surf_{}_for_CMIP6_{}_{}_{}_all.nc'.format(mod,CP,FUT_SCEN_2,ST_YR_FILE,EN_YR_FILE)
        cube_name_2 = 'annual mean surface {} concentration in {}'.format(CP,FUT_SCEN_2)
        
        mod_data_ann_surf_2_in = iris.load_cube(file_path_use+fname_2,cube_name_2)
        check_cube_ann(mod_data_ann_surf_2_in)
        print(mod_data_ann_surf_2_in.summary(shorten=True))
        
        # remove this coordinate from BCC model
        #if (mod == 'BCC-ESM1') or (mod == 'GISS-E2-1-G') or (mod == 'MRI-ESM2-0'): 
        #    mod_data_hist_ann_surf_in.remove_coord('Surface Air Pressure')
        #    mod_data_ann_surf_in.remove_coord('Surface Air Pressure')
        #    if I_FUT_DIFF: mod_data_ann_surf_2_in.remove_coord('Surface Air Pressure')
        
        # remove this coordinate from EC-Earth3-AerChem model
        #if (mod == 'EC-Earth3-AerChem'): 
        #    mod_data_hist_ann_surf_in.remove_coord('air_pressure')
        #    #mod_data_ann_surf.remove_coord('air_pressure')
        #    #if I_FUT_DIFF: mod_data_ann_surf_2.remove_coord('air_pressure')
        
        # Convert input files into 1x1 cubes so can collate a multi-model mean
        print('Regrid model data to 1x1 grid')
        mod_data_ann_surf         = mod_data_ann_surf_in.regrid(h2_reg_codes_flp_cube,iris.analysis.Nearest())
        mod_data_ann_surf_2       = mod_data_ann_surf_2_in.regrid(h2_reg_codes_flp_cube,iris.analysis.Nearest())
        print(mod_data_ann_surf.summary(shorten=True))
        print(mod_data_ann_surf_2.summary(shorten=True))
        
        # Now extract relevant data for each model for 10 years before after relevant temperature threshold
        print('Extract data for each temperature threshold for {}'.format(mod))
        cur_thresholds = THRESHOLDS[mod]
        print(cur_thresholds)
        for ithres,thres in enumerate(cur_thresholds):
            print('Extract data for threshold {} in year {} for {}'.format(THRES_PLOT[ithres],thres,mod))
            
            fur_time_con = iris.Constraint(time=lambda cell: thres-10 <= cell.point.year < thres+10)
            mod_data_ann_surf_ext = mod_data_ann_surf.extract(fur_time_con)
            print(mod_data_ann_surf_ext.summary(shorten=True))
            if (mod == 'EC-Earth3-AerChem'): 
                # EC-Earth has derived pressure coordinates which can#t remove so need to get out of cubes
                mod_data_ann_surf_ext_mn = np.mean(mod_data_ann_surf_ext.data,axis=0)
                print(mod_data_ann_surf_ext_mn.shape)
            else:
                mod_data_ann_surf_ext_mn_in = mod_data_ann_surf_ext.collapsed('time',iris.analysis.MEAN)
                print(mod_data_ann_surf_ext_mn_in.summary(shorten=True))
                mod_data_ann_surf_ext_mn = mod_data_ann_surf_ext_mn_in.data[:,:]
            print(np.min(mod_data_ann_surf_ext_mn.data),np.mean(mod_data_ann_surf_ext_mn.data),np.max(mod_data_ann_surf_ext_mn.data))
            
            # Calculate Difference
            print('Calc future diff')
            mod_data_ann_surf_2_ext     = mod_data_ann_surf_2.extract(fur_time_con)
            if (mod == 'EC-Earth3-AerChem'): 
                mod_data_ann_surf_2_ext_mn = np.mean(mod_data_ann_surf_2_ext.data,axis=0)
                print(mod_data_ann_surf_2_ext_mn.shape)
            else:
                mod_data_ann_surf_2_ext_mn_in  = mod_data_ann_surf_2_ext.collapsed('time',iris.analysis.MEAN)
                print(mod_data_ann_surf_2_ext_mn_in.summary(shorten=True))
                mod_data_ann_surf_2_ext_mn = mod_data_ann_surf_2_ext_mn_in.data[:,:]
                    
            print(np.min(mod_data_ann_surf_2_ext_mn.data),np.mean(mod_data_ann_surf_2_ext_mn.data),np.max(mod_data_ann_surf_2_ext_mn.data))
                
            # Future difference
            #thres_resp = mod_data_ann_surf_ext_mn.data - mod_data_ann_surf_2_ext_mn.data
            thres_resp = mod_data_ann_surf_ext_mn - mod_data_ann_surf_2_ext_mn
            
            print(np.min(thres_resp),np.mean(thres_resp),np.max(thres_resp))
            
            cur_glob_ann_mean_fut = np.average(thres_resp,weights=grid_areas_1x1)#.collapsed(['latitude','longitude'],iris.analysis.MEAN)
            print('Global mean Future Response Data at {} temperature threshold'.format(thres))
            print(cur_glob_ann_mean_fut)
            glob_ann_mean_fut_resp[imod,ithres] = cur_glob_ann_mean_fut
            
            all_mod_ann_fut_resp_o3_1x1[imod,ithres,:,:] = thres_resp[:,:]
            
            # Create significance array for where model response is positive
            pos_resp = np.zeros(thres_resp.shape)
            pos_resp[thres_resp[:,:] > 0.0] = 1.0 # where positive O3 response assign value of 1.0
            pos_resp[thres_resp[:,:] < 0.0] = -1.0 # where negative O3 response assign value of -1.0
            #print(thres_resp[0,110])
            #print(pos_resp[0,110])
            #print(thres_resp[thres_resp < 0.0])
            #print(pos_resp[pos_resp==-1.0])
            #exit()
            all_mod_ann_fut_resp_o3_1x1_pos[imod,ithres,:,:] = pos_resp[:,:]
            
            #plt_ind += no_mods
            print('Finished getting data for {} at {}'.format(mod,THRES_PLOT[ithres]))
        
        print('Finished all temp thresholds for {}'.format(mod))
    
    print('Finished getting data for all models')
    
    #Create significance array for where 3 out of 4 models agree with the sign of change
    sig_test = 3.0/4.0 # greater than or equal to 0.75  
    #Create significance array for where 4 out of 5 models agree with the sign of change
    #sig_test = 4.0/5.0 # greater than or equal to 0.80  
    #neg_sig_test = -2.0/4.0
        
    # Count up where models agree on the sign of change
    #all_mod_ann_fut_resp_o3_1x1_cnt_pos = np.zeros((len(THRES_PLOT),len(reg_lats),len(reg_lons)))
    all_mod_ann_fut_resp_o3_1x1_cnt_pos = np.sum(all_mod_ann_fut_resp_o3_1x1_pos == 1.0,axis=0)
    all_mod_ann_fut_resp_o3_1x1_cnt_neg = np.sum(all_mod_ann_fut_resp_o3_1x1_pos == -1.0,axis=0)
    
    all_mod_ann_fut_resp_o3_1x1_cnt_pos_sig = all_mod_ann_fut_resp_o3_1x1_cnt_pos / len(MOD_LIST)
    all_mod_ann_fut_resp_o3_1x1_cnt_neg_sig = all_mod_ann_fut_resp_o3_1x1_cnt_neg / len(MOD_LIST)
    
    sig_arr = np.zeros(all_mod_ann_fut_resp_o3_1x1_cnt_pos.shape)
    # for all points that are above or below sig_test i.e. stiple where models agree
    sig_arr[all_mod_ann_fut_resp_o3_1x1_cnt_pos_sig[:,:,:] >= sig_test] = 1.0
    sig_arr[all_mod_ann_fut_resp_o3_1x1_cnt_neg_sig[:,:,:] >= sig_test] = 1.0
    
    print(sig_arr.shape)
    print(len(np.where(sig_arr ==1.0)[0]))
    print(len(np.where(sig_arr ==0.0)[0]))
    
    print('Create multi-model mean data')
    all_mod_ann_fut_resp_o3_1x1_mn  = np.mean(all_mod_ann_fut_resp_o3_1x1,axis=0)
    glob_ann_mean_fut_resp_mn       = np.mean(glob_ann_mean_fut_resp,axis=0)
    glob_ann_mean_fut_resp_sd       = np.std(glob_ann_mean_fut_resp,axis=0)
    
    print('Plot up multi-model mean data')
    plt_ind = 1#imod + 1
    lons = np.zeros(reg_lons.shape)#len(mod_data_ann_surf.coord('longitude').points))
    lats = np.zeros(new_reg_lats.shape)
    lats[:] = new_reg_lats[:]#mod_data_ann_surf.coord('latitude').points
    lons[:] = reg_lons[:]#mod_data_ann_surf.coord('longitude').points
    lons[-1] = 360.0 # to force contours to stitch together at zero lon
    lons[0] = 0.0
    x, y = np.meshgrid(lons,lats)
    
    # Plot up multi-model differences
    fig_lab = ['a)','b)','c)','d)']
    for ithres,thres in enumerate(THRES_PLOT):
        print('Plot data for threshold {}'.format(thres))
        #print('Plot up {} response at {} in {}'.format(CP,thres,mod))
        ax1 = plt.subplot(NROWS,no_mods,plt_ind,projection=projection)
        ax1.outline_patch.set_linewidth(0.1) # set linewidth of map projection
        ax1.coastlines(linewidth=0.25) #put coastlines on top plot
        #plt.title('{} change in annual mean surface {} at {}C'.format(fig_lab[ithres],CP_LAB,thres+DEGREE_SIGN),fontsize=8)
        plt.title('{} ozone change at {}C ({:.2f} +/- {:.2f})'.format(fig_lab[ithres],thres+DEGREE_SIGN,glob_ann_mean_fut_resp_mn[ithres],glob_ann_mean_fut_resp_sd[ithres]),fontsize=8)
        cs_1 = ax1.pcolormesh(x, y, all_mod_ann_fut_resp_o3_1x1_mn[ithres,:,:], transform=ccrs.PlateCarree(), norm=norm_diff, cmap=cmap_use_diff)
        
        if SIG_PLOT:
            print('plot up stipling to show model agreement')
            # stipple points where models disagree 
            mask_levs_abs = [0,0.9,1.1]
            #ax1.contourf(x, y, sig_arr[ithres,:,:], transform=ccrs.PlateCarree(), levels = mask_levs_abs, colors='none',hatches=['','.......'],alpha=0.0)
            cs_sig = ax1.contourf(x, y, sig_arr[ithres,:,:], transform=ccrs.PlateCarree(), levels = mask_levs_abs, colors='none',hatches=[5*'//',''],alpha=0.0) #,markerlinewidth=0.5
                        
        plt_ind += 1
    
    print('Finished all contour plots')
    
    print('Add manual Color bars and Save')
    # plot manual colour bars
    # left, bottom, width, height
    
    cax1 = fig.add_axes([0.11,0.08,0.8,0.02])#[0.89, 0.05, 0.02, 0.58])#[0.45, 0.15, 0.02, 0.7])
    cb1 = fig.colorbar(cs_1, cax=cax1, ticks=[-5,-4,-2,-3,-1,1,2,3,4,5], orientation='horizontal',extend='both') 
    
    ##cb = plt.colorbar(cs, orientation='horizontal')
    cb1.ax.tick_params(labelsize=7) # Change fontsize of colour bar labels (ax is function of cb dont change)
    cb1.ax.set_xlabel('{}'.format(UNITS_LAB),fontsize=8) # $cm^{-3}$'
    #cb1.ax.set_title('$\Delta$ {} {}'.format(CP_LAB,UNITS_LAB),fontsize=7)
    
    # Plot up significance in legend
    #ax1.annotate('///' 'Lack of model agreement (threshold: 75%)',xy=(0.325,0.13), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=7.5)
    ax1.annotate('///',color='grey',xy=(0.325,0.13), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=7.5)
    #ax1.annotate('Lack of model agreement (threshold: 75%)',color='black',xy=(0.35,0.13), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=7.5)
    ax1.annotate('Lack of model agreement (threshold: 80%)',color='black',xy=(0.35,0.13), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=7.5)
        
    # Save the plot
    plt.savefig(PLOT_DIR+'Ann_mean_surf_{}_diff_between_{}_and_{}_scenario_2D_plot_{}_CMIP6_models_MMM_resp_at_NEW_ssp370pdSST_temp_thresholds_horiz_V2_NO_SIG_stip_80pc.pdf'.format(CP,FUT_SCEN,FUT_SCEN_2,str(len(MOD_LIST))),orientation='portrait') #print out plot to fi
    plt.close("all")
        
    print('FIN')
    
