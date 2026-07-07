# -*- coding: utf-8 -*-
"""
Module that provides an interface to the pressure-altitude mapping file.

Author: Florian Ladstädter

© Copyright 2021 [ Wegener Center && IGAM ] / UniGraz

"""
# Standard Library
import os

# Third party
import xarray as xr

from pkg_resources import resource_filename

_pres_mapping_file = resource_filename(
    __name__, os.path.join("data", "pressure_mapping.nc")
)

with xr.open_dataset(_pres_mapping_file) as ds_pres_mapping:
    ds_pres_mapping.load()


def pressure_mapping(lat_bounds):
    return ds_pres_mapping.sel(latitude_bins=slice(lat_bounds[0], lat_bounds[1])).mean(
        "latitude_bins"
    )
