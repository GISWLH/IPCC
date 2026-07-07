# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Table_11.SM.1_GSAT_anom.ipynb

# %% cell 2
import conf
from utils import computation
import data_tables

# %% cell 4
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 5
c6_tas_ssp119 = computation.select_by_metadata(c6_tas, exp="ssp119")
c6_tas_ssp126 = computation.select_by_metadata(c6_tas, exp="ssp126")
c6_tas_ssp245 = computation.select_by_metadata(c6_tas, exp="ssp245")
c6_tas_ssp370 = computation.select_by_metadata(c6_tas, exp="ssp370")
c6_tas_ssp585 = computation.select_by_metadata(c6_tas, exp="ssp585")

# %% cell 7
c5_tas = conf.cmip5.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 8
c5_tas_rcp26 = computation.select_by_metadata(c5_tas, exp="rcp26")
c5_tas_rcp45 = computation.select_by_metadata(c5_tas, exp="rcp45")
c5_tas_rcp60 = computation.select_by_metadata(c5_tas, exp="rcp60")
c5_tas_rcp85 = computation.select_by_metadata(c5_tas, exp="rcp85")

# %% cell 9
periods = {
    "2021-2040": slice(2021, 2040),
    "2041-2060": slice(2041, 2060),
    "2081-2100": slice(2081, 2100),
    "2016-2035": slice(2016, 2035),
    "2046-2065": slice(2046, 2065),
    "2020": slice(2011, 2030),
    "2030": slice(2021, 2040),
    "2040": slice(2031, 2050),
    "2050": slice(2041, 2060),
    "2060": slice(2051, 2070),
    "2070": slice(2061, 2080),
    "2080": slice(2071, 2090),
    "2090": slice(2081, 2100),
    "2100": slice(2091, 2100),
}

# %% cell 10
# root = "../data/CCBox_11.1_Table_1_GWL/CCB_11.1_Table_1_GWL_{name}_{cmip}"

# %% cell 11
def print_temperature_range(c_tas_ssp, name, cmip):

    c_tas_ssp_comb = computation.concat_xarray_with_metadata(c_tas_ssp)

    # fN = root.format(name=name, cmip=cmip)
    # data_tables.save_simulation_info_raw(fN + "_md_raw", c_tas_ssp_comb, add_tas=False)

    out = f"{name} ({len(c_tas_ssp)})\n"

    for name, period in periods.items():

        period_mean = c_tas_ssp_comb.sel(year=period).tas.mean("year")

        r = period_mean.mean().item()

        q = period_mean.quantile(q=(0.05, 0.95))

        q05 = q.sel(quantile="0.05").item()
        q95 = q.sel(quantile="0.95").item()

        out += f"{name:9s}: {r:1.1f} ({q05:1.1f}-{q95:1.1f})\n"

    # with open(fN, "w") as f:
        # f.writelines(out)

    print(out)

# %% cell 12
print_temperature_range(c6_tas_ssp119, "SSP1-1.9", "cmip6")
print_temperature_range(c6_tas_ssp126, "SSP1-2.6", "cmip6")
print_temperature_range(c6_tas_ssp245, "SSP2-4.5", "cmip6")
print_temperature_range(c6_tas_ssp370, "SSP3-7.0", "cmip6")
print_temperature_range(c6_tas_ssp585, "SSP5-8.5", "cmip6")

# %% cell 14
print_temperature_range(c5_tas_rcp26, "RCP2.6", "cmip5")
print_temperature_range(c5_tas_rcp45, "RCP4.5", "cmip5")
print_temperature_range(c5_tas_rcp60, "RCP6.0", "cmip5")
print_temperature_range(c5_tas_rcp85, "RCP8.5", "cmip5")
