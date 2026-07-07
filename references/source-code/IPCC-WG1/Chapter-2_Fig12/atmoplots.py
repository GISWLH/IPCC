#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Author: Florian Ladstädter

© Copyright 2021 [ Wegener Center && IGAM ] / UniGraz
"""
# Standard Library
import logging
import os
import sys

# Third party
import click

# First party
from atmoplots import vertical

mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.WARNING)


class GlobOptions(object):
    def __init__(self, output_dir, output_format="png", debug=False, dpi=200):
        if debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(
            level=level,
            handlers=[
                logging.FileHandler(
                    os.path.join(output_dir, f"{os.path.basename(sys.argv[0])}.log")
                ),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.output_dir = output_dir
        self.output_format = output_format
        self.dpi = dpi


@click.group()
@click.option("--output-dir", required=True, type=click.Path(exists=True))
@click.option("--debug/--no-debug", default=False, show_default=True)
@click.option(
    "--output-format",
    default="png",
    show_default=True,
    type=click.Choice(["png", "pdf", "ps", "eps"]),
)
@click.option(
    "--dpi",
    default=200,
    show_default=True,
    type=float,
    help="dpi of raster image.",
)
@click.pass_context
def atmoplots(ctx, output_dir, debug, output_format, dpi):
    ctx.ensure_object(dict)
    ctx.obj = GlobOptions(output_dir, output_format, debug, dpi)
    logging.info(f"Command: {sys.argv[0]} {' '.join(sys.argv[1:])}")


@atmoplots.command()
@click.option(
    "--data",
    multiple=True,
    type=click.Tuple([str, click.Path(exists=True)]),
    help="Label and filepath of data to plot.",
)
@click.option(
    "--var-to-plot",
    required=True,
    help="Base variable name to plot, e.g. 'dry_temperature_anomalies'",
)
@click.option(
    "--vertical-dim",
    default="altitude",
    show_default=True,
    type=click.Choice(["altitude", "pressure", "impact_altitude"]),
    help="The coordinate to be used as y-axis.",
)
@click.option(
    "--vertical-limits",
    nargs=2,
    type=float,
    default=(0, 30000),
    show_default=True,
    help="Specify lower and upper limit for vertical dimension. "
    "In (m) for altitude and (Pa) for pressure vertical dim. "
    "Example: '0 30000' (m) or '100000 1000' (Pa).",
)
@click.option(
    "--xlim",
    nargs=2,
    type=float,
    help="Overrule x-limits for horizontal axis.",
)
@click.option(
    "--mask-below",
    type=float,
    default=None,
    help="Specify below which altitude level RO should be masked "
    "(Recommendation: 8000 for tropics, 5000 outside).",
)
@click.option(
    "--smooth-all",
    type=float,
    help="Smooth all datasets over the given value (in meters); "
    "only for datasets on altitude, overrides values in the config.",
)
@click.option(
    "--add-secondary-axis/--no-add-secondary-axis",
    default=False,
    show_default=True,
    help="Add secondary axis with corresponding pressure or altitude levels.",
)
@click.option(
    "--method-pres-to-alt",
    default="empirical",
    type=click.Choice(["empirical", "simple"]),
    help="How to convert pressure grids to altitude. "
    "empirical: Use RO average pres-to-alt mapping for the lat range; "
    "simple: Use constant log height scale (pressure altitude)",
)
@click.option(
    "--ipcc-style/--no-ipcc-style",
    default=True,
    show_default=True,
    help="Use IPCC color scheme.",
)
@click.option(
    "--errorbar/--no-errorbar",
    default=False,
    show_default=True,
    help="Add errorbar.",
)
@click.option(
    "--ncols",
    type=int,
    default=3,
    help="Specify number of columns to be used in the legend.",
)
@click.option(
    "--add-title/--no-add-title",
    default=True,
    show_default=True,
    help="Add plot title.",
)
@click.option(
    "--filename-prefix",
    default="",
    help="Prepend this string to the filename, to manually "
    "enforce unique filenames if required.",
)
@click.pass_obj
def verticaltrends(
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
    ncols,
    add_title,
    filename_prefix,
):
    vertical.plot_verticaltrends(
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
        ncols,
        add_title,
        filename_prefix,
    )


if __name__ == "__main__":
    atmoplots()
