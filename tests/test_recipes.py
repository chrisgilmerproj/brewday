import unittest

from fixtures import grain_additions
from fixtures import hop_additions
from fixtures import recipe
from brew.recipes import Recipe


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.grain_additions = grain_additions

        # Define Hops
        self.hop_additions = hop_additions

        # Define Recipes
        self.recipe = recipe

    def test_recipe_raises_bad_units(self):
        with self.assertRaises(Exception):
            Recipe(name='pale ale',
                   grain_additions=grain_additions,
                   hop_additions=hop_additions,
                   percent_brew_house_yield=70.0,
                   start_volume=7.0,
                   final_volume=5.0,
                   target_sg=1.057,
                   target_ibu=40.0,
                   units='bad')

    def test_str(self):
        out = str(self.recipe)
        self.assertEquals(out, 'pale ale')

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
        plato_actual = 15.0
        vol_actual = 5.5
        bhy = self.recipe.get_brew_house_yield(plato_actual, vol_actual)
        self.assertEqual(round(bhy, 2), 0.82)

    def test_get_extract_weight(self):
        pounds_extract = self.recipe.get_extract_weight()
        self.assertEquals(round(pounds_extract, 2), 6.17)

    def test_get_working_yield(self):
        wy = self.recipe.get_working_yield(self.grain_additions[0])
        self.assertEquals(round(wy, 2), 0.53)
        wy = self.recipe.get_working_yield(self.grain_additions[1])
        self.assertEquals(round(wy, 2), 0.49)

    def test_get_pounds_malt(self):
        pounds_malt = self.recipe.get_pounds_malt(self.grain_additions[0])
        self.assertEquals(round(pounds_malt, 2), 11.02)
        pounds_malt = self.recipe.get_pounds_malt(self.grain_additions[1])
        self.assertEquals(round(pounds_malt, 2), 0.63)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 11.65)

    def test_get_total_ibu(self):
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
        self.assertEquals(round(wort_color, 2), 3.33)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 1.75)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 5.09)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 3.56)
