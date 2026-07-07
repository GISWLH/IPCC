#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon
from shapely.geometry import Polygon, Point

import csv
import numpy as np
import json
import sys
import os

# -- Retrieve arguments
scenario = sys.argv[1]
horizon = sys.argv[2]

# -- Json output filename
outdir = '/home/jservon/Chapter12_IPCC/data/coastal_recession/'
outfilename = outdir + 'globalErosionProjections_by_AR6_region_'+scenario+'_'+horizon+'.json'

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
        #print(', '.join(row))
        #if row[1]=='Land':
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
        regions_names.append( row[3] )

subregions = geopandas.GeoSeries( subregions_polygons )        
#
# -- Function to return True if lon/lat is within region (dictionary)
def is_in_AR6_region(lon,lat,region_dict):

    lats_vect = np.array(region_dict['lats_vect'])
    lons_vect = np.array(region_dict['lons_vect'])
    lons_lats_vect = np.column_stack((lons_vect, lats_vect)) # Reshape coordinates
    polygon = Polygon(lons_lats_vect) # create polygon
    point = Point(lon,lat) # create point    
    return polygon.contains(point)

#
if not os.path.isfile(outfilename):
    # -- Build input filename
    # -----------------------------------------------------------------
    filename = '/home/ciles/IPCC/coastal/globalErosionProjections_Long_Term_Change_'+scenario+'_'+horizon+'.csv'


    # -- Start a plot to check that the data is properly located in the regions
    # -----------------------------------------------------------------
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
    m = Basemap(projection='robin',lon_0=0,resolution='c')
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

    #for i in np.arange(0,500000,100):
    # -- Retrieve coastal recession data
    # -----------------------------------------------------------------
    print 'Reading coastal recession data for ',scenario,horizon
    coastal_data = []
    median_list = []
    q5_list = []
    q95_list = []
    points_list = []
    lons_list = []
    lats_list = []
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            print i
            lon = float(row[1]
            lat = float(row[0]
            lons_list.append(lon)
            lats_list.append(lat)
            points_list.append( Point(lon, lat) )
            median_list.append( float(row[5]) )
            q5_list.append( float(row[3]) )
            q95_list.append( float(row[7]) )
            ##for subregion in regions.keys():
            ##   found_domain = False
            ##    if is_in_AR6_region(lon,lat,regions[subregion]):
            ##        found_domain = True
            ##        regions_values[subregion]['median'].append(float(row[5]))
            ##        regions_values[subregion]['q5'].append(float(row[3]))
            ##        regions_values[subregion]['q95'].append(float(row[7]))
            ##        color = mycolors[regions.keys().index(subregion)]
            ##        break
            ##if not found_domain:
            ##    color = 'black'
            ##--##x,y = m(lon, lat)
            ##--##m.plot(x, y, color, marker='o', markersize=2 )            
            #coastal_data.append(dict(lat=float(row[0]),
            #                         lon=float(row[1]),
            #                         median=float(row[5]),
            #                         q5=float(row[3]),
            #                         q95=float(row[7])))
            i = i + 1
    #plt.show()
    ##--##fig.savefig(outfilename.replace('.json','.png'))
    #
    points_in_AR6_regions = geopandas.GeoSeries( points_list ).as_matrix()
    # -- points_in_AR6_regions[subregion, point]
    for isubregion in range(0,len(regions.keys())):
        # -- Get the list np.array with the True/False values to identify which points are in the subregion
        is_point_in_subregion = np.array(points_in_AR6_regions[isubregion])
        ind_points_in_subregion = tuple(np.where(is_point_in_subregion==True))
        lons = list(np.array(lons_list[ind_points_in_subregion]))
        lats = list(np.array(lats_list[ind_points_in_subregion]))
        regions_values[regions.keys()[isubregion]] = dict(median = list(np.array(median_list[ind_points_in_subregion])),
                                         q5 = list(np.array(q5_list[ind_points_in_subregion])),
                                         q95 = list(np.array(q5_list[ind_points_in_subregion])),
                                         lons = lons,
                                         lats = lats
                                        )
        x,y = m(lons, lats)
        color = mycolors[isubregion] 
        m.plot( regions_values[regions.keys()[isubregion]]['lons'],
                regions_values[regions.keys()[isubregion]]['lats'],
                color, marker='o', markersize=2 ) 
    #
    fig.savefig(outfilename.replace('.json','.png'))
    # -- Loop on the regions
    # -- Compute averages and put in final_res -> saved in a json file
    # -----------------------------------------------------------------
    print 'Computing averages per subregion'
    final_res = regions.copy()
    for subregion in regions:
        final_res[subregion].pop('lats_vect')
        final_res[subregion].pop('lons_vect')
        for stat in ['median','q5','q95']:
            if regions_values[subregion][stat]:
                final_res[subregion][stat] = np.mean( regions_values[subregion][stat] )

    # -- Save in json file
    # -----------------------------------------------------------------
    # -- subregion / median
    # --             q5
    # --             q95
    # --             long name
    print 'Save '+outfilename
    with open(outfilename, 'w') as fp:
        json.dump(final_res, fp, sort_keys=True, indent=4)
#
