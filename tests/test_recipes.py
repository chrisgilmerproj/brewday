import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
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
