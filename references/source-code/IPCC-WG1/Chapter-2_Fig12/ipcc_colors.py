"""
Author: Martin Jury

© Copyright 2019 Wegener Center / UniGraz
"""
# Standard Library
import os

# Third party
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

from pkg_resources import resource_filename

_ipcc_colormaps_dir = resource_filename(
    __name__, os.path.join("data", "IPCC-WG1-colormaps")
)


def load_colors(
    color_table, Ncolors=256, reverse=False, path_to_ctabels=_ipcc_colormaps_dir
):
    """
    loads IPCC color tables according to color_table (str, also listed under colors_dic

    discrete_colormaps are of maximum Ncolor=21
    categorical_colors are returned as np array
    """

    # for sub in ['categorical_colors_rgb_0-255','continuous_colormaps_rgb_0-255','discrete_colormaps_rgb_0-255']:
    #     files = os.listdir(os.path.join(colors_dir_path, sub))
    #     files = [f[:-4] for f in files if f[-4:] == '.txt']
    #     print('{}:{}'.format(sub,files))
    colors_dic = {
        "categorical_colors_rgb_0-255": [
            "bright_cat",
            "chem_cat",
            "cmip_cat",
            "contrast_cat",
            "dark_cat",
            "gree-blue_cat",
            "rcp_cat",
            "red-yellow_cat",
            "spectrum_cat",
            "ssp_cat_1",
            "ssp_cat_2",
        ],
        "continuous_colormaps_rgb_0-1": [
            "chem_div",
            "chem_seq",
            "cryo_div",
            "cryo_seq",
            "misc_div",
            "misc_seq_1",
            "misc_seq_2",
            "misc_seq_3",
            "prec_div",
            "prec_seq",
            "slev_div",
            "slev_seq",
            "temp_div",
            "temp_seq",
            "wind_div",
            "wind_seq",
        ],
        "discrete_colormaps_rgb_0-255": [
            "chem_div_disc",
            "chem_seq_disc",
            "cryo_div_disc",
            "cryo_seq_disc",
            "misc_div_disc",
            "misc_seq_1_disc",
            "misc_seq_2_disc",
            "misc_seq_3_disc",
            "prec_div_disc",
            "prec_seq_disc",
            "slev_div_disc",
            "slev_seq_disc",
            "temp_div_disc",
            "temp_seq_disc",
            "wind_div_disc",
            "wind_seq_disc",
        ],
    }

    if not any([color_table in vs for k, vs in colors_dic.items()]):  # for v in vs]:
        raise NotImplementedError("Colortable {} not found".format(color_table))

    for k, vs in colors_dic.items():
        if color_table in vs:
            subdir = k
            break

    if subdir == "continuous_colormaps_rgb_0-1":
        rgb_in_txt = np.loadtxt(
            os.path.join(path_to_ctabels, subdir, color_table + ".txt")
        )
        if reverse:
            rgb_in_txt = rgb_in_txt[::-1]
        cm = mcolors.LinearSegmentedColormap.from_list(
            color_table, rgb_in_txt, N=Ncolors
        )
        return cm
    elif subdir == "categorical_colors_rgb_0-255":
        rgb_in_txt = np.loadtxt(
            os.path.join(path_to_ctabels, subdir, color_table + ".txt")
        )
        rgb_in_txt = rgb_in_txt / 255.0
        return rgb_in_txt
    elif subdir == "discrete_colormaps_rgb_0-255":
        if Ncolors > 21:
            print("{} only available for maxminum of 21 colors".format(subdir))
            print("Setting Number of colors to 21")
            Ncolors = 21
        df = pd.read_csv(os.path.join(path_to_ctabels, subdir, color_table + ".txt"))

        str_key_table = "_".join(color_table.split("_")[:-1])

        for idx in df.index:
            strcell = str(df.iloc[idx].values[0])
            if str_key_table in strcell and int(strcell.split("_")[-1]) == Ncolors:
                col_data = df.iloc[idx + 1 : idx + Ncolors + 1].values
                col_data = [[int(da) for da in dat[0].split(" ")] for dat in col_data]
                rgb_in_txt = np.array(col_data)
                break
        rgb_in_txt = rgb_in_txt / 255.0
        if reverse:
            rgb_in_txt = rgb_in_txt[::-1]
        cm = mcolors.LinearSegmentedColormap.from_list(
            color_table + "_" + str(Ncolors), rgb_in_txt, N=Ncolors
        )
        return cm
