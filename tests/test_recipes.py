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

    def test_repr(self):
        out = repr(self.recipe)
        self.assertEquals(out, "Recipe('pale ale', grain_additions=[GrainAddition(Grain('pale 2-row', color=2.0, hwe=308.78), weight=13.96, grain_type='cereal'), GrainAddition(Grain('crystal C20', color=20.0, hwe=292.09), weight=0.78, grain_type='cereal')], hop_additions=[HopAddition(Hop('centennial', percent_alpha_acids=0.14), weight=0.57, boil_time=60.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, units='imperial'), HopAddition(Hop('cascade', percent_alpha_acids=0.07), weight=0.76, boil_time=5.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, units='imperial')], yeast=Yeast('Wyeast 1056', percent_attenuation=0.75), percent_brew_house_yield='0.7', start_volume=7.0, final_volume=5.0, units=imperial)")  # nopep8

    def test_eq(self):
        recipe1 = Recipe('pale ale')
        recipe2 = Recipe('pale ale')
        self.assertEquals(recipe1, recipe2)

    def test_ne_name(self):
        recipe1 = Recipe('pale ale')
        recipe2 = Recipe('ipa')
        self.assertTrue(recipe1 != recipe2)

    def test_ne_grain_additions(self):
        recipe1 = Recipe('pale ale',
                         grain_additions=grain_additions)
        recipe2 = Recipe('pale ale',
                         grain_additions=[grain_additions[0]])
        self.assertTrue(recipe1 != recipe2)

    def test_ne_hop_additions(self):
        recipe1 = Recipe('pale ale',
                         hop_additions=hop_additions)
        recipe2 = Recipe('pale ale',
                         hop_additions=[hop_additions[0]])
        self.assertTrue(recipe1 != recipe2)

    def test_ne_yeast(self):
        recipe1 = Recipe('pale ale',
                         yeast=yeast)
        recipe2 = Recipe('pale ale',
                         yeast=None)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_percent_brew_house_yield(self):
        recipe1 = Recipe('pale ale',
                         percent_brew_house_yield=0.70)
        recipe2 = Recipe('pale ale',
                         percent_brew_house_yield=0.65)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_start_volume(self):
        recipe1 = Recipe('pale ale',
                         start_volume=7.0)
        recipe2 = Recipe('pale ale',
                         start_volume=6.5)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_final_volume(self):
        recipe1 = Recipe('pale ale',
                         final_volume=6.0)
        recipe2 = Recipe('pale ale',
                         final_volume=5.5)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_units(self):
        recipe1 = Recipe('pale ale',
                         units=IMPERIAL_UNITS)
        recipe2 = Recipe('pale ale',
                         units=SI_UNITS)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_recipe_class(self):
        self.assertTrue(recipe != yeast)

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
