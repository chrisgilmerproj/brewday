import textwrap
import unittest

from brew.constants import GRAIN_TYPE_CEREAL
from brew.constants import GRAIN_TYPE_DME
from brew.constants import GRAIN_TYPE_LME
from brew.constants import GRAIN_TYPE_SPECIALTY
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.grains import Grain
from brew.grains import GrainAddition
from fixtures import pale
from fixtures import pale_add


class TestGrains(unittest.TestCase):

    def setUp(self):
        self.grain = pale

    def test_str(self):
        out = str(self.grain)
        self.assertEquals(out, 'Pale 2-row')

    def test_repr(self):
        out = repr(self.grain)
        self.assertEquals(out, "Grain('pale 2-row', short_name='2-row', color=2.0, hwe=308.78)")  # nopep8

    def test_format(self):
        out = self.grain.format()
        msg = textwrap.dedent("""\
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
        pale = Grain('pale 2-row',
                     short_name='2-row',
                     color=2.0,
                     hwe=308.0)
        self.assertEquals(pale.hwe, 308.0)
        self.assertEquals(round(pale.ppg, 2), 36.91)

    def test_grain_ppg_hwe_raises(self):
        with self.assertRaises(Exception):
            Grain('pale 2-row',
                  short_name='2-row',
                  color=2.0,
                  ppg=37.0,
                  hwe=308.0)

    def test_to_dict(self):
        out = self.grain.to_dict()
        expected = {'name': 'pale 2-row',
                    'short_name': '2-row',
                    'color': 2.0,
                    'ppg': 37.0,
                    'hwe': 308.78,
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.grain.to_json()
        expected = '{"color": 2.0, "hwe": 308.78, "name": "pale 2-row", "ppg": 37.0, "short_name": "2-row"}'  # nopep8
        self.assertEquals(out, expected)


class TestGrainAdditions(unittest.TestCase):

    def setUp(self):
        self.grain_add = pale_add

    def test_str(self):
        out = str(self.grain_add)
        self.assertEquals(out, 'Pale 2-row, weight 13.96 lbs')

    def test_repr(self):
        out = repr(self.grain_add)
        self.assertEquals(out, "GrainAddition(Grain('pale 2-row', short_name='2-row', color=2.0, hwe=308.78), weight=13.96, grain_type='cereal')")  # nopep8

    def test_get_weight_cereal(self):
        grain_add = GrainAddition(pale, weight=13.96,
                                  grain_type=GRAIN_TYPE_CEREAL)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_CEREAL)
        out = grain_add.get_cereal_weight()
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 10.47)
        out = grain_add.get_dry_weight()
        self.assertEqual(round(out, 2), 8.38)

    def test_get_weight_lme(self):
        grain_add = GrainAddition(pale, weight=10.47,
                                  grain_type=GRAIN_TYPE_LME)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_LME)
        out = grain_add.get_cereal_weight()
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 10.47)
        out = grain_add.get_dry_weight()
        self.assertEqual(round(out, 2), 8.38)

    def test_get_weight_dry(self):
        grain_add = GrainAddition(pale, weight=8.38,
                                  grain_type=GRAIN_TYPE_DME)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_DME)
        out = grain_add.get_cereal_weight()
        self.assertEqual(round(out, 2), 13.97)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 10.48)
        out = grain_add.get_dry_weight()
        self.assertEqual(round(out, 2), 8.38)

    def test_get_weight_specialty(self):
        grain_add = GrainAddition(pale, weight=13.96,
                                  grain_type=GRAIN_TYPE_SPECIALTY)
        self.assertEquals(grain_add.grain_type, GRAIN_TYPE_SPECIALTY)
        out = grain_add.get_cereal_weight()
        self.assertEqual(round(out, 2), 13.96)
        out = grain_add.get_lme_weight()
        self.assertEqual(round(out, 2), 12.42)
        out = grain_add.get_dry_weight()
        self.assertEqual(round(out, 2), 9.94)

    def test_get_weight_map(self):
        out = self.grain_add.get_weight_map()
        expected = {
            'grain_weight': 13.96,
            'lme_weight': 10.47,
            'dry_weight': 8.38,
        }
        self.assertEquals(out, expected)

    def test_to_dict(self):
        out = self.grain_add.to_dict()
        expected = {'name': 'pale 2-row',
                    'data': {
                        'short_name': '2-row',
                        'color': 2.0,
                        'ppg': 37.0,
                        'hwe': 308.78,
                    },
                    'grain_type': 'cereal',
                    'weight': 13.96,
                    'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.grain_add.to_json()
        expected = '{"data": {"color": 2.0, "hwe": 308.78, "ppg": 37.0, "short_name": "2-row"}, "grain_type": "cereal", "name": "pale 2-row", "units": "imperial", "weight": 13.96}'  # nopep8
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.grain_add.to_dict()
        GrainAddition.validate(data)

    def test_format(self):
        out = self.grain_add.format()
        msg = textwrap.dedent("""\
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
