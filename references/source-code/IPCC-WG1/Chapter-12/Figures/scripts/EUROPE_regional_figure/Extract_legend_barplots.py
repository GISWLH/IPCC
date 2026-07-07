# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/EUROPE_regional_figure/Extract_legend_barplots.ipynb

# %% cell 1
from IPython.display import Image
from PIL import Image as PILImage

def extract_plot(figure_file,trim_figure) :
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((0, 1450, 900,1600))
    im_crop.save(trim_figure, quality=95)

#
figure_file = '/home/jservon/Chapter12_IPCC/figs/Figure_12.5/AFRICA_Q100_boxplot.png'
trim_figure = '/home/jservon/Chapter12_IPCC/figs/Figure_12.9/Legend_boxplot.png'

extract_plot(figure_file, trim_figure)

Image(trim_figure)

# %% cell 2
def extract_plot(figure_file,trim_figure) :
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((700, 60, 3900,2900))
    im_crop.save(trim_figure, quality=95)

#
figure_file = '/home/jservon/Chapter12_IPCC/figs/Fabio_Q100maps_20210309/EUR_Q100_nohatching_divdra.png'
trim_figure = figure_file.replace('.png','_cut.png')
extract_plot(figure_file, trim_figure)
Image(trim_figure)
