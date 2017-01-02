# -*- coding: utf-8 -*-
import sys
import textwrap
import unittest

from brew.constants import HOP_TYPE_WHOLE
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.hops import Hop
from brew.hops import HopAddition
from brew.utilities.sugar import plato_to_sg
from fixtures import cascade
from fixtures import cascade_add
from fixtures import centennial


class TestHops(unittest.TestCase):

    def setUp(self):

        # Define Hops
        self.hop = centennial

    def test_str(self):
        out = str(self.hop)
        self.assertEquals(out, u'Centennial, alpha 14.0%')

    def test_unicode(self):
        hop = Hop(u'Galaxy ®',
                  percent_alpha_acids=0.11)
        out = str(hop)
        if sys.version_info[0] >= 3:
            self.assertEquals(out, u'Galaxy ®, alpha 11.0%')
        else:
            self.assertEquals(out, u'Galaxy ®, alpha 11.0%'.encode('utf8'))

    def test_repr(self):
        out = repr(self.hop)
        self.assertEquals(out, u"Hop('centennial', percent_alpha_acids=0.14)")

    def test_eq(self):
        hop1 = Hop(u'cascade',
                   percent_alpha_acids=0.07)
        hop2 = Hop(u'cascade',
                   percent_alpha_acids=0.07)
        self.assertEquals(hop1, hop2)

    def test_ne_name(self):
        hop1 = Hop(u'cascade',
                   percent_alpha_acids=0.07)
        hop2 = Hop(u'centennial',
                   percent_alpha_acids=0.07)
        self.assertTrue(hop1 != hop2)

    def test_ne_percent_alpha_acids(self):
        hop1 = Hop(u'cascade',
                   percent_alpha_acids=0.07)
        hop2 = Hop(u'cascade',
                   percent_alpha_acids=0.14)
        self.assertTrue(hop1 != hop2)

    def test_ne_hop_add_class(self):
        self.assertTrue(cascade != cascade_add)

    def test_to_dict(self):
        out = self.hop.to_dict()
        expected = {u'name': u'centennial',
                    u'percent_alpha_acids': 0.14,
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.hop.to_json()
        expected = u'{"name": "centennial", "percent_alpha_acids": 0.14}'
        self.assertEquals(out, expected)

    def test_format(self):
        out = self.hop.format()
        msg = textwrap.dedent(u"""\
                centennial Hops
                -----------------------------------
                Alpha Acids:  14.0%""")
        self.assertEquals(out, msg)

    def test_hop_no_percent_alpha_acids(self):
        with self.assertRaises(Exception):
            Hop(u'centennial')


class TestHopAdditions(unittest.TestCase):

    def setUp(self):
        self.hop1 = centennial
        self.hop2 = cascade
        self.addition_kwargs = [
            {
                u'boil_time': 60.0,
                u'weight': 0.57,
                u'utilization_cls_kwargs': {u'units': IMPERIAL_UNITS},
            },
            {
                u'boil_time': 5.0,
                u'weight': 0.76,
                u'utilization_cls_kwargs': {u'units': IMPERIAL_UNITS},
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
            out, u'Centennial, alpha 14.0%, 0.57 oz, 60.0 min, pellet')

    def test_unicode(self):
        hop = Hop(u'Galaxy ®',
                  percent_alpha_acids=0.11)
        hop_add = HopAddition(hop,
                              boil_time=60.0,
                              weight=0.57)
        out = str(hop_add)
        if sys.version_info[0] >= 3:
            self.assertEquals(out, u'Galaxy ®, alpha 11.0%, 0.57 oz, 60.0 min, pellet')  # noqa
        else:
            self.assertEquals(out, u'Galaxy ®, alpha 11.0%, 0.57 oz, 60.0 min, pellet'.encode('utf8'))  # noqa

    def test_repr(self):
        out = repr(self.hop_addition1)
        try:
            st_type = unicode  # noqa
            self.assertEquals(
                    out, u"HopAddition(Hop('centennial', percent_alpha_acids=0.14), weight=0.57, boil_time=60.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, utilization_cls_kwargs={u'units': u'imperial'}, units='imperial')")  # noqa
        except NameError:
            self.assertEquals(
                    out, u"HopAddition(Hop('centennial', percent_alpha_acids=0.14), weight=0.57, boil_time=60.0, hop_type='pellet', utilization_cls=HopsUtilizationGlennTinseth, utilization_cls_kwargs={'units': 'imperial'}, units='imperial')")  # noqa

    def test_eq(self):
        hop_add1 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        hop_add2 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        self.assertTrue(hop_add1 == hop_add2)

    def test_ne_boil_time(self):
        hop_add1 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        hop_add2 = HopAddition(cascade, boil_time=15.0, weight=0.76)
        self.assertTrue(hop_add1 != hop_add2)

    def test_ne_weight(self):
        hop_add1 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        hop_add2 = HopAddition(cascade, boil_time=5.0, weight=1.76)
        self.assertTrue(hop_add1 != hop_add2)

    def test_ne_hop_type(self):
        hop_add1 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        hop_add2 = HopAddition(cascade, boil_time=5.0, weight=0.76,
                               hop_type=HOP_TYPE_WHOLE)
        self.assertTrue(hop_add1 != hop_add2)

    def test_ne_units(self):
        hop_add1 = HopAddition(cascade, boil_time=5.0, weight=0.76)
        hop_add2 = HopAddition(cascade, boil_time=5.0, weight=0.76,
                               units=SI_UNITS)
        self.assertTrue(hop_add1 != hop_add2)

    def test_ne_hop_class(self):
        self.assertTrue(cascade_add != cascade)

    def test_to_dict(self):
        out = self.hop_addition1.to_dict()
        expected = {u'name': u'centennial',
                    u'data': {u'percent_alpha_acids': 0.14},
                    u'weight': 0.57,
                    u'boil_time': 60.0,
                    u'hop_type': u'pellet',
                    u'utilization_cls': u'Glenn Tinseth',
                    u'utilization_cls_kwargs': {u'units': u'imperial'},
                    u'units': u'imperial',
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.hop_addition1.to_json()
        expected = u'{"boil_time": 60.0, "data": {"percent_alpha_acids": 0.14}, "hop_type": "pellet", "name": "centennial", "units": "imperial", "utilization_cls": "Glenn Tinseth", "utilization_cls_kwargs": {"units": "imperial"}, "weight": 0.57}'  # noqa
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.hop_addition1.to_dict()
        HopAddition.validate(data)

    def test_format(self):
        out = self.hop_addition1.format()
        msg = textwrap.dedent(u"""\
                centennial Addition
                -----------------------------------
                Hop Type:     pellet
                AA %:         14.0%
                Weight:       0.57 oz
                Boil Time:    60.0 min""")
        self.assertEquals(out, msg)

    def test_get_alpha_acid_units(self):
        out = self.hop_addition1.get_alpha_acid_units()
        self.assertEquals(round(out, 2), 7.98)

        ha = self.hop_addition1.change_units()
        out = ha.get_alpha_acid_units()
        self.assertEquals(round(out, 2), 7.98)
