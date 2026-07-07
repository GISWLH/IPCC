# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/CID/.ipynb_checkpoints/CID_AR6regions_AFRICA-checkpoint.ipynb

# %% cell 1
import os
from IPython.display import Image

# %% cell 3
region_name = 'OCEANIA'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 5
region_name = 'AFRICA'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions_AFRICA.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 7
region_name = 'SOUTH-AMERICA'

# Missing SCA
outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 9
region_name = 'ASIA'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 11
region_name = 'NORTH-AMERICA'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 13
region_name = 'EUROPE'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 15
region_name = 'NH_POLAR'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 16
region_name = 'SH_POLAR'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 18
region_name = 'OCEANS'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 20
region_name = 'Global_land'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 24
region_name = 'Pacific???'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 25
region_name = 'Caribbean'

outfilename = region_name+'_AR6_regions_CDI'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/CID/'+outfilename+'.png'

cmd = 'python /home/jservon/Chapter12_IPCC/scripts/CID/CID_AR6regions.py '+region_name
os.system(cmd)
Image(trim_figure)

# %% cell 27
from PIL import Image as PILImage
def extract_plot(figure_file,trim_figure) :
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((200, 350, 820, 666))
    im_crop.save(trim_figure, quality=95)
extract_plot(trim_figure,'test.png')
Image('test.png')
