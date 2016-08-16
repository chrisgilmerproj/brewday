import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.recipes import Recipe
from fixtures import grain_additions
from fixtures import hop_additions
from fixtures import recipe
from fixtures import yeast


class TestRecipe(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = grain_additions

        # Define Hops
        self.hop_additions = hop_additions

        # Define Yeast
        self.yeast = yeast

        # Define Recipes
        self.recipe = recipe
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)

    def test_str(self):
        out = str(self.recipe)
        self.assertEquals(out, 'pale ale')

    def test_set_units(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        self.recipe.set_units(SI_UNITS)
        self.assertEquals(self.recipe.units, SI_UNITS)
        self.recipe.set_units(IMPERIAL_UNITS)
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)

    def test_set_raises(self):
        with self.assertRaises(Exception):
            self.recipe.set_units('bad')

    def test_grains_units_mismatch_raises(self):
        grain_additions = [g.change_units() for g in self.grain_additions]
        with self.assertRaises(Exception):
            Recipe(name='pale ale',
                   grain_additions=grain_additions,
                   hop_additions=self.hop_additions,
                   yeast=self.yeast)

    def test_hops_units_mismatch_raises(self):
        hop_additions = [h.change_units() for h in self.hop_additions]
        with self.assertRaises(Exception):
            Recipe(name='pale ale',
                   grain_additions=self.grain_additions,
                   hop_additions=hop_additions,
                   yeast=self.yeast)
