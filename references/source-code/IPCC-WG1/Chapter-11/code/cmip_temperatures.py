# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/cmip_temperatures.ipynb

# %% cell 2
import data_tables
import pandas as pd

import conf
import filefinder
from utils import computation

# %% cell 4
c6_tas_all_no_anom = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean",
    ensnumber=None,
    anomaly="no_check_no_anom",
)

# %% cell 6
c5_tas_all_no_anom = conf.cmip5.load_post_all_concat(
    varn="tas",
    postprocess="global_mean",
    ensnumber=None,
    anomaly="no_check_no_anom",
)

# %% cell 8
periods = {
    # 20-year periods
    "2021-2040": slice(2021, 2040),
    "2041-2060": slice(2041, 2060),
    "2081-2100": slice(2081, 2100),
    "2016-2035": slice(2016, 2035),
    "2046-2065": slice(2046, 2065),
    # 10-year periods
    "2011-2020": slice(2011, 2020),
    "2021-2030": slice(2021, 2030),
    "2031-2040": slice(2031, 2040),
    "2041-2050": slice(2041, 2050),
    "2051-2060": slice(2051, 2060),
    "2061-2070": slice(2061, 2070),
    "2071-2080": slice(2071, 2080),
    "2081-2090": slice(2081, 2090),
    "2091-2100": slice(2091, 2100),
}

# %% cell 10
def temperature_anomaly(c_tas, exp, ensnumber, bounds_check, start=1850, end=1900):
    """calculate temperature anomalies w.r.t. reference period
    
    Parameters
    ----------
    c_tas : datalist
        Datalist with absloute global mean annual mean temperature data for
        CMIP5 or CMIP6.
    exp : str
        Scenario for which to compute the average.
    ensnumber : int or None
        Ensemble number for which to compute the average.
    bounds_check : boolean
        If True removes all simulations that do not cover the whole
        reference period, else keeps them,
    start : int
        Start of the reference period.
    end : int
        End of the reference period.    
    """

    # select subset of data
    c_tas_sel = computation.select_by_metadata(c_tas, exp=exp, ensnumber=ensnumber)

    # calc anomaly - maybe remove models starting after 1850
    how = "absolute" if bounds_check else "no_check_absolute"

    c_tas_anom = computation.process_datalist(
        computation.calc_anomaly,
        c_tas_sel,
        start=start,
        end=end,
        how=how,
        quiet=True,
    )

    # concatenate ensemble members
    c_tas_anom_comb = computation.concat_xarray_with_metadata(c_tas_anom)

    # calculate mean over periods
    period_means = list()
    for name, period in periods.items():
        period_mean = c_tas_anom_comb.sel(year=period).tas.mean("year")

        df = period_mean.drop_vars(["ensnumber", "ensi"]).to_dataframe()

        df = df.rename(columns=dict(tas="mean"))
        df["period"] = name

        # reorder columns
        columns = df.columns.to_list()
        columns = columns[:-2] + columns[-1:] + columns[-2:-1]
        df = df[columns]

        period_means.append(df)

    return pd.concat(period_means), c_tas_anom_comb

# %% cell 11
def temperature_absolute(c_tas, exp, ensnumber, bounds_check, start=1850, end=1900):
    """calculate absolute temperatures

    Parameters
    ----------
    c_tas : datalist
        Datalist with absloute global mean annual mean temperature data for
        CMIP5 or CMIP6.
    exp : str
        Scenario for which to compute the average.
    ensnumber : int or None
        Ensemble number for which to compute the average.
    bounds_check : boolean
        If True removes all simulations that do not cover the whole
        reference period, else keeps them,
    start : int
        Start of the reference period.
    end : int
        End of the reference period.
    """

    # select subset of data
    c_tas_sel = computation.select_by_metadata(c_tas, exp=exp, ensnumber=ensnumber)

    # bounds check - maybe remove models starting after 1850
    how = "no_anom" if bounds_check else "no_check_no_anom"

    c_tas_anom = computation.process_datalist(
        computation.calc_anomaly,
        c_tas_sel,
        start=start,
        end=end,
        how=how,
        quiet=True,
    )

    # concatenate ensemble members
    c_tas_anom_comb = computation.concat_xarray_with_metadata(c_tas_anom)

    # calculate mean over reference periods

    period = slice(start, end)
    period_mean = c_tas_anom_comb.sel(year=period).tas.mean("year")

    df = period_mean.drop_vars(["ensnumber", "ensi"]).to_dataframe()

    df = df.rename(columns=dict(tas="mean"))
    df["period"] = "1850-1900"

    # reorder columns
    columns = df.columns.to_list()
    columns = columns[:-2] + columns[-1:] + columns[-2:-1]
    df = df[columns]

    return df, c_tas_anom_comb

# %% cell 13
ff = filefinder.FileFinder(
    path_pattern="../../cmip_temperatures/temperatures/{cmip}/{extension}",
    file_pattern="{cmip}_temperatures{how}_{ens}_{reference_period}{bounds_check}.{extension}",
)

ff_data_table = filefinder.FileFinder(
    path_pattern="../../cmip_temperatures/temperatures/{cmip}/data_tables",
    file_pattern="{cmip}_temperatures_{ens}_{reference_period}{bounds_check}_{exp}_md_raw",
)

# %% cell 14
def save_temperatures(
    c_tas,
    conf_cmip,
    ensnumber,
    bounds_check,
    how="",
    start=1850,
    end=1900,
    save_data_table=True,
):
    """save temperature for individual ensemble members in a .csv file

    Parameters
    ----------
    c_tas : datalist
        Datalist with absloute global mean annual mean temperature data for
        CMIP5 or CMIP6.
    conf_cmip : _cmip_conf class
        Class with cmip-version specific attributes.
    ensnumber : int or None
        Ensemble number for which to compute the average.
    bounds_check : boolean
        If True removes all simulations that do not cover the whole
        reference period, else keeps them,
    how : str, default: "" | "absolute"
        If the absolute or anomaly should be computed.
    start : int
        Start of the reference period.
    end : int
        End of the reference period.
    save_data_table : bool
        Whether to save the data_table or not.
    """
    
    
    assert ensnumber in [0, "*"]
    
    assert how in ["", "_absolute"]
    
    func = temperature_anomaly if how == "" else temperature_absolute
    

    # loop over scenarios
    temperature_ranges = dict()
    ds_for_data_tables = dict()
    for exp in conf_cmip.scenarios:

        df, ds = func(
            c_tas, exp, ensnumber, bounds_check, start=start, end=end
        )

        if conf_cmip.cmip_version == "cmip5":
            df.pop("grid")

        temperature_ranges[exp] = df
        ds_for_data_tables[exp] = ds

    reference_period = f"{start}_{end}"
    cmip = conf_cmip.cmip_version
    ens = "all_ens" if ensnumber == "*" else "one_ens"
    bounds_check = "" if bounds_check else "_no_bounds_check"

    fN = ff.create_full_name(
        reference_period=reference_period,
        cmip=cmip,
        ens=ens,
        bounds_check=bounds_check,
        how=how,
        extension="csv",
    )

    df = pd.concat(temperature_ranges.values())
    df.to_csv(fN, index=False, float_format="%0.2f")
    
    if save_data_table:
        for exp in conf_cmip.scenarios:
            fN = ff_data_table.create_full_name(
                reference_period=reference_period,
                cmip=cmip,
                ens=ens,
                bounds_check=bounds_check,
                exp=exp,
            )
            ds = ds_for_data_tables[exp]
            data_tables.save_simulation_info_raw(fN, ds, panel=exp, add_tas=False)

    return temperature_ranges

# %% cell 15
def save_mmm(df_cmip, cmip, label):
    """calculate the multi model mean
    
    Parameters
    ----------
    df_cmip : pd.DataFrame
        Summary DataFrame returned by `temperature_anomaly` or `temperature_absolute`
    cmip : str
        CMIP version to save "CMIP5" or "CMIP6".
    label : mapping
        Mapping from scenario abbreviation to clean label.
    
    """


    out = list()
    for exp in df_cmip.keys():
        
        # calculate the mean per period
        g = df_cmip[exp].groupby("period")
        df = g.mean()
        # find number of model runs
        n_ens = g.count().iloc[0, 0]

        df = df.rename(columns=dict(mean=label[exp] + f" ({n_ens})"))
        out.append(df)

    df = pd.concat(out, axis=1)
    df = df.round(2)
    # sort by the periods
    df = df.loc[periods.keys()]
    
    fN = f"../../cmip_temperatures/{cmip}_mmm_temperatures_one_ens_1850_1900.csv"
    df.to_csv(fN)
    
    print(df.to_markdown())
    
    return df

# %% cell 17
# CMIP5
# =====

save_temperatures(
    c5_tas_all_no_anom, conf.cmip5, ensnumber="*", bounds_check=True, start=1850, end=1900
)

df_cmip5 = save_temperatures(
    c5_tas_all_no_anom, conf.cmip5, ensnumber=0, bounds_check=True, start=1850, end=1900
)

save_temperatures(
    c5_tas_all_no_anom, conf.cmip5, ensnumber="*", bounds_check=False, start=1850, end=1900
)

save_temperatures(
    c5_tas_all_no_anom, conf.cmip5, ensnumber=0, bounds_check=False, start=1850, end=1900
)

# CMIP6
# =====

save_temperatures(
    c6_tas_all_no_anom, conf.cmip6, ensnumber="*", bounds_check=True, start=1850, end=1900
)

df_cmip6 = save_temperatures(
    c6_tas_all_no_anom, conf.cmip6, ensnumber=0, bounds_check=True, start=1850, end=1900
)


None

# %% cell 18
save_mmm(df_cmip6, "cmip6", conf.label_ssp)

# %% cell 19
save_mmm(df_cmip5, "cmip5", conf.label_rcp)

# %% cell 21
# CMIP5
# =====

opt = dict(
    how="_absolute",
    start=1850,
    end=1900,
    save_data_table=False,
)

save_temperatures(
    c5_tas_all_no_anom,
    conf.cmip5,
    ensnumber="*",
    bounds_check=True,
    **opt,
)

save_temperatures(
    c5_tas_all_no_anom,
    conf.cmip5,
    ensnumber=0,
    bounds_check=True,
    **opt,
)

save_temperatures(
    c5_tas_all_no_anom,
    conf.cmip5,
    ensnumber="*",
    bounds_check=False,
    **opt,
)

save_temperatures(
    c5_tas_all_no_anom,
    conf.cmip5,
    ensnumber=0,
    bounds_check=False,
    **opt,
)

# CMIP6
# =====

save_temperatures(
    c6_tas_all_no_anom,
    conf.cmip6,
    ensnumber="*",
    bounds_check=True,
    **opt,
)

save_temperatures(
    c6_tas_all_no_anom,
    conf.cmip6,
    ensnumber=0,
    bounds_check=True,
    **opt,
)

None
