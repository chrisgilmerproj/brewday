# -*- coding: utf-8 -*-
import textwrap
import unittest

from brew.constants import GRAIN_TYPE_DME
from brew.constants import GRAIN_TYPE_LME
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.constants import SUCROSE_PLATO
from brew.exceptions import RecipeException
from brew.grains import GrainAddition
from brew.recipes import Recipe
from fixtures import builder
from fixtures import grain_additions
from fixtures import grain_list
from fixtures import hop_additions
from fixtures import pale_dme
from fixtures import pale_lme
from fixtures import ppg_crystal
from fixtures import ppg_pale
from fixtures import recipe
from fixtures import yeast


class TestRecipeImperialUnits(unittest.TestCase):

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

    def test_change_units(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        for hop_add in self.recipe.hop_additions:
            self.assertEquals(hop_add.units, IMPERIAL_UNITS)

        recipe = self.recipe.change_units()
        self.assertEquals(recipe.units, SI_UNITS)
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)

    def test_get_total_points(self):
        out = self.recipe.get_total_points()
        self.assertEquals(round(out, 2), 380.67)

    def test_get_total_points_lme(self):
        pale_lme_add = GrainAddition(pale_lme,
                                     weight=14.35,
                                     grain_type=GRAIN_TYPE_LME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'lme',
                        grain_additions=[pale_lme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_total_points()
        self.assertEquals(round(out, 1), 516.6)

    def test_get_total_points_dme(self):
        pale_dme_add = GrainAddition(pale_dme,
                                     weight=11.74,
                                     grain_type=GRAIN_TYPE_DME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'dme',
                        grain_additions=[pale_dme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_total_points()
        self.assertEquals(round(out, 1), 516.6)

    def test_get_original_gravity_units(self):
        out = self.recipe.get_original_gravity_units()
        self.assertEquals(round(out, 2), 76.13)

    def test_get_original_gravity(self):
        out = self.recipe.get_original_gravity()
        self.assertEquals(round(out, 3), 1.076)

    def test_og(self):
        out = self.recipe.og
        self.assertEquals(round(out, 3), 1.076)

    def test_get_boil_gravity_units(self):
        out = self.recipe.get_boil_gravity_units()
        self.assertEquals(round(out, 2), 54.38)

    def test_get_boil_gravity(self):
        out = self.recipe.get_boil_gravity()
        self.assertEquals(round(out, 3), 1.054)

    def test_bg(self):
        out = self.recipe.bg
        self.assertEquals(round(out, 3), 1.054)

    def test_get_final_gravity_units(self):
        out = self.recipe.get_final_gravity_units()
        self.assertEquals(round(out, 2), 19.03)

    def test_get_final_gravity(self):
        out = self.recipe.get_final_gravity()
        self.assertEquals(round(out, 3), 1.019)

    def test_fg(self):
        out = self.recipe.fg
        self.assertEquals(round(out, 3), 1.019)

    def test_get_degrees_plato(self):
        plato = self.recipe.get_degrees_plato()
        self.assertEquals(round(plato, 2), 13.42)

    def test_plato(self):
        plato = self.recipe.plato
        self.assertEquals(round(plato, 2), 13.42)

    def test_brew_house_yield(self):
        vol_actual = 5.5
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.66)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 5.89)

    def test_get_percent_malt_bill(self):
        out = self.recipe.get_percent_malt_bill(self.grain_additions[0])
        self.assertEquals(round(out, 2), 0.95)
        out = self.recipe.get_percent_malt_bill(self.grain_additions[1])
        self.assertEquals(round(out, 2), 0.05)

    def test_get_grain_add_dry_weight(self):
        out = self.recipe.get_grain_add_dry_weight(self.grain_additions[0])
        self.assertEquals(round(out, 2), 11.74)
        out = self.recipe.get_grain_add_dry_weight(self.grain_additions[1])
        self.assertEquals(round(out, 2), 0.62)

    def test_get_grain_add_dry_weight_lme(self):
        pale_lme_add = GrainAddition(pale_lme,
                                     weight=14.35,
                                     grain_type=GRAIN_TYPE_LME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'lme',
                        grain_additions=[pale_lme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_grain_add_dry_weight(pale_lme_add)
        self.assertEquals(round(out, 2), 11.74)

    def test_get_grain_add_dry_weight_dme(self):
        pale_dme_add = GrainAddition(pale_dme,
                                     weight=11.74,
                                     grain_type=GRAIN_TYPE_DME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'dme',
                        grain_additions=[pale_dme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_grain_add_dry_weight(pale_dme_add)
        self.assertEquals(round(out, 2), 11.74)

    def test_get_total_dry_weight(self):
        out = self.recipe.get_total_dry_weight()
        self.assertEquals(round(out, 2), 12.36)

    def test_get_grain_add_cereal_weight(self):
        out = self.recipe.get_grain_add_cereal_weight(self.grain_additions[0],
                                                      ppg=ppg_pale)
        self.assertEquals(round(out, 2), 13.96)
        out = self.recipe.get_grain_add_cereal_weight(self.grain_additions[1],
                                                      ppg=ppg_crystal)
        self.assertEquals(round(out, 2), 0.78)

    def test_get_grain_add_cereal_weight_lme(self):
        pale_lme_add = GrainAddition(pale_lme,
                                     weight=14.35,
                                     grain_type=GRAIN_TYPE_LME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'lme',
                        grain_additions=[pale_lme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_grain_add_cereal_weight(pale_lme_add,
                                                 ppg=ppg_pale)
        self.assertEquals(round(out, 2), 13.96)

    def test_get_grain_add_cereal_weight_dme(self):
        pale_dme_add = GrainAddition(pale_dme,
                                     weight=11.74,
                                     grain_type=GRAIN_TYPE_DME,
                                     units=IMPERIAL_UNITS)
        recipe = Recipe(u'dme',
                        grain_additions=[pale_dme_add],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=IMPERIAL_UNITS)

        out = recipe.get_grain_add_cereal_weight(pale_dme_add,
                                                 ppg=ppg_pale)
        self.assertEquals(round(out, 2), 13.96)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 14.74)

    def test_get_percent_ibus(self):
        percent_ibus = self.recipe.get_percent_ibus(self.hop_additions[0])
        self.assertEquals(round(percent_ibus, 2), 0.88)
        percent_ibus = self.recipe.get_percent_ibus(self.hop_additions[1])
        self.assertEquals(round(percent_ibus, 2), 0.12)

    def test_get_total_ibu(self):
        self.assertEqual(round(self.recipe.get_boil_gravity(), 3), 1.054)
        self.assertEqual(round(self.recipe.final_volume, 2), 5.0)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 33.03)

    def test_ibu(self):
        total_ibu = self.recipe.ibu
        self.assertEquals(round(total_ibu, 2), 33.03)

    def test_bu_to_gu(self):
        self.assertEqual(round(self.recipe.get_bu_to_gu(), 2), 0.61)

    def test_abv(self):
        abv = self.recipe.abv
        self.assertEqual(round(abv, 4), 0.0749)

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 4.85)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.26)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 6.58)

    def test_color(self):
        total_wort_color = self.recipe.color
        self.assertEquals(round(total_wort_color, 2), 6.58)

    def test_get_total_wort_color_map(self):
        wort_map = self.recipe.get_total_wort_color_map()
        expected = {
            u'srm': {u'daniels': u'N/A', u'morey': 6.6, u'mosher': 7.3},
            u'ebc': {u'daniels': u'N/A', u'morey': 13.0, u'mosher': 14.4},
        }
        self.assertEquals(wort_map, expected)

    def test_to_json(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        out = self.recipe.to_json()
        expected = u'{"data": {"abv_alternative": 0.0798, "abv_standard": 0.0749, "abw_alternative": 0.0633, "abw_standard": 0.0595, "boil_gravity": 1.054, "brew_house_yield": 0.7, "bu_to_gu": 0.6, "final_gravity": 1.019, "original_gravity": 1.076, "total_ibu": 33.0, "total_wort_color_map": {"ebc": {"daniels": "N/A", "morey": 13.0, "mosher": 14.4}, "srm": {"daniels": "N/A", "morey": 6.6, "mosher": 7.3}}, "units": "imperial"}, "final_volume": 5.0, "grains": [{"data": {"color": 2.0, "hwe": 308.78, "percent_malt_bill": 0.95, "ppg": 37.0, "working_yield": 0.56, "wort_color_ebc": 9.6, "wort_color_srm": 4.9}, "grain_type": "cereal", "name": "pale 2-row", "units": "imperial", "weight": 13.96}, {"data": {"color": 20.0, "hwe": 292.09, "percent_malt_bill": 0.05, "ppg": 35.0, "working_yield": 0.53, "wort_color_ebc": 6.4, "wort_color_srm": 3.3}, "grain_type": "cereal", "name": "crystal C20", "units": "imperial", "weight": 0.78}], "hops": [{"boil_time": 60.0, "data": {"ibus": 29.2, "percent_alpha_acids": 0.14, "utilization": 0.244}, "hop_type": "pellet", "name": "centennial", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {}, "weight": 0.57}, {"boil_time": 5.0, "data": {"ibus": 3.9, "percent_alpha_acids": 0.07, "utilization": 0.049}, "hop_type": "pellet", "name": "cascade", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {}, "weight": 0.76}], "name": "pale ale", "start_volume": 7.0, "yeast": {"data": {"percent_attenuation": 0.75}, "name": "Wyeast 1056"}}'  # noqa
        self.assertEquals(out, expected)

    def test_format(self):
        self.assertEquals(self.recipe.units, IMPERIAL_UNITS)
        out = self.recipe.format()
        expected = textwrap.dedent(u"""\
            pale ale
            ===================================

            Brew House Yield:   70.0%
            Start Volume:       7.0
            Final Volume:       5.0

            Boil Gravity:       1.054 (Evaporation @ 0.0%)
            Original Gravity:   1.076
            Final Gravity:      1.019

            ABV / ABW Standard: 7.49% / 5.95%
            ABV / ABW Alt:      7.98% / 6.33%

            IBU:                33.0 ibu
            BU/GU:              0.6

            Morey   (SRM/EBC):  6.6 degL / 13.0
            Daniels (SRM/EBC):  N/A degL / N/A
            Mosher  (SRM/EBC):  7.3 degL / 14.4

            Grains
            ===================================

            pale 2-row Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            13.96 lbs
            Percent Malt Bill: 95.0%
            Working Yield:     56.0%
            SRM/EBC:           4.9 degL / 9.6

            crystal C20 Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            0.78 lbs
            Percent Malt Bill: 5.0%
            Working Yield:     53.0%
            SRM/EBC:           3.3 degL / 6.4

            Hops
            ===================================

            centennial Addition
            -----------------------------------
            Hop Type:     pellet
            AA %:         14.0%
            Weight:       0.57 oz
            Boil Time:    60.0 min
            IBUs:         29.2
            Utilization:  24.4%

            cascade Addition
            -----------------------------------
            Hop Type:     pellet
            AA %:         7.0%
            Weight:       0.76 oz
            Boil Time:    5.0 min
            IBUs:         3.9
            Utilization:  4.9%

            Yeast
            ===================================

            Wyeast 1056 Yeast
            -----------------------------------
            Attenuation:  75.0%""")
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.recipe.to_dict()
        Recipe.validate(data)


class TestRecipeBuilderImperialUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_list = grain_list

        # Define Recipes
        self.builder = builder
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)

    def test_change_units(self):
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)
        builder = self.builder.change_units()
        self.assertEquals(builder.units, SI_UNITS)
        self.assertEquals(self.builder.units, IMPERIAL_UNITS)

    def test_get_grain_additions(self):
        percent_list = [0.95, 0.05]
        out = self.builder.get_grain_additions(percent_list)
        expected = grain_additions
        self.assertEquals(out, expected)

    def test_get_grain_additions_raises_percent_sum_invalid(self):
        percent_list = [0.90, 0.05]
        with self.assertRaises(RecipeException) as ctx:
            self.builder.get_grain_additions(percent_list)
        self.assertEquals(str(ctx.exception),
                          u"Percentages must sum to 1.0")

    def test_get_grain_additions_raises_percent_length_mismatch(self):
        percent_list = [0.90, 0.05, 0.05]
        with self.assertRaises(RecipeException) as ctx:
            self.builder.get_grain_additions(percent_list)
        self.assertEquals(str(ctx.exception),
                          u"The length of percent_list must equal length of self.grain_list")  # noqa

    def test_get_hop_additions(self):
        percent_list = [0.8827, 0.1173]
        boil_time_list = [60.0, 5.0]
        out = self.builder.get_hop_additions(percent_list, boil_time_list)
        expected = hop_additions
        self.assertEquals(out, expected)

    def test_get_hop_additions_raises_percent_sum_invalid(self):
        percent_list = [0.8827, 0.2173]
        boil_time_list = [60.0, 5.0]
        with self.assertRaises(RecipeException) as ctx:
            self.builder.get_hop_additions(percent_list, boil_time_list)
        self.assertEquals(str(ctx.exception),
                          u"Percentages must sum to 1.0")

    def test_get_hop_additions_raises_percent_length_mismatch(self):
        percent_list = [0.8827, 0.0173, 0.10]
        boil_time_list = [60.0, 5.0]
        with self.assertRaises(RecipeException) as ctx:
            self.builder.get_hop_additions(percent_list, boil_time_list)
        self.assertEquals(str(ctx.exception),
                          u"The length of percent_list must equal length of self.grain_list")  # noqa

    def test_get_hop_additions_raises_boil_time_length_mismatch(self):
        percent_list = [0.8827, 0.1173]
        boil_time_list = [60.0, 5.0, 5.0]
        with self.assertRaises(RecipeException) as ctx:
            self.builder.get_hop_additions(percent_list, boil_time_list)
        self.assertEquals(str(ctx.exception),
                          u"The length of boil_time_list must equal length of self.hop_list")  # noqa

    def test_get_yeast_attenuation(self):
        abv = 0.0749
        attenuation = self.builder.get_yeast_attenuation(abv)
        self.assertEquals(round(attenuation, 2), 0.75)
