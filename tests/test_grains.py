import textwrap
import unittest

from fixtures import pale
from fixtures import pale_add


class TestGrains(unittest.TestCase):

    def setUp(self):
        self.grain = pale

    def test_str(self):
        out = str(self.grain)
        self.assertEquals(out, 'Pale 2-row')

    def test_repr(self):
        out = repr(self.grain)
        self.assertEquals(out, "Grain('pale 2-row', short_name='2-row', color=2, hot_water_extract=293.4)")  # nopep8

    def test_format(self):
        out = self.grain.format()
        msg = textwrap.dedent("""\
            Pale 2-row Grain
            ----------------
            Color:             2 degL
            Hot Water Extract: 293.4""")
        self.assertEquals(out, msg)

    def test_get_working_yield(self):
        wy = self.grain.get_working_yield(0.70)
        self.assertEquals(round(wy, 2), 0.53)


class TestGrainAdditions(unittest.TestCase):

    def setUp(self):
        self.grain_add = pale_add

    def test_str(self):
        out = str(self.grain_add)
        self.assertEquals(out, 'Pale 2-row, weight 13.96 lbs')

    def test_repr(self):
        out = repr(self.grain_add)
        self.assertEquals(out, "GrainAddition(Grain('pale 2-row', short_name='2-row', color=2, hot_water_extract=293.4), weight=13.96)")  # nopep8

    def test_format(self):
        out = self.grain_add.format()
        msg = textwrap.dedent("""\
            Pale 2-row Addition
            ----------------
            Malt Bill:         13.96 lbs""")
        self.assertEquals(out, msg)
