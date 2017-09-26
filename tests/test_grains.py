# -*- coding: utf-8 -*-
import sys
import textwrap
import unittest

from brew.constants import GRAIN_TYPE_CEREAL
from brew.constants import GRAIN_TYPE_DME
from brew.constants import GRAIN_TYPE_LME
from brew.constants import GRAIN_TYPE_SPECIALTY
from brew.constants import IMPERIAL_UNITS
from brew.constants import PPG_DME
from brew.constants import PPG_LME
from brew.constants import SI_UNITS
from brew.exceptions import GrainException
from brew.grains import Grain
from brew.grains import GrainAddition
from fixtures import BHY
from fixtures import crystal
from fixtures import pale
from fixtures import pale_dme
from fixtures import pale_lme
from fixtures import pale_add
from fixtures import ppg_pale


class TestGrains(unittest.TestCase):

    def setUp(self):
        self.grain = pale

    def test_str(self):
        out = str(self.grain)
        self.assertEquals(out, u'pale 2-row')

    def test_unicode(self):
        grain = Grain(u'château pilsen 2rs',
                      color=3.0,
                      ppg=ppg_pale)
        out = str(grain)
        if sys.version_info[0] >= 3:
            self.assertEquals(out, u'château pilsen 2rs')
        else:
            self.assertEquals(out, u'château pilsen 2rs'.encode('utf8'))

    def test_repr(self):
        out = repr(self.grain)
        self.assertEquals(out, u"Grain('pale 2-row', color=2.0, hwe=308.78)")  # noqa

    def test_format(self):
        out = self.grain.format()
        msg = textwrap.dedent(u"""\
            pale 2-row Grain
            -----------------------------------
            Color:             2.0 degL
            PPG:               37.00
            Hot Water Extract: 308.78""")
        self.assertEquals(out, msg)

    def test_get_working_yield(self):
        wy = self.grain.get_working_yield(0.70)
        self.assertEquals(round(wy, 2), 0.56)

    def test_grain_hwe(self):
        pale = Grain(u'pale 2-row',
                     color=2.0,
                     hwe=308.0)
        self.assertEquals(pale.hwe, 308.0)
        self.assertEquals(round(pale.ppg, 2), 36.91)

    def test_grain_no_color_raises(self):
        with self.assertRaises(GrainException) as ctx:
            Grain(u'pale 2-row',
                  ppg=ppg_pale)
        self.assertEquals(str(ctx.exception),
                          u'pale 2-row: Must provide color value')

    def test_grain_no_ppg_or_hwe_raises(self):
        with self.assertRaises(GrainException) as ctx:
            Grain(u'pale 2-row',
                  color=2.0)
        self.assertEquals(str(ctx.exception),
                          u'pale 2-row: Must provide ppg or hwe')

    def test_grain_ppg_hwe_raises(self):
        with self.assertRaises(GrainException) as ctx:
            Grain(u'pale 2-row',
                  color=2.0,
                  ppg=ppg_pale,
                  hwe=308.0)
        self.assertEquals(str(ctx.exception),
                          u'pale 2-row: Cannot provide both ppg and hwe')

    def test_eq(self):
        grain1 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=ppg_pale)
        grain2 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=ppg_pale)
        self.assertEquals(grain1, grain2)

    def test_ne_name(self):
        grain1 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=ppg_pale)
        grain2 = Grain(u'pale row',
                       color=2.0,
                       ppg=ppg_pale)
        self.assertTrue(grain1 != grain2)

    def test_ne_color(self):
        grain1 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=ppg_pale)
        grain2 = Grain(u'pale 2-row',
                       color=4.0,
                       ppg=ppg_pale)
        self.assertTrue(grain1 != grain2)

    def test_ne_ppg(self):
        grain1 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=ppg_pale)
        grain2 = Grain(u'pale 2-row',
                       color=2.0,
                       ppg=35.0)
        self.assertTrue(grain1 != grain2)

    def test_ne_grain_add_class(self):
        self.assertTrue(pale != pale_add)

    def test_to_dict(self):
        out = self.grain.to_dict()
        expected = {u'name': u'pale 2-row',
                    u'color': 2.0,
                    u'ppg': ppg_pale,
                    u'hwe': 308.78,
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.grain.to_json()
        expected = u'{"color": 2.0, "hwe": 308.78, "name": "pale 2-row", "ppg": 37.0}'  # noqa
        self.assertEquals(out, expected)

    def test_convert_to_cereal(self):
        ppg = ppg_pale
        ga_cereal = pale_lme.convert_to_cereal(ppg=ppg)
        self.assertEquals(ga_cereal.ppg, ppg)

    def test_convert_to_cereal_raises(self):
        with self.assertRaises(GrainException) as ctx:
            pale_lme.convert_to_cereal()
        self.assertEquals(str(ctx.exception),
                          u'Must provide PPG to convert to cereal')

    def test_convert_to_lme(self):
        ga_lme = self.grain.convert_to_lme(ppg=PPG_LME)
        self.assertEquals(ga_lme.ppg, PPG_LME)

    def test_convert_to_dme(self):
        ga_dme = self.grain.convert_to_dme(ppg=PPG_DME)
        self.assertEquals(ga_dme.ppg, PPG_DME)


class TestGrainAdditions(unittest.TestCase):

    def setUp(self):
        self.grain_add = pale_add

    def test_str(self):
        out = str(self.grain_add)
        self.assertEquals(out, u'pale 2-row, weight 13.96 lbs')

    def test_unicode(self):
        grain = Grain(u'château pilsen 2rs',
                      color=3.0,
                      ppg=ppg_pale)
        grain_add = GrainAddition(grain,
                                  weight=0.78)
        out = str(grain_add)
        if sys.version_info[0] >= 3:
            self.assertEquals(out, u'château pilsen 2rs, weight 0.78 lbs')  # noqa
        else:
            self.assertEquals(out, u'château pilsen 2rs, weight 0.78 lbs'.encode('utf8'))  # noqa

    def test_repr(self):
        out = repr(self.grain_add)
        self.assertEquals(out, u"GrainAddition(Grain('pale 2-row', color=2.0, hwe=308.78), weight=13.96, grain_type='cereal', units='imperial')")  # noqa

    def test_get_weight_cereal(self):
        grain_add = GrainAddition(pale, weight=13.96,
                                  grain_type=GRAIN_TYPE_CEREAL)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_CEREAL)
        out = grain_add.get_cereal_weight(ppg=ppg_pale)
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 14.35)
        out = grain_add.get_dme_weight()
        self.assertEqual(round(out, 2), 11.74)

    def test_get_weight_lme(self):
        grain_add = GrainAddition(pale_lme, weight=14.35,
                                  grain_type=GRAIN_TYPE_LME)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_LME)
        out = grain_add.get_cereal_weight(ppg=ppg_pale)
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 14.35)
        out = grain_add.get_dme_weight()
        self.assertEqual(round(out, 2), 11.74)

    def test_get_weight_dme(self):
        grain_add = GrainAddition(pale_dme, weight=11.74,
                                  grain_type=GRAIN_TYPE_DME)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_DME)
        out = grain_add.get_cereal_weight(ppg=ppg_pale)
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 14.35)
        out = grain_add.get_dme_weight()
        self.assertEqual(round(out, 2), 11.74)

    def test_get_weight_specialty(self):
        grain_add = GrainAddition(pale, weight=13.96,
                                  grain_type=GRAIN_TYPE_SPECIALTY)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_SPECIALTY)
        out = grain_add.get_cereal_weight(ppg=ppg_pale)
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 14.35)
        out = grain_add.get_dme_weight()
        self.assertEqual(round(out, 2), 11.74)

    def test_get_weight_map(self):
        out = self.grain_add.get_weight_map()
        expected = {
            u'grain_weight': 13.96,
            u'lme_weight': 14.35,
            u'dry_weight': 11.74,
        }
        self.assertEquals(out, expected)

    def test_convert_to_cereal(self):
        grain_add = GrainAddition(pale,
                                  weight=1.0,
                                  grain_type=GRAIN_TYPE_CEREAL)
        ga_cereal = grain_add.convert_to_cereal(ppg=ppg_pale,
                                                brew_house_yield=BHY)
        ga_lme = grain_add.convert_to_lme(ppg=PPG_LME, brew_house_yield=BHY)
        ga_dme = grain_add.convert_to_dme(ppg=PPG_DME, brew_house_yield=BHY)

        self.assertEquals(ga_cereal.weight, 1.0)
        self.assertEquals(round(ga_lme.weight, 2), 0.72)
        self.assertEquals(round(ga_dme.weight, 2), 0.59)

    def test_convert_to_cereal_raises(self):
        grain_add = GrainAddition(pale_lme,
                                  weight=1.0,
                                  grain_type=GRAIN_TYPE_LME)
        with self.assertRaises(GrainException) as ctx:
            grain_add.convert_to_cereal(brew_house_yield=BHY)
        self.assertEquals(str(ctx.exception),
                          u'Must provide PPG to convert to cereal')

    def test_convert_to_lme(self):
        grain_add = GrainAddition(pale_lme,
                                  weight=1.0,
                                  grain_type=GRAIN_TYPE_LME)
        ga_cereal = grain_add.convert_to_cereal(ppg=ppg_pale,
                                                brew_house_yield=BHY)
        ga_lme = grain_add.convert_to_lme(ppg=PPG_LME, brew_house_yield=BHY)
        ga_dme = grain_add.convert_to_dme(ppg=PPG_DME, brew_house_yield=BHY)

        self.assertEquals(round(ga_cereal.weight, 2), 1.39)
        self.assertEquals(ga_lme.weight, 1.0)
        self.assertEquals(round(ga_dme.weight, 2), 0.82)

    def test_convert_to_dme(self):
        grain_add = GrainAddition(pale_dme,
                                  weight=1.0,
                                  grain_type=GRAIN_TYPE_DME)
        ga_cereal = grain_add.convert_to_cereal(ppg=ppg_pale,
                                                brew_house_yield=BHY)
        ga_lme = grain_add.convert_to_lme(ppg=PPG_LME, brew_house_yield=BHY)
        ga_dme = grain_add.convert_to_dme(ppg=PPG_DME, brew_house_yield=BHY)

        self.assertEquals(round(ga_cereal.weight, 2), 1.7)
        self.assertEquals(round(ga_lme.weight, 2), 1.22)
        self.assertEquals(ga_dme.weight, 1.0)

    def test_eq(self):
        grain_add1 = GrainAddition(pale, weight=13.96)
        grain_add2 = GrainAddition(pale, weight=13.96)
        self.assertTrue(grain_add1 == grain_add2)

    def test_ne_grain(self):
        grain_add1 = GrainAddition(pale, weight=13.96)
        grain_add2 = GrainAddition(crystal, weight=13.96)
        self.assertTrue(grain_add1 != grain_add2)

    def test_ne_weight(self):
        grain_add1 = GrainAddition(pale, weight=13.96)
        grain_add2 = GrainAddition(pale, weight=3.96)
        self.assertTrue(grain_add1 != grain_add2)

    def test_ne_grain_type(self):
        grain_add1 = GrainAddition(pale, weight=13.96)
        grain_add2 = GrainAddition(pale, weight=13.96,
                                   grain_type=GRAIN_TYPE_DME)
        self.assertTrue(grain_add1 != grain_add2)

    def test_ne_units(self):
        grain_add1 = GrainAddition(pale, weight=13.96)
        grain_add2 = GrainAddition(pale, weight=13.96,
                                   units=SI_UNITS)
        self.assertTrue(grain_add1 != grain_add2)

    def test_ne_grain_class(self):
        self.assertTrue(pale_add != pale)

    def test_gu(self):
        out = self.grain_add.gu
        expected = 516.52
        self.assertEquals(out, expected)

    def test_get_gravity_units(self):
        out = self.grain_add.get_gravity_units()
        expected = 516.52
        self.assertEquals(out, expected)

    def test_to_dict(self):
        out = self.grain_add.to_dict()
        expected = {u'name': u'pale 2-row',
                    u'data': {
                        u'color': 2.0,
                        u'ppg': ppg_pale,
                        u'hwe': 308.78,
                    },
                    u'grain_type': u'cereal',
                    u'weight': 13.96,
                    u'units': u'imperial',
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.grain_add.to_json()
        expected = u'{"data": {"color": 2.0, "hwe": 308.78, "ppg": 37.0}, "grain_type": "cereal", "name": "pale 2-row", "units": "imperial", "weight": 13.96}'  # noqa
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.grain_add.to_dict()
        GrainAddition.validate(data)

    def test_format(self):
        out = self.grain_add.format()
        msg = textwrap.dedent(u"""\
            pale 2-row Addition
            -----------------------------------
            Grain Type:        cereal
            Weight:            13.96 lbs""")
        self.assertEquals(out, msg)

    def test_grain_change_units_imperial_to_si(self):
        self.assertEquals(self.grain_add.units, IMPERIAL_UNITS)
        self.assertEquals(round(self.grain_add.weight, 2), 13.96)
        grain_add = self.grain_add.change_units()
        self.assertEquals(grain_add.units, SI_UNITS)
        self.assertEquals(round(grain_add.weight, 2), 6.33)

    def test_grain_change_units_si_to_imperial(self):
        grain_add = self.grain_add.change_units()
        self.assertEquals(grain_add.units, SI_UNITS)
        self.assertEquals(round(grain_add.weight, 2), 6.33)
        grain_add = grain_add.change_units()
        self.assertEquals(grain_add.units, IMPERIAL_UNITS)
        self.assertEquals(round(grain_add.weight, 2), 13.96)
