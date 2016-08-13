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

    def test_to_json(self):
        out = self.recipe.to_json()
        expected = '{"data": {"abv_alternative": 378.9715884459693, "abv_standard": 62.544816900030774, "boil_gravity": 1.453839941224713, "bu_to_gu": 0.00143475021660474, "extract_weight": 6.126730690145841, "final_gravity": 1.1588439794286496, "original_gravity": 1.6353759177145983, "percent_brew_house_yield": 0.7, "total_grain_weight": 14.74, "total_ibu": 0.9116057355664553, "total_wort_color_map": {"ebc": {"daniels": 45.167539595407334, "morey": 55.57344378629793, "mosher": 52.18830939311099}, "srm": {"daniels": 22.927685073810828, "morey": 28.209869942283213, "mosher": 26.49152761071624}}, "units": "metric"}, "final_volume": 5.0, "grains": [{"data": {"color": 2.0, "dry_weight": 8.376000000000001, "grain_weight": 13.96, "hwe": 308.78, "lme_weight": 10.47, "percent_malt_bill": 0.9470827679782903, "ppg": 37.0, "short_name": "2-row", "working_yield": 0.5599638594662277, "wort_color_ebc": 40.98679740902168, "wort_color_srm": 20.80548091828512}, "grain_type": "cereal", "name": "pale 2-row", "units": "imperial", "weight": 13.96}, {"data": {"color": 20.0, "dry_weight": 0.46799999999999997, "grain_weight": 0.78, "hwe": 292.09, "lme_weight": 0.585, "percent_malt_bill": 0.052917232021709615, "ppg": 35.0, "short_name": "C20", "working_yield": 0.5296955427383235, "wort_color_ebc": 27.495065885051854, "wort_color_srm": 13.956886236066932}, "grain_type": "cereal", "name": "crystal C20", "units": "imperial", "weight": 0.78}], "hops": [{"boil_time": 60.0, "data": {"ibus": 0.1574211686301996, "percent_alpha_acids": 0.14, "utilization": 0.006732076130876399}, "hop_type": "pellet", "name": "centennial", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {}, "weight": 0.57}, {"boil_time": 5.0, "data": {"ibus": 0.020921720083378285, "percent_alpha_acids": 0.07, "utilization": 0.001342068035853423}, "hop_type": "pellet", "name": "cascade", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {}, "weight": 0.76}], "name": "Pale Ale", "start_volume": 7.0, "yeast": {"data": {"percent_attenuation": 0.75}, "name": "Wyeast 1056"}}'  # nopep8
        self.assertEquals(out, expected)

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

            Morey   (SRM/EBC):  6.58 degL / 12.97
            Daneils (SRM/EBC):  10.14 degL / 19.98
            Mosher  (SRM/EBC):  7.31 degL / 14.40

            Extract Weight:     5.89 lbs
            Total Grain Weight: 14.74 lbs

            Grains
            ===================================

            pale 2-row Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            13.96 lbs
            Weight DME:        8.38 lbs
            Weight LME:        10.47 lbs
            Weight Grain:      13.96 lbs
            Percent Malt Bill: 0.95 %
            Working Yield:     0.56 %
            SRM:               4.85 degL
            EBC:               9.56

            crystal C20 Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            0.78 lbs
            Weight DME:        0.47 lbs
            Weight LME:        0.58 lbs
            Weight Grain:      0.78 lbs
            Percent Malt Bill: 0.05 %
            Working Yield:     0.53 %
            SRM:               3.26 degL
            EBC:               6.42

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
