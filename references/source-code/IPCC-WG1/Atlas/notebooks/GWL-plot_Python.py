# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/GWL-plot_Python.ipynb

# %% cell 4
import glob
import matplotlib.pyplot as plt
import os.path
import pandas as pd
from matplotlib import cm
from sklearn import linear_model

# %% cell 6
var = 'tas'
mask = 'landsea'
project = 'CMIP6' # CMIP5, CMIP6 or CORDEX
project_gsat = 'CMIP6' # CMIP5 or CMIP6
scenario = 'ssp585' # e.g. ssp585 or rcp45
region = 'MED'
season = 'Annual'
period_hist = slice('1850','1900')

# %% cell 8
basedir = f'../datasets-aggregated-regionally/data/{project}/{project}_{var}_{mask}'
basedir_gsat = f'../datasets-aggregated-regionally/data/{project_gsat}/{project_gsat}_tas_landsea'
longname = dict(pr = 'Precipitation', tas = 'Near surface temperature')
units = dict(pr='%', tas='K')
months = dict(DJF=[1,2,12], MAM=[3,4,5], JJA=[6,7,8], SON=[9,10,11], Annual=range(1,13))

# %% cell 10
def read_files(csvlist):
  '''Concatenates a list of CSV files as a dataframe'''
  csvdata = [pd.read_csv(csv, comment = '#') for csv in csvlist]
  csvdata = pd.concat(csvdata)
  csvdata['date'] = pd.to_datetime(csvdata['date'], format='%Y-%m')
  return(csvdata.set_index('date'))

def get_average(df, period, region = 'world', season = 'Annual'):
  '''Computes the seasonal average for a given region and period'''
  rval = df.loc[period,region]
  return(rval[rval.index.month.isin(months[season])].mean())

def get_run(filepath):
  '''Extracts member identifier from filename'''
  return( filepath.split('_')[-1].split('.')[0] )

def get_model(filepath):
  '''Extracts model name from filename'''
  return( filepath.split('_')[-3].split('.')[0] )

# %% cell 12
def decadal_anomalies(basedir, project, region = 'world', season = 'Annual', relative = False):
  data = pd.DataFrame(columns = ['model', 'run', 'decade', region])
  files_scen = glob.glob(f'{basedir}/{project}_*_{scenario}*.csv')
  for scenfile in files_scen:
    histfile = scenfile.replace(scenario, 'historical')
    if not os.path.exists(histfile):
      print(f'Missing historical file for {scenfile}')
      continue
    member_data = read_files([histfile, scenfile])
    reference_value = get_average(member_data, period_hist, region, season)
    # get decadal anomalies w.r.t. reference
    for decade_start in range(2010,2099,10):
      decade = slice(str(decade_start), str(decade_start+9))
      dfrow = dict(
        model = get_model(scenfile),
        run = get_run(scenfile),
        decade = f'{decade.start}-{decade.stop}'
      )
      dfrow[region] = get_average(member_data, decade, region, season) - reference_value
      if relative:
        dfrow[region] = 100. * dfrow[region] / reference_value
      data = data.append(dfrow, ignore_index=True)
  return(data.set_index(['model', 'run', 'decade']))

ydata = decadal_anomalies(basedir, project, region, season, relative = var=='pr')
xdata = decadal_anomalies(basedir_gsat, project_gsat)
data = pd.concat([xdata, ydata], axis=1, join='inner').dropna()

# %% cell 14
data

# %% cell 16
decades = sorted(list(set(data.index.get_level_values(2))))
colors = cm.get_cmap('viridis_r', len(decades))
fig, ax = plt.subplots(figsize=(4,4))
h = []
for k,decade in enumerate(decades):
  decdata = data.xs(decade, level=2)
  h.append(ax.scatter(x=decdata['world'], y=decdata[region], color=colors(k)))
# Set legend outside the plot
ax.legend(h, decades, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
# Add decadal means
decadal_means = data.groupby('decade').mean()
ax.plot(decadal_means['world'], decadal_means[region], 'or')
# Add linear fit
lm = linear_model.LinearRegression()
X = data['world'].values.reshape(-1, 1)
y = data[region]
model = lm.fit(X, y)
ax.set_xlim(left=0)
#ax.set_xlim(0,8)
#ax.set_ylim(0,16)
ax.text(0.05, 0.92, '$\\beta:$ %.2f %s/K\n$R^2:$ %4.2f' % (model.coef_, units[var], lm.score(X, y)), color='k',
        verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, 
        fontsize=15, fontweight = 'bold', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5})
X[0] = 0
ax.plot(X, model.predict(X), color = 'k', linewidth = 2)
# Grid and labels
ax.set_axisbelow(True)
ax.grid()
ax.axline((1, 1), slope=1, ls="--", c="k")
plt.xlabel(f'{project_gsat} GWL (K)')
plt.ylabel(f'{region} {longname[var]} ({units[var]})')
plt.savefig(f'GWL-plot-{project}_{scenario}_{region}_{var}_{mask}.png', dpi=150, bbox_inches = 'tight', facecolor = 'w')
