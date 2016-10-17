import textwrap
import unittest

from brew.constants import GRAIN_TYPE_DME
from brew.constants import GRAIN_TYPE_LME
from brew.constants import IMPERIAL_UNITS
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.constants import SUCROSE_PLATO
from brew.grains import GrainAddition
from brew.recipes import Recipe
from fixtures import builder
from fixtures import grain_additions
from fixtures import grain_list
from fixtures import hop_additions
from fixtures import pale
from fixtures import recipe
from fixtures import yeast


class TestRecipeSIUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = [ga.change_units() for ga in
                                grain_additions]

        # Define Hops
        self.hop_additions = [ha.change_units() for ha in
                              hop_additions]

        # Define Yeast
        self.yeast = yeast

        # Define Recipes
        self.recipe = recipe.change_units()
        self.assertEquals(self.recipe.units, SI_UNITS)

    def test_change_units(self):
        self.assertEquals(self.recipe.units, SI_UNITS)
        self.assertEquals(round(self.recipe.start_volume, 2), 26.50)
        self.assertEquals(round(self.recipe.final_volume, 2), 18.93)
        self.assertEquals(round(self.recipe.grain_additions[0].weight, 2), 6.33)  # nopep8
        self.assertEquals(round(self.recipe.grain_additions[1].weight, 2), 0.35)  # nopep8
        self.assertEquals(round(self.recipe.hop_additions[0].weight, 2), 16159.21)  # nopep8
        self.assertEquals(round(self.recipe.hop_additions[1].weight, 2), 21545.62)  # nopep8
        for grain_add in self.recipe.grain_additions:
            self.assertEquals(grain_add.units, SI_UNITS)
        for hop_add in self.recipe.hop_additions:
            self.assertEquals(hop_add.units, SI_UNITS)

        recipe = self.recipe.change_units()
        self.assertEquals(recipe.units, IMPERIAL_UNITS)
        self.assertEquals(self.recipe.units, SI_UNITS)

    def test_get_total_points(self):
        out = self.recipe.get_total_points()
        self.assertEquals(round(out, 2), 1441.01)

    def test_get_total_points_lme(self):
        pale_lme = GrainAddition(pale,
                                 weight=4.75,
                                 grain_type=GRAIN_TYPE_LME,
                                 units=SI_UNITS)
        recipe = Recipe('lme',
                        grain_additions=[pale_lme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_total_points()
        self.assertEquals(round(out, 2), 1466.71)

    def test_get_total_points_dme(self):
        pale_dme = GrainAddition(pale,
                                 weight=3.80,
                                 grain_type=GRAIN_TYPE_DME,
                                 units=SI_UNITS)
        recipe = Recipe('dme',
                        grain_additions=[pale_dme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_total_points()
        self.assertEquals(round(out, 2), 1173.36)

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
        vol_actual = 5.5 * LITER_PER_GAL
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.66)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 2.68)

    def test_get_percent_malt_bill(self):
        out = self.recipe.get_percent_malt_bill(self.grain_additions[0])
        self.assertEquals(round(out, 2), 0.95)
        out = self.recipe.get_percent_malt_bill(self.grain_additions[1])
        self.assertEquals(round(out, 2), 0.05)

    def test_get_grain_add_dry_weight(self):
        out = self.recipe.get_grain_add_dry_weight(self.grain_additions[0])
        self.assertEquals(round(out, 2), 2.66)
        out = self.recipe.get_grain_add_dry_weight(self.grain_additions[1])
        self.assertEquals(round(out, 2), 0.15)

    def test_get_grain_add_dry_weight_lme(self):
        pale_lme = GrainAddition(pale,
                                 weight=4.75,
                                 grain_type=GRAIN_TYPE_LME,
                                 units=SI_UNITS)
        recipe = Recipe('lme',
                        grain_additions=[pale_lme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_grain_add_dry_weight(pale_lme)
        self.assertEquals(round(out, 2), 3.80)

    def test_get_grain_add_dry_weight_dme(self):
        pale_dme = GrainAddition(pale,
                                 weight=3.80,
                                 grain_type=GRAIN_TYPE_DME,
                                 units=SI_UNITS)
        recipe = Recipe('dme',
                        grain_additions=[pale_dme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_grain_add_dry_weight(pale_dme)
        self.assertEquals(round(out, 2), 3.80)

    def test_get_total_dry_weight(self):
        out = self.recipe.get_total_dry_weight()
        self.assertEquals(round(out, 2), 2.81)

    def test_get_grain_add_cereal_weight(self):
        out = self.recipe.get_grain_add_cereal_weight(self.grain_additions[0])
        self.assertEquals(round(out, 2), 6.33)
        out = self.recipe.get_grain_add_cereal_weight(self.grain_additions[1])
        self.assertEquals(round(out, 2), 0.35)

    def test_get_grain_add_cereal_weight_lme(self):
        pale_lme = GrainAddition(pale,
                                 weight=4.75,
                                 grain_type=GRAIN_TYPE_LME,
                                 units=SI_UNITS)
        recipe = Recipe('lme',
                        grain_additions=[pale_lme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_grain_add_cereal_weight(pale_lme)
        self.assertEquals(round(out, 2), 9.05)

    def test_get_grain_add_cereal_weight_dme(self):
        pale_dme = GrainAddition(pale,
                                 weight=3.80,
                                 grain_type=GRAIN_TYPE_DME,
                                 units=SI_UNITS)
        recipe = Recipe('dme',
                        grain_additions=[pale_dme],
                        hop_additions=self.hop_additions,
                        yeast=self.yeast,
                        units=SI_UNITS)

        out = recipe.get_grain_add_cereal_weight(pale_dme)
        self.assertEquals(round(out, 2), 9.05)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.recipe.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 6.69)

    def test_get_percent_ibus(self):
        percent_ibus = self.recipe.get_percent_ibus(self.hop_additions[0])
        self.assertEquals(round(percent_ibus, 2), 0.88)
        percent_ibus = self.recipe.get_percent_ibus(self.hop_additions[1])
        self.assertEquals(round(percent_ibus, 2), 0.12)

    def test_get_total_ibu(self):
        self.assertEqual(round(self.recipe.get_boil_gravity(), 3), 1.054)
        self.assertEqual(round(self.recipe.final_volume, 2), 18.93)
        total_ibu = self.recipe.get_total_ibu()
        self.assertEquals(round(total_ibu, 2), 33.03)

    def test_bu_to_gu(self):
        self.assertEqual(round(self.recipe.get_bu_to_gu(), 2), 0.61)

    def test_get_strike_temp(self):
        strike_temp = self.recipe.get_strike_temp(152.0, 60.0, 3.0 / 1.0)
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.recipe.get_mash_water_volume(3.0 / 1.0)
        self.assertEquals(round(mash_water_vol, 2), 8.42)

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
            'srm': {'daniels': 'N/A', 'morey': 6.6, 'mosher': 7.3},
            'ebc': {'daniels': 'N/A', 'morey': 13.0, 'mosher': 14.4},
        }
        self.assertEquals(wort_map, expected)

    def test_to_json(self):
        self.assertEquals(self.recipe.units, SI_UNITS)
        out = self.recipe.to_json()
        expected = '{"data": {"abv_alternative": 0.0798, "abv_standard": 0.0749, "abw_alternative": 0.0633, "abw_standard": 0.0595, "boil_gravity": 1.054, "bu_to_gu": 0.6, "final_gravity": 1.019, "original_gravity": 1.076, "percent_brew_house_yield": 0.7, "total_ibu": 33.0, "total_wort_color_map": {"ebc": {"daniels": "N/A", "morey": 13.0, "mosher": 14.4}, "srm": {"daniels": "N/A", "morey": 6.6, "mosher": 7.3}}, "units": "metric"}, "final_volume": 18.93, "grains": [{"data": {"color": 2.0, "hwe": 308.78, "percent_malt_bill": 0.95, "ppg": 37.0, "working_yield": 0.56, "wort_color_ebc": 9.6, "wort_color_srm": 4.9}, "grain_type": "cereal", "name": "pale 2-row", "units": "metric", "weight": 6.33}, {"data": {"color": 20.0, "hwe": 292.09, "percent_malt_bill": 0.05, "ppg": 35.0, "working_yield": 0.53, "wort_color_ebc": 6.4, "wort_color_srm": 3.3}, "grain_type": "cereal", "name": "crystal C20", "units": "metric", "weight": 0.35}], "hops": [{"boil_time": 60.0, "data": {"ibus": 29.2, "percent_alpha_acids": 0.14, "utilization": 0.24}, "hop_type": "pellet", "name": "centennial", "units": "metric", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "metric"}, "weight": 16159.21}, {"boil_time": 5.0, "data": {"ibus": 3.9, "percent_alpha_acids": 0.07, "utilization": 0.05}, "hop_type": "pellet", "name": "cascade", "units": "metric", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "metric"}, "weight": 21545.62}], "name": "pale ale", "start_volume": 26.5, "yeast": {"data": {"percent_attenuation": 0.75}, "name": "Wyeast 1056"}}'  # nopep8
        self.assertEquals(out, expected)

    def test_format(self):
        self.assertEquals(self.recipe.units, SI_UNITS)
        out = self.recipe.format()
        expected = textwrap.dedent("""\
            pale ale
            ===================================

            Brew House Yield:   70.0%
            Start Volume:       26.5
            Final Volume:       18.9

            Boil Gravity:       1.054
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
            Weight:            6.33 kg
            Percent Malt Bill: 95.0%
            Working Yield:     56.0%
            SRM/EBC:           4.9 degL / 9.6

            crystal C20 Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            0.35 kg
            Percent Malt Bill: 5.0%
            Working Yield:     53.0%
            SRM/EBC:           3.3 degL / 6.4

            Hops
            ===================================

            centennial Addition
            -----------------------------------
            Hop Type:     pellet
            AA %:         14.0%
            Weight:       16159.21 mg
            Boil Time:    60.0 min
            IBUs:         29.2
            Utilization:  24.0%

            cascade Addition
            -----------------------------------
            Hop Type:     pellet
            AA %:         7.0%
            Weight:       21545.62 mg
            Boil Time:    5.0 min
            IBUs:         3.9
            Utilization:  5.0%

            Yeast
            ===================================

            Wyeast 1056 Yeast
            -----------------------------------
            Attenuation:  75.0%""")
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.recipe.to_dict()
        Recipe.validate(data)


class TestRecipeBuilderSIUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_list = grain_list

        # Define Recipes
        self.builder = builder.change_units()
        self.assertEquals(self.builder.units, SI_UNITS)

    def test_change_units(self):
        self.assertEquals(self.builder.units, SI_UNITS)
        builder = self.builder.change_units()
        self.assertEquals(builder.units, IMPERIAL_UNITS)
        self.assertEquals(self.builder.units, SI_UNITS)

    def test_get_grain_additions(self):
        percent_list = [0.95, 0.05]
        out = self.builder.get_grain_additions(percent_list)
        expected = [ga.change_units() for ga in grain_additions]
        self.assertEquals(out[0], expected[0])

    def test_get_grain_additions_raises_sum_invalid(self):
        percent_list = [0.90, 0.05]
        with self.assertRaises(Exception):
            self.builder.get_grain_additions(percent_list)

    def test_get_grain_additions_raises_length_mismatch(self):
        percent_list = [0.90, 0.05, 0.05]
        with self.assertRaises(Exception):
            self.builder.get_grain_additions(percent_list)

    def test_get_hop_additions(self):
        percent_list = [0.8827, 0.1173]
        boil_time_list = [60.0, 5.0]
        out = self.builder.get_hop_additions(percent_list, boil_time_list)
        expected = [ha.change_units() for ha in hop_additions]
        self.assertEquals(out, expected)

    def test_get_hop_additions_raises_percent_sum_invalid(self):
        percent_list = [0.8827, 0.2173]
        boil_time_list = [60.0, 5.0]
        with self.assertRaises(Exception):
            self.builder.get_hop_additions(percent_list, boil_time_list)

    def test_get_hop_additions_raises_percent_length_mismatch(self):
        percent_list = [0.8827, 0.0173, 0.10]
        boil_time_list = [60.0, 5.0]
        with self.assertRaises(Exception):
            self.builder.get_hop_additions(percent_list, boil_time_list)

    def test_get_hop_additions_raises_boil_time_length_mismatch(self):
        percent_list = [0.8827, 0.1173]
        boil_time_list = [60.0, 5.0, 5.0]
        with self.assertRaises(Exception):
            self.builder.get_hop_additions(percent_list, boil_time_list)

    def test_get_yeast_attenuation(self):
        abv = 0.0749
        attenuation = self.builder.get_yeast_attenuation(abv)
        self.assertEquals(round(attenuation, 2), 0.75)
