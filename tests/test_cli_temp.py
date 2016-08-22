
import unittest

from brew.cli.temp import get_parser
from brew.cli.temp import get_temp_conversion


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
