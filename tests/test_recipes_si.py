import textwrap
import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import LITER_PER_GAL
from brew.constants import SI_UNITS
from brew.constants import SUCROSE_PLATO
from brew.recipes import Recipe
from fixtures import grain_additions
from fixtures import hop_additions
from fixtures import recipe


class TestRecipeSIUnits(unittest.TestCase):

    def setUp(self):
        # Define Grains
        self.grain_additions = [ga.change_units() for ga in
                                grain_additions]

        # Define Hops
        self.hop_additions = [ha.change_units() for ha in
                              hop_additions]

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

    def test_get_original_gravity_units(self):
        out = self.recipe.get_original_gravity_units()
        self.assertEquals(round(out, 2), 76.13)

    def test_get_original_gravity(self):
        out = self.recipe.get_original_gravity()
        self.assertEquals(round(out, 3), 1.076)

    def test_get_boil_gravity_units(self):
        out = self.recipe.get_boil_gravity_units()
        self.assertEquals(round(out, 2), 54.38)

    def test_get_boil_gravity(self):
        out = self.recipe.get_boil_gravity()
        self.assertEquals(round(out, 3), 1.054)

    def test_get_final_gravity_units(self):
        out = self.recipe.get_final_gravity_units()
        self.assertEquals(round(out, 2), 19.03)

    def test_get_final_gravity(self):
        out = self.recipe.get_final_gravity()
        self.assertEquals(round(out, 3), 1.019)

    def test_brew_house_yield(self):
        vol_actual = 5.5 * LITER_PER_GAL
        bhy = self.recipe.get_brew_house_yield(SUCROSE_PLATO, vol_actual)
        self.assertEqual(round(bhy, 2), 0.66)

    def test_get_extract_weight(self):
        extract_weight = self.recipe.get_extract_weight()
        self.assertEquals(round(extract_weight, 2), 2.68)

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

    def test_get_wort_color(self):
        wort_color = self.recipe.get_wort_color(self.grain_additions[0])
        self.assertEquals(round(wort_color, 2), 4.85)
        wort_color = self.recipe.get_wort_color(self.grain_additions[1])
        self.assertEquals(round(wort_color, 2), 3.26)

    def test_get_total_wort_color(self):
        total_wort_color = self.recipe.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 6.58)

    def test_get_total_wort_color_map(self):
        wort_map = self.recipe.get_total_wort_color_map()
        expected = {
            'srm': {'daniels': 10.1408,
                    'morey': 6.582338571537348,
                    'mosher': 7.3112},
            'ebc': {'daniels': 19.977376,
                    'morey': 12.967206985928575,
                    'mosher': 14.403064}
        }
        self.assertEquals(wort_map, expected)

    def test_to_json(self):
        out = self.recipe.to_json()
        expected = '{"data": {"abv_alternative": 7.977918720821163, "abv_standard": 7.494519374999988, "abw_alternative": 6.331276296843674, "abw_standard": 5.94765057599999, "boil_gravity": 1.054382, "bu_to_gu": 0.6073963307717898, "final_gravity": 1.0190337, "original_gravity": 1.0761348, "percent_brew_house_yield": 0.7, "total_ibu": 33.031427260031464, "total_wort_color_map": {"ebc": {"daniels": 19.977376, "morey": 12.967206985928575, "mosher": 14.403064}, "srm": {"daniels": 10.1408, "morey": 6.582338571537348, "mosher": 7.3112}}, "units": "metric"}, "final_volume": 18.92705, "grains": [{"data": {"color": 2.0, "hwe": 308.78, "percent_malt_bill": 0.9470827679782904, "ppg": 37.0, "short_name": "2-row", "working_yield": 0.5599638594662277, "wort_color_ebc": 9.563637764412702, "wort_color_srm": 4.854638459092742}, "grain_type": "cereal", "name": "pale 2-row", "units": "metric", "weight": 6.33214432}, {"data": {"color": 20.0, "hwe": 292.09, "percent_malt_bill": 0.05291723202170964, "ppg": 35.0, "short_name": "C20", "working_yield": 0.5296955427383235, "wort_color_ebc": 6.415550056502296, "wort_color_srm": 3.256624394163602}, "grain_type": "cereal", "name": "crystal C20", "units": "metric", "weight": 0.35380176}], "hops": [{"boil_time": 60.0, "data": {"ibus": 29.156452036327828, "percent_alpha_acids": 0.14, "utilization": 0.24393229918399}, "hop_type": "pellet", "name": "centennial", "units": "metric", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "metric"}, "weight": 16159.214999999998}, {"boil_time": 5.0, "data": {"ibus": 3.8749752237036366, "percent_alpha_acids": 0.07, "utilization": 0.04862894228803807}, "hop_type": "pellet", "name": "cascade", "units": "metric", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "metric"}, "weight": 21545.62}], "name": "Pale Ale", "start_volume": 26.497870000000002, "yeast": {"data": {"percent_attenuation": 0.75}, "name": "Wyeast 1056"}}'  # nopep8
        self.assertEquals(out, expected)

    def test_format(self):
        out = self.recipe.format()
        expected = textwrap.dedent("""\
            Pale Ale
            ===================================

            Brew House Yield:   0.70
            Start Volume:       26.5
            Final Volume:       18.9

            Original Gravity:   1.076
            Boil Gravity:       1.054
            Final Gravity:      1.019

            ABV / ABW Standard: 7.49 % / 5.95 %
            ABV / ABW Alt:      7.98 % / 6.33 %

            IBU:                33.03 ibu
            BU/GU:              0.61

            Morey   (SRM/EBC):  6.58 degL / 12.97
            Daneils (SRM/EBC):  10.14 degL / 19.98
            Mosher  (SRM/EBC):  7.31 degL / 14.40

            Grains
            ===================================

            pale 2-row Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            6.33 kg
            Percent Malt Bill: 0.95 %
            Working Yield:     0.56 %
            SRM:               4.85 degL
            EBC:               9.56

            crystal C20 Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            0.35 kg
            Percent Malt Bill: 0.05 %
            Working Yield:     0.53 %
            SRM:               3.26 degL
            EBC:               6.42

            Hops
            ===================================

            centennial Addition
            -----------------------------------
            Weight:       16159.21 mg
            Boil Time:    60.00 min
            Hop Type:     pellet
            IBUs:         29.16
            Utilization:  0.24 %
            Util Cls:     Glenn Tinseth

            cascade Addition
            -----------------------------------
            Weight:       21545.62 mg
            Boil Time:    5.00 min
            Hop Type:     pellet
            IBUs:         3.87
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
