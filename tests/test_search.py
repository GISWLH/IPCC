"""Behavioral coverage for retrieval; no third-party test dependencies."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from ipcc_rag_search import FAMILIES, bundled_source, load_chunks, search


def chunk(name='plot.py', **overrides):
    return {'repo': 'Chapter', 'file_path': name, 'chunk_id': name,
            'chunk_type': 'code', 'plot_family': ['map'],
            'language': 'Python', 'text': 'map precipitation hatching',
            'commit': 'a' * 40, **overrides}


class SearchTests(unittest.TestCase):
    def test_family_and_repo_filters(self):
        rows = [chunk(), chunk('other.py', repo='Other', plot_family=['scatter'])]
        self.assertEqual(len(search('map', chunks=rows, family='map', repo='chapter')), 1)
        self.assertEqual(search('map', chunks=rows, family='distribution'), [])

    def test_no_match_and_empty_query(self):
        self.assertEqual(search('zzzzzz', chunks=[chunk()]), [])
        self.assertEqual(search('!!!', chunks=[chunk()]), [])

    def test_limit_must_be_positive(self):
        for limit in [0, -1]:
            with self.assertRaises(ValueError):
                search('map', chunks=[], limit=limit)

    def test_best_chunk_per_file_and_rank(self):
        rows = [chunk(text='map', chunk_id='a'), chunk(text='map ' * 8, chunk_id='b'),
                chunk('second.py', text='map')]
        result = search('map', chunks=rows, unique_files=True)
        self.assertEqual([row['chunk_id'] for row in result], ['b', 'second.py'])
        self.assertGreater(result[0]['score'], result[1]['score'])

    def test_normalized_paths_and_source_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Chapter').mkdir()
            (root / 'Chapter' / 'plot.py').write_text('pass')
            rows = [chunk(r'Chapter\\plot.py'), chunk('missing.py'),
                    chunk('Chapter/plot.py', chunk_type='data_dependency')]
            result = search('map', chunks=rows, source_only=True, source_root=root)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['source_path'], 'Chapter/plot.py')
            self.assertTrue(result[0]['source_available'])
            self.assertIsNone(bundled_source(chunk('../outside.py'), root))
            self.assertIsNone(bundled_source(chunk(__file__), root))

    def test_excluded_checkpoint_and_cache_paths(self):
        rows = [chunk(r'Chapter\.ipynb_checkpoints\plot.py'), chunk('Chapter/__pycache__/plot.py')]
        self.assertEqual(search('map', chunks=rows), [])
        self.assertEqual(len(search('map', chunks=rows, include_checkpoints=True)), 2)

    def test_invalid_index_has_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.jsonl'
            path.write_text('\n{broken}\n')
            with self.assertRaisesRegex(ValueError, ':2: invalid index JSON'):
                list(load_chunks(path))

    def test_all_bundled_families_have_real_source_examples(self):
        for family in FAMILIES:
            with self.subTest(family=family):
                rows = search(family, family=family, source_only=True, unique_files=True, limit=3)
                self.assertEqual(len(rows), 3)
                for row in rows:
                    self.assertTrue(row['source_available'])
                    self.assertTrue(row['commit'])
                    self.assertIn(family, row['plot_family'])

    def test_cli_from_another_directory(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/search_ipcc_examples.py'),
                                 'map hatching', '--family', 'map', '--json', '--limit', '2'],
                                cwd=tempfile.gettempdir(), capture_output=True, text=True, check=True)
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row['source_available'] for row in rows))

    def test_cli_rejects_invalid_limit(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/search_ipcc_examples.py'),
                                 '--limit', '-1'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('at least 1', result.stderr)


if __name__ == '__main__':
    unittest.main()
