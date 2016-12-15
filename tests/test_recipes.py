# -*- coding: utf-8 -*-
import sys
import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.recipes import Recipe
from brew.recipes import RecipeBuilder
from fixtures import builder
from fixtures import grain_additions
from fixtures import grain_list
from fixtures import hop_additions
from fixtures import hop_list
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
        self.assertEquals(out, u'pale ale')

    def test_unicode(self):
        recipe = Recipe(name=u'Kölsch Ale',
                        grain_additions=grain_additions,
                        hop_additions=hop_additions,
                        yeast=yeast,
                        percent_brew_house_yield=0.70,
                        start_volume=7.0,
                        final_volume=5.0,
                        )
        out = str(recipe)
        if sys.version_info[0] >= 3:
            self.assertEquals(out, u'Kölsch Ale')
        else:
            self.assertEquals(out, u'Kölsch Ale'.encode('utf8'))

    def test_repr(self):
        out = repr(self.recipe)
        self.assertEquals(out, u"Recipe('pale ale', grain_additions=[GrainAddition(Grain('pale 2-row', color=2.0, hwe=308.78), weight=13.96, grain_type='cereal', units='imperial'), GrainAddition(Grain('crystal C20', color=20.0, hwe=292.09), weight=0.78, grain_type='cereal', units='imperial')], hop_additions=[HopAddition(Hop('centennial', percent_alpha_acids=0.14), weight=0.57, boil_time=60.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, units='imperial'), HopAddition(Hop('cascade', percent_alpha_acids=0.07), weight=0.76, boil_time=5.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, units='imperial')], yeast=Yeast('Wyeast 1056', percent_attenuation=0.75), percent_brew_house_yield=0.7, start_volume=7.0, final_volume=5.0, units=imperial)")  # noqa

    def test_eq(self):
        recipe1 = Recipe(u'pale ale')
        recipe2 = Recipe(u'pale ale')
        self.assertEquals(recipe1, recipe2)

    def test_ne_name(self):
        recipe1 = Recipe(u'pale ale')
        recipe2 = Recipe(u'ipa')
        self.assertTrue(recipe1 != recipe2)

    def test_ne_grain_additions(self):
        recipe1 = Recipe(u'pale ale',
                         grain_additions=grain_additions)
        recipe2 = Recipe(u'pale ale',
                         grain_additions=[grain_additions[0]])
        self.assertTrue(recipe1 != recipe2)

    def test_ne_hop_additions(self):
        recipe1 = Recipe(u'pale ale',
                         hop_additions=hop_additions)
        recipe2 = Recipe(u'pale ale',
                         hop_additions=[hop_additions[0]])
        self.assertTrue(recipe1 != recipe2)

    def test_ne_yeast(self):
        recipe1 = Recipe(u'pale ale',
                         yeast=yeast)
        recipe2 = Recipe(u'pale ale',
                         yeast=None)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_percent_brew_house_yield(self):
        recipe1 = Recipe(u'pale ale',
                         percent_brew_house_yield=0.70)
        recipe2 = Recipe(u'pale ale',
                         percent_brew_house_yield=0.65)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_start_volume(self):
        recipe1 = Recipe(u'pale ale',
                         start_volume=7.0)
        recipe2 = Recipe(u'pale ale',
                         start_volume=6.5)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_final_volume(self):
        recipe1 = Recipe(u'pale ale',
                         final_volume=6.0)
        recipe2 = Recipe(u'pale ale',
                         final_volume=5.5)
        self.assertTrue(recipe1 != recipe2)

    def test_ne_units(self):
        recipe1 = Recipe(u'pale ale',
                         units=IMPERIAL_UNITS)
        recipe2 = Recipe(u'pale ale',
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
            self.recipe.set_units(u'bad')

    def test_grains_units_mismatch_raises(self):
        grain_additions = [g.change_units() for g in self.grain_additions]
        with self.assertRaises(Exception):
            Recipe(name=u'pale ale',
                   grain_additions=grain_additions,
                   hop_additions=self.hop_additions,
                   yeast=self.yeast)

    def test_hops_units_mismatch_raises(self):
        hop_additions = [h.change_units() for h in self.hop_additions]
        with self.assertRaises(Exception):
            Recipe(name=u'pale ale',
                   grain_additions=self.grain_additions,
                   hop_additions=hop_additions,
                   yeast=self.yeast)


class TestRecipeBuilder(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_list = grain_list

        # Define Recipes
        self.builder = builder
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)

    def test_str(self):
        out = str(self.builder)
        self.assertEquals(out, u'pale ale')

    def test_repr(self):
        out = repr(self.builder)
        self.assertEquals(out, u"RecipeBuilder('pale ale', grain_list=[Grain('pale 2-row', color=2.0, hwe=308.78), Grain('crystal C20', color=20.0, hwe=292.09)], hop_list=[Hop('centennial', percent_alpha_acids=0.14), Hop('cascade', percent_alpha_acids=0.07)], target_og=1.0761348, percent_brew_house_yield=0.7, start_volume=7.0, final_volume=5.0, units=imperial)")  # noqa

    def test_eq(self):
        builder1 = RecipeBuilder(u'pale ale')
        builder2 = RecipeBuilder(u'pale ale')
        self.assertEquals(builder1, builder2)

    def test_ne_name(self):
        builder1 = RecipeBuilder(u'pale ale')
        builder2 = RecipeBuilder(u'ipa')
        self.assertTrue(builder1 != builder2)

    def test_ne_grain_list(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 grain_list=grain_list)
        builder2 = RecipeBuilder(u'pale ale',
                                 grain_list=[grain_list[0]])
        self.assertTrue(builder1 != builder2)

    def test_ne_hop_list(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 hop_list=hop_list)
        builder2 = RecipeBuilder(u'pale ale',
                                 hop_list=[hop_list[0]])
        self.assertTrue(builder1 != builder2)

    def test_ne_percent_brew_house_yield(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 percent_brew_house_yield=0.70)
        builder2 = RecipeBuilder(u'pale ale',
                                 percent_brew_house_yield=0.65)
        self.assertTrue(builder1 != builder2)

    def test_ne_start_volume(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 start_volume=7.0)
        builder2 = RecipeBuilder(u'pale ale',
                                 start_volume=6.5)
        self.assertTrue(builder1 != builder2)

    def test_ne_final_volume(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 final_volume=6.0)
        builder2 = RecipeBuilder(u'pale ale',
                                 final_volume=5.5)
        self.assertTrue(builder1 != builder2)

    def test_ne_units(self):
        builder1 = RecipeBuilder(u'pale ale',
                                 units=IMPERIAL_UNITS)
        builder2 = RecipeBuilder(u'pale ale',
                                 units=SI_UNITS)
        self.assertTrue(builder1 != builder2)

    def test_ne_builder_class(self):
        self.assertTrue(builder != recipe)

    def test_set_units(self):
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)
        self.builder.set_units(SI_UNITS)
        self.assertEquals(self.builder.units, SI_UNITS)
        self.builder.set_units(IMPERIAL_UNITS)
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)

    def test_set_raises(self):
        with self.assertRaises(Exception):
            self.builder.set_units(u'bad')
