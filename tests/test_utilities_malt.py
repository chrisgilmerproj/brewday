import unittest

from brew.utilities.malt import as_is_basis_to_dry_basis
from brew.utilities.malt import basis_to_hwe
from brew.utilities.malt import coarse_grind_to_fine_grind
from brew.utilities.malt import dry_basis_to_as_is_basis
from brew.utilities.malt import dry_to_liquid_malt_weight
from brew.utilities.malt import dry_malt_to_grain_weight
from brew.utilities.malt import fine_grind_to_coarse_grind
from brew.utilities.malt import grain_to_dry_malt_weight
from brew.utilities.malt import grain_to_liquid_malt_weight
from brew.utilities.malt import hwe_to_basis
from brew.utilities.malt import hwe_to_ppg
from brew.utilities.malt import liquid_malt_to_grain_weight
from brew.utilities.malt import liquid_malt_to_specialty_grain_weight
from brew.utilities.malt import liquid_to_dry_malt_weight
from brew.utilities.malt import plato_from_dry_basis
from brew.utilities.malt import ppg_to_hwe
from brew.utilities.malt import sg_from_dry_basis
from brew.utilities.malt import specialty_grain_to_liquid_malt_weight


class TestMaltUtilities(unittest.TestCase):

    def test_dry_to_liquid_malt_weight(self):
        out = dry_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 6.25)

    def test_liquid_to_dry_malt_weight(self):
        out = liquid_to_dry_malt_weight(6.25)
        self.assertEquals(out, 5.0)

    def test_grain_to_liquid_malt_weight(self):
        out = grain_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 3.75)

    def test_liquid_malt_to_grain_weight(self):
        out = liquid_malt_to_grain_weight(3.75)
        self.assertEquals(out, 5.0)

    def test_grain_to_dry_malt_weight(self):
        out = grain_to_dry_malt_weight(5.0)
        self.assertEquals(out, 3.0)

    def test_dry_malt_to_grain_weight(self):
        out = dry_malt_to_grain_weight(3.75)
        self.assertEquals(out, 6.25)

    def test_specialty_grain_to_liquid_malt_weight(self):
        out = specialty_grain_to_liquid_malt_weight(5.0)
        self.assertEquals(out, 4.45)

    def test_liquid_malt_to_specialty_grain_weight(self):
        out = liquid_malt_to_specialty_grain_weight(4.45)
        self.assertEquals(out, 5.0)

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

    def test_ppg_to_hwe(self):
        hwe = ppg_to_hwe(37)
        self.assertEqual(round(hwe, 2), 308.78)

    def test_hwe_to_ppg(self):
        ppg = hwe_to_ppg(308.78)
        self.assertEqual(round(ppg, 2), 37)
