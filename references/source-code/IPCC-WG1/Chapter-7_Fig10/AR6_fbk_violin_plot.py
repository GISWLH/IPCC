# Code to generate the CMIP5, CMIP6, and AR6 assessed feedback "violin plot"
import matplotlib.pyplot as plt
import numpy as np
import json

# IPCC COLORBAR
# https://github.com/IPCC-WG1/colormaps/blob/master/categorical_colors_rgb_0-255/rcp_cat.txt
red = (153/255, 0/255, 2/255)
orange = (196/255, 121/255, 0/255)
lt_blue = (112/255, 160/255, 205/255)

def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))

names4=['NET_fbk','PL_fbk','WVLR_fbk','ALB_fbk','CLD_fbk','resid_fbk']

##################################################################################
# AR6 expert-assessed values provided by Masa on 1/27/21:
Masa_names =      ['Net',       'Planck',   'WV+LR','Albedo','Cloud','Other']
AR6 =    np.array([-1.16081,    -3.22,      1.30,    0.35,    0.42,  -0.01081]) 
AR6p5 =  np.array([-1.81313204, -3.39,      1.13,    0.18,   -0.10,  -0.27159185]) 
AR6p95 = np.array([-0.50848796, -3.05,      1.47,    0.52,    0.94,   0.24997185])  
AR6p17 = np.array([-1.539513677,-3.32,      1.20,    0.25,    0.12,  -0.16411])  
AR6p83 = np.array([-0.782106323,-3.12,      1.40,    0.45,    0.72,   0.14248]) 
##################################################################################


##################################################################################
# load in json containing all model's feedbacks (already averaged across 6 kernels)
f = open('cmip56_feedbacks_AR6.json','r')
cmip_fbks = json.load(f)
f.close()
##################################################################################


fig, axes = plt.subplots(figsize=(10, 5))
axes.axhline(y=0,color='k',zorder=0)
dx=2

# First plot the AR6 values:
positions=np.arange(0.5,12.5,dx) - 0.025
positions[-1]=11 # move the last one over a tad to the right
EDGE='k'
FACE=red
X=np.ma.zeros((10000,6))
for i,name in enumerate(Masa_names):
    mean = AR6[i]
    p5,p17,p83,p95 = AR6p5[i],AR6p17[i],AR6p83[i],AR6p95[i]
    CI90 = p95-p5
    # 90% confidence interval corresponds to +/- 1.64485 times the standard deviation 
    std = CI90/2/1.64485
    print('Inferred AR6 '+name+' standard deviation = '+str(np.round(std,2)))
    this = sorted(np.random.normal(mean, std, 10000))
    # Clip the tails
    p2p5,p97p5 = np.percentile(this,[2.5,97.5])
    X[:,i] = np.ma.masked_outside(this, p2p5,p97p5)

parts = plt.violinplot(X, positions = positions, showmeans=False, showmedians=False,showextrema=False)
for pc in parts['bodies']:
    pc.set_facecolor(FACE)
    pc.set_edgecolor(EDGE)
    pc.set_alpha(1)
pc.set_label('AR6')

inds = positions
plt.scatter(inds, AR6, marker='_', color='white', s=16, zorder=3)
plt.vlines(inds, AR6p17, AR6p83, color=EDGE, linestyle='-', lw=5)
plt.vlines(inds, AR6p5, AR6p95, color=EDGE, linestyle='-', lw=1)

# Now plot the CMIP5/6 values:
for gen in ['5','6']:   
    N = len(cmip_fbks['cmip'+gen]['models'])
    X=np.zeros((N,6))
    for n,name in enumerate(names4):
        X[:,n] = cmip_fbks['cmip'+gen][name]

    LABEL='CMIP'+gen
    if gen=='5':
        positions=np.arange(1,13,dx)
        EDGE='k'
        FACE=lt_blue
    else:
        positions=np.arange(1.5,13.5,dx) + 0.025
        EDGE='k'
        FACE=orange

    p5,p17,p83,p95 = np.percentile(X[:,:-1],[5,17,83,95],axis=0)
    means = np.ma.average(X[:,:-1],axis=0)
    inds = positions[:-1]
    parts = plt.violinplot(X[:,:-1], positions = inds, showmeans=False, showmedians=False,showextrema=False)
    for pc in parts['bodies']:
        #pc.set_label(LABEL)
        pc.set_facecolor(FACE)
        pc.set_edgecolor(EDGE)
        pc.set_alpha(1)
    pc.set_label('CMIP'+gen)
    
    plt.scatter(inds, means, marker='_', color='white', s=16, zorder=3)
    axes.vlines(inds, p17, p83, color=EDGE, linestyle='-', lw=5)
    axes.vlines(inds, p5, p95, color=EDGE, linestyle='-', lw=1)
    legend_without_duplicate_labels(axes)

plt.yticks(np.arange(-3.5,3.5,0.5),np.arange(-3.5,3.5,0.5),fontsize=14)
plt.text(1,-0.3,'Net',fontsize=12,ha='center',va='center')
plt.text(3,-2.8,'Planck',fontsize=12,ha='center',va='center')
plt.text(5, 1.65,'Water Vapour + Lapse Rate',fontsize=12,ha='center',va='center')
plt.text(7, 0.75,'Surface Albedo',fontsize=12,ha='center',va='center')
plt.text(9, 1.35,'Cloud',fontsize=12,ha='center',va='center')
plt.text(11.,0.9,'Biogeophysical\nand non-CO$_2$\nBiogeochemical',fontsize=12,ha='center',va='center')
plt.tick_params(bottom=False,labelbottom=False) 
axes.set_title('Assessment of Climate Feedbacks',fontsize=16)
axes.set_ylabel('Climate Feedback (W m$^{-2}$ $^{\circ}$C$^{-1}$)',fontsize=14)
axes.yaxis.grid(True,color='k',ls=':',lw=0.5,alpha=0.5)
axes.set_axisbelow(True) # set the grid lines behind the data
plt.ylim(-3.5,2.0)
plt.xlim(1.0-1.25,11.0+1.25)
plt.legend(fancybox=False, handletextpad=0.4,framealpha=0,loc='upper right', bbox_to_anchor=(1,0.1),ncol=3,fontsize=12) 
plt.savefig('/work/zelinka1/figures/CMIP6/feedbacks/abrupt-4xCO2/fbk_estimates_AR6_SOD_violin.pdf',bbox_inches='tight')
plt.savefig('/work/zelinka1/figures/CMIP6/feedbacks/abrupt-4xCO2/fbk_estimates_AR6_SOD_violin.eps',bbox_inches='tight')
plt.savefig('/work/zelinka1/figures/CMIP6/feedbacks/abrupt-4xCO2/fbk_estimates_AR6_SOD_violin.jpg',bbox_inches='tight')
