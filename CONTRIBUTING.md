# Contributing

Start with the [project guide](docs/project-guide.md). Small, verifiable improvements to retrieval, figure examples, accessibility, and provenance are especially useful.

## Development setup

Retrieval needs Python 3.10+ and no third-party packages. For the complete demo workflow, use Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-demo.txt
python -m unittest discover -s tests -v
python examples/generate.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. For a headless machine, the generator already selects Matplotlib’s Agg backend.

## Before a pull request

- Run the tests and confirm both retrieval and demo tests execute when plotting code changes.
- For a figure change, inspect the PNG and PDF, verify labels and uncertainty semantics, and refresh the affected README preview using the command in [examples/README.md](examples/README.md).
- Preserve upstream source files and attribution. Add maintained code under `scripts/` or `examples/`, not inside the historical archive.
- Keep large datasets, credentials, local environments, and generated result directories out of Git.
- Describe what changed, the checks you ran, and any limitations. Include before/after previews when a visual changes.

A new demo should run on small synthetic or publicly redistributable inputs, declare its random seed and units, include its source references, and label synthetic values visibly. Avoid implying that an illustrative plot is an assessed IPCC result.

Licensing for original project material remains undeclared; see [provenance and licensing](docs/provenance.md). Do not add a blanket license to third-party code without checking its terms.
