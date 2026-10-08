#!/usr/bin/env python3
"""Find usable, source-grounded IPCC plotting examples from any working directory."""
from __future__ import annotations

import argparse
from ipcc_rag_search import FAMILIES, positive_int, print_results, search


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='*', help='Search keywords; defaults to the selected family.')
    parser.add_argument('--family', choices=FAMILIES, default='')
    parser.add_argument('--limit', type=positive_int, default=5)
    parser.add_argument('--all-types', action='store_true', help='Also include references to omitted data, text, and output artifacts.')
    parser.add_argument('--json', action='store_true', help='Emit JSONL with provenance and source availability.')
    args = parser.parse_args()
    query = ' '.join(args.query) or args.family or 'IPCC plotting style'
    try:
        results = search(query, family=args.family, limit=args.limit,
                         source_only=not args.all_types, unique_files=True)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Search failed: {exc}\n')
    print_results(results, as_json=args.json)


if __name__ == '__main__':
    main()
