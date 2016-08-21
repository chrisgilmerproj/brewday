
import unittest

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
