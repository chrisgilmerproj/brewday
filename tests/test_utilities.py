import unittest

from brew.utilities import alcohol_by_volume_alternative
from brew.utilities import alcohol_by_volume_standard
from brew.utilities import celsius_to_fahrenheit
from brew.utilities import fahrenheit_to_celsius
from brew.utilities import hydrometer_adjustment
from brew.utilities import plato_to_sg
from brew.utilities import sg_to_plato


class TestUtilities(unittest.TestCase):

    def test_alcohol_by_volume_alternative(self):
        abv = alcohol_by_volume_alternative(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.95)

    def test_alcohol_by_volume_standard(self):
        abv = alcohol_by_volume_standard(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.78)

    def test_fahrenheit_to_celsius(self):
        ctemp = fahrenheit_to_celsius(212.0)
        self.assertEquals(ctemp, 100.0)
        ctemp = fahrenheit_to_celsius(32.0)
        self.assertEquals(ctemp, 0.0)
        ctemp = fahrenheit_to_celsius(-40.0)
        self.assertEquals(ctemp, -40.0)

    def test_celsius_to_fahrenheit(self):
        ftemp = celsius_to_fahrenheit(100.0)
        self.assertEquals(ftemp, 212.0)
        ftemp = celsius_to_fahrenheit(0.0)
        self.assertEquals(ftemp, 32.0)
        ftemp = celsius_to_fahrenheit(-40.0)
        self.assertEquals(ftemp, -40.0)

    def test_plato_to_sg(self):
        sg = plato_to_sg(14.0)
        self.assertEquals(round(sg, 3), 1.057)

    def test_sg_to_plato(self):
        sg = sg_to_plato(1.0570)
        self.assertEquals(round(sg, 2), 14.04)

    def test_hydrometer_adjustment(self):
        sg = hydrometer_adjustment(1.050, 59.0)
        self.assertEquals(round(sg, 3), 1.050)

        sg = hydrometer_adjustment(1.050, 70.0)
        self.assertEquals(round(sg, 3), 1.051)
