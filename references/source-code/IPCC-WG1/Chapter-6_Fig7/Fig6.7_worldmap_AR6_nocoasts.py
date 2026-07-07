#Equidistant Cylindrical Projection
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#sys.setrecursionlimit(limit)

AR6_file = Dataset('../input/AR6WG3_Atlas_IntermedRegions_1.0x1.0.nc','r')
IMPROVE_file = Dataset('../input/stations/IMPROVE.nc','r')
EPA_file     = Dataset('../input/stations/EPA.nc','r')
EMEP_file    = Dataset('../input/stations/EMEP.nc','r')
EMEP2_file   = Dataset('../input/stations/EMEP2.nc','r')
EANET_file   = Dataset('../input/stations/EANET.nc','r')
EASIA_file   = Dataset('../input/stations/EASIA.nc','r')
SPARTAN_file = Dataset('../input/stations/SPARTAN.nc','r')

AR6=AR6_file.variables["AR6WG3RegionIntm"]
lat = AR6_file.variables['latitude'][:]
lon = AR6_file.variables['longitude'][:]
IMPROVE_LON=IMPROVE_file.variables["LON"][-1,:]
IMPROVE_LON_rg=IMPROVE_LON-360
IMPROVE_LAT=IMPROVE_file.variables["LAT"][-1,:]
EPA_LON=EPA_file.variables["LON"][-1,:]
EPA_LAT=EPA_file.variables["LAT"][-1,:]
EMEP_LON=EMEP_file.variables["LON"][-1,:]
EMEP_LAT=EMEP_file.variables["LAT"][-1,:]
EMEP2_LON=EMEP2_file.variables["LON"][-1,:]
EMEP2_LAT=EMEP2_file.variables["LAT"][-1,:]
EANET_LON=EANET_file.variables["LON"][-1,:]
EANET_LAT=EANET_file.variables["LAT"][-1,:]
EASIA_LON=EASIA_file.variables["LON"][-1,:]
EASIA_LAT=EASIA_file.variables["LAT"][-1,:]
SPARTAN_LON=SPARTAN_file.variables["LON"][-1,:]
SPARTAN_LAT=SPARTAN_file.variables["LAT"][-1,:]
ASIA_LON = np.array([39.9,39.3,38.0,23.3,30.6,29.5,34.3,28.9])
ASIA_LAT = np.array([116.4,117.4,114.5,112.9,104.1,106.6,108.9,41.02])
OCEANIA_LON = np.array([174.7,175.2,175.2,139.34])
OCEANIA_LAT = np.array([-36.9,-43.5,-37.8,-25.9])
Africa_LON = np.array([31.21,31.25,37.66,39.29,-13.6,-13.72,-13.62])
Africa_LAT = np.array([30.03,30.06,-6.83,-6.81,9.60,9.51,9.62])
N_America_LON = np.array([-72, -46, -43.21, -43.21, -43.71, -59.5, -54.7, -56.1, -61.93, -43.13, -45.87])
N_America_LAT = np.array([-36.57, -23, -22.9, -22.79, -22.74, -1.9, -2.5, -9.9, -10.08, -22.9, -23.21])

IMPROVE_LON_f = list(IMPROVE_LON_rg)
IMPROVE_LAT_f = list(IMPROVE_LAT)
EPA_LON_f = list(EPA_LON)
EPA_LAT_f = list(EPA_LAT)
EMEP_LON_f = list(EMEP_LON)
EMEP_LAT_f = list(EMEP_LAT)
EMEP2_LON_f = list(EMEP2_LON)
EMEP2_LAT_f = list(EMEP2_LAT)
EANET_LON_f = list(EANET_LON)
EANET_LAT_f = list(EANET_LAT)
EASIA_LON_f = list(EASIA_LON)
EASIA_LAT_f = list(EASIA_LAT)
SPARTAN_LON_f = list(SPARTAN_LON)
SPARTAN_LAT_f = list(SPARTAN_LAT)
ASIA_LON_f = list(ASIA_LON)
ASIA_LAT_f = list(ASIA_LAT)
OCEANIA_LON_f = list(OCEANIA_LON)
OCEANIA_LAT_f = list(OCEANIA_LAT)
Africa_LON_f = list(Africa_LON)
Africa_LAT_f = list(Africa_LAT)
N_America_LON_f = list(N_America_LON)
N_America_LAT_f = list(N_America_LAT)

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.

m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

coasts = m.drawcoastlines(zorder=1,color='white',linewidth=0)
coasts_paths = coasts.get_paths()
ipolygons = range(0,79) #Main ocean coasts  
for ipoly in ipolygons:
    r = coasts_paths[ipoly]
    # Convert into lon/lat vertices
    polygon_vertices = [(vertex[0],vertex[1]) for (vertex,code) in
                        r.iter_segments(simplify=False)]
    px = [polygon_vertices[i][0] for i in range(len(polygon_vertices))]
    py = [polygon_vertices[i][1] for i in range(len(polygon_vertices))]
    m.plot(px,py,linewidth=0.5,zorder=3,color='black')

ipolygons = range(81,82) # Black/Caspian Seas 
for ipoly in ipolygons:
    r = coasts_paths[ipoly]
    # Convert into lon/lat vertices
    polygon_vertices = [(vertex[0],vertex[1]) for (vertex,code) in
                        r.iter_segments(simplify=False)]
    px = [polygon_vertices[i][0] for i in range(len(polygon_vertices))]
    py = [polygon_vertices[i][1] for i in range(len(polygon_vertices))]
    m.plot(px,py,linewidth=0.5,zorder=3,color='black')

ipolygons = [147] #Antarctica 
for ipoly in ipolygons:
    r = coasts_paths[ipoly]
    # Convert into lon/lat vertices
    polygon_vertices = [(vertex[0],vertex[1]) for (vertex,code) in
                        r.iter_segments(simplify=False)]
    px = [polygon_vertices[i][0] for i in range(len(polygon_vertices))]
    py = [polygon_vertices[i][1] for i in range(len(polygon_vertices))]
    m.plot(px,py,linewidth=0.5,zorder=3,color='black')

lon, lat = np.meshgrid(lon, lat)
colors = ['oldlace','khaki','lightgoldenrodyellow','tan','peru','burlywood','gold','bisque','navajowhite','wheat','Black']
cmap = mpl.colors.ListedColormap(colors[:-1], "")
cmap.set_under("white")
m.pcolormesh(lon, lat, AR6, latlon=True,cmap=cmap)
plt.clim(1, 11)

plt.plot(IMPROVE_LON_f,IMPROVE_LAT_f,    color='k',marker='.',ms=5,ls='')
plt.plot(EPA_LON_f,EPA_LAT_f,            color='k',marker='.',ms=5,ls='')
plt.plot(EMEP_LON_f,EMEP_LAT_f,          color='k',marker='.',ms=5,ls='')
plt.plot(EMEP2_LON_f,EMEP2_LAT_f,        color='k',marker='.',ms=5,ls='')
plt.plot(EANET_LON_f,EANET_LAT_f,        color='k',marker='.',ms=5,ls='')
plt.plot(EASIA_LON_f,EASIA_LAT_f,        color='k',marker='.',ms=5,ls='')
plt.plot(ASIA_LON_f,ASIA_LAT_f,          color='k',marker='.',ms=5,ls='')
plt.plot(OCEANIA_LON_f,OCEANIA_LAT_f,    color='k',marker='.',ms=5,ls='')
plt.plot(Africa_LON_f,Africa_LAT_f,      color='k',marker='.',ms=5,ls='')
plt.plot(N_America_LON_f,N_America_LAT_f,color='k',marker='.',ms=5,ls='')
plt.plot(SPARTAN_LON_f,SPARTAN_LAT_f,    color='k',marker='.',ms=5,ls='')
plt.savefig('worldmap_25.01.21.png', dpi=300)
plt.show()
