import unittest

from brew.utilities.temperature import celsius_to_fahrenheit
from brew.utilities.temperature import fahrenheit_to_celsius


class TestTemperatureUtilities(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        ftemp = celsius_to_fahrenheit(100.0)
        self.assertEquals(ftemp, 212.0)
        ftemp = celsius_to_fahrenheit(0.0)
        self.assertEquals(ftemp, 32.0)
        ftemp = celsius_to_fahrenheit(-40.0)
        self.assertEquals(ftemp, -40.0)

    def test_fahrenheit_to_celsius(self):
        ctemp = fahrenheit_to_celsius(212.0)
        self.assertEquals(ctemp, 100.0)
        ctemp = fahrenheit_to_celsius(32.0)
        self.assertEquals(ctemp, 0.0)
        ctemp = fahrenheit_to_celsius(-40.0)
        self.assertEquals(ctemp, -40.0)
