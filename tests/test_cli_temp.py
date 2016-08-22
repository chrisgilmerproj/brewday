
import unittest

from brew.cli.temp import get_parser
from brew.cli.temp import get_temp_conversion
from brew.cli.temp import main


class TestCliTemp(unittest.TestCase):

    def setUp(self):
        self.c = 15.6
        self.f = 60.1

    def test_get_sugar_conversion_fahrenheit(self):
        out = get_temp_conversion(self.f, None)
        self.assertEquals(out, self.c)

    def test_get_sugar_conversion_celsius(self):
        out = get_temp_conversion(None, self.c)
        self.assertEquals(out, self.f)


class TestCliArgparserTemp(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser_celsius(self):
        args = ['-c', '25.0']
        out = self.parser.parse_args(args)
        expected = {
            'celsius': 25.0,
            'fahrenheit': None,
        }
        self.assertEquals(out.__dict__, expected)

    def test_get_parser_fahrenheit(self):
        args = ['-f', '62.0']
        out = self.parser.parse_args(args)
        expected = {
            'celsius': None,
            'fahrenheit': 62.0,
        }
        self.assertEquals(out.__dict__, expected)


class TestCliMainTemp(unittest.TestCase):

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
        args = {'output': {'celsius': None,
                           'fahrenheit': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_both_args(self):
        args = {'output': {'celsius': 25.0,
                           'fahrenheit': 62.0}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_no_kwargs(self):
        with self.assertRaises(AttributeError):
            self.main(parser_fn=self.parser_fn)

    def test_main_celsius(self):
        args = {'output': {'celsius': 25.0,
                           'fahrenheit': None}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)

    def test_main_fahrenheit(self):
        args = {'output': {'celsius': None,
                           'fahrenheit': 62.0}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)
