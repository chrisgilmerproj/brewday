import unittest

from fixtures import grain_list
from fixtures import hop_additions
from fixtures import recipe


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.grain_list = grain_list

        # Define Hops
        self.hop_additions = hop_additions

        # Define Recipes
        self.recipe = recipe

    def test_get_specific_gravity(self):
        sg = self.recipe.get_specific_gravity()
        self.assertEquals(round(sg, 3), 1.057)

    def test_get_degrees_plato(self):
        deg_plato = self.recipe.get_degrees_plato()
        self.assertEquals(round(deg_plato, 3), 14.003)

    def test_get_extract_weight(self):
        pounds_extract = self.recipe.get_extract_weight()
        self.assertEquals(round(pounds_extract, 2), 6.16)

    def test_get_working_yield(self):
        wy = self.recipe.get_working_yield(self.grain_list[0])
        self.assertEquals(round(wy, 2), 53.20)
        wy = self.recipe.get_working_yield(self.grain_list[1])
        self.assertEquals(round(wy, 2), 49.00)

    def test_get_pounds_malt(self):
        pounds_malt = self.recipe.get_pounds_malt(self.grain_list[0])
        self.assertEquals(round(pounds_malt, 2), 10.99)
        pounds_malt = self.recipe.get_pounds_malt(self.grain_list[1])
        self.assertEquals(round(pounds_malt, 2), 0.63)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 11.62)

    def test_get_total_ibu(self):
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 40.03)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp()
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume()
        self.assertEquals(round(mash_water_vol, 2), 4.19)

    # def test_get_wort_color(self):
    #     wort_color = self.recipe.get_wort_color(self.grain_list[0])
    #     self.assertEquals(round(wort_color, 2), 3.32)
    #     wort_color = self.recipe.get_wort_color(self.grain_list[1])
    #     self.assertEquals(round(wort_color, 2), 1.75)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 5.07)

    def test_get_beer_color(self):
        recipe_color = self.recipe.get_beer_color()
        self.assertEquals(round(recipe_color, 2), 3.55)
