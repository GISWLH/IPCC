import Ngl, Nio
import os, numpy
from IPython.display import Image

import sys

baseline = sys.argv[1]
future = sys.argv[2]
horizon = int(sys.argv[3])
rcp = sys.argv[4]
title = sys.argv[5]
label = sys.argv[6]
trim_figure = sys.argv[7]
figformat = sys.argv[8]



#----------------------------------------------------------------------
#  nint returns the nearest integer to a given floating value.
#----------------------------------------------------------------------
def nint(r):
    if (abs(int(r)-r) < 0.5):
        return int(r)
    else:
        if (r >= 0.):
            return int(r)+1
        else:
            return int(r)-1

#----------------------------------------------------------------------
# Create map 
#----------------------------------------------------------------------
def create_map(wks, mpOutlineOn=False):
    #---Map resources
    res            = Ngl.Resources()   # map resources
    res.nglDraw    = False         # don't draw map
    res.nglFrame   = False         # don't advance frame

    res.mpDataBaseVersion = "MediumRes"   # better map outlines

    res.mpLimitMode = "LatLon"
    res.mpProjection = "Robinson"
    #res.mpMaxLatF   = -20           # select subregion
    #res.mpMinLatF   = -62
    #res.mpMinLonF   = -78
    #res.mpMaxLonF   = -25

    res.mpOutlineOn     = mpOutlineOn
    #res.mpOutlineOn     = True
    #res.mpGridAndLimbOn = True
    res.mpGridLineColor = -1
    res.mpFillOn               = True
    res.mpLandFillColor        = "Transparent"
    res.mpOceanFillColor       = "Transparent"
    res.mpInlandWaterFillColor = "Transparent"
    #res.mpGeophysicalLineThicknessF = 2.
    # Remove box around plot
    res.pmTickMarkDisplayMode = "Never"

    # Remove Lon/lat ticks
    res.tmXBOn = False
    res.tmYLOn = False
    res.tmXTOn = False
    res.tmYROn = False


    #res.tiMainString = title
    #res.tiMainFontHeightF = 0.02

    map = Ngl.map(wks,res)    # Draw map.

    return map

#----------------------------------------------------------------------
#  Add the trajectory lines.
#----------------------------------------------------------------------
def color_index(val, inc):
    
    ninc = len(inc) #len(inc)-1 : n ticks => n-1 colors ; + 2 => left and right colors

    if val in inc:
        ind = list(inc).index(val)
    elif val<numpy.array(inc).min():
        ind = -1
    elif val>numpy.array(inc).max():
        ind = len(inc)-1
    else:
        tmp = val - numpy.array(inc)
        if val<0:
            tmp = tmp * -1
        dum = tmp[tmp<0]
        if val<0:
            ind = list(tmp).index(dum[dum.argmax()])
        else:
            ind = list(tmp).index(dum[dum.argmax()]) - 1
    return ind+1

def add_trajectories(wks,map, filename_baseline, filename_future, horizon, inc, colormap):
    #ncfile = Nio.open_file(filename)
   
    mres  = Ngl.Resources()                    # marker resources
    mres.gsMarkerSizeF       = 10.0            # marker size
    mres.gsMarkerIndex       = 16              # circle with an X
    mres.gsMarkerThicknessF  = 1.0             # thicker marker outlines

    sid = []

    #---Open the netCDF file containing the salinity data for the trajectories.
    ncfile_baseline = Nio.open_file(filename_baseline)
    ncfile_future = Nio.open_file(filename_future)

    if horizon==2050:
        decade_index = 4
    if horizon==2100:
        decade_index = 9

    TWL_baseline  = ncfile_baseline.variables["TWL"][:,1]
    TWL_future  = ncfile_future.variables["TWL"][:,1,decade_index]
    lat  = ncfile_baseline.variables["latitude"][:]
    lon  = ncfile_baseline.variables["longitude"][:]

    TWL = TWL_future - TWL_baseline

    #
    if isinstance(colormap, str):
        colors = Ngl.read_colormap_file(colormap)
    else:
        colors = colormap
    ninc = len(inc) #len(inc)-1 : n ticks => n-1 colors ; + 2 => left and right colors
    indcolors = [0]
    for val in numpy.arange(0, len(colors)-1, float(len(colors)-1)/(ninc+1)).tolist()[1:-1]:
        indcolors.append(int(val))
    indcolors.append(len(colors)-1)
    cmap = []
    for ind in indcolors:
        cmap.append(colors[ind])
    #cmap = colors[indcolors]
    cmap = colors
    #print len(cmap), len(inc)

    #for j in numpy.arange(0,len(lat)-1, 10):
    for j in range(len(lat)-1):
        cindex = color_index(TWL[j], inc)
        mres.gsMarkerColor = cmap[cindex]
        sid.append(Ngl.add_polymarker(wks,map,lon[j],lat[j],mres))
        Ngl.add_polymarker(wks,map,lon[j],lat[j],mres)

    return



def add_labelbar(wks,map,inc,colormap):
    gsres = Ngl.Resources()  # Line resources.

    txres = Ngl.Resources()          # For labeling the label bar.
    txres.txFontHeightF = 0.015
    #txres.txJust        = "CenterLeft"       # Left justify
    gid = []
    lid = []
    tid = []
    
    if isinstance(colormap, str):
        colors = Ngl.read_colormap_file(colormap)
    else:
        colors = colormap
    ninc = len(inc) #len(inc)-1 : n ticks => n-1 colors ; + 2 => left and right colors
    indcolors = [0]
    for val in numpy.arange(0, len(colors)-1, float(len(colors)-1)/(ninc+1)).tolist()[1:-1]:
        indcolors.append(int(val))
    indcolors.append(len(colors)-1)
    print 'indcolors'
    print indcolors
    cmap = []
    for ind in indcolors:
        cmap.append(colors[ind])
    #print len(cmap)
    #print ninc
    cmap = colors
    
    yp = 0.2
    height = 0.03
    xp = 0.2
    xpend = 0.8
    width = (xpend - xp) / len(cmap)
    for i in range(0,len(cmap)):
        xbox = [xp,xp+width,xp+width,xp,xp]
        ybox = [yp,yp,yp-height,yp-height,yp]
        gsres.gsFillColor = cmap[i]    # Change fill color.
        if i==0:
            xbox = [xp,xp+width,xp+width,xp]
            ybox = [yp-height/2,yp,yp-height,yp-height/2]
        elif i==len(inc):
            xbox = [xp,xp+width,xp,xp]
            ybox = [yp,yp-height/2,yp-height,yp]
        gid.append(Ngl.polygon_ndc(wks,xbox,ybox,gsres))
        lid.append(Ngl.polyline_ndc(wks,xbox,ybox,gsres))            
        if i<len(inc):
            tid.append(Ngl.text_ndc(wks,str(inc[i]),xp+width, yp-height-0.02,txres))
        xp = xp + width

  
    return
    
    
def plot_esl_change(wks, baseline, future, horizon, inc, colormap, title):
    #
    map = create_map(wks, mpOutlineOn=True)
    wmap_empty = create_map(wks, mpOutlineOn=False)
    
    add_trajectories(wks,
                     wmap_empty,
                     baseline,
                     future,
                     horizon,
                     inc,
                     colormap)
    
    Ngl.overlay(map, wmap_empty)

    Ngl.draw(map)
    Ngl.draw(wmap_empty)

    add_labelbar(wks, map, inc, colormap)

    # Set up some text resources.
    txres                       = Ngl.Resources()  
    txres.txFontHeightF         = 0.03

    # Draw a text string labeling the marker
    Ngl.text_ndc(wks,"Change in extreme total water level",0.5,0.78,txres)

    tmainxres                       = Ngl.Resources()  
    tmainxres.txFontHeightF         = 0.032
    tmainxres.txFont         = 22
    Ngl.text_ndc(wks,title,0.5,0.83,tmainxres)

    Ngl.frame(wks)

    Ngl.end()
    
    del(wks)
    del(map)
#


# -- Do the plot
# -----------------------------------------------
colormap = "WhViBlGrYeOrRe"
colormap = "nice_gfdl"

slev_seq_disc21_raw = [
[254., 254., 254.],
[250., 250., 235.],
[244., 244., 214.],
[232., 234., 191.],
[212., 218., 167.],
[187., 199., 148.],
[165., 182., 137.],
[147., 168., 135.],
[132., 158., 137.],
[119., 149., 141.],
[107., 141., 146.],
[95.,  133., 151.],
[83.,  125., 155.],
[71.,  115., 157.],
[58.,  103., 155.],
[46.,  89.,  149.],
[35.,  74.,  139.],
[24.,  57.,  126.],
[15.,  41.,  110.],
[5.,   24.,  92.],
[0.,   5.,   74.]]

test = []
for elt in slev_seq_disc21_raw:
    tmp = []
    for eelt in elt:
        tmp.append(eelt/256.)
    tmp.append(1.)
    test.append(tmp)
slev_seq_disc21 = numpy.array(test)

colormap = slev_seq_disc21
#colormap = "cmocean_deep"

# -- Original
test_raw = [
[127., 68., 170.],
[48., 79., 191.],
[54., 156., 232.],
[36., 147., 126.],
[236., 209., 81.],
[237., 128., 55.],
[204., 64., 74.]]

# -- Inverse light blue and dark blue
test_raw = [
[127., 68., 170.],
[54., 156., 232.],
[48., 79., 191.],
[36., 147., 126.],
[236., 209., 81.],
[237., 128., 55.],
[204., 64., 74.]]
test = []
for elt in test_raw:
    tmp = []
    for eelt in elt:
        tmp.append(eelt/256.)
    tmp.append(1.)
    test.append(tmp)
test_disc7 = numpy.array(test)
colormap = test_disc7


inc = [0, 0.2, 0.4, 0.6, 0.8, 1]

outfilename = 'ESL_'+str(horizon)+'_'+rcp

if figformat=='png':
    wks = Ngl.open_wks("png",outfilename)
    plot_esl_change(wks, baseline, future, horizon, inc, colormap, title)


    # -- Trim the figure and extract the colorbar
    # -----------------------------------------------
    from PIL import Image as PILImage

    def extract_labelbar(figure_file,labelbar_file) :
        im = PILImage.open(figure_file)
        im_crop = im.crop((190, 810, 820, 885))
        im_crop.save(labelbar_file, quality=95)

    def extract_plot(figure_file,trim_figure) :
        im = PILImage.open(figure_file)
        im_crop = im.crop((20, 152, 1010, 763))
        im_crop.save(trim_figure, quality=95)


    outfilename = 'ESL_'+str(horizon)+'_'+rcp+'.png'

    # -- color bar file
    variable = 'ESL'
    colorbar_file = '/home/jservon/Chapter12_IPCC/figs/global_figure_12.4/'+variable+'_colorbar.png'
    # -- Extract the colorbar
    extract_labelbar(outfilename,colorbar_file)
    extract_plot(outfilename,trim_figure)

if figformat=='pdf':
    wks = Ngl.open_wks("pdf",outfilename)
    plot_esl_change(wks, baseline, future, horizon, inc, colormap, title)

    outfilename = 'ESL_'+str(horizon)+'_'+rcp+'.pdf'
    cmd = 'pdfcrop '+outfilename+' '+trim_figure
    os.system(cmd)
    
