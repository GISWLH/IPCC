# Corpus coverage and methodology

The figures below are reproducible measurements of this repository’s bundled index and source files. They describe the available evidence, not a claim that every IPCC figure has been reproduced or that a specified number of papers was reviewed.

## What is counted

| Measure | Count | Definition |
|---|---:|---|
| Upstream repositories | 135 | Distinct `repo` values in the index |
| Figure-specific repositories | 121 | Repository names containing an explicit, recognized figure identifier |
| Named figure targets | 122 | Explicit repository-name identifiers, normalized as described below |
| Targets in repositories with bundled code | 65 | Named targets whose associated repository has at least one indexed code or notebook record resolving to a local source file |
| Figure-specific repositories with bundled code | 64 | Repository-level source availability; the other 57 contain metadata/reference records only |
| Total index records | 13,219 | All nonempty JSONL records, including code, text, data dependencies, and output references |
| Code and notebook records | 3,465 | Records typed `code` or `notebook_cell_group`; these may overlap or repeat content |
| Bundled source files | 1,141 | Files under `references/source-code/IPCC-WG1/`; the separate packaging manifest is not counted as source code |
| Plot families | 9 | Categories exposed by the retrieval interface |

**Paper count: not established.** The bundle does not contain a deduplicated bibliography of papers. Repository, chunk, and figure counts must not be relabeled as publication counts.

### Figure-counting rules

The count of **122 named figure targets** is derived from repository names, not from an audit of all figure panels or all output files:

- `Chapter-6_Fig12_22_24` contributes three targets: Figures 6.12, 6.22, and 6.24.
- `Chapter-3_Fig02b` and `Chapter-3_Figure3.2a` contribute one parent target: Figure 3.2. Panels are not counted as separate figures.
- Chapter, box, FAQ, and Technical Summary scopes are retained so unrelated “Figure 1” identifiers are not merged.
- Chapter-wide repositories such as `Chapter-9` can contain further figures, but this conservative inventory does not infer targets from their internal filenames.

The **65** figure targets associated with available code inherit that status from their repositories. It does not prove that all code, panels, data, or dependencies needed for any one target are present. The remaining **57** named targets have only metadata/reference evidence within their figure-specific repositories. Related code might also exist in a broader chapter repository; that cross-repository reconciliation is outside this count.

The complete target-to-repository mapping and code-availability flags are recorded in [corpus-audit.json](corpus-audit.json). No estimate of distinct papers or exhaustive assessment-wide figure coverage is implied.

## Techniques in the distributed workflow

1. **Selective source packaging.** The archive retains plotting scripts and code-only notebooks, with Python exports for inspection. Large scientific datasets, rendered outputs, and notebook narrative cells are excluded. A packaging manifest accompanies the archive.
2. **Structured evidence indexing.** JSONL records carry text or code excerpts together with upstream repository, file path, commit, record type, and plot-family tags. The index also retains references to excluded inputs and outputs for context.
3. **Plot-family routing and distilled guidance.** A nine-family taxonomy routes requests to maps, time series, distributions, uncertainty, multi-panel layouts, color style, raster/stripes, bars/density, and scatter plots. Evidence packs summarize relevant conventions and provide excerpts for source inspection.
4. **Local lexical retrieval.** The ranker uses case-insensitive tokens, term frequency normalized by document length, and explicit path/family boosts. The main CLI restricts results to available code, excludes caches/checkpoints, and keeps the best chunk per file. This is keyword retrieval, not embedding search or model fine-tuning.
5. **Provenance-aware adaptation and validation.** An assistant or researcher reads the source before adapting a convention. The demos render deterministic synthetic inputs and export figures with a manifest of source references, actual arrays, seed, and package versions. This checks the plotting workflow, not the scientific validity of a real-world analysis.

The current score adds, for each query token, a path-substring boost of 2, an exact family-tag boost of 3, and token frequency divided by `1 + ln(1 + token_count)`. Ranking is deterministic, with chunk identifiers breaking ties. See [the retrieval implementation](../scripts/ipcc_rag_search.py).

These statements describe the distributed artifacts and executable implementation. The original index-generation and distillation scripts are not included. Their exact historical extraction procedure, any model used during authoring, and any manual-review protocol are not established by this package and are not claimed here.

## Reproduce the audit

From the repository root, using Python 3.10+ and no third-party packages:

```bash
python scripts/audit_corpus.py          # Regenerate the committed JSON inventory.
python scripts/audit_corpus.py --check  # Verify it without rewriting files.
```

The audit fails on a new figure-named repository that lacks an explicit parsing rule, so it cannot silently disappear from the inventory. Reconcile scope and panel naming before extending the rules. After changing the corpus, update the audited numbers and explanation in all three READMEs together.

For authorship and reuse terms, see [provenance and licensing](provenance.md).
