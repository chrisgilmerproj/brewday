import textwrap
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

    def test_format(self):
        out = self.recipe.format()
        expected = textwrap.dedent("""\
            Pale Ale
            ===================================

            Brew House Yield:   0.70
            Start Volume:       7.0
            Final Volume:       5.0

            Original Gravity:   1.076
            Boil Gravity:       1.054
            Final Gravity:      1.019

            ABV Standard:       7.49 %
            ABV Alternative:    7.98 %

            IBU:                33.03 ibu
            BU/GU:              0.43

            Morey   (SRM/EBC):  6.45 degL / 12.70
            Daneils (SRM/EBC):  10.09 degL / 19.88
            Mosher  (SRM/EBC):  7.23 degL / 14.25

            Extract Weight:     5.89 lbs
            Total Grain Weight: 14.74 lbs

            Grains
            ===================================

            pale 2-row Addition
            -----------------------------------
            Malt Bill:         13.96 lbs
            Working Yield:     0.56 %
            Weight DME:        8.38 lbs
            Weight LME:        10.47 lbs
            Weight Grain:      13.96 lbs
            SRM:               4.69 degL
            EBC:               9.24

            crystal C20 Addition
            -----------------------------------
            Malt Bill:         0.78 lbs
            Working Yield:     0.53 %
            Weight DME:        0.47 lbs
            Weight LME:        0.58 lbs
            Weight Grain:      0.78 lbs
            SRM:               3.27 degL
            EBC:               6.44

            Hops
            ===================================

            centennial Addition
            -----------------------------------
            Weight:       0.57 oz
            Boil Time:    60.00 min
            Hop Type:     pellet
            IBUs:         23.98
            Utilization:  0.24 %
            Util Cls:     Glenn Tinseth

            cascade Addition
            -----------------------------------
            Weight:       0.76 oz
            Boil Time:    5.00 min
            Hop Type:     pellet
            IBUs:         3.19
            Utilization:  0.05 %
            Util Cls:     Glenn Tinseth

            Yeast
            ===================================

            Wyeast 1056 Yeast
            -----------------------------------
            Attenuation:  0.75 %""")
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.recipe.to_dict()
        Recipe.validate(data)
