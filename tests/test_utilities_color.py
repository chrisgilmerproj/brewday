import unittest

from brew.constants import KG_PER_POUND
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.utilities.color import calculate_mcu
from brew.utilities.color import calculate_srm
from brew.utilities.color import ebc_to_a430
from brew.utilities.color import ebc_to_srm
from brew.utilities.color import lovibond_to_srm
from brew.utilities.color import srm_to_a430
from brew.utilities.color import srm_to_ebc
from brew.utilities.color import srm_to_lovibond


class TestColorUtilities(unittest.TestCase):

    def test_srm_to_ebc(self):
        ebc = srm_to_ebc(3.0)
        self.assertEquals(round(ebc, 2), 5.91)

    def test_ebc_to_srm(self):
        srm = ebc_to_srm(5.91)
        self.assertEquals(round(srm, 2), 3.0)

    def test_calculate_srm_imperial(self):
        weight = 1.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        srm = calculate_srm(mcu)
        self.assertEquals(round(srm, 2), 4.78)
        ebc = srm_to_ebc(srm)
        self.assertEquals(round(ebc, 2), 9.41)

    def test_calculate_srm_metric(self):
        weight = 1.0 * KG_PER_POUND  # kg
        color = 30.0  # degL
        vol = 5.5 * LITER_PER_GAL  # liter
        self.assertEquals(round(weight, 2), 0.45)
        self.assertEquals(round(vol, 2), 20.82)

        mcu = calculate_mcu(weight, color, vol, units=SI_UNITS)
        srm = calculate_srm(mcu)
        self.assertEquals(round(srm, 2), 4.78)
        ebc = srm_to_ebc(srm)
        self.assertEquals(round(ebc, 2), 9.41)

    def test_calculate_srm_raises(self):
        weight = 1.0  # lbs
        color = 1000.0  # degL
        vol = 1.0  # gal
        with self.assertRaises(Exception):
            calculate_srm(weight, color, vol)

    def test_lovibond_to_srm(self):
        out = lovibond_to_srm(30)
        self.assertEquals(round(out, 2), 39.88)

    def test_srm_to_lovibond(self):
        out = srm_to_lovibond(40)
        self.assertEquals(round(out, 2), 30.09)

    def test_srm_to_a430(self):
        out = srm_to_a430(30)
        self.assertEquals(round(out, 2), 2.36)

    def test_ebc_to_a430(self):
        out = ebc_to_a430(60)
        self.assertEquals(round(out, 2), 2.4)
