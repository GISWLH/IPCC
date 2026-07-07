# -*- coding: utf-8 -*-
"""

Author: Florian Ladstädter

© Copyright 2021 [ Wegener Center && IGAM ] / UniGraz
"""
# Standard Library
import logging
import os
import time

from collections import Counter

# Third party
import click
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from matplotlib.ticker import FixedLocator, MultipleLocator, ScalarFormatter
from scipy.interpolate import interp1d

# First party
import atmoplots.ipcc_colors as ipcc_colors

from atmoplots.plotconfig import PlotConfig
from atmoplots.pressure_mapping import pressure_mapping

# Local imports
from . import common

logger = logging.getLogger(__name__)


mpl.rcParams["hatch.color"] = "black"
mpl.rcParams["hatch.linewidth"] = 0.1
mpl.rc("lines", markersize=3)  # markersize scatterplots

plot_style = {
    "ipcc": {
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "figure.figsize": (4, 8),
        "xtick.minor.visible": False,
        "axes.linewidth": 0.5,
        "axes.labelsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "axes.titlesize": 11,
    },
    "regular": {
        "xtick.direction": "in",
        "ytick.direction": "in",
        "axes.grid": True,
        "figure.figsize": (5, 8),
        "xtick.minor.visible": True,
        "axes.linewidth": 0.5,
    },
}

# Names for palette come from:
# guidelines_SOD_Figures.pdf
# or: https://github.com/IPCC-WG1/colormaps
# or: ipcc_colors module
palette = "spectrum_cat"
# palette = 'gree-blue_cat'
# palette = 'bright_cat'
# palette = 'red-yellow_cat'
# palette = 'dark_cat'
# palette = 'ssp_cat_2'
logger.debug(f"Use colors from IPCC colors module, with palette: {palette}")
COLOR_IPCC_ORDER = ipcc_colors.load_colors(palette)

PLOT_VAR_CONF = {
    "temperature": {
        "type": "absolute",
        "limits_resid": [0, 2],
        "limits_trend": [-0.7, 0.7],
        "unit": "°C",
        "unit_var": "$K^{2}$",
        "x_ticks": (0.5, 0.1),
    },
    "pressure": {
        "type": "relative",
        "limits_resid": [0, 0],
        "limits_trend": [-0.5, 0.5],
        "unit": "%",
        "unit_var": "",
        "x_ticks": (0.1, 0.1),
    },
    "dry_temperature": {
        "type": "absolute",
        "limits_resid": [0, 2],
        # 'limits_trend': [-3., 3.],
        # "limits_trend": [-1.0, 1.0],
        "limits_trend": [-0.7, 0.7],
        "unit": "°C",
        "unit_var": "$K^{2}$",
        "x_ticks": (0.5, 0.1),
        "x_label": "temperature",
    },
    "dry_pressure": {
        "type": "relative",
        "limits_resid": [0, 0],
        "limits_trend": [-1.5, 1.5],
        "unit": "%",
        "unit_var": "",
        "x_ticks": (0.5, 0.1),
    },
    "refractivity": {
        "type": "relative",
        "limits_resid": [0, 0],
        "limits_trend": [-1.5, 1.5],
        "unit": "%",
        "unit_var": "",
        "x_ticks": (0.5, 0.1),
    },
    "bending_angle": {
        "type": "relative",
        "limits_resid": [0, 0],
        # 'limits_trend': [-3., 3.],
        "limits_trend": [-1.0, 1.0],
        "unit": "%",
        "unit_var": "",
        "x_ticks": (0.5, 0.1),
    },
    "optimized_bending_angle": {
        "type": "relative",
        "limits_resid": [0, 0],
        # 'limits_trend': [-3., 3.],
        "limits_trend": [-1.0, 1.0],
        "unit": "%",
        "unit_var": "",
        "x_ticks": (0.5, 0.1),
    },
}

today_time = time.strftime("%Y%m%d_%H%M%S")
MEAN_SCALE_HEIGHT = 7000.0
MEAN_P_SURF = 101325.0


def press_to_press_altitude(pressure):
    """
    calculates the pressure altitude out of the pressure using the
    hypsometric equation;
    definition of pressure altitude:
    Pressure Altitude [m] = -7000 m * ln( P [Pa] / 101325 Pa)
    """
    return -MEAN_SCALE_HEIGHT * np.log(pressure / MEAN_P_SURF)


def press_altitude_to_press(press_alt):
    """
    calculates pressure out of pressure altitude using the
    hypsometric equation;
    definition of pressure altitude:
    Pressure [Pa] = 101325 Pa * exp( - Pressure Altitude [m] / 7000 m)

    """
    return MEAN_P_SURF * np.exp(-press_alt / MEAN_SCALE_HEIGHT)


def get_pres_mapping(lat_bounds=None, method="empirical"):
    if method == "empirical":
        # mean RO pres-to-alt mapping for lat range
        if lat_bounds is None:
            raise ValueError(
                "lat_bounds information is required for 'empirical' pressure mapping."
            )
        pres_mapping = pressure_mapping(lat_bounds)["altitude"]
    elif method == "simple":
        # Prepare pressure mapping, in case we need it for secondary pressure axis
        equid_grid = np.exp(np.linspace(np.log(1000), np.log(100000), 351))
        pres_mapping_arr = press_to_press_altitude(equid_grid)
        pres_mapping = xr.DataArray(
            pres_mapping_arr,
            coords=[equid_grid],
            dims=["pressure"],
            name="altitude",
        )
    else:
        raise NotImplementedError(f"Pressure mapping method {method} not implemented.")
    return pres_mapping


def add_pres_mapping(ds, method="empirical"):
    if "latitude_bins_bounds" in ds:
        lat_bounds = (
            ds["latitude_bins_bounds"].squeeze().data if method == "empirical" else None
        )
    elif "shape" in ds:
        if method == "empirical":
            lat_bounds = (
                ds["latitude_bins"].where(~ds["shape"].isnull()).min(),
                ds["latitude_bins"].where(~ds["shape"].isnull()).max(),
            )
        else:
            lat_bounds = None
    else:
        lat_bounds = None
    pres_mapping = get_pres_mapping(lat_bounds, method)

    # Remove NaNs in mapping, to use it later for secondary pressure axis
    pres_axis_mapping = pres_mapping.where(
        ~pres_mapping.isnull(), drop=True
    )
    # Add mapping for secondary axis to original ds, using different varnames
    pres_axis_mapping_ds = pres_axis_mapping.rename(
        {"pressure": "pressure_mapping"}
    ).rename("altitude_mapping")
    ds = ds.merge(pres_axis_mapping_ds)
    return ds


def swap_to_altitude(ds, method="empirical"):
    if "latitude_bins_bounds" in ds:
        lat_bounds = (
            ds["latitude_bins_bounds"].squeeze().data if method == "empirical" else None
        )
    elif "shape" in ds:
        if method == "empirical":
            lat_bounds = (
                ds["latitude_bins"].where(~ds["shape"].isnull()).min(),
                ds["latitude_bins"].where(~ds["shape"].isnull()).max(),
            )
        else:
            lat_bounds = None
    else:
        lat_bounds = None
    pres_mapping = get_pres_mapping(lat_bounds, method)

    if "altitude" in ds:
        ds = ds.drop_vars(["altitude"])
        logger.warning(
            "Dropping existing altitude values and use newly computed ones "
            "according to chosen pressure mapping method."
        )

    if method == "empirical":
        ds["altitude"] = pres_mapping.interp(pressure=ds["pressure"])
    elif method == "simple":
        # pressure altitude
        ds["altitude"] = press_to_press_altitude(ds["pressure"])
    else:
        raise NotImplementedError(f"Pressure mapping method {method} not implemented.")
    logger.debug("Swap ds from pressure to altitude.")
    ds = ds.swap_dims({"pressure": "altitude"}).dropna("altitude", subset=["altitude"])
    return ds


def swap_to_pressure(ds, method="empirical"):
    lat_bounds = (
        ds["latitude_bins_bounds"].squeeze().data if method == "empirical" else None
    )
    pres_mapping = get_pres_mapping(lat_bounds, method)
    # Swap mapping to altitude-pressure mapping
    pres_mapping = (
        pres_mapping.to_dataset()
        .swap_dims({"pressure": "altitude"})
        .dropna("altitude", subset=["altitude"])
        .reset_coords("pressure")["pressure"]
    )

    if "pressure" in ds:
        ds = ds.drop_vars(["pressure"])
        logger.warning(
            "Dropping existing pressure values and use newly computed ones "
            "according to chosen pressure mapping method."
        )

    if method == "empirical":
        ds["pressure"] = pres_mapping.interp(altitude=ds["altitude"])
    elif method == "simple":
        # pressure altitude
        ds["pressure"] = press_altitude_to_press(ds["altitude"])
    else:
        raise NotImplementedError(f"Pressure mapping method {method} not implemented.")
    logger.debug("Swap ds from altitude to pressure.")
    ds = ds.swap_dims({"altitude": "pressure"}).dropna("pressure", subset=["pressure"])
    return ds


def plot_verticaltrends(
    glob_opts,
    data,
    var_to_plot,
    vertical_dim,
    vertical_limits,
    xlim,
    mask_below,
    smooth_all,
    add_secondary_axis,
    method_pres_to_alt,
    ipcc_style,
    errorbar,
    ncol,
    add_title,
    filename_prefix,
):
    """
    TODO proper treatment of vertical coordinate is not yet implemented. It should be possible
    to use a mixture of datasets on altitude and pressure coordinates, and choose via vertical_dim
    whether to plot those on altitude or pressure y-axis.
    """
    any_pres_mapping = False
    data_dict = {}
    data_types = []
    for label, fn in data:
        logger.info(f"Get data for: {label} from {fn}")
        try:
            pconf = PlotConfig()[label]
        except KeyError:
            logger.debug(
                f"Data key {label} not found in plot config file; use default settings for this dataset."
            )
            pconf = {}

        ds = xr.open_dataset(fn).load()

        try:
            data_type = ds.attrs["data_type"]
            logger.debug(f"Data type is: {data_type}")
            data_types.append(data_type)
        except KeyError:
            logger.error(
                "data_type attribute missing. Needs additional implementation here."
            )
            data_type = None

        # Build up output filename
        try:
            common_fn_parts = common_fn_parts.intersection(
                os.path.basename(fn)[:-3].split("_")
            )
        except NameError:
            common_fn_parts = set(os.path.basename(fn)[:-3].split("_"))

        # Determine if data is on pressure
        is_pressure = "pressure" in ds.dims

        if add_secondary_axis:
            if vertical_dim == "pressure" and method_pres_to_alt != "simple":
                raise click.BadParameter(
                    "--add-secondary-axis for vertical_dim 'pressure' "
                    "is currently only working with --method-pres-to-alt 'simple'"
                )
            any_pres_mapping = True
            ds = add_pres_mapping(ds, method_pres_to_alt)

        if is_pressure and vertical_dim == "altitude":
            any_pres_mapping = True
            ds = swap_to_altitude(ds, method_pres_to_alt)

        if not is_pressure and vertical_dim == "pressure":
            any_pres_mapping = True
            ds = swap_to_pressure(ds, method_pres_to_alt)

        # Smoothing
        if smooth_all is not None and vertical_dim == "altitude":
            alt_dist = np.unique(
                ds["altitude"]
                .sortby("altitude")
                .sel(altitude=slice(*vertical_limits))
                .diff("altitude")
            ).mean()
            smooth_vertical_steps = int(smooth_all / alt_dist)
            logger.info(
                f"{label}: Vertically smooth all values over {smooth_vertical_steps} steps"
            )
            ds = ds.rolling(altitude=smooth_vertical_steps, center=True).mean()
        elif "smooth_vertical_steps" in pconf and vertical_dim == "altitude":
            logger.info(f"{label}: Vertically smooth all values.")
            ds = ds.rolling(altitude=pconf["smooth_vertical_steps"], center=True).mean()

        # Mask below, if requested TODO
        if data_type == "RO" and mask_below is not None and vertical_dim == "altitude":
            regr_params = common.get_regr_params(ds, var_to_plot)
            ds[f"{var_to_plot}_params_{regr_params['model_name']}"] = ds[
                f"{var_to_plot}_params_{regr_params['model_name']}"
            ].where(ds.altitude >= mask_below)
        elif data_type == "RO" and mask_below is not None:
            raise click.BadParameter(
                "--mask-below currently only implemented for vertical-dim 'altitude'"
            )

        # Cut AIRS at 11.5 km (information from Stephen Leroy from telecon 21 Nov 2019)
        if data_type == "AIRS" and vertical_dim == "altitude":
            ds = ds.sortby("altitude").sel(altitude=slice(11500, None))

        # Cut the lowest levels for ERA5.1, they might contain some artifacts
        if data_type == "ERA51" and vertical_dim == "altitude":
            ds = ds.sortby("altitude").sel(
                altitude=slice(ds["altitude"].min() + 1000, None)
            )

        # If dry_temperature is requested, rename temperature variables for non-RO datasets
        # TODO better determination of variable name
        if (
            data_type is not None
            and data_type != "RO"
            and var_to_plot == "dry_temperature_anomalies"
        ):
            temp_vars = [
                vv
                for vv in ds.data_vars
                if "temperature" in vv and not vv.startswith("dry_temperature")
            ]
            for vv in temp_vars:
                vv_new = vv.replace("temperature", "dry_temperature")
                if vv_new not in ds:
                    logger.debug(f"Rename {vv} to {vv_new}")
                    ds = ds.rename({vv: vv_new})
                else:
                    logger.debug(
                        f"Do NOT rename {vv} to {vv_new}: {vv_new} exists already in dataset"
                    )

        # Cleanup
        try:
            ds = ds.squeeze(dim=["latitude_bins", "longitude_bins"])
        except (KeyError, ValueError):
            pass

        if (
            max(vertical_limits) < ds[vertical_dim].min()
            or min(vertical_limits) > ds[vertical_dim].max()
        ):
            raise click.BadParameter(
                f"--vertical-limits {vertical_limits} do not contain "
                f"range of {vertical_dim}, which is "
                f"{ds[vertical_dim].min().data} to "
                f"{ds[vertical_dim].max().data}"
            )

        data_dict[label] = ds

    if ipcc_style:
        logger.debug("Use IPCC style")
        mpl.rcParams.update(**plot_style["ipcc"])
    else:
        logger.debug("Use regular style")
        mpl.rcParams.update(**plot_style["regular"])

    # Build up output filename
    # Take arbitrary (first) filename to determine order of filename parts
    one_filename = os.path.basename(data[0][1])
    plot_filename = "_".join(
        [part for part in one_filename[:-3].split("_") if part in common_fn_parts]
    )
    # Remove variable names from filename
    possible_var_strings = [
        "bending_angle",
        "optimized_bending_angle",
        "refractivity",
        "dry_temperature",
        "dry_pressure",
        "density",
        "temperature",
        "pressure",
        "specific_humidity",
        "geopotential_height",
    ]
    # Var names might or might not be part of filename
    for ss in possible_var_strings:
        plot_filename = plot_filename.replace("_" + ss, "")
    # Add actual varname now
    plot_filename = plot_filename + "_" + var_to_plot.replace("_anomalies", "")
    if any_pres_mapping:
        plot_filename = plot_filename + "_" + method_pres_to_alt
    if filename_prefix:
        plot_filename = f"{filename_prefix}_{plot_filename}"
    data_types = sorted(list(set(data_types)))
    if data_types:
        plot_filename += f"_{'_'.join(data_types)}"
        plot_filename = plot_filename.replace(" ", "_").replace(";", "")
    if vertical_dim == "pressure":
        plot_filename += "_pressure"
    plot_filename += f".{glob_opts.output_format}"
    plot_filename = os.path.join(glob_opts.output_dir, plot_filename)

    draw(
        data_dict,
        var_to_plot,
        vertical_dim,
        vertical_limits,
        xlim,
        plot_filename,
        ipcc_style,
        errorbar,
        ncol,
        add_title,
        glob_opts.dpi,
    )


def draw(
    data_dict,
    var_to_plot,
    v_dim,
    vertical_limits,
    xlim,
    plot_filename,
    ipcc_style,
    errorbar,
    ncol,
    add_title,
    dpi,
):

    base_var_name = var_to_plot.replace("_anomalies", "")
    # residual_var_name = var_to_plot + "_resid_{}".format(model_name)
    climatology_var_name = var_to_plot.replace("_anomalies", "_climatology")

    # relev_dims_in_ds = list(
    #     set(("altitude", "pressure", "impact_altitude")) & set(ds.dims)
    # )
    # if len(relev_dims_in_ds) != 1:
    #     raise ValueError(
    #         f"Cannot uniquely determine vertical dimension from {list(ds.dims)}"
    #     )
    # v_dim = relev_dims_in_ds[0]

    # Reserve subplot below actual plot for the legend
    fig, (ax, lax) = plt.subplots(nrows=2, gridspec_kw={"height_ratios": [12, 1]})

    # Now get the data...
    idx = 0
    title_l = []
    for key, ds in data_dict.items():
        logger.info(f"Plot: {key}")
        try:
            pconf = PlotConfig()[key]
        except KeyError:
            logger.debug(
                f"Data key {key} not found in plot config file; use default settings for this dataset."
            )
            pconf = {}

        try:
            time_range = (
                pd.to_datetime(ds["time"].values[0]),
                pd.to_datetime(ds["time"].values[-1]),
            )
            start_date = time_range[0]
            end_date = time_range[1]
        except KeyError:
            logger.warning(
                f"No time information available in {key}. Assume that time "
                "range is consistent with all other datasets"
            )
            start_date = end_date = None

        # if "RO" in key and v_dim == "pressure":
        #     ds = ds.isel(**{v_dim: ds.indexes[v_dim].argsort()})
        # if "ERAI" in key and v_dim == "pressure":
        #     ds = ds.isel(**{v_dim: ds.indexes[v_dim].argsort()})
        # if "fullfield" in key and v_dim == "altitude":
        #     ds = ds.isel(**{v_dim: ds.indexes[v_dim].argsort()})
        # ds = ds.isel(**{v_dim: ds.indexes[v_dim].argsort()})

        # Convert from [m] to [km] or [Pa] to [hPa]
        if v_dim in ["altitude", "impact_altitude"]:
            v_factor = 1.0 / 1000
            dim_unit = "km"
        elif v_dim == "pressure":
            v_factor = 1.0 / 100
            dim_unit = "hPa"

        if start_date is not None:
            # Need to know if its lat-range or continent
            if "spatial_confinement" in ds.attrs:
                lat_str = ds.attrs["spatial_confinement"]
                tt = "{:02d}/{} $-$ {:02d}/{} for {}".format(
                    start_date.month,
                    start_date.year,
                    end_date.month,
                    end_date.year,
                    lat_str,
                )
            else:
                lat_bounds = ds.latitude_bins_bounds.squeeze().data
                if (
                    start_date.month == 1
                    and end_date.month == 12
                    and np.all(lat_bounds == (-20, 20))
                ):
                    tt = r"Tropics ({}$-${})".format(start_date.year, end_date.year)
                elif (
                    start_date.month == 1
                    and end_date.month == 12
                    and np.all(lat_bounds == (-70, 70))
                    or np.all(lat_bounds == (-90, 90))
                ):
                    tt = r"Global ({}$-${})".format(start_date.year, end_date.year)
                else:
                    lat_str = "{}_to_{}".format(lat_bounds[0], lat_bounds[1])
                    tt = (
                        "{:02d}/{} $-$ {:02d}/{}  for  {}$^\circ$ to {}$^\circ$".format(
                            start_date.month,
                            start_date.year,
                            end_date.month,
                            end_date.year,
                            lat_bounds[0],
                            lat_bounds[1],
                        )
                    )
            title_l.append(tt)

        # Get Trend
        regr_params = common.get_regr_params(ds, var_to_plot)

        # relative trends?
        if PLOT_VAR_CONF[base_var_name]["type"] == "relative":
            clim = ds[climatology_var_name].squeeze()
            # hack for erroneous 'time' coordinate in process_clim output
            # of climatology variables
            if "time" in clim.coords:
                # to be sure ...
                assert clim.squeeze().diff(dim="time").sum() == 0
                clim = clim.isel(time=0)
            clim = clim.mean("month")
            logger.debug(
                "Relative trends using mean {} profile as reference.".format(key)
            )
            regr_params["regr"] = (regr_params["regr"] / clim) * 100

        if ipcc_style:
            if "color-ipcc-palette-idx" in pconf:
                logger.debug("Take IPCC color index from config")
                color_idx = pconf["color-ipcc-palette-idx"]
            else:
                color_idx = idx
            color = COLOR_IPCC_ORDER[color_idx]
        else:
            try:
                logger.debug("Use color from config file.")
                color = pconf["color"]
            except KeyError:
                logger.debug("No config found for this dataset, use IPCC colors.")
                color = COLOR_IPCC_ORDER[idx]

        if "x_label" in PLOT_VAR_CONF[base_var_name]:
            x_label = PLOT_VAR_CONF[base_var_name]["x_label"]
        else:
            x_label = base_var_name

        if "scatter" in pconf and pconf["scatter"]:
            ax.plot(
                regr_params["regr"].values,
                regr_params["regr"][v_dim].values * v_factor,
                label=key,
                color=color,
                alpha=0.5,
                marker="o",
            )
        else:
            ax.plot(
                regr_params["regr"].values,
                regr_params["regr"][v_dim].values * v_factor,
                label=key,
                color=color,
                alpha=0.9,
                **pconf["plot_kwargs"] if "plot_kwargs" in pconf else {},
            )
        if errorbar:
            ax.errorbar(
                regr_params["regr"].values,
                regr_params["regr"][v_dim].values * v_factor,
                # label='95% conf. interval',
                xerr=regr_params["conf_interv_95"],
                color=color,
                alpha=0.4,
            )

        idx += 1

    if add_title:
        titles = list(set(title_l))
        if len(titles) > 1:
            title_cnt = Counter(title_l)
            title_mostcommon = title_cnt.most_common(1)
            title = title_mostcommon[0][0]
            logger.debug(
                f"Could not uniquely determine title string, found: {titles}; "
                f"use the most common one: {title}"
            )
        else:
            title = titles[0]
        ax.set_title(title)

    hh, ll = ax.get_legend_handles_labels()
    legend = lax.legend(hh, ll, borderaxespad=0, ncol=ncol, loc="upper center")
    lax.axis("off")
    # legend = ax.legend(loc=3, fancybox=False, edgecolor="black")

    legend.get_frame().set_linewidth(0.5)
    ax.set_ylabel("{} ({})".format(v_dim.capitalize(), dim_unit))
    ax.set_xlabel(
        "{} trend ({} per decade)".format(
            x_label.capitalize(), PLOT_VAR_CONF[base_var_name]["unit"]
        )
    )
    if xlim:
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(PLOT_VAR_CONF[base_var_name]["limits_trend"])
    ax.xaxis.set_major_locator(
        MultipleLocator(PLOT_VAR_CONF[base_var_name]["x_ticks"][0])
    )
    ax.tick_params(axis="x", which="both", bottom=True, top=False, labelbottom=True)
    ax.tick_params(axis="y", which="both", left=True, right=False)

    if ipcc_style:
        ax.axvline(0, linestyle="dashed", color="black", linewidth=0.5)

    if v_dim == "pressure":
        ax.set_ylim([vertical_limits[1] * v_factor, vertical_limits[0] * v_factor])
        ax.set_yscale("log")
        # ax.set_yticks([1000, 800, 700, 600, 500, 400, 300, 200,
        #                100, 80, 70, 60, 50, 40, 30, 20, 10])
        ax.get_yaxis().set_major_formatter(ScalarFormatter())
        ax.get_yaxis().set_minor_formatter(ScalarFormatter())
    else:
        ax.set_ylim([vertical_limits[0] * v_factor, vertical_limits[1] * v_factor])

    if v_dim == "pressure":
        if "pressure_mapping" in ds:

            # TODO This is currently resulting in wrong numbers for the
            # secondary axis. See https://stackoverflow.com/q/65900231/6751132
            # For now, manually use "simple" pressure mapping here.
            # pres_arr = ds["pressure_mapping"].values / 100.0
            # alt_arr = ds["altitude_mapping"].values / 1000.0

            # def inverse(x):
            #     x = np.ma.filled(x, np.nan)
            #     return interp1d(alt_arr, pres_arr, fill_value="extrapolate")(x)

            # def forward(x):
            #     x = np.ma.filled(x, np.nan)
            #     return interp1d(pres_arr, alt_arr, fill_value="extrapolate")(x)

            # ax1 = ax.secondary_yaxis("right", functions=(forward, inverse))
            # ax1.set_yscale("linear")
            # ax1.set_ylabel("Altitude (km)")

            # TODO this is hard-coded, since the above code does not yet work. It
            # should be replaced by the above, then it would also work for other
            # pressure mappings (empirical).
            ax1 = ax.twinx()
            pressure_altitude = press_to_press_altitude(
                [vertical_limits[0], vertical_limits[1]]
            )
            ax1.set_ylim(
                (pressure_altitude.min() / 1000.0, pressure_altitude.max() / 1000.0)
            )
            ax1.set_ylabel("Pressure altitude (km)")
            ax1.spines["right"].set_visible(True)
    else:
        if "pressure_mapping" in ds:
            pres_arr = ds["pressure_mapping"].values / 100.0
            alt_arr = ds["altitude_mapping"].values / 1000.0

            def forward(x):
                return interp1d(alt_arr, pres_arr, fill_value="extrapolate")(x)

            def inverse(x):
                return interp1d(pres_arr, alt_arr, fill_value="extrapolate")(x)

            ax1 = ax.secondary_yaxis("right", functions=(forward, inverse))
            ax1.yaxis.set_major_locator(
                FixedLocator((50, 100, 200, 300, 400, 500, 700, 900))
            )
            ax1.set_ylabel("Pressure (hPa)")

    logger.info("Save plot to: {}".format(plot_filename))
    plt.tight_layout()
    plt.savefig(plot_filename, dpi=dpi, bbox_inches="tight")
