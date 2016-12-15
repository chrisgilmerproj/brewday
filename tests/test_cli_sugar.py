# -*- coding: utf-8 -*-
import unittest

from brew.cli.sugar import get_parser
from brew.cli.sugar import get_sugar_conversion
from brew.cli.sugar import main


class TestCliSugar(unittest.TestCase):

    def setUp(self):
        self.brix = 22.0
        self.plato = 22.0
        self.sg = 1.092

    def test_get_sugar_conversion_brix_to_brix(self):
        out = get_sugar_conversion(self.brix, None, None, u'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_brix_to_plato(self):
        out = get_sugar_conversion(self.brix, None, None, u'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_brix_to_sg(self):
        out = get_sugar_conversion(self.brix, None, None, u's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_plato_to_brix(self):
        out = get_sugar_conversion(None, self.plato, None, u'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_plato_to_plato(self):
        out = get_sugar_conversion(None, self.plato, None, u'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_plato_to_sg(self):
        out = get_sugar_conversion(None, self.plato, None, u's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_sg_to_brix(self):
        out = get_sugar_conversion(None, None, self.sg, u'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_sg_to_plato(self):
        out = get_sugar_conversion(None, None, self.sg, u'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_sg_to_sg(self):
        out = get_sugar_conversion(None, None, self.sg, u's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_all_brix(self):
        out = get_sugar_conversion(self.brix, None, None, None)
        expected = u'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_plato(self):
        out = get_sugar_conversion(None, self.plato, None, None)
        expected = u'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_sg(self):
        out = get_sugar_conversion(None, None, self.sg, None)
        expected = u'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)


class TestCliArgparserSugar(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser_brix_in_none_out(self):
        args = [u'-b', u'22.0']
        out = self.parser.parse_args(args)
        expected = {
            u'brix': 22.0,
            u'plato': None,
            u'sg': None,
            u'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_plato_in_none_out(self):
        args = [u'-p', u'22.0']
        out = self.parser.parse_args(args)
        expected = {
            u'brix': None,
            u'plato': 22.0,
            u'sg': None,
            u'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_sg_in_none_out(self):
        args = [u'-s', u'1.060']
        out = self.parser.parse_args(args)
        expected = {
            u'brix': None,
            u'plato': None,
            u'sg': 1.060,
            u'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_sg_in_brix_out(self):
        args = [u'-s', u'1.060', u'-o', u'b']
        out = self.parser.parse_args(args)
        expected = {
            u'brix': None,
            u'plato': None,
            u'sg': 1.060,
            u'out': u'b',
        }
        self.assertEquals(out.__dict__, expected)


class TestCliMainSugar(unittest.TestCase):

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

    def test_main_no_args(self):
        args = {u'output': {u'brix': None,
                            u'plato': None,
                            u'sg': None,
                            u'out': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_no_kwargs(self):
        with self.assertRaises(AttributeError):
            self.main(parser_fn=self.parser_fn)

    def test_main_two_args(self):
        args = {u'output': {u'brix': 22.0,
                            u'plato': 22.0,
                            u'sg': None,
                            u'out': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_one_arg(self):
        args = {u'output': {u'brix': 22.0,
                            u'plato': None,
                            u'sg': None,
                            u'out': None}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)
