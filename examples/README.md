# Reproducible figure demos

Run from the repository root with Python 3.12:

```bash
python -m pip install -r requirements-demo.txt
python examples/generate.py
```

The generator writes three figures in PNG and PDF, plus `manifest.json`, to `results/demos/`. Use `--formats png pdf svg` for all export formats, or `--output-dir /path/to/output` to keep a separate run. Existing files with the same demo names in that directory are regenerated; choose another directory to preserve a previous run.

| Demo | Demonstrates | Synthetic input |
|---|---|---|
| `scenarios` | Median lines, 5–95% bands, consistent SSP colors | 80 members per scenario over 2020–2100 |
| `precipitation` | Robinson projection, zero-centered diverging scale, stippling | A trigonometric field; dots where absolute change is below 4% |
| `ensembles` | Grouped boxes and percentile whiskers | 40 members for each of four regions and three scenarios |

These are independent, original demonstrations of plotting conventions. They do not reproduce an assessed IPCC figure or provide projections. Scenario labels, region names, and physical units illustrate presentation only. The map mask is not a significance test or a computed model-agreement statistic.

The manifest records the fixed random seed, library versions, actual synthetic arrays, output filenames, and retrieved source references. The generator verifies the land layer’s SHA-256 checksum before using it. It does not download data at runtime. PNG rendering can vary with fonts and library versions; PDF files can also contain creation-time metadata, so byte-for-byte identity is not promised across environments.

## Adapt to your data

Replace arrays inside the relevant builder in `generate.py`, preserve the coordinate shapes, and revise units, baseline periods, and captions. For a real map, replace the synthetic low-agreement rule with your documented agreement calculation. For a real ensemble, specify what members represent and why the selected quantiles are appropriate. Remove the synthetic label only after all inputs and captions describe the real analysis.

Retrieve and inspect the style evidence relevant to your changes before updating a plot. Style references are recorded from the local index, not used as a source of observations or model output. Scenario color conventions can vary among IPCC figures; these demos use a consistent three-color subset.

## Refresh the README previews

After reviewing the generated figures:

```bash
python examples/generate.py --output-dir assets/demos --formats png
```

Commit the three PNG previews along with their generator changes. The generated manifest in `assets/demos/` is ignored; the complete run manifest belongs in your local results directory. The header is a separate designed asset; see [assets/README.md](../assets/README.md).

## Style reference trail

The run manifest records exact commits and the current top two source matches. Useful starting points for inspection include:

- Scenario shading: [Chapter 7, Figure 7.SM.1 Python export](../references/source-code/IPCC-WG1/Chapter-7/notebooks/115_chapter7_fig7.SM.1.py), using scenario lines with `fill_between` uncertainty bands.
- Geographic qualification: [Chapter 9, example plotting from metadata](../references/source-code/IPCC-WG1/Chapter-9/Plotting_code_and_data/Fig9_03_SST/Plot_Figure/Example_plotting_from_metadata.m), by Brodie Pearson, showing mapped fields and a stippling mask.
- Regional comparisons: [Atlas, boxplots and scatterplots](../references/source-code/IPCC-WG1/Atlas/reproducibility/projections/boxplots_TandP.R), by M. Iturbide / Santander Meteorology Group, with CC BY 4.0 attribution in the source. The original uses different percentile conventions; this demo explicitly chooses 5–95% whiskers.

These are design references. The demo implementation and synthetic data are separate from the upstream scientific calculations.
