import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SUCROSE_PLATO
from fixtures import grain_additions
from fixtures import hop_additions
from fixtures import recipe


class TestRecipeImperialUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = grain_additions

        # Define Hops
        self.hop_additions = hop_additions

        # Define Recipes
        self.recipe = recipe
        self.recipe.set_units(IMPERIAL_UNITS)

    def test_change_units(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        for hop_add in self.recipe.hop_additions:
            self.assertEquals(hop_add.units, IMPERIAL_UNITS)

    def test_get_original_gravity_units(self):
        out = self.recipe.get_original_gravity_units()
        self.assertEquals(round(out, 2), 76.13)

    def test_get_original_gravity(self):
        out = self.recipe.get_original_gravity()
        self.assertEquals(round(out, 3), 1.076)

    def test_get_boil_gravity_units(self):
        out = self.recipe.get_boil_gravity_units()
        self.assertEquals(round(out, 2), 54.38)

    def test_get_boil_gravity(self):
        out = self.recipe.get_boil_gravity()
        self.assertEquals(round(out, 3), 1.054)

    def test_get_final_gravity_units(self):
        out = self.recipe.get_final_gravity_units()
        self.assertEquals(round(out, 2), 19.03)

    def test_get_final_gravity(self):
        out = self.recipe.get_final_gravity()
        self.assertEquals(round(out, 3), 1.019)

    def test_brew_house_yield(self):
        vol_actual = 5.5
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.66)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 5.89)

    def test_get_malt_weight(self):
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[0])
        self.assertEquals(round(malt_weight, 2), 9.96)
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[1])
        self.assertEquals(round(malt_weight, 2), 0.59)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 14.74)

    def test_get_total_malt_weight(self):
        total_malt_weight = self.recipe.get_total_malt_weight()
        self.assertEquals(round(total_malt_weight, 2), 10.55)

    def test_get_total_ibu(self):
        self.assertEqual(round(self.recipe.get_boil_gravity(), 3), 1.054)
        self.assertEqual(self.recipe.final_volume, 5.0)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.51)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 3.8)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 4.69)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.27)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 7.96)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 5.57)
