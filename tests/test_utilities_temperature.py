# -*- coding: utf-8 -*-
import unittest

from brew.utilities.temperature import boiling_point
from brew.utilities.temperature import celsius_to_fahrenheit
from brew.utilities.temperature import fahrenheit_to_celsius
from brew.utilities.temperature import mash_infusion
from brew.utilities.temperature import strike_temp


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

    def test_strike_temp(self):
        temp = strike_temp(104.0, 70.0, 1.0 / 1.0, )
        self.assertEquals(round(temp, 2), 110.8)

    def test_mash_infusion(self):
        vol = mash_infusion(140.0, 104.0, 8.0, 8.0, 210.0)
        self.assertEquals(round(vol, 2), 4.94)

    def test_boiling_point(self):
        bp = boiling_point(0)
        self.assertEquals(round(bp, 2), 212.01)
        bp = boiling_point(3000)
        self.assertEquals(round(bp, 2), 206.62)
