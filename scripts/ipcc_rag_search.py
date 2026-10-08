#!/usr/bin/env python3
"""Dependency-free ranked retrieval over the bundled IPCC-WG1 evidence index."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
from typing import Iterable

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHUNKS = SKILL_ROOT / 'references' / 'rag' / 'ipcc_chunks.jsonl'
SOURCE_ROOT = SKILL_ROOT / 'references' / 'source-code' / 'IPCC-WG1'
FAMILIES = (
    'bar_hist_density', 'color_style', 'distribution', 'map', 'multi_panel',
    'raster_stripes', 'scatter', 'time_series', 'uncertainty',
)
SOURCE_TYPES = frozenset({'code', 'notebook_cell_group'})


def tokenize(text: str) -> list[str]:
    return re.findall(r'[A-Za-z0-9_./-]+', text.lower())


def normalize_path(value: str) -> str:
    """Normalize both single and doubled Windows separators in the source index."""
    return re.sub(r'[/\\]+', '/', value)


def bundled_source(chunk: dict, source_root: Path = SOURCE_ROOT) -> Path | None:
    """Resolve an existing source file without allowing paths outside the bundle."""
    root = source_root.resolve()
    candidate = (root / normalize_path(chunk.get('file_path', ''))).resolve()
    if candidate.is_relative_to(root) and candidate.is_file():
        return candidate
    return None


def load_chunks(path: Path) -> Iterable[dict]:
    with path.open(encoding='utf-8') as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f'{path}:{number}: invalid index JSON: {exc.msg}') from exc


def score_chunk(query_terms: list[str], chunk: dict) -> float:
    path = normalize_path(chunk.get('file_path', '')).lower()
    families = [family.lower() for family in chunk.get('plot_family', [])]
    haystack = ' '.join([
        chunk.get('repo', ''), chunk.get('chapter', ''), chunk.get('figure_id', ''),
        chunk.get('language', ''), path, ' '.join(families), chunk.get('text', ''),
    ])
    tokens = tokenize(haystack)
    counts = Counter(tokens)
    length_norm = 1.0 + math.log1p(len(tokens))
    return sum((2.0 if term in path else 0.0)
               + (3.0 if term in families else 0.0)
               + counts.get(term, 0) / length_norm for term in query_terms)


def search(query: str, *, chunks: Iterable[dict] | None = None, family: str = '',
           repo: str = '', language: str = '', limit: int = 10,
           source_only: bool = False, unique_files: bool = False,
           include_checkpoints: bool = False,
           source_root: Path = SOURCE_ROOT) -> list[dict]:
    """Return ranked records, retaining original provenance and marking local availability."""
    if limit < 1:
        raise ValueError('limit must be at least 1')
    terms = tokenize(query)
    if not terms:
        return []
    scored = []
    for chunk in load_chunks(CHUNKS) if chunks is None else chunks:
        path = normalize_path(chunk.get('file_path', '')).lower()
        if not include_checkpoints and any(part in path.split('/') for part in ('.ipynb_checkpoints', '__pycache__')):
            continue
        if family and family not in chunk.get('plot_family', []):
            continue
        if repo and repo.lower() not in chunk.get('repo', '').lower():
            continue
        if language and language.lower() not in chunk.get('language', '').lower():
            continue
        if source_only and (chunk.get('chunk_type') not in SOURCE_TYPES or bundled_source(chunk, source_root) is None):
            continue
        score = score_chunk(terms, chunk)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda item: (-item[0], item[1].get('chunk_id', '')))
    results, seen = [], set()
    for score, chunk in scored:
        key = (chunk.get('repo', ''), normalize_path(chunk.get('file_path', '')))
        if unique_files and key in seen:
            continue
        seen.add(key)
        source = bundled_source(chunk, source_root)
        results.append({**chunk, 'score': round(score, 3),
                        'source_available': source is not None,
                        'source_path': source.relative_to(source_root.resolve()).as_posix() if source else None})
        if len(results) == limit:
            break
    return results


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('must be at least 1')
    return number


def print_results(results: list[dict], *, as_json: bool = False) -> None:
    for row in results:
        if as_json:
            print(json.dumps(row, ensure_ascii=False))
            continue
        print(f"[{row['score']:.2f}] {row.get('repo')} | {normalize_path(row.get('file_path', ''))}")
        print(f"  family={','.join(row.get('plot_family', [])) or '-'} type={row.get('chunk_type')}")
        print(f"  commit={row.get('commit') or 'unknown'} | source={'bundled' if row['source_available'] else 'reference only'}")
        excerpt = re.sub(r'\s+', ' ', row.get('text', '')).strip()
        print(f'  {excerpt[:420]}\n')
    if not results and not as_json:
        print('No matching examples. Try fewer keywords or another plot family.')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--family', choices=FAMILIES, default='')
    parser.add_argument('--repo', default='', help='Filter by upstream repository name.')
    parser.add_argument('--language', default='', help='Filter by indexed language metadata (may describe the repository).')
    parser.add_argument('--limit', type=positive_int, default=10)
    parser.add_argument('--source-only', action='store_true', help='Return only code available in the local source bundle.')
    parser.add_argument('--unique-files', action='store_true', help='Keep the best matching chunk per source file.')
    parser.add_argument('--include-checkpoints', action='store_true')
    parser.add_argument('--json', action='store_true', help='Emit one JSON record per line (JSONL).')
    args = parser.parse_args()
    options = vars(args).copy()
    as_json = options.pop('json')
    try:
        print_results(search(**options), as_json=as_json)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Search failed: {exc}\n')


if __name__ == '__main__':
    main()
