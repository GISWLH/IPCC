import Ngl, Nio
import os, numpy, csv, json
from IPython.display import Image
from shapely.geometry import Polygon, Point
import geopandas
import sys

region_name = sys.argv[1]

# -- Create empty map over region
# --    test with and without gray fill over continent
#----------------------------------------------------------------------
# Create map of southern tip of South America
#----------------------------------------------------------------------
def create_map(wks, region_dict, mpOutlineOn=True):
    #---Map resources
    res            = Ngl.Resources()   # map resources
    res.nglDraw    = False         # don't draw map
    res.nglFrame   = False         # don't advance frame
    res.nglMaximize = False
    res.mpDataBaseVersion = "MediumRes"   # better map outlines
    #res.mpCenterLonF = 145
    #res.mpCenterLatF = 0

    #res.mpLimitMode = "MaximalArea"
    if 'Robinson' in region_dict:
        res.mpProjection = "Robinson"
        #res.mpEllipticalBoundary  = True
    else:
        res.mpLimitMode = "LatLon"
        #res.mpCenterLonF = 145
        res.mpMaxLatF   = region_dict['latmax']           # select subregion
        res.mpMinLatF   = region_dict['latmin']
        res.mpMinLonF   = region_dict['lonmin']
        res.mpMaxLonF   = region_dict['lonmax']
        
    if 'Orthographic_NAM' in region_dict:
        #-#res.mpProjection = "Satellite"
        #-#res.mpCenterLatF = 80.
        #-#res.mpCenterLonF = -70.
        res.mpProjection = "Orthographic"
        #res.mpSatelliteDistF = 0.5
        res.mpEllipticalBoundary  = True
        res.mpCenterLatF = 40.
        res.mpCenterLonF = -100.
    if 'NH_stereographic' in region_dict:
        #-#res.mpProjection = "Satellite"
        #-#res.mpCenterLatF = 80.
        #-#res.mpCenterLonF = -70.
        res.mpProjection = "Orthographic"
        res.mpEllipticalBoundary  = True
        res.mpCenterLatF = 80.
        res.mpCenterLonF = -70.
    if 'SH_stereographic' in region_dict:
        #res.mpProjection = "Satellite"
        res.mpProjection = "Orthographic"
        res.mpEllipticalBoundary  = True
        #res.mpCenterLatF = 90.
        res.mpCenterLatF = -90.
        res.mpCenterLonF = 0.
        #res.mpProjection = "Stereographic"
        #res.mpEllipticalBoundary  = True

    res.mpOutlineOn     = mpOutlineOn
    res.mpGridAndLimbOn = True
    res.mpGridLineColor = -1
    res.mpFillOn               = mpOutlineOn
    res.mpLandFillColor        = "grey"
    res.mpOceanFillColor       = "white"
    res.mpInlandWaterFillColor = "white"
    # Remove box around plot
    #res.pmTickMarkDisplayMode = "Never"

    # Remove Lon/lat ticks
    res.tmXBOn = False
    res.tmYLOn = False
    res.tmXTOn = False
    res.tmYROn = False


    res.tiMainString = ' '
    #res.tiMainFontHeightF = 0.02

    map = Ngl.map(wks,res)    # Draw map.

    return map




# -- Je lis les AR6 regions et garde uniquement celles de la region_name
# --   - pour la selection des points: subregions_polygons
# --   - pour le plot des polygons : lons_array / lats_array
# -- add_trajectories:
# --   - je lis le fichier
# --   - je verifie si le point est dans une des subregions
# --   - si oui, je rajoute au plot

#
def retrieve_AR6regions_for_region(region_name, list_of_regions=None):

    regions_filename='/home/jservon/Chapter12_IPCC/scripts/ATLAS/reference-regions/IPCC-WGI-reference-regions-v4_coordinates.csv'

    # -- Store the informations by region in the 'regions' dictionary
    regions = dict()
    with open(regions_filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
        for row in spamreader:
            if list_of_regions:
                if row[3] in list_of_regions:
                    region_dict = dict()
                    lats_vect = []
                    lons_vect = []
                    tmp_polygon_vertices = []
                    for vertice in row[4:-1]:
                        if vertice:
                            dum = vertice.split('|')
                            lons_vect.append(float(dum[0]))
                            lats_vect.append(float(dum[1]))
                            tmp_polygon_vertices.append( (float(dum[0]), float(dum[1])) )
                    region_dict['polygon'] = Polygon(tmp_polygon_vertices)
                    region_dict['lons_vect'] = lons_vect
                    region_dict['lats_vect'] = lats_vect
                    #
                    regions[row[3]] = region_dict
            else:
                if region_name in ['NORTH-AMERICA','SOUTH-AMERICA']:
                    if row[0] in [region_name, 'CENTRAL-AMERICA'] :
                        region_dict = dict()
                        lats_vect = []
                        lons_vect = []
                        tmp_polygon_vertices = []
                        for vertice in row[4:-1]:
                            if vertice:
                                dum = vertice.split('|')
                                lons_vect.append(float(dum[0]))
                                lats_vect.append(float(dum[1]))
                                tmp_polygon_vertices.append( (float(dum[0]), float(dum[1])) )
                        region_dict['polygon'] = Polygon(tmp_polygon_vertices)
                        region_dict['lons_vect'] = lons_vect
                        region_dict['lats_vect'] = lats_vect
                        #
                        regions[row[3]] = region_dict
                elif region_name=='OCEANS':
                    if row[1]=='Ocean':
                        region_dict = dict()
                        lats_vect = []
                        lons_vect = []
                        tmp_polygon_vertices = []
                        for vertice in row[4:-1]:
                            if vertice:
                                dum = vertice.split('|')
                                lons_vect.append(float(dum[0]))
                                lats_vect.append(float(dum[1]))
                                tmp_polygon_vertices.append( (float(dum[0]), float(dum[1])) )
                        region_dict['polygon'] = Polygon(tmp_polygon_vertices)
                        region_dict['lons_vect'] = lons_vect
                        region_dict['lats_vect'] = lats_vect
                        #
                        regions[row[3]] = region_dict
                else:
                    if region_name in row[0]:
                        region_dict = dict()
                        lats_vect = []
                        lons_vect = []
                        tmp_polygon_vertices = []
                        for vertice in row[4:-1]:
                            if vertice:
                                dum = vertice.split('|')
                                lons_vect.append(float(dum[0]))
                                lats_vect.append(float(dum[1]))
                                tmp_polygon_vertices.append( (float(dum[0]), float(dum[1])) )
                        region_dict['polygon'] = Polygon(tmp_polygon_vertices)
                        region_dict['lons_vect'] = lons_vect
                        region_dict['lats_vect'] = lats_vect
                        #
                        regions[row[3]] = region_dict
    #
    return regions



def add_AR6regions(wks, base_map, regions, text_size, adjp = dict(), exclude_regions = []):
    #
    txres                       = Ngl.Resources()  
    txres.txFontHeightF         = text_size
    txres.txFont                = 22
    
    gsres                   = Ngl.Resources()
    # Polyline resources.
    gsres.gsLineColor       = "Black"
    gsres.gsLineThicknessF  = 4.0      # thrice thickness
    
    
    for subregion in regions:
        if subregion not in exclude_regions:
            #if regions[subregion]['region']==region_name:
            lons_vect = regions[subregion]['lons_vect']
            lats_vect = regions[subregion]['lats_vect']
            # Draw a text string labeling the marker
            lonp = numpy.mean(lons_vect)
            latp = numpy.mean(lats_vect)
            #print subregion, lonp, latp
            if subregion in adjp:
                lonp += adjp[subregion]['lon']
                latp += adjp[subregion]['lat']
            Ngl.add_text(wks,base_map, subregion, lonp, latp, txres)

            # -- Close the polygon
            lons_vect.append(lons_vect[0])
            lats_vect.append(lats_vect[0])
            poly1 = Ngl.add_polyline(wks,base_map,lons_vect,lats_vect,gsres)

    return





#
# -- Plot parameters
# -----------------------------------------------
text_size = 0.025
    
plot_dict = {
    
    'AFRICA': dict(
        lonmin = -25,
        lonmax = 60,
        latmin = -40,
        latmax = 47,
        text_size = text_size,
        adjp = dict(
            WSAF = dict(lon=-3, lat=7),
            ESAF = dict(lon=3, lat=7),
            SEAF = dict(lon=2, lat=0),
            NEAF = dict(lon=-3.5, lat=-2),
            MDG = dict(lon=0, lat=-4),
            #MED = dict(lat=-5, lon=-15),
        ),
        trim = (211, 200, 815, 820)
        
    ),
    
    'OCEANIA': dict(
        lonmin = -255,
        lonmax = -175,
        latmin = -57,
        latmax = 0,
        text_size = text_size + 0.005,
        adjp = dict(
            CAU = dict(lon=0, lat=1.5),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        trim = (200, 270, 820, 745)
    ),
    
    'SOUTH-AMERICA': dict(
        lonmin = -109,
        lonmax = -30,
        latmin = -60,
        latmax = 27,
        text_size = text_size + 0.005,
        adjp = dict(
            CAU = dict(lon=0, lat=1.5),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = ['NCA','CNA','ENA','CAR'],
        trim = (225, 200, 792, 820)
    ),

    'NORTH-AMERICA': dict(
        lonmin = -175,
        lonmax = -40,
        latmin = 0,
        latmax = 90,
        #Orthographic_NAM = True,
        text_size = text_size + 0.005,
        adjp = dict(
            WNA = dict(lon=-5, lat=0),
            EAU = dict(lon=0, lat=1),
            ENA = dict(lon=0, lat=5),
        ),
        exclude_regions = ['SCA','CAR'],
        trim = (204, 300, 820, 720)
    ),
    
    'ASIA': dict(
        lonmin = 30, #20
        lonmax = 180,
        #lonmin = -250, #20
        #lonmax = -160,
        latmin = -15, #-20
        latmax = 75, #80
        text_size = text_size,
        adjp = dict(
            CAU = dict(lon=0, lat=1.5),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        trim = (204, 320, 820, 705)
    ),
    'EUROPE': dict(
        lonmin = -15, #20
        lonmax = 65,
        #lonmin = -250, #20
        #lonmax = -160,
        latmin = 25, #-20
        latmax = 75, #80
        text_size = text_size+0.01,
        adjp = dict(
            CAU = dict(lon=0, lat=1.5),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        trim = (204, 310, 820, 705)
    ),
    'NH_POLAR': dict(
        NH_stereographic = True,
        #"Orthographic"
        lonmin = 0, #20
        lonmax = 360,
        #lonmin = -250, #20
        #lonmax = -160,
        latmin = 40., #-20
        latmax = 90., #80
        text_size = text_size + 0.015,
        adjp = dict(
            CAU = dict(lon=0, lat=1.5),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        list_of_regions = ['RAR','NWN','NEN','NEU','GIC'],
        trim = (200, 200, 820, 815)
    ),
    'SH_POLAR': dict(
        SH_stereographic = True,
        lonmin = 0, #20
        lonmax = 360,
        latmin = -50., #-20
        latmax = -90., #80
        text_size = text_size + 0.015,
        adjp = dict(
            EAN = dict(lon=120, lat=0),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        list_of_regions = ['EAN','WAN'],
        trim = (200, 200, 820, 820)
    ),
    'OCEANS': dict(
        lonmin = 0, #20
        lonmax = 360,
        latmin = -90., #-20
        latmax = 90., #80
        text_size = text_size,
        adjp = {
            'SAO' : dict(lon=10, lat=0),
            'ARO' : dict(lon=50, lat=2),
            'ARS' : dict(lon=-20, lat=3),
            'BOB' : dict(lon=10, lat=10),
            'NPO*': dict(lon=0, lat=-10),
            'NPO': dict(lon=0, lat=-10),
            'SPO': dict(lon=-8, lat=0),
            'SOO' : dict(lon=20, lat=7),
        },
        exclude_regions = [],
        #list_of_regions = ['EAN','WAN'],
        trim = (200, 350, 820, 666)
    ),
    'Caribbean': dict(
        lonmin = -92, #20
        lonmax = -53,
        latmin = 5., #-20
        latmax = 30., #80
        text_size = text_size,
        adjp = dict(
            EAN = dict(lon=120, lat=0),
            EAU = dict(lon=0, lat=1),
        ),
        exclude_regions = [],
        list_of_regions = ['CAR'],
        trim = None#(204, 310, 820, 705)
    ),
    'Global_land': dict(
        lonmin = -180, #20
        lonmax = 180,
        latmin = -90, #-20
        latmax = 90., #80
        Robinson=True,
        text_size = text_size-0.016,
        adjp = dict(
            #WNA = dict(lon=-5, lat=0),
            ENA = dict(lon=0, lat=5),
            NWS = dict(lon=-5, lat=0),
            SWS = dict(lon=-5, lat=0),
            WSAF = dict(lon=-3, lat=5),
            ESAF = dict(lon=4, lat=5),
            MDG = dict(lon=4, lat=-3),
        ),
        exclude_regions = [],
        list_of_regions = ['NAU','CAU','EAU','SAU','NZ','SEA','ARP','SAS','WCA',
                           'TIB','ECA','EAS','NSA','SCA','CAR','NWS','NSA','SAM',
                           'NES','SWS','SES','SSA','NWN','NEN','WNA','CNA','ENA',
                           'NCA','MED','WCE','NEU','WAF','SAH','CAF','WSAF','ESAF',
                           'MDG','SEAF','NEAF','ARP', 'EEU', 'RAR', 'WSB','ESB','RFE'],

        trim = (200, 350, 820, 670)
    ),




    
    
}


    
# -- Do the plot
# -----------------------------------------------
region_dict = plot_dict[region_name]
adjp = region_dict['adjp']



outfilename = region_name+'_AR6_regions_CDI'


# -- Start the ngl plot here
# -----------------------------------------------
wks = Ngl.open_wks("png",outfilename)
wmap = create_map(wks, region_dict)

# -- Extract the subregions of the region
if 'list_of_regions' in region_dict:
    regions = retrieve_AR6regions_for_region(region_name, region_dict['list_of_regions'])
else:
    regions = retrieve_AR6regions_for_region(region_name)

# -- Add the AR6 regions
add_AR6regions(wks, wmap, regions, region_dict['text_size'], adjp, exclude_regions = region_dict['exclude_regions'])

Ngl.draw(wmap)


# Set up some text resources.
txres                       = Ngl.Resources()  
txres.txFontHeightF         = 0.035


Ngl.frame(wks)
Ngl.end()

del(wks)
del(wmap)
#

# -- Trim the figure and extract the colorbar
# -----------------------------------------------
from PIL import Image as PILImage
def extract_plot(figure_file,trim_figure, trim) :
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    if trim:
        im_crop = im.crop(trim)
    else:
        im_crop = im
    im_crop.save(trim_figure, quality=95)


# -- color bar file
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'
# -- Extract the colorbar
extract_plot(outfilename+'.png', trim_figure, region_dict['trim'])

print 'uncropped figure: ',outfilename+'.png'
print 'final figuer: ', trim_figure
