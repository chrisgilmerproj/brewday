import textwrap
import unittest

from fixtures import pale


class TestGrains(unittest.TestCase):

    def setUp(self):
        self.grain = pale

    def test_str(self):
        out = str(self.grain)
        self.assertEquals(out, 'pale 2-row')

    def test_format(self):
        out = self.grain.format()
        msg = textwrap.dedent("""\
            Pale 2-row Grain
            ----------------
            Color:             2 degL
            Hot Water Extract: 0.76
            Extract:           95 %""")
        self.assertEquals(out, msg)

    def test_get_dry_to_liquid_malt_weight(self):
        out = self.grain.get_dry_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 6.25)

    def test_get_liquid_to_dry_malt_weight(self):
        out = self.grain.get_liquid_to_dry_malt_weight(6.25)
        self.assertEquals(out, 5.0)

    def test_get_grain_to_liquid_malt_weight(self):
        out = self.grain.get_grain_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 3.75)

    def test_get_liquid_malt_to_grain_weight(self):
        out = self.grain.get_liquid_malt_to_grain_weight(3.75)
        self.assertEquals(out, 5.0)

    def test_get_specialty_grain_to_liquid_malt_weight(self):
        out = self.grain.get_specialty_grain_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 4.45)

    def test_get_liquid_malt_to_specialty_grain_weight(self):
        out = self.grain.get_liquid_malt_to_specialty_grain_weight(4.45)
        self.assertEquals(out, 5.0)
