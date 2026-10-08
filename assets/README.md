# Visual assets

## Header identity

`hero.png` is a generated, minimalist wordmark for **IPCC Plotting Style**. An open globe contour and three trajectories connect geography, scenario comparison, and scientific plotting. The palette is midnight navy, blue, muted teal, and warm rust on an off-white background.

Design brief: a wide horizontal banner with generous negative space; a precise, flat geometric globe/trajectory symbol to the left; “IPCC” and “PLOTTING STYLE” to the right; the line “Climate figures. Grounded in source.” No decorative weather icons, shadows, 3D effects, or official institutional emblems. Generated with the available image-generation tool from the previous header as redesign context.

This identity belongs to an independent community project and must not be presented as an official IPCC mark. The previous cartoon header and its generation prompt are retained in Git history.

## Demo previews

`demos/scenarios.png`, `demos/precipitation.png`, and `demos/ensembles.png` are rendered by `examples/generate.py`; they are not image-generated charts. Regenerate them from the repository root:

```bash
python examples/generate.py --output-dir assets/demos --formats png
```

Inspect labels, legends, and margins before committing refreshed previews. Full exports and provenance manifests belong in `results/demos/`.
