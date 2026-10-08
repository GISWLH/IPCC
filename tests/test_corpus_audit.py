"""Verify the counting rules behind public corpus-coverage claims."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_corpus import figure_targets


class CorpusAuditTests(unittest.TestCase):
    def test_bundle_expands_into_three_targets(self):
        self.assertEqual(figure_targets('Chapter-6_Fig12_22_24'),
                         ['Chapter 6 / Figure 12', 'Chapter 6 / Figure 22', 'Chapter 6 / Figure 24'])

    def test_panels_collapse_to_the_same_figure(self):
        self.assertEqual(figure_targets('Chapter-3_Fig02b'), figure_targets('Chapter-3_Figure3.2a'))
        self.assertEqual(figure_targets('Chapter-3_Figure3.2a'), ['Chapter 3 / Figure 2'])

    def test_boxes_and_faqs_keep_their_scope(self):
        targets = [figure_targets(name)[0] for name in [
            'Chapter-3_CCBOX3.1_Fig1', 'Chapter-3_CCBOX3.2_Fig1',
            'Chapter-3_FAQ2_Fig01', 'Box_TS4_Fig1', 'TS_Box5_Figure1', 'TS_Fig12']]
        self.assertEqual(len(set(targets)), 6)
        self.assertEqual(targets[-1], 'Technical Summary / Figure 12')

    def test_chapter_collections_do_not_invent_counts(self):
        for name in ['Chapter-9', 'Atlas', 'CEDA_IPCC_AR6_WGI_Figures_data', 'colormaps']:
            self.assertEqual(figure_targets(name), [])

    def test_ambiguous_names_require_an_explicit_rule(self):
        for name in ['Other_Fig3', 'Chapter-3_Figure4.2']:
            with self.assertRaises(ValueError):
                figure_targets(name)


if __name__ == '__main__':
    unittest.main()
