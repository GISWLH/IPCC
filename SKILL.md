---
name: ipcc-plotting-style
description: Use for making, adapting, or improving climate-science figures in IPCC-WG1 style. Trigger when the user asks for IPCC style plotting, IPCC 风格绘图, publication-quality climate figures, or wants source-grounded plotting code/templates for maps, time series, uncertainty hatching, ensemble boxplots, heatmaps/stripes, multi-panel figures, colorbars, legends, bars, density plots, or scatter relationships using the local IPCC-WG1 code/RAG index.
---

# IPCC Plotting Style

Use this as the single entry point for IPCC-style plotting. Internally classify
the requested figure type, retrieve matching IPCC-WG1 source examples, then
generate aesthetically strong plotting code with provenance.

## Core Workflow

1. Classify the request into one or more plot families using
   `references/category-router.md`.
2. Retrieve source examples with `scripts/search_ipcc_examples.py`.
3. Read only the relevant evidence file(s) under `references/evidence/`.
4. Extract the visual conventions that matter: colormap, colorbar, legend,
   panel layout, uncertainty encoding, region handling, labels, and output
   format.
5. Generate or modify plotting code in the user's preferred stack. Prefer
   Python/Matplotlib/Cartopy/Xarray unless the user asks for R, MATLAB, NCL, or
   another source language.
6. Cite local source provenance: repository, file path, and commit when
   available.
7. Validate with a tiny synthetic demo or clear run instructions when real IPCC
   data is too large or absent.

## Retrieval

Use:

```bash
python skills/ipcc-plotting-style/scripts/search_ipcc_examples.py "regional map hatching AR6 regions" --family map
python skills/ipcc-plotting-style/scripts/search_ipcc_examples.py "time series scenario uncertainty" --family time_series
python skills/ipcc-plotting-style/scripts/search_ipcc_examples.py "colormap colorbar legend" --family color_style
```

The skill is self-contained for retrieval: `references/rag/ipcc_chunks.jsonl`
and `scripts/ipcc_rag_search.py` are bundled inside this skill. If the full
IPCC-skills repository is also present, the search entry point can still fall
back to the repository-level RAG index.

For vague requests like "use IPCC style", first search `color_style`, then infer
the main plot family from the user's data shape.

## Output Contract

When producing plotting code, include:

- Selected plot family or families.
- Retrieved IPCC examples used as style/code evidence.
- A concise implementation, preferably runnable with small synthetic data.
- Notes on what must be replaced by real data paths or variables.
- Visual polish: readable labels, stable layout, publication-friendly colors,
  clear colorbar/legend, and uncertainty encoding when applicable.

## Data Boundary

Do not copy large climate datasets into outputs or skills. Use local IPCC source
files as style/provenance evidence and create minimal demos with synthetic or
small sample data unless the user provides real data.

The bundled RAG index contains lightweight code/text chunks, output artifact
paths, data-dependency paths, and provenance metadata. It does not vendor the
large upstream IPCC-WG1 source mirrors or datasets.

For provenance follow-up, code-only upstream sources are bundled under
`references/source-code/IPCC-WG1/`. Ordinary scripts are copied as text files.
Notebooks are stored as code-only `.ipynb` files with outputs removed and are
also exported as `.py` files. Figures, rendered notebook outputs, and large data
files are intentionally excluded.

## Internal Evidence

Load these only as needed:

- `references/evidence/map.md`
- `references/evidence/time_series.md`
- `references/evidence/distribution.md`
- `references/evidence/uncertainty.md`
- `references/evidence/multi_panel.md`
- `references/evidence/color_style.md`
- `references/evidence/raster_stripes.md`
- `references/evidence/bar_hist_density.md`
- `references/evidence/scatter.md`
