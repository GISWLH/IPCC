#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


FAMILIES = {
    "map",
    "time_series",
    "distribution",
    "uncertainty",
    "multi_panel",
    "color_style",
    "raster_stripes",
    "bar_hist_density",
    "scatter",
}


def find_search_script() -> Path:
    here = Path(__file__).resolve()
    local_script = here.with_name("ipcc_rag_search.py")
    local_index = here.parents[1] / "references" / "rag" / "ipcc_chunks.jsonl"
    if local_script.exists() and local_index.exists():
        return local_script

    for parent in here.parents:
        repo_script = parent / "scripts" / "ipcc_rag_search.py"
        repo_index = parent / "manifests" / "rag" / "ipcc_chunks.jsonl"
        if repo_script.exists() and repo_index.exists():
            return repo_script
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        repo_script = parent / "scripts" / "ipcc_rag_search.py"
        repo_index = parent / "manifests" / "rag" / "ipcc_chunks.jsonl"
        if repo_script.exists() and repo_index.exists():
            return repo_script
    raise SystemExit("Cannot find ipcc_rag_search.py with a matching RAG index")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", help="Search query.")
    parser.add_argument("--family", choices=sorted(FAMILIES), default="")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    script = find_search_script()
    query = " ".join(args.query) or args.family or "IPCC plotting style"
    cmd = [sys.executable, str(script), query, "--limit", str(args.limit)]
    if args.family:
        cmd.extend(["--family", args.family])
    if args.json:
        cmd.append("--json")
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
