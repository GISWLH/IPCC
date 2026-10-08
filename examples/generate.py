#!/usr/bin/env python3
"""Render deterministic, synthetic climate-figure demos and their provenance."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from ipcc_rag_search import search

NAVY, MUTED, GRID = '#182d40', '#536779', '#e3e8ec'
COLORS = {'SSP1-2.6': '#173c66', 'SSP2-4.5': '#d98725', 'SSP5-8.5': '#951b1e'}
SEED = 42
LAND = Path(__file__).with_name('data') / 'ne_110m_land.geojson'
LAND_SHA256 = '9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9'
QUERIES = {
    'scenarios': ('time_series', 'scenario uncertainty fill_between'),
    'precipitation': ('map', 'stippling'),
    'ensembles': ('distribution', 'boxplot'),
}


def style():
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 11,
        'text.color': NAVY, 'axes.labelcolor': MUTED, 'xtick.color': MUTED,
        'ytick.color': MUTED, 'axes.edgecolor': GRID, 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.titleweight': 'bold',
        'savefig.facecolor': 'white', 'figure.facecolor': 'white',
        'pdf.fonttype': 42, 'svg.fonttype': 'none',
    })


def heading(fig, number, title, subtitle):
    fig.text(0.08, 0.955, f'{number}  /  IPCC PLOTTING STYLE', fontsize=10,
             color=MUTED, weight='bold', va='top')
    fig.text(0.08, 0.897, title, fontsize=25, weight='bold', va='top')
    fig.text(0.08, 0.82, subtitle, fontsize=11, color=MUTED, va='top')
    fig.text(0.08, 0.035, 'SYNTHETIC DEMO  ·  Illustrative data, not IPCC findings or projections.',
             fontsize=9, color=MUTED)


def scenarios():
    rng = np.random.default_rng(SEED)
    years = np.arange(2020, 2101)
    t = (years - years[0]) / 80
    fig, ax = plt.subplots(figsize=(11, 6.4))
    fig.subplots_adjust(left=0.10, right=0.94, bottom=0.17, top=0.74)
    heading(fig, '01', 'Show the trajectory. Keep the uncertainty.',
            'Scenario comparison with a median line and a 5–95% synthetic ensemble range.')
    data = {}
    for (label, color), endpoint in zip(COLORS.items(), [1.0, 2.2, 4.0]):
        members = 0.2 + endpoint * t ** 1.15 + rng.normal(0, 0.30, (80, 1)) * t
        low, median, high = np.quantile(members, [0.05, 0.5, 0.95], axis=0)
        ax.fill_between(years, low, high, color=color, alpha=0.15, linewidth=0)
        ax.plot(years, median, color=color, lw=2.4, label=label)
        data[label] = {'p05': low.tolist(), 'median': median.tolist(), 'p95': high.tolist()}
    ax.set(xlim=(2020, 2100), ylim=(0, 5), xlabel='Year', ylabel='Illustrative temperature anomaly (°C)')
    ax.set_axisbelow(True)
    ax.grid(axis='y', color=GRID)
    ax.legend(loc='upper left', frameon=False, fontsize=10)
    return fig, {'years': years.tolist(), 'scenarios': data, 'ensemble_size': 80}


def precipitation():
    # Coordinate edges keep pcolormesh cells inside valid lon/lat limits.
    lon_edges = np.linspace(-180, 180, 73)
    lat_edges = np.linspace(-90, 90, 37)
    lon, lat = (lon_edges[:-1] + lon_edges[1:]) / 2, (lat_edges[:-1] + lat_edges[1:]) / 2
    xx, yy = np.meshgrid(lon, lat)
    signal = 16 * np.sin(np.deg2rad(yy * 2)) + 9 * np.cos(np.deg2rad(xx * 1.5)) * np.cos(np.deg2rad(yy))
    # An explicit synthetic rule, not a claim of calibrated confidence.
    low_agreement = np.abs(signal) < 4
    land_bytes = LAND.read_bytes()
    if hashlib.sha256(land_bytes).hexdigest() != LAND_SHA256:
        raise ValueError('The bundled Natural Earth land file failed its SHA-256 check.')
    geometries = [shape(feature['geometry']) for feature in json.loads(land_bytes)['features']]
    fig = plt.figure(figsize=(11, 6.8))
    heading(fig, '02', 'Make the pattern legible.',
            'A centered diverging scale, restrained geography, and explicit agreement marks.')
    ax = fig.add_axes([0.07, 0.25, 0.86, 0.485], projection=ccrs.Robinson())
    mesh = ax.pcolormesh(lon_edges, lat_edges, signal, transform=ccrs.PlateCarree(),
                         cmap='BrBG', vmin=-25, vmax=25, rasterized=True)
    ax.add_geometries(geometries, crs=ccrs.PlateCarree(), facecolor='none',
                      edgecolor=NAVY, linewidth=0.45)
    ax.scatter(xx[low_agreement], yy[low_agreement], transform=ccrs.PlateCarree(),
               s=1.8, color=NAVY, alpha=0.6, linewidths=0)
    ax.set_global()
    ax.spines['geo'].set_edgecolor(GRID)
    ax.gridlines(linewidth=0.4, color=NAVY, alpha=0.15)
    cax = fig.add_axes([0.25, 0.18, 0.5, 0.019])
    fig.colorbar(mesh, cax=cax, orientation='horizontal', ticks=[-25, 0, 25],
                 label='Illustrative precipitation change (%)')
    fig.text(0.50, 0.075, 'Dots: synthetic low-agreement mask  |  Geography: Natural Earth, 1:110m',
             ha='center', fontsize=9, color=MUTED)
    return fig, {'longitude': lon.tolist(), 'latitude': lat.tolist(),
                 'change_percent': signal.tolist(), 'low_agreement': low_agreement.tolist(),
                 'mask_rule': 'absolute synthetic signal < 4 percent', 'land_sha256': LAND_SHA256}


def ensembles():
    rng = np.random.default_rng(SEED)
    regions = ['West Africa', 'Mediterranean', 'South Asia', 'Northern Europe']
    fig, ax = plt.subplots(figsize=(11, 6.4))
    fig.subplots_adjust(left=0.10, right=0.94, bottom=0.19, top=0.70)
    heading(fig, '03', 'Let the spread tell the story.',
            'Regional runoff response across 40 synthetic ensemble members per scenario.')
    data = {}
    centers = np.arange(len(regions))
    for index, ((label, color), offset) in enumerate(zip(COLORS.items(), [-0.24, 0, 0.24])):
        means = np.array([3, -5, 6, 8]) * (1 + index * 0.8)
        values = rng.normal(means, np.array([5, 4, 6, 4]) * (1 + index * 0.25), (40, 4))
        boxes = ax.boxplot(values, positions=centers + offset, widths=0.19,
                           whis=(5, 95), showfliers=False, patch_artist=True,
                           medianprops={'color': color, 'linewidth': 2},
                           whiskerprops={'color': color}, capprops={'color': color})
        for box in boxes['boxes']:
            box.set(facecolor=color, edgecolor=color, alpha=0.23)
        data[label] = values.tolist()
    ax.axhline(0, color=NAVY, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.grid(axis='y', color=GRID)
    ax.set(xticks=centers, xticklabels=regions, ylabel='Illustrative runoff change (%)',
           xlim=(-0.6, 3.6), ylim=(-35, 40))
    ax.legend(handles=[Patch(facecolor=c, edgecolor='none', label=l, alpha=0.6) for l, c in COLORS.items()],
              loc='upper left', bbox_to_anchor=(0, 1.14), ncol=3, frameon=False, fontsize=10)
    fig.text(0.10, 0.095, 'Box: 25–75%  ·  Line: median  ·  Whiskers: 5–95%  ·  Outside values omitted',
             fontsize=9, color=MUTED)
    return fig, {'regions': regions, 'scenarios': data, 'ensemble_size': 40}


BUILDERS = {'scenarios': scenarios, 'precipitation': precipitation, 'ensembles': ensembles}


def generate(output: Path, formats: list[str]) -> dict:
    style()
    output.mkdir(parents=True, exist_ok=True)
    manifest = {'synthetic': True, 'seed': SEED,
                'description': 'Illustrative plotting demonstrations, not IPCC results.',
                'versions': {name: importlib.metadata.version(name) for name in ['numpy', 'matplotlib', 'Cartopy']},
                'demos': {}}
    for name, builder in BUILDERS.items():
        family, query = QUERIES[name]
        references = search(query, family=family, source_only=True, unique_files=True, limit=2)
        if not references:
            raise RuntimeError(f'No bundled style evidence found for {name}')
        fig, data = builder()
        paths = []
        for extension in formats:
            target = output / f'{name}.{extension}'
            fig.savefig(target, dpi=160)
            paths.append(target.name)
            print(target)
        plt.close(fig)
        manifest['demos'][name] = {'family': family, 'query': query, 'outputs': paths,
                                  'data': data, 'style_references': [
                                      {key: row[key] for key in ['repo', 'file_path', 'commit', 'source_path', 'chunk_id']}
                                      for row in references]}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results' / 'demos')
    parser.add_argument('--formats', nargs='+', choices=['png', 'pdf', 'svg'], default=['png', 'pdf'])
    args = parser.parse_args()
    generate(args.output_dir, args.formats)


if __name__ == '__main__':
    main()
