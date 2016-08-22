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
        out = get_sugar_conversion(self.brix, None, None, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_brix_to_plato(self):
        out = get_sugar_conversion(self.brix, None, None, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_brix_to_sg(self):
        out = get_sugar_conversion(self.brix, None, None, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_plato_to_brix(self):
        out = get_sugar_conversion(None, self.plato, None, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_plato_to_plato(self):
        out = get_sugar_conversion(None, self.plato, None, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_plato_to_sg(self):
        out = get_sugar_conversion(None, self.plato, None, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_sg_to_brix(self):
        out = get_sugar_conversion(None, None, self.sg, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_sg_to_plato(self):
        out = get_sugar_conversion(None, None, self.sg, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_sg_to_sg(self):
        out = get_sugar_conversion(None, None, self.sg, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_all_brix(self):
        out = get_sugar_conversion(self.brix, None, None, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_plato(self):
        out = get_sugar_conversion(None, self.plato, None, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_sg(self):
        out = get_sugar_conversion(None, None, self.sg, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)


class TestCliArgparserSugar(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser_brix_in_none_out(self):
        args = ['-b', '22.0']
        out = self.parser.parse_args(args)
        expected = {
            'brix': 22.0,
            'plato': None,
            'sg': None,
            'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_plato_in_none_out(self):
        args = ['-p', '22.0']
        out = self.parser.parse_args(args)
        expected = {
            'brix': None,
            'plato': 22.0,
            'sg': None,
            'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_sg_in_none_out(self):
        args = ['-s', '1.060']
        out = self.parser.parse_args(args)
        expected = {
            'brix': None,
            'plato': None,
            'sg': 1.060,
            'out': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_sg_in_brix_out(self):
        args = ['-s', '1.060', '-o', 'b']
        out = self.parser.parse_args(args)
        expected = {
            'brix': None,
            'plato': None,
            'sg': 1.060,
            'out': 'b',
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
        args = {'output': {'brix': None,
                           'plato': None,
                           'sg': None,
                           'out': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_no_kwargs(self):
        with self.assertRaises(AttributeError):
            self.main(parser_fn=self.parser_fn)

    def test_main_two_args(self):
        args = {'output': {'brix': 22.0,
                           'plato': 22.0,
                           'sg': None,
                           'out': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_one_arg(self):
        args = {'output': {'brix': 22.0,
                           'plato': None,
                           'sg': None,
                           'out': None}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)
