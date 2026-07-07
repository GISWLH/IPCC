# -*- coding: utf-8 -*-
"""

Author: Florian Ladstädter

© Copyright 2021 [ Wegener Center && IGAM ] / UniGraz
"""
# Standard Library
import logging

# Third party
import numpy as np

logger = logging.getLogger(__name__)


def get_regr_params(ds, varname):
    """"""
    regr_params = {}
    k_trend_idx = list(np.atleast_1d(ds["regr_coef_names"].values)).index("trend_index")
    k_trend = ds["k"].isel(k=k_trend_idx)
    try:
        k_const_idx = list(np.atleast_1d(ds["regr_coef_names"].values)).index("const")
        k_const = ds["k"].isel(k=k_const_idx)
        k_variab = ds["regr_coef_names"].drop_sel(k=[k_trend, k_const]).k
    except ValueError:
        logger.debug("Cannot determine variability regression coef names.")
        k_variab = None

    pvars = [
        v
        for v in ds.data_vars
        if v.startswith(varname + "_params_") and not v.endswith("_not_weighted")
    ]
    if len(pvars) != 1:
        raise ValueError(
            f"Could not uniquely determine trend variable name; found: {pvars};\n"
            f"searched for {varname + '_params_'};\n"
            f"have: {list(ds.data_vars)}"
        )

    regr_params["model_name"] = pvars[0].strip(varname + "_params_")

    param_name = pvars[0]
    stderror_name = param_name.replace("_params_", "_bse_")
    stderror_corr_name = param_name.replace("_params_", "_bse_corrected_")
    reconstr_vec_name = param_name.replace("_params_", "_reconstr_vector_")
    pvalue_name = param_name.replace("_params_", "_pvalues_")

    # Calculate the explained variability, without constant and linear trend part
    try:
        reconstr_variab = ds[reconstr_vec_name].sel(k=k_variab).sum("k")

        # Calculate anomalies minus the explained variability, without linear trend part
        # i.e., the residual plus trend.
        if reconstr_variab.sum() != 0:
            regr_params["resid_and_trend"] = ds[varname] - reconstr_variab
        else:
            regr_params["resid_and_trend"] = None
    except KeyError:
        logger.debug("No reconstructed vector information found in file.")
        pass

    # Standard error. For OLS, use the manually corrected one; for GLSAR,
    # an AR(1) process is already assumed in the model.
    try:
        if regr_params["model_name"] == "OLS":
            logger.info("Use *corrected* BSE value instead of standard one.")
            regr_params["bse_trend"] = ds[stderror_corr_name].sel(k=k_trend)
        else:
            regr_params["bse_trend"] = ds[stderror_name].sel(k=k_trend)
    except KeyError:
        logger.debug("No stderror information found in file.")
        pass

    # p value (careful! this value is not corrected for autocorrelated residuals!)
    try:
        regr_params["pvalue_trend_uncorrected"] = ds[pvalue_name].sel(k=k_trend)
    except KeyError:
        logger.debug("No pvalue found in file.")
        pass

    # Get decadal trends
    regr_params["regr"] = ds[param_name].sel(
        k=k_trend
    ) * determine_trend_factor_for_decadal(ds)

    # Confidence interval from standard error. Since we have the corrected SE for OLS,
    # it is better to calculate the 95% confidence interval here instead of taking the
    # one contained in conf_interval, which is not corrected.
    # The confidence interval is this value on either side of the trend value
    try:
        regr_params["conf_interv_95"] = (
            regr_params["bse_trend"] * 1.96 * determine_trend_factor_for_decadal(ds)
        )
    except KeyError:
        pass

    return regr_params


def determine_trend_factor_for_decadal(ds):
    """
    Determine time resolution and corresponding decadal trend factor.

    Using the time coordinate of the incoming dataset,
    determine the time spacing and choose the appropriate
    factor to multiplicate the trend values with to get decadal
    trends. E.g., for monthly resolution the factor is 120,
    for yearly it is 10.

    ds: xarray dataset containing the "time" coordinate
    returns: factor (integer)
    """
    factor = None
    try:
        timesteps = ds["time"].diff("time").values.astype("timedelta64[D]")
    except KeyError:
        logger.warning("time variable not found, assume monthly resolution.")
        factor = 120
    else:
        timesteps_unique = np.unique(timesteps)
        if timesteps_unique.min() >= np.timedelta64(
            28, "D"
        ) and timesteps_unique.max() <= np.timedelta64(31, "D"):
            logger.debug(
                "Trend seems to be computed on monthly time steps, calculate decadal trends from that."
            )
            factor = 120
        elif timesteps_unique.min() >= np.timedelta64(
            365, "D"
        ) and timesteps_unique.max() <= np.timedelta64(366, "D"):
            logger.debug(
                "Trend seems to be computed on yearly time steps, calculate decadal trends from that."
            )
            # Consistency checks with trend index coordinate, to be sure
            try:
                trend_indices_steps = ds["trend_index"].diff("time").values
            except KeyError:
                raise NotImplementedError(
                    "Yearly time steps, and no 'trend_index' dimension found to verify "
                    "that trend is calculated per month. Not sure what to do."
                )
            else:
                trend_ind_unique = np.unique(trend_indices_steps)
                if len(trend_ind_unique) != 1 or trend_ind_unique[0] != 12:
                    raise ValueError(
                        "Cannot safely interpret the unit of trend values. Needs manual check."
                    )
                factor = 120
        else:
            raise ValueError(
                f"Trends seem to be computed on time steps other than "
                f"monthly or yearly ({timesteps_unique.min()}), this is not implemented."
            )
    return factor
