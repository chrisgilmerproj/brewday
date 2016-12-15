# -*- coding: utf-8 -*-
import textwrap
import unittest

from brew.cli.abv import get_abv
from brew.cli.abv import get_parser
from brew.cli.abv import main
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS


class TestCliAbv(unittest.TestCase):

    def setUp(self):
        self.og = 1.057
        self.fg = 1.013

    def test_get_abv(self):
        abv = get_abv(self.og, self.fg)
        self.assertEquals(round(abv * 100, 2), 5.78)

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
            get_abv(self.og, self.og, units=u'bad')

    def test_get_abv_units_imperial(self):
        abv = get_abv(self.og, self.fg, units=IMPERIAL_UNITS)
        self.assertEquals(round(abv * 100, 2), 5.78)

    def test_get_abv_units_si(self):
        abv = get_abv(self.og, self.fg, units=SI_UNITS)
        self.assertEquals(round(abv * 100, 2), 5.78)

    def test_get_abv_alternative(self):
        abv = get_abv(self.og, self.fg, alternative=True)
        self.assertEquals(round(abv * 100, 2), 5.95)

    def test_get_abv_refractometer(self):
        abv = get_abv(self.og, self.fg, refractometer=True)
        self.assertEquals(round(abv * 100, 2), 6.97)

    def test_get_abv_alternative_refractometer(self):
        abv = get_abv(self.og, self.fg, alternative=True, refractometer=True)
        self.assertEquals(round(abv * 100, 2), 7.12)

    def test_get_abv_verbose(self):
        out = get_abv(self.og, self.fg, verbose=True)
        expected = textwrap.dedent(u"""\
            OG     : 1.057
            OG Adj : 1.057
            OG Temp: 59.00 F
            FG     : 1.013
            FG Adj : 1.013
            FG Temp: 59.00 F
            ABV    : 5.78%""")
        self.assertEquals(out, expected)


class TestCliArgparserAbv(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser_required_og_and_fg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_get_parser_required_og(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([u'-f', u'1.010'])

    def test_get_parser_required_fg(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([u'-o', u'1.060'])

    def test_get_parser_og_and_fg(self):
        args = [u'-o', u'1.060', u'-f', u'1.010']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': False,
            u'fg': 1.01,
            u'fg_temp': 59.0,
            u'og': 1.06,
            u'og_temp': 59.0,
            u'refractometer': False,
            u'units': u'imperial',
            u'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_update_temp(self):
        args = [u'-o', u'1.060', u'-f', u'1.010',
                u'--og-temp', u'61.0',
                u'--fg-temp', u'61.0']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': False,
            u'fg': 1.01,
            u'fg_temp': 61.0,
            u'og': 1.06,
            u'og_temp': 61.0,
            u'refractometer': False,
            u'units': u'imperial',
            u'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_alternative(self):
        args = [u'-o', u'1.060', u'-f', u'1.010', u'--alternative']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': True,
            u'fg': 1.01,
            u'fg_temp': 59.0,
            u'og': 1.06,
            u'og_temp': 59.0,
            u'refractometer': False,
            u'units': u'imperial',
            u'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_refractometer(self):
        args = [u'-o', u'1.060', u'-f', u'1.010', u'--refractometer']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': False,
            u'fg': 1.01,
            u'fg_temp': 59.0,
            u'og': 1.06,
            u'og_temp': 59.0,
            u'refractometer': True,
            u'units': u'imperial',
            u'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_units(self):
        args = [u'-o', u'1.060', u'-f', u'1.010', u'--units', u'si']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': False,
            u'fg': 1.01,
            u'fg_temp': 59.0,
            u'og': 1.06,
            u'og_temp': 59.0,
            u'refractometer': False,
            u'units': u'si',
            u'verbose': False,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_verbose(self):
        args = [u'-o', u'1.060', u'-f', u'1.010', u'-v']
        out = self.parser.parse_args(args)
        expected = {
            u'alternative': False,
            u'fg': 1.01,
            u'fg_temp': 59.0,
            u'og': 1.06,
            u'og_temp': 59.0,
            u'refractometer': False,
            u'units': u'imperial',
            u'verbose': True,
        }
        self.assertEquals(out.__dict__, expected)


class TestCliMainAbv(unittest.TestCase):

    def setUp(self):
        class Parser(object):
            def __init__(self, output):
                self.output = output

            def parse_args(self):
                class Args(object):
                    pass
                args = Args()
                if self.output:
                    for k, v in self.output.items():
                        setattr(args, k, v)
                return args

        def g_parser(output=None):
            return Parser(output)
        self.parser_fn = g_parser
        self.main = main

    def test_main_no_kwargs(self):
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn)

    def test_main_with_args(self):
        args = {u'output': {u'og': 1.060,
                            u'fg': 1.010,
                            u'og_temp': 59.0,
                            u'fg_temp': 59.0,
                            u'alternative': False,
                            u'refractometer': False,
                            u'units': u'imperial',
                            u'verbose': False}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)

    def test_main_verbose(self):
        args = {u'output': {u'og': 1.060,
                            u'fg': 1.010,
                            u'og_temp': 59.0,
                            u'fg_temp': 59.0,
                            u'alternative': False,
                            u'refractometer': False,
                            u'units': u'imperial',
                            u'verbose': True}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)
