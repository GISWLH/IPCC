# Project guide

The project has three layers: the assistant skill, the local retrieval implementation, and reproducible demonstration figures. The historical IPCC-WG1 source archive supports all three as evidence; it is not the application code to modernize or execute wholesale.

## Where work belongs

- **Retrieval behavior:** `scripts/ipcc_rag_search.py` exposes `search()` and source-resolution helpers. `scripts/search_ipcc_examples.py` is the concise user interface. Tests live in `tests/test_search.py`.
- **Figure examples:** `examples/generate.py` owns synthetic data, plotting, export, and provenance recording. Supporting small inputs belong in `examples/data/` with source and checksum records.
- **Presentation:** `assets/hero.png` is the header identity. `assets/demos/` contains only the curated README previews. `assets/README.md` explains their generation.
- **Local results:** `results/demos/` receives full-resolution exports and the run manifest. These are ignored by Git; curated previews remain reviewable in `assets/demos/`.
- **Assistant guidance:** `SKILL.md`, `agents/openai.yaml`, and `references/category-router.md` direct the plotting workflow. Evidence packs are scoped by plot family.
- **Archived evidence:** `references/source-code/IPCC-WG1/` and `references/rag/` preserve original source paths and metadata. Do not refactor or reformat these as if they were maintained project code.

## Retrieval contract

The main search CLI returns existing bundled code by default, excludes notebook checkpoints and Python caches, and keeps the highest-ranked chunk per source file. JSON output is JSONL: one result object per line. Original index fields remain present, with `score`, `source_available`, and `source_path` added.

`source_path` is a normalized path relative to `references/source-code/IPCC-WG1/`, or `null` for an unbundled reference. Source resolution handles Windows separators and rejects paths that resolve outside the source root. A result’s `commit` is provenance from the index, not a guarantee that every bundled export is byte-identical to the upstream file.

`--all-types` on the main CLI includes metadata for omitted data, documents, and output artifacts. The lower-level CLI searches all record types by default and supports `--source-only`, `--unique-files`, `--repo`, `--language`, and `--include-checkpoints`. Nonpositive limits are rejected. A valid query with no matches exits successfully; JSON output is empty, while text output explains how to broaden the query.

The ranker is a lightweight keyword scorer with path and family boosts and document-length normalization. It is not BM25, embedding search, or a scientific relevance assessment. Inspect retrieved code before adapting it.

## Maintenance boundaries

There are no repository build requirements for retrieval. The optional demos use the pinned top-level packages in `requirements-demo.txt`. Upstream chapter environment files are archival inputs and are not installation instructions for this project.

The original index-building and packaging scripts mentioned in earlier documentation are not distributed here. Until a maintained regeneration pipeline is added, treat index updates as deliberate data releases: preserve provenance, document the source revision, and run retrieval checks. Do not advertise an unavailable regeneration command.
