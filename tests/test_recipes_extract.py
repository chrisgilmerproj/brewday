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
            self.assertEquals(
                recipe_data[key],
                recipe_data_lme[key])

    def test_recipe_is_recipe_dme(self):
        recipe_data = self.recipe.to_dict()[u'data']
        recipe_data_dme = self.recipe_dme.to_dict()[u'data']
        for key in recipe_data.keys():
            self.assertEquals(
                recipe_data[key],
                recipe_data_dme[key])
