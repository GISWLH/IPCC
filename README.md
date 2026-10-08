<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <img src="assets/hero.png" alt="IPCC Plotting Style — climate figures grounded in source" width="100%">
</p>

<h1 align="center">IPCC Plotting Style</h1>
<p align="center"><strong>An evidence-based visual language for climate research.</strong></p>
<p align="center">
  <a href="https://github.com/GISWLH/IPCC/actions/workflows/checks.yml"><img src="https://github.com/GISWLH/IPCC/actions/workflows/checks.yml/badge.svg" alt="Retrieval and demo checks"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-173c66" alt="Python 3.10 or newer for retrieval">
  <img src="https://img.shields.io/badge/Retrieval-offline-287d7d" alt="Offline retrieval">
  <a href="https://github.com/GISWLH/IPCC/stargazers"><img src="https://img.shields.io/github/stars/GISWLH/IPCC?style=flat&color=d98725" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="#overview">Overview</a> · <a href="#quick-start">Quick start</a> · <a href="#gallery">Gallery</a> · <a href="#method">Methodology</a> · <a href="CONTRIBUTING.md">Contributing</a>
</p>

<a id="overview"></a>
## Overview

**IPCC Plotting Style translates conventions from public IPCC Working Group I figure code into a reusable workflow for scientific visualization.** It combines a local evidence library, focused style guidance, and executable examples to help researchers make deliberate choices about color, layout, scenarios, and uncertainty.

Designed for Codex, Claude, and direct command-line use, the project is particularly relevant to precipitation, runoff, drought, regional water stress, and ensemble comparison. Every retrieved example retains its source provenance; every demo can be regenerated from small synthetic inputs.

| Evidence base | Audited coverage |
|---|---:|
| Upstream repositories | **135** |
| Explicitly named figure targets¹ | **122** |
| Indexed code and notebook records | **3,465** |
| Plot families | **9** |

¹ The 122 targets are inferred from **121 figure-specific repository names**, with bundled figure numbers expanded and panel variants merged. **65 targets are associated with repositories containing bundled code**; the remaining 57 have reference/metadata evidence in those figure-specific repositories. Broader chapter collections contribute additional material. These counts do not establish complete figure reproducibility or a number of papers reviewed. The [auditable inventory and counting rules](docs/corpus-methodology.md) explain the scope precisely.

**Local by design.** Retrieval uses Python’s standard library, with no API key, embedding service, or database. Independent community project; not affiliated with or endorsed by the IPCC.

<a id="quick-start"></a>
## Quick start

Python **3.10+** for retrieval; Python **3.12** is the tested environment for the optional demos.

```bash
git clone https://github.com/GISWLH/IPCC.git
cd IPCC

# Find available source code and its provenance. No installation required.
python scripts/search_ipcc_examples.py "scenario uncertainty" --family time_series --limit 3
python scripts/search_ipcc_examples.py "stippling" --family map --json
```

The main command returns the best matching chunk per available source file. Results include the upstream repository, original path, commit, and normalized local source path. `--json` emits JSONL; `--all-types` also includes references to omitted inputs, documents, and output artifacts.

For finer filtering:

```bash
python scripts/ipcc_rag_search.py "uncertainty" --repo Chapter-11 --source-only --unique-files
```

To use the assistant skill, expose this checkout as `ipcc-plotting-style` through your assistant’s skill installation mechanism, or point it to [SKILL.md](SKILL.md). Keep `scripts/` and `references/` alongside that file.

> “Create a precipitation-change map with a centered diverging scale and low-agreement stippling. Retrieve IPCC source examples, explain the design choices, and cite the original code.”

<a id="gallery"></a>
## Reproducible gallery

**All values below are synthetic.** These examples demonstrate visual conventions and are not IPCC findings or projections.

### 01 · Scenario trajectories

Median trajectories and 5–95% ensemble bands keep the central estimate and its spread visible together. Consistent scenario colors support comparison across figures.

![Synthetic scenario trajectories and uncertainty bands](assets/demos/scenarios.png)

### 02 · Spatial change and agreement

A Robinson projection, a zero-centered diverging scale, and stippling distinguish spatial patterns from their qualifications. The mask is an illustrative rule, not a statistical assessment.

![Synthetic precipitation change with illustrative low-agreement stippling](assets/demos/precipitation.png)

### 03 · Regional ensemble distributions

Grouped boxes compare four regions and three scenarios. Boxes represent the interquartile range; whiskers use 5–95% limits, with outside values omitted.

![Synthetic regional runoff distributions by scenario](assets/demos/ensembles.png)

Render all three after installing the optional plotting dependencies, preferably in a virtual environment:

```bash
python -m pip install -r requirements-demo.txt
python examples/generate.py
```

Outputs in `results/demos/` include PNG/PDF figures and a manifest recording the actual synthetic arrays, seed, package versions, and style references. Add `--formats png pdf svg` for SVG export. The small Natural Earth land layer is bundled and checksummed; rendering requires no runtime downloads. See the [demo guide](examples/README.md).

<a id="method"></a>
## From source evidence to a figure

| Stage | Technique | Purpose |
|---|---|---|
| Package | Selected scripts, code-only notebooks, and Python exports | Keep plotting evidence inspectable without large climate datasets |
| Index | Structured JSONL chunks with repository, path, commit, and family tags | Preserve a traceable connection to the source |
| Route | Nine plot families and distilled evidence packs | Match a visual task to relevant conventions |
| Retrieve | Length-normalized lexical scoring, path/family boosts, and file-level deduplication | Surface available local code for inspection |
| Adapt and verify | Source review, synthetic rendering, and provenance manifests | Turn a convention into a runnable, reviewable example |

The implementation uses **keyword retrieval**, not embeddings or model fine-tuning. Concrete terms such as `fill_between`, `boxplot`, `stippling`, and `colorbar` work well. Indexed language labels can describe an upstream repository rather than an individual file. Historical index-generation scripts are not distributed; the [methodology](docs/corpus-methodology.md) distinguishes verified implementation details from undocumented authoring history.

Supported families: `map`, `time_series`, `distribution`, `uncertainty`, `multi_panel`, `color_style`, `raster_stripes`, `bar_hist_density`, and `scatter`.

## Project map

| Location | Role |
|---|---|
| [SKILL.md](SKILL.md) | Assistant workflow and output contract |
| [scripts/](scripts/) | Retrieval commands, reusable search functions, and corpus audit |
| [examples/](examples/) · [assets/](assets/) · [results/](results/) | Demo code, curated previews, and local generated outputs |
| [references/evidence/](references/evidence/) | Guidance organized by plot family |
| [references/rag/](references/rag/) | 13,219 index records and the classification table |
| [references/source-code/](references/source-code/) | 1,141 archived source files plus a separate packaging manifest |
| [tests/](tests/) · [docs/](docs/) | Behavioral checks, methodology, provenance, and project guidance |

## Develop and verify

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-demo.txt
python -m unittest discover -s tests -v
python scripts/audit_corpus.py --check
python examples/generate.py
```

Retrieval and corpus-audit tests need no third-party packages. Demo tests explicitly skip if plotting dependencies are absent; CI installs them and runs the full suite. Read the [contributor guide](CONTRIBUTING.md) before changing sources or refreshing previews. Keep coverage claims and commands aligned across all three READMEs.

## Attribution and scope

Cite the upstream repository, source path, commit, and original authors when adapting a convention. A style reference does not replace a scientific data citation or justify an uncertainty calculation. Large climate datasets are excluded, and archived scripts may require their original environments.

The source archive retains heterogeneous upstream terms; no blanket project-wide license has been declared. Consult [provenance and licensing](docs/provenance.md) before redistribution. Natural Earth geography is public domain, with its exact source recorded [here](examples/data/README.md).

If this workflow supports your research, a GitHub star helps others discover it. Reproducible examples, issue reports, and careful source attribution make the project more useful to the community.
