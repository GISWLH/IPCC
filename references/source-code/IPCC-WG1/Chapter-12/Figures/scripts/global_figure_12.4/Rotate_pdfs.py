# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/Rotate_pdfs.ipynb

# %% cell 1
import os, glob


lopdf = glob.glob(os.getwcd()+'/../../figs/global_figure_12.4/*.pdf')
for wpdf in lopdf:
    print wpdf
    if 'rotated90' not in wpdf and '-final.pdf' not in wpdf and 'colorbar' not in wpdf:
        rotated = wpdf.replace('.pdf','-rotated90.pdf')
        finalname = rotated.replace('-rotated90.pdf','-final.pdf')
        cmd = 'pdf90 '+wpdf+' ; mv '+os.path.basename(rotated)+' '+finalname
        print cmd
        os.system(cmd)

# %% cell 2
os.getcwd()
