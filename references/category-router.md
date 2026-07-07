# IPCC Plot Category Router

Use this router internally. Do not expose categories as separate skills.

## Families

| Family | Use when request mentions | Strong source signals |
|---|---|---|
| `map` | map, region, AR6 region, NetCDF field, projection, hatching map | cartopy, Ngl, Nio, geopandas, shapely, pcolormesh, contourf |
| `time_series` | time series, trend, scenario trajectory, observed/model line | plot, geom_line, xyplot, scenario, historical, smoothing |
| `distribution` | boxplot, ensemble spread, quantile, likely range | boxplot, quantile, percentile, model spread |
| `uncertainty` | hatching, stippling, confidence, agreement, likely range | hatch, stipple, agreement, confidence, fill_between, errorbar |
| `multi_panel` | panel, subplot, figure assembly, shared legend/colorbar | subplot, GridSpec, panel labels, Figure Manager |
| `color_style` | IPCC colors, colormap, palette, colorbar, legend | colormap, colorbar, legend, RColorBrewer, cmap |
| `raster_stripes` | heatmap, raster, stripes, matrix, model-year grid | heatmap, image, pcolor, raster, computeStripes |
| `bar_hist_density` | bar, stacked bar, histogram, density | barplot, geom_bar, hist, density |
| `scatter` | scatter, relationship, regression, warming-level relationship | scatter, geom_point, regression, relationship |

## Routing Rules

1. Always include `color_style` if the user asks for "IPCC style", "美观",
   publication quality, colorbars, or legends.
2. Include `uncertainty` when the user mentions model agreement, confidence,
   hatching, stippling, quantiles, likely ranges, or error bars.
3. Include `multi_panel` when more than one panel or a chapter-style figure is
   requested.
4. Prefer `map` over `raster_stripes` when the data has lon/lat or a region
   mask. Prefer `raster_stripes` when rows/columns are semantic categories such
   as model x year.
5. For vague requests like "IPCC 风格绘图", retrieve broad examples from
   `color_style`, then route by data shape:
   - lon/lat grid -> `map`
   - time coordinate -> `time_series`
   - ensemble table -> `distribution`
   - 2D matrix -> `raster_stripes`
   - x/y paired variables -> `scatter`

## Evidence Files

Detailed evidence packs live under `references/evidence/` with one file per
family. Load only the relevant family files.
