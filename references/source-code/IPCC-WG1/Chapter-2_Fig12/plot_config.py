# -*- coding: utf-8 -*-
"""
Module that provides an interface to the plot style definition file.

Author: Florian Ladstädter

Code partly copied from satellites.py, sharix project (© Armin Leuprecht).

© Copyright 2021 [ Wegener Center && IGAM ] / UniGraz

"""
# Standard Library
import os

from copy import copy

# Third party
import yaml

from pkg_resources import resource_filename

_plot_config_file = resource_filename(__name__, os.path.join("data", "plotconfig.yml"))

with open(_plot_config_file, "r") as f:
    _plot_config = yaml.load(f, Loader=yaml.Loader)


class PlotConfig:
    """This class holds the datatype-specific settings relevant to
    plotting.

    """

    def __init__(self):
        self._plotconfig = copy(_plot_config["datatype_settings"])
        self._names = {}
        for v in list(self._plotconfig.keys()):
            self._plotconfig[v]["name"] = v
            self._names[v] = v

            if "label" not in self._plotconfig[v]:
                raise ValueError(f"Entry {v} misses the mandatory 'label' entry.")

        self._names.update(self._get_alternative_names())

    def _get_alternative_names(self):
        alt_names = {}
        for k, v in self._plotconfig.items():
            if (v["label"] != k) and (v["label"] in list(self._plotconfig.keys())):
                raise ValueError(
                    f"plotconfig entry {k} contains label name ({v['label']}) which is also the key of another entry."
                )
            else:
                alt_names.update({v["label"]: k})
            if "alternative_names" in v:
                alt_names.update({vv: k for vv in v["alternative_names"]})
        return alt_names

    def __getitem__(self, key):
        try:
            return self._plotconfig[self._names[key]]
        except KeyError:
            raise KeyError(
                f"{key} not found in plotconfig (add to alternative_names?)."
            )
