# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Table_11.SM_cmip_indices_regional.ipynb

# %% cell 2
import os
import textwrap

import data_tables
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import conf
import filefinder
from utils import computation, file_utils

# %% cell 3
warming_levels = [1.5, 2.0, 3.0, 4.0]

# %% cell 6
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean",
)

# %% cell 7
def get_data(varn, postprocess, anomaly):
    c6_index_reg = conf.cmip6.load_post_all_concat(
        varn=varn, postprocess=postprocess, anomaly=anomaly
    )

    c6_at_warming_index = computation.at_warming_levels_dict(
        c6_tas, c6_index_reg, warming_levels=warming_levels
    )

    return c6_at_warming_index

# %% cell 8
c6_at_warming_txx = get_data(
    varn="tasmax", postprocess="txx_reg_ave_ar6", anomaly="absolute"
)

# %% cell 9
c6_at_warming_tnn = get_data(
    varn="tasmin", postprocess="tnn_reg_ave_ar6", anomaly="absolute"
)

# %% cell 10
c6_at_warming_rx1day = get_data(
    varn="pr", postprocess="rx1day_reg_ave_ar6", anomaly="relative"
)

# %% cell 11
c6_at_warming_rx5day = get_data(
    varn="pr", postprocess="rx5day_reg_ave_ar6", anomaly="relative"
)

# %% cell 12
c6_at_warming_mrso = get_data(
    varn="mrso", postprocess="sm_annmean_reg_ave_ar6", anomaly="norm"
)

# %% cell 13
c6_at_warming_mrsos = get_data(
    varn="mrsos", postprocess="sm_annmean_reg_ave_ar6", anomaly="norm"
)

# %% cell 14
c6_at_warming_cdd = get_data(
    varn="pr", postprocess="cdd_reg_ave_ar6", anomaly="absolute"
)

# %% cell 15
ff = filefinder.FileFinder(
    path_pattern="../../cmip_indices_regional/indices{what}/{extension}",
    file_pattern="cmip_indices{what}_regional_{index}.{extension}",
)

ff_data_table = filefinder.FileFinder(
    path_pattern="../../cmip_indices_regional/indices{what}/data_tables/{index}",
    file_pattern="cmip_indices_regional_{index}_md{wl}",
)

# %% cell 17
def to_csv(fN, df, title, header, write_index=True):
    """save pandas.DataFrame to csv file

    Parameters
    ----------
    fN : str
        Filename.
    df : pd.DataFrame
        Pandas DataFrame to convert to a csv file.
    title : str
        Title of the csv file.
    header : str
        Header to add to the csv file. Should be prepended with '#'
        to denote comments.
    write_index : bool, default: True
        Whether to add the index of the DataFrame.
    """

    with open(fN, "w") as f:
        f.writelines(title)
        f.writelines(header)
        df.to_csv(f, index=write_index)


def to_markdown(fN, df, title, header):
    """save pandas.DataFrame in markdown format

    Parameters
    ----------
    fN : str
        Filename.
    df : pd.DataFrame
        Pandas DataFrame to convert to a markdown file.
    title : str
        Title of the markdown file.
    header : str
        Header to add to the csv file. '#' will be replaced with "-"
        to denote comments.
    """

    header = header.replace("#", "-")

    # replace Na with None for missingval
    df = df.where(df.notna(), None)

    with open(fN, "w") as f:

        f.writelines(title)
        f.writelines(["\n"])
        f.writelines(header)
        f.writelines(["\n"])
        df.reset_index().to_markdown(f, index=False, missingval="-")


def to_datatable(fNs, index):
    """write final datatable"""

    what = "_multi_model_median"
    fN_out = ff_data_table.create_full_name(
        extension="_raw", index=index, wl="", what=what
    )
    data_tables.save_cmip6_info_post(fNs, fN_out)


def to_excel(fN, df, title, units):
    """save pandas.DataFrame to excel file

    Parameters
    ----------
    fN : str
        Filename.
    df : pd.DataFrame
        Pandas DataFrame to convert to a csv file.
    title : str
        Title of the csv file.
    units : str
        Units to add to the table header.
    """

    # combine index to "Name (abbrev)"
    df = df.reset_index()
    name = df.names + " (" + df.abbrevs + ")"
    df = df.drop(columns=["abbrevs", "region", "names"])
    df.index = name

    # create columns
    columns = df.columns.to_list()
    proj = ["Projections"] * len(columns)
    columns = [f"+{i}°C GWL" for i in columns]
    columns = pd.MultiIndex.from_arrays([proj, columns])
    df.columns = columns

    def to_str(x):
        if np.isnan(x):
            return "-"
        return f"{x:0.2f}{units}"

    # add units
    df = df.applymap(to_str)

    df.to_excel(fN)

# %% cell 18
def to_warming_level_df_all_models_one_ens(
    c6_at_warming_, varn, invalidate_global=False
):

    columns = [
        "region",
        "abbrevs",
        "names",
        "model",
        "ens",
        "exp",
        "table",
        "grid",
        "varn",
    ]

    out = list()
    for key in c6_at_warming_.keys():

        da = c6_at_warming_[key].copy(deep=True)

        if invalidate_global:
            da.loc[{"region": [-4, -3, -2]}] = np.NaN

        df = (
            da.drop(["type", "depth", "ensnumber", "ensi"], errors="ignore")
            .to_dataframe()
            .reset_index()  # remove the multi index
            .drop(columns=["mod_ens"])
            .reset_index(drop=True)
            .drop(columns=["postprocess"])
            .set_index(columns)
            .rename(columns={varn: key})
            .round(2)
        )

        out.append(df)

    df = pd.concat(out, axis=1)

    return df.reset_index().sort_values(["region", "model"]).reset_index(drop=True)

# %% cell 19
def to_warming_level_df(c6_at_warming_, varn, invalidate_global=False):

    # convert to a dataframe, concatenate the warming levels

    out = list()
    for key in c6_at_warming_.keys():

        da = c6_at_warming_[key].copy(deep=True)

        if invalidate_global:
            da.loc[{"region": [-4, -3, -2]}] = np.NaN

        df = (
            da.median("mod_ens")
            .swap_dims({"region": "abbrevs"})
            .to_dataframe()
            .drop(columns=["type", "depth"], errors="ignore")
            .reset_index()
            .set_index(["abbrevs", "region", "names"])
            .rename(columns={varn: key})
            .round(2)
        )

        out.append(df)

    return pd.concat(out, axis=1)


df = to_warming_level_df(c6_at_warming_txx, "tasmax")

# %% cell 20
def save_index(
    c6_at_warming_, varn, index, units, invalidate_global=False, write_data_table=True
):

    what = "_multi_model_median"

    title = f"# cmip6: multi-model-median regional means at warming levels - {index}"

    wl = "+" + "°C, +".join(c6_at_warming_.keys()) + "°C"
    header = f"""
    # anomalies w.r.t. 1850-1900
    # warming levels: {wl}
    # index: {index}
    # variable: {varn}
    # units: {units}
    """
    header = textwrap.dedent(header)

    df = to_warming_level_df(c6_at_warming_, varn, invalidate_global=invalidate_global)

    # save as csv
    fN_csv = ff.create_full_name(extension="csv", index=index, what=what)
    to_csv(fN_csv, df, title, header)

    # save as markdown
    fN_md = ff.create_full_name(extension="md", index=index, what=what)
    to_markdown(fN_md, df, title, header)

    # save as excel
    fN_excel = ff.create_full_name(extension="xlsx", index=index, what=what)
    to_excel(fN_excel, df, title, units)

    # print markdown links for README
    path_csv = os.path.join(*fN_csv.split("/")[3:])
    path_md = os.path.join(*fN_md.split("/")[3:])
    print(f"|{index}|[{index}.md]({path_md})|[{index}.csv]({path_csv})|")

    # save individual models
    df_all_models_one_ens = to_warming_level_df_all_models_one_ens(
        c6_at_warming_, varn, invalidate_global=False
    )
    fN_csv_all_models_one_ens = ff.create_full_name(
        extension="csv", index=index, what="_all_models_one_ens"
    )
    title_all = (
        f"# cmip6: regional means at warming levels for individual models - {index}"
    )
    to_csv(
        fN_csv_all_models_one_ens,
        df_all_models_one_ens,
        title_all,
        header,
        write_index=False,
    )

    # write datalists

    folder = ff_data_table.create_path_name(index=index, what=what)
    file_utils.mkdir(folder)

    fNs = list()
    for key, value in c6_at_warming_.items():
        fN = ff_data_table.create_full_name(index=index, wl=f"_{key}_raw", what=what)
        data_tables.save_simulation_info_raw(fN, value, panel=key)
        fNs.append(fN)

    # combine datatable
    if write_data_table:
        to_datatable(fNs, index)

# %% cell 22
save_index(c6_at_warming_txx, varn="tasmax", index="TXx", units="°C")
save_index(c6_at_warming_tnn, varn="tasmin", index="TNn", units="°C")

# %% cell 23
save_index(c6_at_warming_rx1day, varn="pr", index="Rx1day", units="%")
save_index(c6_at_warming_rx5day, varn="pr", index="Rx5day", units="%")

# %% cell 24
save_index(c6_at_warming_mrso, varn="mrso", index="SM_total", units="σ", invalidate_global=True)
save_index(c6_at_warming_mrsos, varn="mrsos", index="SM_top", units="σ", invalidate_global=True)
save_index(c6_at_warming_cdd, varn="pr", index="CDD", units="day")
