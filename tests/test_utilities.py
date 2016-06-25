import unittest

from brew.constants import KG_PER_POUND
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.utilities.abv import alcohol_by_volume_alternative
from brew.utilities.abv import alcohol_by_volume_standard
from brew.utilities.color import calculate_srm
from brew.utilities.color import ebc_to_a430
from brew.utilities.color import ebc_to_srm
from brew.utilities.color import lovibond_to_srm
from brew.utilities.color import srm_to_a430
from brew.utilities.color import srm_to_ebc
from brew.utilities.color import srm_to_lovibond
from brew.utilities.malt import as_is_basis_to_dry_basis
from brew.utilities.malt import basis_to_hwe
from brew.utilities.malt import coarse_grind_to_fine_grind
from brew.utilities.malt import dry_basis_to_as_is_basis
from brew.utilities.malt import fine_grind_to_coarse_grind
from brew.utilities.malt import hwe_to_basis
from brew.utilities.malt import plato_from_dry_basis
from brew.utilities.malt import sg_from_dry_basis
from brew.utilities.sugar import brix_to_plato
from brew.utilities.sugar import brix_to_sg
from brew.utilities.sugar import gu_to_sg
from brew.utilities.sugar import hydrometer_adjustment
from brew.utilities.sugar import plato_to_brix
from brew.utilities.sugar import plato_to_sg
from brew.utilities.sugar import refractometer_adjustment
from brew.utilities.sugar import sg_to_brix
from brew.utilities.sugar import sg_to_gu
from brew.utilities.sugar import sg_to_plato
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


class TestSugarUtilities(unittest.TestCase):

    def test_brix_to_plato(self):
        plato = brix_to_plato(22.0)
        self.assertEquals(round(plato, 3), 22.001)

    def test_brix_to_sg(self):
        sg = brix_to_sg(22.0)
        self.assertEquals(round(sg, 3), 1.092)

    def test_gu_to_sg(self):
        sg = gu_to_sg(57.0)
        self.assertEquals(round(sg, 3), 1.057)

    def test_plato_to_brix(self):
        brix = plato_to_brix(14.0)
        self.assertEquals(round(brix, 3), 14.002)

    def test_plato_to_sg(self):
        sg = plato_to_sg(14.0)
        self.assertEquals(round(sg, 3), 1.057)

    def test_sg_to_brix(self):
        brix = sg_to_brix(1.092)
        self.assertEquals(round(brix, 1), 22.0)

    def test_sg_to_brix_raises(self):
        with self.assertRaises(Exception):
            sg_to_brix(1.18)

    def test_sg_to_plato(self):
        plato = sg_to_plato(1.0570)
        self.assertEquals(round(plato, 2), 14.04)

    def test_sg_to_gu(self):
        gu = sg_to_gu(1.057)
        self.assertEquals(round(gu, 2), 57.0)


class TestABVUtilities(unittest.TestCase):

    def test_alcohol_by_volume_alternative(self):
        abv = alcohol_by_volume_alternative(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.95)

    def test_alcohol_by_volume_standard(self):
        abv = alcohol_by_volume_standard(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.78)

    def test_hydrometer_adjustment(self):
        sg = hydrometer_adjustment(1.050, 70.0)
        self.assertEquals(round(sg, 3), 1.051)

    def test_hydrometer_adjustment_no_adjustment(self):
        sg = hydrometer_adjustment(1.050, 59.0)
        self.assertEquals(round(sg, 3), 1.050)

    def test_hydromter_adjustment_si_units(self):
        sg = hydrometer_adjustment(1.050, 16.0, units=SI_UNITS)
        self.assertEquals(round(sg, 3), 1.050)

    def test_hydrometer_adjustment_raises_bad_units(self):
        with self.assertRaises(Exception):
            hydrometer_adjustment(1.050, 16.0, units='bad')

    def test_hydrometer_adjustment_raises_bad_temp(self):
        with self.assertRaises(Exception):
            hydrometer_adjustment(1.050, -1.0)

        with self.assertRaises(Exception):
            hydrometer_adjustment(1.050, 213.0)

        with self.assertRaises(Exception):
            hydrometer_adjustment(1.050, -1.0, units=SI_UNITS)

        with self.assertRaises(Exception):
            hydrometer_adjustment(1.050, 101.0, units=SI_UNITS)

    def test_refractometer_adjustment(self):
        fg = refractometer_adjustment(1.050, 1.011)
        self.assertEquals(round(fg, 3), 1.004)


class TestMaltUtilities(unittest.TestCase):

    def test_fine_grind_to_coarse_grind(self):
        cg = fine_grind_to_coarse_grind(0.81)
        self.assertEquals(round(cg, 2), 0.79)

    def test_coarse_grind_to_fine_grind(self):
        fg = coarse_grind_to_fine_grind(0.79)
        self.assertEquals(round(fg, 2), 0.81)

    def test_dry_basis_to_as_is_basis(self):
        asb = dry_basis_to_as_is_basis(0.40)
        self.assertEquals(round(asb, 2), 0.38)

    def test_as_is_basis_to_dry_basis(self):
        db = as_is_basis_to_dry_basis(0.38)
        self.assertEquals(round(db, 2), 0.40)

    def test_sg_from_dry_basis(self):
        sg = sg_from_dry_basis(0.80)
        self.assertEquals(round(sg, 3), 1.032)

    def test_plato_from_dry_basis(self):
        plato = plato_from_dry_basis(0.80)
        self.assertEquals(round(plato, 2), 7.86)

    def test_basis_to_hwe(self):
        hwe = basis_to_hwe(0.8)
        self.assertEquals(round(hwe, 2), 308.8)

    def test_hwe_to_basis(self):
        basis = hwe_to_basis(308.8)
        self.assertEquals(round(basis, 3), 0.8)


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
        srm = calculate_srm(weight, color, vol)
        self.assertEquals(round(srm, 2), 4.78)
        ebc = srm_to_ebc(srm)
        self.assertEquals(round(ebc, 2), 9.41)

    def test_calculate_srm_metric(self):
        weight = 1.0 * KG_PER_POUND  # kg
        color = 30.0  # degL
        vol = 5.5 * LITER_PER_GAL  # liter
        self.assertEquals(round(weight, 2), 0.45)
        self.assertEquals(round(vol, 2), 20.82)

        srm = calculate_srm(weight, color, vol, units=SI_UNITS)
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
