import textwrap
import unittest

from brew.cli.abv import get_abv
from brew.cli.abv import get_parser
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


class TestCliArgparser(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser_required_og_and_fg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_get_parser_required_og(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-f', '1.010'])

    def test_get_parser_required_fg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-o', '1.060'])

    def test_get_parser_og_and_fg(self):
        args = ['-o', '1.060', '-f', '1.010']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': False,
            'fg': 1.01,
            'fg_temp': 59.0,
            'og': 1.06,
            'og_temp': 59.0,
            'refractometer': False,
            'units': 'imperial',
            'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_update_temp(self):
        args = ['-o', '1.060', '-f', '1.010',
                '--og-temp', '61.0',
                '--fg-temp', '61.0']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': False,
            'fg': 1.01,
            'fg_temp': 61.0,
            'og': 1.06,
            'og_temp': 61.0,
            'refractometer': False,
            'units': 'imperial',
            'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_alternative(self):
        args = ['-o', '1.060', '-f', '1.010', '--alternative']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': True,
            'fg': 1.01,
            'fg_temp': 59.0,
            'og': 1.06,
            'og_temp': 59.0,
            'refractometer': False,
            'units': 'imperial',
            'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_refractometer(self):
        args = ['-o', '1.060', '-f', '1.010', '--refractometer']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': False,
            'fg': 1.01,
            'fg_temp': 59.0,
            'og': 1.06,
            'og_temp': 59.0,
            'refractometer': True,
            'units': 'imperial',
            'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_units(self):
        args = ['-o', '1.060', '-f', '1.010', '--units', 'si']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': False,
            'fg': 1.01,
            'fg_temp': 59.0,
            'og': 1.06,
            'og_temp': 59.0,
            'refractometer': False,
            'units': 'si',
            'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_verbose(self):
        args = ['-o', '1.060', '-f', '1.010', '-v']
        out = self.parser.parse_args(args)
        expected = {
            'alternative': False,
            'fg': 1.01,
            'fg_temp': 59.0,
            'og': 1.06,
            'og_temp': 59.0,
            'refractometer': False,
            'units': 'imperial',
            'verbose': True,
        }
        self.assertEquals(out.__dict__, expected)
