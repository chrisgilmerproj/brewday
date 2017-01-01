# -*- coding: utf-8 -*-
import unittest

from brew.utilities.abv import alcohol_by_volume_alternative
from brew.utilities.abv import alcohol_by_volume_standard
from brew.utilities.abv import alcohol_by_weight
from brew.utilities.abv import apparent_attenuation
from brew.utilities.abv import final_gravity_from_abv_standard
from brew.utilities.abv import real_attenuation
from brew.utilities.abv import real_attenuation_from_apparent_extract
from brew.utilities.sugar import apparent_extract_to_real_extract
from brew.utilities.sugar import sg_to_plato


class TestABVUtilities(unittest.TestCase):

    def test_apparent_attenuation(self):
        oe = sg_to_plato(1.060)
        ae = sg_to_plato(1.010)
        out = apparent_attenuation(oe, ae)
        self.assertEquals(round(out, 2), 0.83)

    def test_real_attenuation(self):
        oe = sg_to_plato(1.060)
        ae = sg_to_plato(1.010)
        re = apparent_extract_to_real_extract(oe, ae)
        out = real_attenuation(oe, re)
        self.assertEquals(round(out, 2), 0.67)

    def test_real_attenuation_from_apparent_extract(self):
        oe = sg_to_plato(1.060)
        ae = sg_to_plato(1.010)
        out = real_attenuation_from_apparent_extract(oe, ae)
        self.assertEquals(round(out, 2), 0.67)

    def test_alcohol_by_volume_alternative(self):
        abv = alcohol_by_volume_alternative(1.057, 1.013)
        self.assertEquals(round(abv * 100.0, 2), 5.95)

    def test_alcohol_by_volume_standard(self):
        abv = alcohol_by_volume_standard(1.057, 1.013)
        self.assertEquals(round(abv * 100.0, 2), 5.78)

    def test_final_gravity_from_abv_standard(self):
        fg = final_gravity_from_abv_standard(1.057, 0.0578)
        self.assertEquals(round(fg, 3), 1.013)

    def test_alcohol_by_weight(self):
        abw = alcohol_by_weight(5.78 / 100.0)
        self.assertEquals(round(abw * 100.0, 2), 4.59)
