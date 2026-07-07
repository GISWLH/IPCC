#!/usr/bin/env python3
"""Search the local IPCC-WG1 RAG chunk index.

This is a lightweight keyword/BM25-like retriever for the first distillation
pass. It intentionally has no external dependencies.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHUNKS = SKILL_ROOT / "references" / "rag" / "ipcc_chunks.jsonl"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./-]+", text.lower())


def load_chunks(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def score_chunk(query_terms: list[str], chunk: dict) -> float:
    haystack = " ".join(
        [
            chunk.get("repo", ""),
            chunk.get("chapter", ""),
            chunk.get("figure_id", ""),
            chunk.get("language", ""),
            chunk.get("file_path", ""),
            " ".join(chunk.get("plot_family", [])),
            chunk.get("text", ""),
        ]
    )
    tokens = tokenize(haystack)
    counts = Counter(tokens)
    length_norm = 1.0 + math.log(1 + len(tokens))
    score = 0.0
    for term in query_terms:
        score += (2.0 if term in chunk.get("file_path", "").lower() else 0.0)
        score += (3.0 if term in [x.lower() for x in chunk.get("plot_family", [])] else 0.0)
        score += counts.get(term, 0) / length_norm
    return score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--family", default="", help="Filter by plot family tag.")
    parser.add_argument("--repo", default="", help="Filter by repository name substring.")
    parser.add_argument("--language", default="", help="Filter by language substring.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--include-checkpoints", action="store_true", help="Include notebook checkpoints/cache files.")
    parser.add_argument("--json", action="store_true", help="Emit JSONL records.")
    args = parser.parse_args()

    query_terms = tokenize(args.query)
    scored = []
    for chunk in load_chunks(CHUNKS):
        path = chunk.get("file_path", "").lower()
        if not args.include_checkpoints and (
            ".ipynb_checkpoints" in path or "\\__pycache__\\" in path or "/__pycache__/" in path
        ):
            continue
        if args.family and args.family not in chunk.get("plot_family", []):
            continue
        if args.repo and args.repo.lower() not in chunk.get("repo", "").lower():
            continue
        if args.language and args.language.lower() not in chunk.get("language", "").lower():
            continue
        score = score_chunk(query_terms, chunk)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    for score, chunk in scored[: args.limit]:
        if args.json:
            print(json.dumps({"score": round(score, 3), **chunk}, ensure_ascii=False))
            continue
        text = re.sub(r"\s+", " ", chunk.get("text", "")).strip()
        print(f"[{score:.2f}] {chunk.get('repo')} | {chunk.get('file_path')}")
        print(f"  family={','.join(chunk.get('plot_family', [])) or '-'} type={chunk.get('chunk_type')}")
        print(f"  {text[:420]}")
        print()


if __name__ == "__main__":
    main()
