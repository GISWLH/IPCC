import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

c1 = "#000000"
c2 = "#5492CD"
c3 = "#C47900"

regkey = "tropics"; regfilein = "tropic"; extra = ""; titleletter = "e) "; ylo = -10; yup = 50
# regkey = "extra"; regfilein = "extra"; extra = "extra"; titleletter = "f) "; ylo = -5; yup = 65

with open('Hydro_vars_change_20210201_derived_'+regfilein+'.json') as f:
  stat = json.load(f)

nGWLs = len(stat["pr"]["mean"][regkey+"_annual"]["nq83"].keys())

keys = stat["pr"]["mean"][regkey+"_annual"]["nq83"].keys()

GWL = np.empty((nGWLs),np.float)
for key, value in enumerate(keys) :
    GWL[key] = value
GWL = np.sort(GWL)
GWLstr = []
for i in range(nGWLs):
    GWLstr.append(str(GWL[i]))
    
# print(GWLstr)
xticks = [2,6,10,14]
GWLticks = []
for i in range(len(xticks)):
    GWLticks.append(GWLstr[xticks[i]])

pr_mean_mean = np.empty((nGWLs),np.float)
pr_std_mean = np.empty((nGWLs),np.float)
mrro_mean_mean = np.empty((nGWLs),np.float)
mrro_std_mean = np.empty((nGWLs),np.float)
prw_mean_mean = np.empty((nGWLs),np.float)

pr_mean_n95 = np.empty((nGWLs),np.float)
pr_std_n95 = np.empty((nGWLs),np.float)
mrro_mean_n95 = np.empty((nGWLs),np.float)
mrro_std_n95 = np.empty((nGWLs),np.float)
prw_mean_n95 = np.empty((nGWLs),np.float)

pr_mean_n83 = np.empty((nGWLs),np.float)
pr_std_n83 = np.empty((nGWLs),np.float)
mrro_mean_n83 = np.empty((nGWLs),np.float)
mrro_std_n83 = np.empty((nGWLs),np.float)
prw_mean_n83 = np.empty((nGWLs),np.float)

pr_mean_n17 = np.empty((nGWLs),np.float)
pr_std_n17 = np.empty((nGWLs),np.float)
mrro_mean_n17 = np.empty((nGWLs),np.float)
mrro_std_n17 = np.empty((nGWLs),np.float)
prw_mean_n17 = np.empty((nGWLs),np.float)

pr_mean_n5 = np.empty((nGWLs),np.float)
pr_std_n5 = np.empty((nGWLs),np.float)
mrro_mean_n5 = np.empty((nGWLs),np.float)
mrro_std_n5 = np.empty((nGWLs),np.float)
prw_mean_n5 = np.empty((nGWLs),np.float)

for i in range(nGWLs):
    pr_mean_mean[i] = stat["pr"]["mean"][regkey+"_annual"]["mean"][str(GWL[i])]
    pr_std_mean[i] = stat["pr"]["std"][regkey+"_annual"]["mean"][str(GWL[i])]
    mrro_mean_mean[i] = stat["mrro"]["mean"][regkey+"_annual"]["mean"][str(GWL[i])]
    mrro_std_mean[i] = stat["mrro"]["std"][regkey+"_annual"]["mean"][str(GWL[i])]
    prw_mean_mean[i] = stat["prw"]["mean"][regkey+"_annual"]["mean"][str(GWL[i])]

    pr_mean_n95[i] = stat["pr"]["mean"][regkey+"_annual"]["nq95"][str(GWL[i])]
    pr_std_n95[i] = stat["pr"]["std"][regkey+"_annual"]["nq95"][str(GWL[i])]
    mrro_mean_n95[i] = stat["mrro"]["mean"][regkey+"_annual"]["nq95"][str(GWL[i])]
    mrro_std_n95[i] = stat["mrro"]["std"][regkey+"_annual"]["nq95"][str(GWL[i])]
    prw_mean_n95[i] = stat["prw"]["mean"][regkey+"_annual"]["nq95"][str(GWL[i])]

    pr_mean_n83[i] = stat["pr"]["mean"][regkey+"_annual"]["nq83"][str(GWL[i])]
    pr_std_n83[i] = stat["pr"]["std"][regkey+"_annual"]["nq83"][str(GWL[i])]
    mrro_mean_n83[i] = stat["mrro"]["mean"][regkey+"_annual"]["nq83"][str(GWL[i])]
    mrro_std_n83[i] = stat["mrro"]["std"][regkey+"_annual"]["nq83"][str(GWL[i])]
    prw_mean_n83[i] = stat["prw"]["mean"][regkey+"_annual"]["nq83"][str(GWL[i])]

    pr_mean_n17[i] = stat["pr"]["mean"][regkey+"_annual"]["nq17"][str(GWL[i])]
    pr_std_n17[i] = stat["pr"]["std"][regkey+"_annual"]["nq17"][str(GWL[i])]
    mrro_mean_n17[i] = stat["mrro"]["mean"][regkey+"_annual"]["nq17"][str(GWL[i])]
    mrro_std_n17[i] = stat["mrro"]["std"][regkey+"_annual"]["nq17"][str(GWL[i])]
    prw_mean_n17[i] = stat["prw"]["mean"][regkey+"_annual"]["nq17"][str(GWL[i])]

    pr_mean_n5[i] = stat["pr"]["mean"][regkey+"_annual"]["nq5"][str(GWL[i])]
    pr_std_n5[i] = stat["pr"]["std"][regkey+"_annual"]["nq5"][str(GWL[i])]
    mrro_mean_n5[i] = stat["mrro"]["mean"][regkey+"_annual"]["nq5"][str(GWL[i])]
    mrro_std_n5[i] = stat["mrro"]["std"][regkey+"_annual"]["nq5"][str(GWL[i])]
    prw_mean_n5[i] = stat["prw"]["mean"][regkey+"_annual"]["nq5"][str(GWL[i])]

prw_mean_5K_n83 = stat["prw"]["mean"][regkey+"_annual"]["nq83"][str(GWL[-1])]
prw_mean_5K_n17 = stat["prw"]["mean"][regkey+"_annual"]["nq17"][str(GWL[-1])]
pr_mean_5K_n83 = stat["pr"]["mean"][regkey+"_annual"]["nq83"][str(GWL[-1])]
pr_mean_5K_n17 = stat["pr"]["mean"][regkey+"_annual"]["nq17"][str(GWL[-1])]
mrro_mean_5K_n83 = stat["mrro"]["mean"][regkey+"_annual"]["nq83"][str(GWL[-1])]
mrro_mean_5K_n17 = stat["mrro"]["mean"][regkey+"_annual"]["nq17"][str(GWL[-1])]  
pr_std_5K_n83 = stat["pr"]["std"][regkey+"_annual"]["nq83"][str(GWL[-1])]
pr_std_5K_n17 = stat["pr"]["std"][regkey+"_annual"]["nq17"][str(GWL[-1])]
mrro_std_5K_n83 = stat["mrro"]["std"][regkey+"_annual"]["nq83"][str(GWL[-1])]
mrro_std_5K_n17 = stat["mrro"]["std"][regkey+"_annual"]["nq17"][str(GWL[-1])]

sellevs = [0, 2, 10]
print('q5, q17, mean, q83, q95')
for i,lev in enumerate(sellevs):
   print()
   print('level : {}°C'.format(GWL[lev]))
   print('pr_mean :',pr_mean_n5[lev], pr_mean_n17[lev], pr_mean_mean[lev], pr_mean_n83[lev], pr_mean_n95[lev])
   print('pr_std :',pr_std_n5[lev], pr_std_n17[lev], pr_std_mean[lev], pr_std_n83[lev], pr_std_n95[lev])
   print('mrro_mean :',mrro_mean_n5[lev], mrro_mean_n17[lev], mrro_mean_mean[lev], mrro_mean_n83[lev], mrro_mean_n95[lev])
   print('mrro_std :',mrro_std_n5[lev], mrro_std_n17[lev], mrro_std_mean[lev], mrro_std_n83[lev], mrro_std_n95[lev])
 
fig, ax = plt.subplots()

ax.plot(prw_mean_mean, color=c1, marker="o",
        linestyle="-",
        label="Precipitable water annual mean")
ax.plot(pr_mean_mean, color=c2, marker="o",
        linestyle="-",
        label="Precipitation annual mean")
ax.plot(mrro_mean_mean, color=c3, marker="o",
        linestyle="-",
        label="Runoff annual mean")

ax.plot(pr_std_mean, color=c2, marker="o",
        linestyle="--",
        label="Precipitation interannual variability")
ax.plot(mrro_std_mean, color=c3, marker="o",
        linestyle="--",
        label="Runoff interannual variability")

x = nGWLs
ax.scatter([x],[prw_mean_mean[-1]], marker='o', c=c1)
ax.plot([x,x],[prw_mean_5K_n17, prw_mean_5K_n83],
                linestyle="-", c=c1)
x = nGWLs+.5
ax.scatter([x],[pr_mean_mean[-1]], marker='o', c=c2)
ax.plot([x,x],[pr_mean_5K_n17, pr_mean_5K_n83],
                linestyle="-", c=c2)
x = nGWLs+1
ax.scatter([x],[mrro_mean_mean[-1]], marker='o', c=c3)
ax.plot([x,x],[mrro_mean_5K_n17, mrro_mean_5K_n83],
                linestyle="-", c=c3)
x = nGWLs+1.5
ax.scatter([x],[pr_std_mean[-1]], marker='o', c=c2)
ax.plot([x,x],[pr_std_5K_n17, pr_std_5K_n83],
                linestyle="--", c=c2)
x = nGWLs+2
ax.scatter([x],[mrro_std_mean[-1]], marker='o', c=c3)
ax.plot([x,x],[mrro_std_5K_n17, mrro_std_5K_n83],
                linestyle="--", c=c3)

ax.legend()

ax.set_xticks(xticks)
ax.set_xticklabels(GWLticks)
ax.set_ylabel('% change - 15 models mean - ssp5-85')
ax.set_xlabel('Global surface temperature change since 1850-1900 (°C)')
ax.set_title(titleletter+'Hydrological change over '+extra+'tropical land')
ax.xaxis.set_minor_locator(MultipleLocator(2))
ax.set_ylim(ylo,yup)

if (regkey == "tropics"):
    xl1 = nGWLs+1.25; xl2 = nGWLs+.25; yl1 = -3; yl2 = -9
else:
    xl1 = nGWLs+1.25; xl2 = nGWLs+.25; yl1 = 5; yl2 = -1

ax.errorbar(xl1, yl1, xerr=1.5, capsize=5, capthick=1, c=c1)
ax.text(xl2, yl2,"17-83%\nrange")

# plt.show()

plt.savefig("WaterCycle_"+extra+"tropics.png")
plt.savefig("WaterCycle_"+extra+"tropics.pdf")
