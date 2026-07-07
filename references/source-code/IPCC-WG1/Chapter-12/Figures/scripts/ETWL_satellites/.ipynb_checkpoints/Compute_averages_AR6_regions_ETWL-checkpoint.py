# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/ETWL_satellites/.ipynb_checkpoints/Compute_averages_AR6_regions_ETWL-checkpoint.ipynb

# %% cell 1
from shapely.geometry import Polygon, Point
import geopandas
import csv
import numpy as np
import json
import os
#import Nio
import xarray as xr

# -- Retrieve arguments

# -- Loop on scenarios and horizons
#for scenario in ['RCP85']:
#    for horizon in ['2100']:
for scenario in ['RCP45','RCP85']:
    for horizon in ['2050','2100']:
        
        # -- Json output filename
        outdir = '/home/jservon/Chapter12_IPCC/data/ETWL/'
        outfilename = outdir + 'Vousdoukas_ETWL_by_AR6_region_'+scenario+'_'+horizon+'.json'
        baseline_outfilename = outdir + 'Vousdoukas_ETWL_by_AR6_region_modern.json'

        # ---------------------------------------------------------------------------------------------------
        # --
        # -- Retrieve the AR6 regions from the reference regions file provided by ATLAS (Santander Group)
        # --
        # ---------------------------------------------------------------------------------------------------
        regions_filename='/home/jservon/Chapter12_IPCC/scripts/ATLAS/reference-regions/IPCC-WGI-reference-regions-v4_coordinates.csv'

        # -- Store the informations by region in the 'regions' dictionary
        regions = dict()
        subregions_names = []
        subregions_polygons = []
        with open(regions_filename) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
            for row in spamreader:
                region_dict = dict(region = row[0],
                                   domain = row[1],
                                   long_name = row[2],
                                  )
                lats_vect = []
                lons_vect = []
                tmp_polygon_vertices = []
                for vertice in row[4:-1]:
                    if vertice:
                        dum = vertice.split('|')
                        lons_vect.append(float(dum[0]))
                        lats_vect.append(float(dum[1]))
                        tmp_polygon_vertices.append( (float(dum[0]), float(dum[1])) )
                subregions_polygons.append( Polygon(tmp_polygon_vertices) )
                region_dict['lons_vect'] = np.array(lons_vect)
                region_dict['lats_vect'] = np.array(lats_vect)
                #
                regions[row[3]] = region_dict
                subregions_names.append( row[3] )

        subregions = geopandas.GeoSeries( subregions_polygons )

        # -- Start a plot to check that the data is properly located in the regions
        # -----------------------------------------------------------------
        #filename = '/home/ciles/IPCC/coastal/globalErosionProjections_Long_Term_Change_'+scenario+'_'+horizon+'.csv'

        import matplotlib
        matplotlib.use('Agg')
        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon as Polygon_patches
        import matplotlib.colors as mcolors

        # -- Open the figure
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(12,8))

        # -- Prepare the map
        # -----------------------------------------------------------------
        # setup Lambert Conformal basemap.
        m = Basemap(projection='robin', lon_0=0, resolution='c')
        # draw coastlines.
        m.drawcoastlines()
        # draw a boundary around the map, fill the background.
        # this background will end up being the ocean color, since
        # the continents will be drawn on top.
        m.drawmapboundary(fill_color='white')
        # fill continents, set lake color same as ocean color.
        m.fillcontinents(color='white',lake_color='white')


        # -- Colors for the regions
        # -----------------------------------------------------------------
        tmpcolors = ['blue','green','red','brown','goldenrod','darkcyan','orange']
        mycolors = []
        for i in range(0,30):
            mycolors += tmpcolors

        # -- Function to draw the regions
        # -----------------------------------------------------------------
        def draw_screen_poly( lats, lons, m, color='red'):
            x, y = m( lons, lats )
            xy = zip(x,y)
            poly = Polygon_patches( xy, edgecolor = color, facecolor='none')
            plt.gca().add_patch(poly)

        for subregion in regions.keys():
            lons = regions[subregion]['lons_vect']
            lats = regions[subregion]['lats_vect']
            draw_screen_poly( lats, lons, m, color=mycolors[regions.keys().index(subregion)])



        # -- Attributing the points to the regions
        # -----------------------------------------------------------------
        print 'Attributing values to the regions'
        regions_values = dict()
        for subregion in regions.keys():
            regions_values[subregion] = dict(median=[], q5=[], q95=[])

        # -- Retrieve TWL data
        # -----------------------------------------------------------------
        print 'Reading TWL data for ',scenario,horizon

        #horizon = 2050
        TWL_baseline_file = '/data/ciles/IPCC/SOD/ESL/globalTWL_baseline.nc'
        TWL_file = '/data/ciles/IPCC/SOD/ESL/globalTWL_'+scenario+'.nc'
        #ncfile_baseline = Nio.open_file(TWL_baseline_file)
        #ncfile = Nio.open_file(TWL_file)
        ncfile_baseline = xr.open_dataset(TWL_baseline_file)
        ncfile = xr.open_dataset(TWL_file)

        if horizon=='2050':
            decade_index = 4
        if horizon=='2100':
            decade_index = 9

        TWL_baseline_q5     = ncfile_baseline.variables["TWL"][:,0]
        TWL_baseline_median = ncfile_baseline.variables["TWL"][:,1]
        TWL_baseline_q95    = ncfile_baseline.variables["TWL"][:,2]
        
        TWL_median = ncfile.variables["TWL"][:,1,decade_index]# - TWL_baseline
        TWL_q5     = ncfile.variables["TWL"][:,0,decade_index]# - TWL_baseline
        TWL_q95    = ncfile.variables["TWL"][:,2,decade_index]# - TWL_baseline
        lat  = ncfile.variables["latitude"][:]
        lon  = ncfile.variables["longitude"][:]
        
        #median_list = TWL_median
        #q5_list = TWL_q5
        #q95_list = TWL_q95
        points_list = []
        for i in range(0,len(lon)):
            points_list.append( Point(lon[i], lat[i]) )
        lons_list = lon
        lats_list = lat
        
        points_in_AR6_regions = geopandas.GeoSeries( points_list )
        are_points_in_subregions = subregions.apply(lambda x: points_in_AR6_regions.within(x)).as_matrix()

        # -- points_in_AR6_regions[subregion, point]
        regions_values = dict()
        baseline_regions_values = dict()
        #if None:
        for isubregion in range(0,len(subregions_names)):
            #print subregions_names[isubregion]
            # -- Get the list np.array with the True/False values to identify which points are in the subregion
            is_point_in_subregion = np.array(are_points_in_subregions[isubregion])
            ind_points_in_subregion = tuple(np.where(is_point_in_subregion==True))
            lons = list(np.array(lons_list)[ind_points_in_subregion])
            lats = list(np.array(lats_list)[ind_points_in_subregion])
            regions_values[subregions_names[isubregion]] = dict(median = list(np.array(TWL_median)[ind_points_in_subregion]),
                                             q5 = list(np.array(TWL_q5)[ind_points_in_subregion]),
                                             q95 = list(np.array(TWL_q95)[ind_points_in_subregion]),
                                            )
            baseline_regions_values[subregions_names[isubregion]] = dict(median = list(np.array(TWL_baseline_median)[ind_points_in_subregion]),
                                             q5 = list(np.array(TWL_baseline_q5)[ind_points_in_subregion]),
                                             q95 = list(np.array(TWL_baseline_q95)[ind_points_in_subregion]),
                                            )
            if lons:
                #print '-->', len(lons),'points'
                x,y = m(lons, lats)
                color = mycolors[isubregion]
                m.plot( x,
                        y,
                        color,linestyle="", marker='o', markersize=2 )

        fig.savefig(outfilename.replace('.json','.png'))
        # -- Loop on the regions
        # -- Compute averages and put in final_res -> saved in a json file
        # -----------------------------------------------------------------
        print 'Computing averages per subregion'
        #final_res = regions.copy()
        final_res = dict()
        baseline_final_res = regions.copy()
        #for subregion in regions:
        # Ajouter la moyenne globale
        for subregion in subregions_names:
            final_res[subregion]=dict(domain=regions[subregion]['domain'], long_name=regions[subregion]['long_name'])
            #final_res[subregion].pop('lats_vect')
            #final_res[subregion].pop('lons_vect')
            for stat in ['median','q5','q95']:
                if regions_values[subregion][stat]:
                    final_res[subregion][stat] = np.mean( regions_values[subregion][stat] )
            if 'lats_vect' in baseline_final_res[subregion]:
                baseline_final_res[subregion].pop('lats_vect')
                baseline_final_res[subregion].pop('lons_vect')
            for stat in ['median','q5','q95']:
                if baseline_regions_values[subregion][stat]:
                    baseline_final_res[subregion][stat] = np.mean( baseline_regions_values[subregion][stat] )
        # -- Add the global mean
        subregion = 'Global'
        final_res[subregion] = dict()
        final_res[subregion]['median'] = float(np.mean( TWL_median ))
        print float(np.mean(TWL_median))
        final_res[subregion]['q5'] = float(np.mean( TWL_q5 ))
        final_res[subregion]['q95'] = float(np.mean( TWL_q95 ))
        baseline_final_res[subregion] = dict()
        baseline_final_res[subregion]['median'] = float(np.mean( TWL_baseline_median ))
        baseline_final_res[subregion]['q5'] = float(np.mean( TWL_baseline_q5 ))
        baseline_final_res[subregion]['q95'] = float(np.mean( TWL_baseline_q95 ))
        
        # -- Save in json file
        # -----------------------------------------------------------------
        # -- subregion / median
        # --             q5
        # --             q95
        # --             long name
        print 'final_res = ', final_res['RFE']
        print 'regions_values =', np.mean(regions_values['RFE']['median'])
        print 'baseline_regions_values =', np.mean(baseline_regions_values['RFE']['median'])
        print 'Save '+outfilename+' and '+baseline_outfilename
        with open(outfilename, 'w') as fp:
            json.dump(final_res, fp, sort_keys=True, indent=4)
        with open(baseline_outfilename, 'w') as fp:
            json.dump(baseline_final_res, fp, sort_keys=True, indent=4)

        #from IPython.display import Image
        #Image(outfilename.replace('.json','.png'))

# %% cell 2
#Computing averages per subregion
#3.21403534677
#{'domain': 'Land', 'q5': 2.991485812240689, 'q95': 3.9162027436652505, 'region': 'ASIA', 'median': 3.4603456307708966, 'long_name': 'Russian-Far-East'}
#Save /home/jservon/Chapter12_IPCC/data/ETWL/Vousdoukas_ETWL_by_AR6_region_RCP85_2100.json and /home/jservon/Chapter12_IPCC/data/ETWL/Vousdoukas_ETWL_by_AR6_region_modern.json
final_res['Global']

# %% cell 3
from IPython.display import Image
scenario = 'RCP85'
horizon = '2100'
outfilename = outdir + 'ETWL_by_AR6_region_'+scenario+'_'+horizon+'.json'
Image(outfilename.replace('.json','.png'))

# %% cell 4
TWL_median = ncfile.variables["TWL"][:,1,decade_index]
TWL_median

# %% cell 5
#!ls /data/ciles/IPCC/SOD/ESL/
import Nio

rcp = 'RCP85'
horizon = 2050
baseline = '/data/ciles/IPCC/SOD/ESL/globalTWL_baseline.nc'
future = '/data/ciles/IPCC/SOD/ESL/globalTWL_'+rcp+'.nc'

#ncfile_baseline = Nio.open_file(baseline)
ncfile_future = Nio.open_file(future)

if horizon==2050:
    decade_index = 4
if horizon==2100:
    decade_index = 9

#TWL_baseline  = ncfile_baseline.variables["TWL"][:,1]
TWL_future  = ncfile_future.variables["TWL"][:,1,decade_index]
lat  = ncfile_future.variables["latitude"][:]
lon  = ncfile_future.variables["longitude"][:]

# %% cell 6
Ebru_file = '/home/jservon/Chapter12_IPCC/data/ETWL/Ebrus_ESL.csv'
Ebru_res = dict()
with open(Ebru_file) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')#, quotechar='|')
    for row in spamreader:
        print row
        Ebru_res[row[0]] = dict()
