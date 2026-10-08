#!/usr/bin/env python3
"""Reproduce the source-coverage inventory used in the project documentation."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

from ipcc_rag_search import CHUNKS, FAMILIES, SKILL_ROOT, SOURCE_ROOT, SOURCE_TYPES, bundled_source, load_chunks


def figure_targets(repository: str) -> list[str]:
    """Conservatively interpret explicit figure names, preserving box/FAQ scope.

    Panels a/b collapse to their parent figure; a numbered bundle expands to
    separate targets. Chapter-wide repositories have no inferred figure count.
    """
    match = re.fullmatch(r'Chapter-(\d+)_(?:(.+)_)?Fig(?:ure)?([\d.a-z_]+)', repository, re.I)
    if match:
        chapter, scope, labels = match.groups()
        prefix = f'Chapter {int(chapter)}'
        if scope:
            prefix += f' / {scope}'
        result = []
        for label in labels.split('_'):
            if '.' in label:
                number_chapter, label = label.split('.', 1)
                if int(number_chapter) != int(chapter):
                    raise ValueError(f'Conflicting chapter/figure identifier: {repository}')
            number = re.fullmatch(r'(\d+)[a-z]?', label, re.I)
            if not number:
                raise ValueError(f'Unrecognized figure identifier: {repository}')
            result.append(f'{prefix} / Figure {int(number.group(1))}')
        return result
    for pattern, prefix in [
        (r'Box_TS(\d+)_Fig(\d+)', 'Technical Summary / Box {box}'),
        (r'TS_Box(\d+)_Figure(\d+)', 'Technical Summary / Box {box}'),
    ]:
        match = re.fullmatch(pattern, repository, re.I)
        if match:
            box, number = map(int, match.groups())
            return [prefix.format(box=box) + f' / Figure {number}']
    match = re.fullmatch(r'TS_Fig(\d+)', repository, re.I)
    if match:
        return [f'Technical Summary / Figure {int(match.group(1))}']
    if re.search(r'fig(?:ure)?\d', repository, re.I):
        raise ValueError(f'Figure-named repository requires an explicit counting rule: {repository}')
    return []


def inventory() -> dict:
    records = list(load_chunks(CHUNKS))
    by_repo = defaultdict(list)
    for record in records:
        by_repo[record['repo']].append(record)
    repositories, targets = [], {}
    for name, rows in sorted(by_repo.items()):
        labels = figure_targets(name)
        has_code = any(r.get('chunk_type') in SOURCE_TYPES and bundled_source(r) is not None for r in rows)
        repositories.append({'repository': name, 'figure_targets': labels,
                             'has_bundled_code': has_code, 'index_records': len(rows)})
        for label in labels:
            target = targets.setdefault(label, {'label': label, 'repositories': [], 'has_bundled_code': False})
            target['repositories'].append(name)
            target['has_bundled_code'] |= has_code
    figure_repos = [r for r in repositories if r['figure_targets']]
    return {
        'method': 'Explicit repository-name targets; panel suffixes collapsed; numbered bundles expanded; chapter/box/FAQ scopes preserved. Code availability is assessed at repository level, not per panel.',
        'metrics': {
            'upstream_repositories': len(repositories),
            'figure_specific_repositories': len(figure_repos),
            'figure_specific_repositories_with_bundled_code': sum(r['has_bundled_code'] for r in figure_repos),
            'named_figure_targets': len(targets),
            'targets_in_repositories_with_bundled_code': sum(t['has_bundled_code'] for t in targets.values()),
            'index_records': len(records),
            'code_and_notebook_records': sum(r.get('chunk_type') in SOURCE_TYPES for r in records),
            'bundled_source_files': sum(p.is_file() for p in SOURCE_ROOT.rglob('*')),
            'plot_families': len(FAMILIES),
        },
        'paper_count': None,
        'paper_count_note': 'No deduplicated paper bibliography is distributed; a paper count cannot be established from this corpus.',
        'figure_targets': sorted(targets.values(), key=lambda t: t['label']),
        'repositories': repositories,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the committed inventory is stale.')
    args = parser.parse_args()
    destination = SKILL_ROOT / 'docs' / 'corpus-audit.json'
    report = inventory()
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if not destination.is_file() or destination.read_text(encoding='utf-8') != serialized:
            parser.exit(1, 'Corpus inventory is stale. Run python scripts/audit_corpus.py.\n')
        print('Corpus inventory matches the bundled index and source files.')
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(serialized, encoding='utf-8')
    print(json.dumps(report['metrics'], indent=2))


if __name__ == '__main__':
    main()
