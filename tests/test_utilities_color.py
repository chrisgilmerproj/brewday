import unittest

from brew.constants import KG_PER_POUND
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.utilities.color import calculate_mcu
from brew.utilities.color import calculate_srm
from brew.utilities.color import calculate_srm_daniels
from brew.utilities.color import calculate_srm_daniels_power
from brew.utilities.color import calculate_srm_morey
from brew.utilities.color import calculate_srm_morey_hybrid
from brew.utilities.color import calculate_srm_mosher
from brew.utilities.color import calculate_srm_noonan_power
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

    def test_calculate_mcu(self):
        weight = 1.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        self.assertEquals(round(mcu, 2), 5.45)

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

    def test_calculate_srm_all(self):
        weight = 3.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        srm = calculate_srm_mosher(mcu)
        self.assertEquals(round(srm, 2), 9.61)
        srm = calculate_srm_daniels(mcu)
        self.assertEquals(round(srm, 2), 11.67)
        srm = calculate_srm_daniels_power(mcu)
        self.assertEquals(round(srm, 2), 10.08)
        srm = calculate_srm_noonan_power(mcu)
        self.assertEquals(round(srm, 2), 16.44)
        srm = calculate_srm_morey_hybrid(mcu)
        self.assertEquals(round(srm, 2), 11.67)
        srm = calculate_srm_morey(mcu)
        self.assertEquals(round(srm, 2), 10.15)

    def test_calculate_srm_morey_hybrid(self):
        mcu = calculate_mcu(1.0, 30.0, 5.5)
        self.assertTrue(0 < mcu < 10)
        srm = calculate_srm_morey_hybrid(mcu)
        self.assertEquals(round(srm, 2), 5.45)

        mcu = calculate_mcu(3.0, 30.0, 5.5)
        self.assertTrue(10 <= mcu < 37)
        srm = calculate_srm_morey_hybrid(mcu)
        self.assertEquals(round(srm, 2), 11.67)

        mcu = calculate_mcu(8.0, 30.0, 5.5)
        self.assertTrue(37 <= mcu < 50)
        srm = calculate_srm_morey_hybrid(mcu)
        self.assertEquals(round(srm, 2), 17.79)

        mcu = calculate_mcu(100.0, 30.0, 5.5)
        self.assertTrue(50 < mcu)
        with self.assertRaises(Exception):
            calculate_srm_morey_hybrid(mcu)

    def test_calculate_srm_mosher_raises(self):
        weight = 1.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        with self.assertRaises(Exception):
            calculate_srm_mosher(mcu)

    # def test_calculate_srm_daniels_raises(self):
    #     weight = 1.0  # lbs
    #     color = 30.0  # degL
    #     vol = 5.5  # gal
    #     mcu = calculate_mcu(weight, color, vol)
    #     with self.assertRaises(Exception):
    #         calculate_srm_daniels(mcu)

    def test_calculate_srm_daniels_power_raises(self):
        weight = 100.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        with self.assertRaises(Exception):
            calculate_srm_daniels_power(mcu)

    def test_calculate_srm_noonan_power_raises(self):
        weight = 100.0  # lbs
        color = 30.0  # degL
        vol = 5.5  # gal
        mcu = calculate_mcu(weight, color, vol)
        with self.assertRaises(Exception):
            calculate_srm_noonan_power(mcu)

    def test_calculate_srm_morey_raises(self):
        weight = 1.0  # lbs
        color = 1000.0  # degL
        vol = 1.0  # gal
        mcu = calculate_mcu(weight, color, vol)
        with self.assertRaises(Exception):
            calculate_srm_morey(mcu)

    def test_calculate_srm_raises(self):
        weight = 1.0  # lbs
        color = 1000.0  # degL
        vol = 1.0  # gal
        mcu = calculate_mcu(weight, color, vol)
        with self.assertRaises(Exception):
            calculate_srm(mcu)

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
