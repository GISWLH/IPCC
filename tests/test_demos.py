"""Integration checks for optional figure generation and reproducibility."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HAS_PLOTTING = all(importlib.util.find_spec(name) is not None for name in ['numpy', 'matplotlib', 'cartopy'])
if HAS_PLOTTING:
    sys.path.insert(0, str(ROOT / 'examples'))
    import generate


@unittest.skipUnless(HAS_PLOTTING, 'Install requirements-demo.txt to validate figure generation')
class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.output = Path(cls.directory.name)
        cls.manifest = generate.generate(cls.output, ['png', 'pdf', 'svg'])

    def test_exports_are_real_png_pdf_and_svg(self):
        for name in generate.BUILDERS:
            with self.subTest(demo=name):
                png = (self.output / f'{name}.png').read_bytes()
                self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                width, height = struct.unpack('>II', png[16:24])
                self.assertEqual(width, 1760)
                self.assertGreater(height, 1000)
                self.assertGreater(len(png), 10000)
                self.assertTrue((self.output / f'{name}.pdf').read_bytes().startswith(b'%PDF-'))
                self.assertIn('<svg', (self.output / f'{name}.svg').read_text())

    def test_manifest_is_synthetic_with_local_provenance(self):
        saved = json.loads((self.output / 'manifest.json').read_text())
        self.assertEqual(saved, self.manifest)
        self.assertIs(saved['synthetic'], True)
        self.assertEqual(saved['seed'], 42)
        for demo in saved['demos'].values():
            self.assertEqual(len(demo['style_references']), 2)
            for reference in demo['style_references']:
                self.assertEqual(len(reference['commit']), 40)
                self.assertTrue((ROOT / 'references/source-code/IPCC-WG1' / reference['source_path']).is_file())

    def test_scenario_quantiles_and_map_shapes(self):
        data = self.manifest['demos']['scenarios']['data']
        for scenario in data['scenarios'].values():
            self.assertEqual(len(scenario['median']), len(data['years']))
            for low, median, high in zip(scenario['p05'], scenario['median'], scenario['p95']):
                self.assertLessEqual(low, median)
                self.assertLessEqual(median, high)
        grid = self.manifest['demos']['precipitation']['data']
        self.assertEqual(len(grid['change_percent']), len(grid['latitude']))
        self.assertTrue(all(len(row) == len(grid['longitude']) for row in grid['change_percent']))
        self.assertEqual(grid['land_sha256'], hashlib.sha256(generate.LAND.read_bytes()).hexdigest())

    def test_seed_reproduces_arrays(self):
        for name in ['scenarios', 'ensembles']:
            figure, data = generate.BUILDERS[name]()
            try:
                self.assertEqual(data, self.manifest['demos'][name]['data'])
            finally:
                generate.plt.close(figure)


if __name__ == '__main__':
    unittest.main()
