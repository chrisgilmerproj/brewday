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

    def test_get_total_gravity_units(self):
        out = self.recipe.get_total_gravity_units()
        self.assertEquals(round(out, 2), 285.0)

    def test_get_starting_sg(self):
        out = self.recipe.get_starting_sg()
        self.assertEquals(round(out, 3), 1.041)

    def test_get_starting_plato(self):
        out = self.recipe.get_starting_plato()
        self.assertEquals(round(out, 2), 10.17)

    def test_brew_house_yield(self):
        vol_actual = 5.5
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.63)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 6.17)

    def test_get_malt_weight(self):
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[0])
        self.assertEquals(round(malt_weight, 2), 10.99)
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[1])
        self.assertEquals(round(malt_weight, 2), 0.67)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 14.74)

    def test_get_total_malt_weight(self):
        total_malt_weight = self.recipe.get_total_malt_weight()
        self.assertEquals(round(total_malt_weight, 2), 11.66)

    def test_get_total_ibu(self):
        self.assertEqual(self.recipe.target_sg, 1.057)
        self.assertEqual(self.recipe.final_volume, 5.0)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.0)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 4.20)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 5.02)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.56)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 8.58)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 6.01)


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

    def test_get_total_gravity_units(self):
        out = self.recipe.get_total_gravity_units()
        self.assertEquals(round(out, 2), 1078.84)

    def test_get_starting_sg(self):
        out = self.recipe.get_starting_sg()
        self.assertEquals(round(out, 3), 1.041)

    def test_get_starting_plato(self):
        out = self.recipe.get_starting_plato()
        self.assertEquals(round(out, 2), 10.17)

    def test_brew_house_yield(self):
        vol_actual = 5.5 * LITER_PER_GAL
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.63)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 2.81)

    def test_get_malt_weight(self):
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[0])
        self.assertEquals(round(malt_weight, 2), 5.0)
        malt_weight = self.recipe.get_malt_weight(self.grain_additions[1])
        self.assertEquals(round(malt_weight, 2), 0.3)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 6.69)

    def test_get_total_malt_weight(self):
        total_malt_weight = self.recipe.get_total_malt_weight()
        self.assertEquals(round(total_malt_weight, 2), 5.3)

    def test_get_total_ibu(self):
        self.assertEqual(self.recipe.target_sg, 1.057)
        self.assertEqual(round(self.recipe.final_volume, 2), 18.93)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.0)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 15.91)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 5.03)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.57)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 8.6)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 6.02)
