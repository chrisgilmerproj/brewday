import textwrap
import unittest

from brew.cli.abv import get_abv
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS


class TestCliAbv(unittest.TestCase):
    def setUp(self):
        self.og = 1.057
        self.fg = 1.013

    def test_get_abv(self):
        abv = get_abv(self.og, self.fg)
        self.assertEquals(round(abv, 2), 5.78)

    def test_get_abv_no_og_raises(self):
        with self.assertRaises(Exception):
            get_abv(None, self.fg)

    def test_get_abv_no_fg_raises(self):
        with self.assertRaises(Exception):
            get_abv(self.og, None)

    def test_get_abv_og_fg_reversed_raises(self):
        with self.assertRaises(Exception):
            get_abv(self.fg, self.og)

    def test_get_abv_bad_units_raises(self):
        with self.assertRaises(Exception):
            get_abv(self.og, self.og, units='bad')

    def test_get_abv_units_imperial(self):
        abv = get_abv(self.og, self.fg, units=IMPERIAL_UNITS)
        self.assertEquals(round(abv, 2), 5.78)

    def test_get_abv_units_si(self):
        abv = get_abv(self.og, self.fg, units=SI_UNITS)
        self.assertEquals(round(abv, 2), 5.78)

    def test_get_abv_alternative(self):
        abv = get_abv(self.og, self.fg, alternative=True)
        self.assertEquals(round(abv, 2), 5.95)

    def test_get_abv_refractometer(self):
        abv = get_abv(self.og, self.fg, refractometer=True)
        self.assertEquals(round(abv, 2), 6.97)

    def test_get_abv_alternative_refractometer(self):
        abv = get_abv(self.og, self.fg, alternative=True, refractometer=True)
        self.assertEquals(round(abv, 2), 7.12)

    def test_get_abv_verbose(self):
        out = get_abv(self.og, self.fg, verbose=True)
        expected = textwrap.dedent("""\
            OG     : 1.057
            OG Adj : 1.057
            OG Temp: 59.00 F
            FG     : 1.013
            FG Adj : 1.013
            FG Temp: 59.00 F
            ABV    : 5.78 %""")
        self.assertEquals(out, expected)
