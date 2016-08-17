import textwrap
import unittest

from brew.constants import LITER_PER_GAL
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.hops import HopAddition
from brew.utilities.sugar import plato_to_sg
from fixtures import cascade
from fixtures import centennial


class TestHops(unittest.TestCase):

    def setUp(self):

        # Define Hops
        self.hop = centennial

    def test_str(self):
        out = str(self.hop)
        self.assertEquals(out, 'Centennial, alpha 0.14%')

    def test_repr(self):
        out = repr(self.hop)
        self.assertEquals(out, "Hop('centennial', percent_alpha_acids=0.14)")

    def test_to_dict(self):
        out = self.hop.to_dict()
        expected = {'name': 'centennial',
                    'percent_alpha_acids': 0.14,
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.hop.to_json()
        expected = '{"name": "centennial", "percent_alpha_acids": 0.14}'
        self.assertEquals(out, expected)

    def test_format(self):
        out = self.hop.format()
        msg = textwrap.dedent("""\
                centennial Hops
                -----------------------------------
                Alpha Acids:  0.14 %""")
        self.assertEquals(out, msg)


class TestHopAdditions(unittest.TestCase):

    def setUp(self):
        self.hop1 = centennial
        self.hop2 = cascade
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
                'utilization_cls_kwargs': {'units': IMPERIAL_UNITS},
            },
            {
                'boil_time': 5.0,
                'weight': 0.76,
                'utilization_cls_kwargs': {'units': IMPERIAL_UNITS},
            },
        ]

        # Additions
        self.hop_addition1 = HopAddition(self.hop1,
                                         **self.addition_kwargs[0])
        self.hop_addition2 = HopAddition(self.hop2,
                                         **self.addition_kwargs[1])

        # Define Hops
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.target_ibu = 40.0
        self.final_volume = 5.0

    def test_change_units(self):
        self.assertEquals(self.hop_addition1.units, IMPERIAL_UNITS)
        ha = self.hop_addition1.change_units()
        self.assertEquals(ha.units, SI_UNITS)
        self.assertEquals(ha.utilization_cls.units, SI_UNITS)
        ha = ha.change_units()
        self.assertEquals(ha.units, IMPERIAL_UNITS)
        self.assertEquals(ha.utilization_cls.units, IMPERIAL_UNITS)

    def test_str(self):
        out = str(self.hop_addition1)
        self.assertEquals(
            out, 'Centennial, alpha 0.14%, 0.57 oz, 60.0 min, pellet')

    def test_repr(self):
        out = repr(self.hop_addition1)
        self.assertEquals(
                out, "HopAddition(Hop('centennial', percent_alpha_acids=0.14), weight=0.57, boil_time=60.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, utilization_cls_kwargs={'units': 'imperial'}, units='imperial')")  # nopep8

    def test_to_dict(self):
        out = self.hop_addition1.to_dict()
        expected = {'name': 'centennial',
                    'data': {'percent_alpha_acids': 0.14},
                    'weight': 0.57,
                    'boil_time': 60.0,
                    'hop_type': 'pellet',
                    'utilization_cls': 'Glenn Tinseth',
                    'utilization_cls_kwargs': {'units': 'imperial'},
                    'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.hop_addition1.to_json()
        expected = '{"boil_time": 60.0, "data": {"percent_alpha_acids": 0.14}, "hop_type": "pellet", "name": "centennial", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "imperial"}, "weight": 0.57}'  # nopep8
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.hop_addition1.to_dict()
        HopAddition.validate(data)

    def test_format(self):
        out = self.hop_addition1.format()
        msg = textwrap.dedent("""\
                centennial Addition
                -----------------------------------
                Hop Type:     pellet
                AA %:         0.14 %
                Weight:       0.57 oz
                Boil Time:    60.0 min""")
        self.assertEquals(out, msg)

    def test_get_hops_weight(self):
        hops_weight = self.hop_addition1.get_hops_weight(
            self.sg,
            self.target_ibu,
            self.final_volume,
            0.95)
        self.assertEquals(round(hops_weight, 2), 0.84)

        hops_weight = self.hop_addition2.get_hops_weight(
            self.sg,
            self.target_ibu,
            self.final_volume,
            0.05)
        self.assertEquals(round(hops_weight, 2), 0.44)

    def test_get_hops_weight_metric(self):
        ha1 = self.hop_addition1.change_units()
        hops_weight = ha1.get_hops_weight(
            self.sg,
            self.target_ibu,
            self.final_volume * LITER_PER_GAL,
            0.95)
        self.assertEquals(round(hops_weight, 2), 23684.97)

        ha2 = self.hop_addition2.change_units()
        hops_weight = ha2.get_hops_weight(
            self.sg,
            self.target_ibu,
            self.final_volume * LITER_PER_GAL,
            0.05)
        self.assertEquals(round(hops_weight, 2), 12506.15)

    def test_get_alpha_acid_units(self):
        out = self.hop_addition1.get_alpha_acid_units()
        self.assertEquals(round(out, 2), 7.98)

        ha = self.hop_addition1.change_units()
        out = ha.get_alpha_acid_units()
        self.assertEquals(round(out, 2), 7.98)
