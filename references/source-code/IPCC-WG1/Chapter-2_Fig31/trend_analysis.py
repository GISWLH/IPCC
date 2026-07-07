
import numpy as np
import pandas as pd
import xarray as xr

from multiprocess import linregress, processify

def add_climatology(ds, fieldname="data"):
    """Calculate climology of monthly data"""
    ds["climatology"] = (("lat", "lon"), np.nanmedian(ds[fieldname], axis=0))
    ds["climatology"].attrs["description"] = "Median values each element" 
    return ds

def add_deseason(ds, fieldname="data"):
    """Remove seasonality in global Chl"""
    dtmvec = pd.DatetimeIndex(ds.time.to_pandas()) 
    fieldarr = ds[fieldname].load().data.copy()
    for month in range(1,13):
        mnmask = dtmvec.month == month
        mnclim = np.nanmedian(ds[fieldname][mnmask,:,:], axis=0)     
        for tpos in np.nonzero(mnmask)[0]:
            fieldarr[tpos,:,:] -= mnclim
            print(month,tpos)
    ds["deseas"] = (("time","lat","lon"), fieldarr)
    ds["deseas"].attrs["description"] = (
        "Dataset deseasonalized using monthly climatologies")
    return ds

def add_linregress(ds, fieldname="data"):
    """Perform linear regression analysis for part of the globe"""
    if not "deseas" in ds:
        add_deseason(ds=ds, fieldname=fieldname)
    regr = linregress(ds.deseas.data) 
    for key in ["slope", "intercept", "rvalue", "pvalue"]:
        ds[key] = (("lat", "lon"), getattr(regr, key))
    return ds

#@processify                     
def add_trends(ds, fieldname="data"):
    print("Calc climatology")
    ds = add_climatology(ds=ds, fieldname=fieldname)
    print("Deseason")
    ds = add_deseason(ds=ds, fieldname=fieldname)
    print("Calc regression")
    ds = add_linregress(ds=ds, fieldname=fieldname)
    ds["trend"] = (100 * (ds.slope*12) / (ds.climatology+ds.intercept))
    return ds
