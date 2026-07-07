import os
from pathlib import Path

import numpy as np
import pylab as pl
import pandas as pd
import xarray as xr
from matplotlib import cm
from matplotlib.colors import LogNorm
import requests
import matplotlib as mpl

import projmap
import trend_analysis

Path("figs").mkdir(parents=True, exist_ok=True)

def filename(dtm, ver="4.2", datadir=None):
    """Generate OC-CCI filenames based on datetime object"""
    if datadir is None:
        datadir = "ncfiles/OC-CCI"
        Path(datadir).mkdir(parents=True, exist_ok=True)
    dstr = f"{dtm.year}{dtm.month:02}"
    return (f"{datadir}/ESACCI-OC-L3S-CHLOR_A-MERGED-" + 
            f"1M_MONTHLY_4km_GEO_PML_OCx-{dstr}-fv{ver}.nc")

def download(dtm, download_timeout=10):
    """Download OC-CCI monthly netcdf files"""
    local_filename = filename(dtm)
    url = "https://www.oceancolour.org/browser/get.php"
    params = dict(date=f"{dtm.year}-{dtm.month:02}-{dtm.day:02}",
                  product="chlor_a",
                  period="monthly",
                  format="netcdf",
                  mapping="GEO",
                  version="42")
    print(f"downloading {params['date']}")
    try:
        r = requests.get(url, params=params, stream=True, 
                            timeout=download_timeout)
    except requests.ReadTimeout:
        warnings.warn("Connection to server timed out.")
        return False
    if r.ok:
        if local_filename is None:
            return r.text
        else:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
    else:
        requests.RequestException("Could not download file from server")

def load(i1=None,i2=None, j1=None,j2=None, ver="4.2", year1=1998,year2=2018):
    """Load all monthly netcdf files to an xarray mfdataset"""
    i1 =    0 if i1 is None else i1
    j1 =    0 if j1 is None else j1
    i= 8640 if i2 is None else i2
    j2 = 4320 if j2 is None else j2
    dtmvec = pd.date_range(f"{year1}-01-01", f"{year2}-12-31", freq="1MS")
    for dtm in dtmvec:
        if not os.path.isfile(filename(dtm)):
            download(dtm=dtm)
    ds = xr.open_mfdataset([filename(dtm) for dtm in dtmvec], parallel=True)
    ds["chl"] = ds["chlor_a"]
    return ds.isel(lon=slice(i1, i2), lat=slice(j1, j2)) 

def process(j1=None, j2=None, ver="4.2", islice=540, year1=1998):
    """Calculate climatologies and linear trends and save to netcdf file"""
    j1 =    0 if j1 is None else j1
    j2 = 4320 if j2 is None else j2
    verstr = str(ver.replace(".",""))
    for ipos in range(0, 8640, islice):
        print (ipos)
        print("load")
        ds = load(i1=ipos, i2=ipos+islice, j1=j1, j2=j2, year1=year1, ver=ver)
        ds = trend_analysis.add_trends(ds, fieldname="chlor_a")
        fname = (f"ncfiles/OC-CCI_{year1}_2018_v{verstr}" + 
                 f"_{j1:04}_{j2:04}_{ipos:04}_{ipos+1080:04}.nc")
        ds = ds.drop_vars(["MERIS_nobs_sum", "MODISA_nobs_sum",
                           "SeaWiFS_nobs_sum", "chlor_a_log10_bias",
                           "chlor_a_log10_rmsd", "total_nobs_sum",
                           "VIIRS_nobs_sum", "crs", "chlor_a", "deseas",
                           "chl"])  
        ds.to_netcdf(fname)

def plot_trend(ds):
    mp = projmap.Map("glob")
    mp.style["landface"] = "0.6"
    mp.style["oceancolor"] = "0.8"
    pl.clf()
    mp.nice(borders=False)
    mp.pcolor(ds.lon, ds.lat, ds.trend, vmin=-5, vmax=5, cmap=cm.RdBu_r,
              colorbar=True, rasterized=True)
    mp._cb.ax.tick_params(labelsize=16)
    mp._cb.set_label("Percent change yr$^{-1}$", size=16)
    return mp

def plot_chl_trend(ds=None,year1=1998, ver="4.2"):
    verstr = str(ver.replace(".",""))
    if ds is None:
        ds = xr.open_mfdataset("ncfiles/OC-CCI_1998_2018_v42_0000_4320_*")
    trend = (100 * (ds.slope*12) / (ds.climatology+ds.intercept)).data
    mask = ds.pvalue.data > 0.05
    trend[mask] = np.nan
    ds["trend"] = (("lat", "lon"), trend)
    plot_trend(ds)
    sf_kw = dict(dpi=600, bbox_inches="tight")
    for ftype in ["png", "pdf", "eps", "svg"]:
        pl.savefig(
            f"figs/OC-CCI_Chl_trend_v{verstr}_{year1}-2018.{ftype}", **sf_kw)

def plot_hatched_chl_trend(ds=None,year1=1998, ver="4.2", pcut=0.1):
    verstr = str(ver.replace(".",""))
    if ds is None:
        ds = xr.open_mfdataset("ncfiles/OC-CCI_1998_2018_v42_0000_4320_*")
    trend = (100 * (ds.slope*12) / (ds.climatology+ds.intercept)).data
    mask = ds.pvalue.data > pcut
    hatchmask = np.zeros(trend.shape)
    hatchmask[mask==0] = np.nan
    #trend[mask] = np.nan
    ds["trend"] = (("lat", "lon"), trend)

    mpl.rcParams['hatch.linewidth'] = 0.2
    pl.close("all")
    pl.figure(1, (11,8))
    mp = plot_trend(ds)
    mp.contourf(ds.lon[4::8], ds.lat[4::8], hatchmask[4::8,4::8], 
                hatches=["XXXXXX"], colors="none")
    sf_kw = dict(dpi=600)#, bbox_inches="tight")
    pstr = str(pcut).replace(".", "o")
    for ftype in ["png", "pdf", "eps", "svg"]:
        pl.savefig(
            f"figs/OC-CCI_Chl_trend_v{verstr}_{year1}-2018_hatch{pstr}.{ftype}", **sf_kw)


def plot_chl_clim(ds=None, ver="4.2"):
    verstr = str(ver.replace(".",""))
    if ds is None:
        ds = xr.open_mfdataset("ncfiles/OC-CCI_1998_2018_v42_0000_4320_*")
    mp = projmap.Map("glob")
    mp.style["landface"]="0.6"
    mp.style["oceancolor"]="0.8"
    sf_kw = dict(dpi=600)#, bbox_inches="tight")

    def create_map(cmap):
        pl.close("all")
        pl.figure(1, (11,8))
        mp.pcolor(ds.lon, ds.lat, ds.climatology, norm=LogNorm(vmin=0.01,vmax=10), 
                  cmap=getattr(cm, cmap), colorbar=True, rasterized=True)
        mp._cb.set_label("mg Chl m$^{-3}$", size=16)
        mp._cb.ax.tick_params(labelsize=16)
        mp.nice(borders=False)
        for ftype in ["png", "pdf", "eps", "svg"]:
            pl.savefig(
                f"figs/OC-CCI_Chl_clim_v{verstr}_1998-2018_{cmap.split('_')[0]}.{ftype}", 
                **sf_kw)
    create_map("viridis")
    create_map("nipy_spectral")
 
def hist(ds=None, ver="4.2", cut=20, ylog=True, pcut=0.1):
    verstr = str(ver.replace(".",""))
    if ds is None:
        filename = f"ncfiles/OC-CCI_1998_2018_v{verstr}_0000_4320_????_????.nc"
        ds = xr.open_mfdataset(filename)
    trend = ds.trend.values
    area = xr.open_dataset("oc-cci_grid_area.nc")["area"].data

    pl.close("all")
    pl.figure(3,(4*2.074021843846364,4))
    pl.clf()
    mask = np.isfinite(trend) & (trend>-cut) & (trend<cut)                                            
    y,x = np.histogram(trend[mask], np.linspace(-cut,cut, 200), weights=area[mask])
    pl.fill_between((x[1:]+x[:-1])/2,y, alpha=0.20, color="#1f77b4")

    mask = np.isfinite(trend) & (trend>-cut) & (trend<cut)   & (ds.pvalue.values < pcut)
    y,x = np.histogram(trend[mask], np.linspace(-cut,cut, 200), weights=area[mask])
    pl.plot((x[1:]+x[:-1])/2,y, lw=1)    
    pl.fill_between((x[1:]+x[:-1])/2,y, alpha=0.20, color="#1f77b4")
    #pl.setp(pl.gca(), yscale="log")
    y1,y2 = pl.ylim()
    pl.plot([0,0], [1000,1e8], ":", c="0.5")
    if ylog:
        pl.setp(pl.gca(), yscale="log")
    pl.ylim(1000, 1e8)
    pl.xlabel("Percent change (yr$^{-1}$)", fontsize=14)
    pl.ylabel("Area (km$^3$)", fontsize=14)
    pl.gca().tick_params(labelsize=14)
    pstr = str(pcut).replace(".", "o")
    pl.savefig(f"figs/OC-CCI_Chl_trend_hist_{cut}_{pstr}.pdf", bbox_inches="tight")
