# Provenance and licensing

## IPCC-WG1 evidence

The bundled records and source excerpts originate from public repositories in the [IPCC-WG1 GitHub organization](https://github.com/IPCC-WG1). Search results retain upstream repository names, file paths, and commit identifiers. Cite these when adapting a pattern, and consult the upstream file for authorship, context, and applicable terms.

The bundle is intentionally selective. Large climate inputs, rendered plots, and notebook outputs are omitted. Notebook markdown and outputs were removed, and Python exports were created for easier reading. Index records may still describe those excluded assets. A `source_available` value of `false` means the path cannot be inspected as a file in this bundle; it does not mean the upstream resource never existed.

Language metadata can describe the repository’s primary language instead of the individual file. Original index fields have been preserved rather than silently rewritten. Source paths also contain Windows separators; the retrieval code provides a normalized local path without changing the index.

## How to credit a figure

For a figure adapted from an upstream example, record:

1. Original authors or citation from the source, where supplied.
2. Upstream repository, file path, and commit.
3. Which design or code elements were adapted.
4. Your own input data, transformations, uncertainty definition, and output version.

A style citation is not a data citation. Demo manifests provide source pointers for design conventions; they do not establish the scientific validity of the synthetic inputs. Several source files may have identical or related content across upstream repositories.

## License status

This repository does not currently declare a blanket license for its original code and documentation. The source archive has heterogeneous upstream terms; attribution alone does not grant redistribution permission. Check the source-specific license before reusing or distributing an excerpt. A future project license needs an explicit maintainer decision and must preserve upstream exceptions.

The Natural Earth geometry used by the demos is public domain. Its pinned source and checksum are documented in [examples/data/README.md](../examples/data/README.md).

The new header was generated with an image-generation tool. Its design brief is recorded in [assets/README.md](../assets/README.md); it is a project identity, not an official IPCC mark. This repository is not affiliated with or endorsed by the IPCC.
