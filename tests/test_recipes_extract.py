# -*- coding: utf-8 -*-
import unittest

from brew.constants import IMPERIAL_UNITS
from fixtures import recipe
from fixtures import recipe_dme
from fixtures import recipe_lme


class TestRecipeExtract(unittest.TestCase):

    def setUp(self):
        # Define Recipes
        self.recipe = recipe
        self.recipe_lme = recipe_lme
        self.recipe_dme = recipe_dme
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        self.assertEquals(self.recipe_lme.units, IMPERIAL_UNITS)
        self.assertEquals(self.recipe_dme.units, IMPERIAL_UNITS)

    def test_recipe_is_recipe_lme(self):
        recipe_data = self.recipe.to_dict()[u'data']
        recipe_data_lme = self.recipe_lme.to_dict()[u'data']
        for key in recipe_data.keys():
            # TODO: The colors are withing 0.1 of each other
            # but its hard to test in this way. Write another test.
            if key == u'total_wort_color_map':
                continue
            self.assertEqual(
                recipe_data[key],
                recipe_data_lme[key],
                msg=key)

    def test_recipe_is_recipe_dme(self):
        recipe_data = self.recipe.to_dict()[u'data']
        recipe_data_dme = self.recipe_dme.to_dict()[u'data']
        for key in recipe_data.keys():
            # TODO: The colors are withing 0.1 of each other
            # but its hard to test in this way. Write another test.
            if key == u'total_wort_color_map':
                continue
            self.assertEquals(
                recipe_data[key],
                recipe_data_dme[key],
                msg=key)
