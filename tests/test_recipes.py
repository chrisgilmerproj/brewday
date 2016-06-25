import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.constants import SUCROSE_PLATO
from fixtures import grain_additions
from fixtures import hop_additions
from fixtures import recipe


class TestRecipe(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = grain_additions

        # Define Hops
        self.hop_additions = hop_additions

        # Define Recipes
        self.recipe = recipe

    def test_str(self):
        out = str(self.recipe)
        self.assertEquals(out, 'pale ale')

    def test_set_units(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        self.recipe.set_units(SI_UNITS)
        self.assertEquals(self.recipe.units, SI_UNITS)

    def test_set_raises(self):
        with self.assertRaises(Exception):
            self.recipe.set_units('bad')


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

    def test_get_original_gravity(self):
        out = self.recipe.get_original_gravity()
        self.assertEquals(round(out, 3), 1.076)

    def test_get_boil_gravity(self):
        out = self.recipe.get_boil_gravity()
        self.assertEquals(round(out, 3), 1.054)

    def test_get_boil_gravity_units(self):
        out = self.recipe.get_boil_gravity_units()
        self.assertEquals(round(out, 2), 54.38)

    def test_brew_house_yield(self):
        vol_actual = 5.5
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.63)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 6.16)

    def test_get_malt_weight(self):
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[0])
        self.assertEquals(round(malt_weight, 2), 10.42)
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[1])
        self.assertEquals(round(malt_weight, 2), 0.62)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 14.74)

    def test_get_total_malt_weight(self):
        total_malt_weight = self.recipe.get_total_malt_weight()
        self.assertEquals(round(total_malt_weight, 2), 11.03)

    def test_get_total_ibu(self):
        self.assertEqual(self.recipe.target_sg, 1.057)
        self.assertEqual(self.recipe.final_volume, 5.0)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.51)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 3.98)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 4.84)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.37)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 8.21)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 5.75)


class TestRecipeSIUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = [ga.change_units() for ga in
                                grain_additions]

        # Define Hops
        self.hop_additions = [ha.change_units() for ha in
                              hop_additions]

        # Define Recipes
        self.recipe = recipe.change_units()

    def test_change_units(self):
        self.assertEquals(self.recipe.units, SI_UNITS)
        self.assertEquals(round(self.recipe.start_volume, 2), 26.50)
        self.assertEquals(round(self.recipe.final_volume, 2), 18.93)
        self.assertEquals(round(self.recipe.grain_additions[0].weight, 2), 6.33)  # nopep8
        self.assertEquals(round(self.recipe.grain_additions[1].weight, 2), 0.35)  # nopep8
        self.assertEquals(round(self.recipe.hop_additions[0].weight, 2), 16159.21)  # nopep8
        self.assertEquals(round(self.recipe.hop_additions[1].weight, 2), 21545.62)  # nopep8
        for grain_add in self.recipe.grain_additions:
            self.assertEquals(grain_add.units, SI_UNITS)
        for hop_add in self.recipe.hop_additions:
            self.assertEquals(hop_add.units, SI_UNITS)

    def test_get_boil_gravity(self):
        out = self.recipe.get_boil_gravity()
        self.assertEquals(round(out, 3), 1.054)

    def test_get_boil_gravity_units(self):
        out = self.recipe.get_boil_gravity_units()
        self.assertEquals(round(out, 2), 54.38)

    def test_brew_house_yield(self):
        vol_actual = 5.5 * LITER_PER_GAL
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.63)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 2.8)

    def test_get_malt_weight(self):
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[0])
        self.assertEquals(round(malt_weight, 2), 4.74)
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[1])
        self.assertEquals(round(malt_weight, 2), 0.28)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 6.69)

    def test_get_total_malt_weight(self):
        total_malt_weight = self.recipe.get_total_malt_weight()
        self.assertEquals(round(total_malt_weight, 2), 5.02)

    def test_get_total_ibu(self):
        self.assertEqual(self.recipe.target_sg, 1.057)
        self.assertEqual(round(self.recipe.final_volume, 2), 18.93)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.51)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 15.06)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 4.85)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.38)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 8.23)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 5.76)
