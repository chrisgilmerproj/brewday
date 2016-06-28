import textwrap
import unittest

from brew.constants import LITER_PER_GAL
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.hops import HopAddition
from brew.hops import HopsUtilization
from brew.hops import HopsUtilizationGlennTinseth
from brew.hops import HopsUtilizationJackieRager
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

    def test_format(self):
        out = self.hop.format()
        msg = textwrap.dedent("""\
                Centennial Hops
                ---------------
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

    def test_format(self):
        out = self.hop_addition1.format()
        msg = textwrap.dedent("""\
                Centennial, alpha 0.14%
                ------------------------
                Weight:       0.57 oz
                Boil Time:    60.00 min""")
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


class TestHopsUtilization(unittest.TestCase):

    def setUp(self):
        self.utilization_cls = HopsUtilization
        self.hop = centennial
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
            }
        ]

        # Additions
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.final_volume = 5.0
        self.boil_time = 60.0
        self.hop_addition = HopAddition(self.hop,
                                        boil_time=self.boil_time,
                                        weight=0.57,
                                        utilization_cls=self.utilization_cls)

    def test_get_ibus_raises(self):
        with self.assertRaises(NotImplementedError):
            self.hop_addition.get_ibus(self.sg, self.final_volume)

    def test_get_percent_utilization_raises(self):
        with self.assertRaises(NotImplementedError):
            self.hop_addition.utilization_cls.get_percent_utilization(
                    self.sg, self.final_volume)

    def test_change_units(self):
        self.assertEquals(self.hop_addition.utilization_cls.units,
                          IMPERIAL_UNITS)
        util = self.hop_addition.utilization_cls.change_units()
        self.assertEquals(util.units, SI_UNITS)
        util = util.change_units()
        self.assertEquals(util.units, IMPERIAL_UNITS)


class TestHopsUtilizationJackieRager(unittest.TestCase):

    def setUp(self):
        self.utilization_cls = HopsUtilizationJackieRager
        self.hop = centennial
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
            }
        ]

        # Additions
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.final_volume = 5.0
        self.boil_time = 60.0
        self.hop_addition = HopAddition(self.hop,
                                        boil_time=self.boil_time,
                                        weight=0.57,
                                        utilization_cls=self.utilization_cls)

    def test_str(self):
        self.assertEquals(str(self.hop_addition.utilization_cls),
                          "Jackie Rager")

    def test_get_c_gravity(self):
        out = self.hop_addition.utilization_cls.get_c_gravity(self.sg)
        self.assertEquals(round(out, 3), 1.034)
        out = self.hop_addition.utilization_cls.get_c_gravity(1.050)
        self.assertEquals(round(out, 3), 1.000)
        out = self.hop_addition.utilization_cls.get_c_gravity(1.010)
        self.assertEquals(round(out, 3), 1.000)

    def test_get_ibus(self):
        ibu = self.hop_addition.get_ibus(self.sg,
                                         self.final_volume)
        self.assertEquals(round(ibu, 2), 39.18)

    def test_get_percent_utilization(self):
        utilization = self.hop_addition.utilization_cls.get_percent_utilization(  # nopep8
                self.sg, self.boil_time)
        self.assertEquals(round(utilization * 100, 2), 29.80)

    def test_get_utilization_table(self):
        gravity_list = list(range(1030, 1140, 10))
        boil_time_list = list(range(0, 60, 3)) + list(range(60, 130, 10))
        table = self.utilization_cls.get_utilization_table(
                gravity_list,
                boil_time_list)
        self.assertEquals(table[0][0], 0.051)
        self.assertEquals(table[13][5], 0.205)
        self.assertEquals(table[26][10], 0.228)

    def test_print_utilization_table(self):
        pass


class TestHopsUtilizationGlennTinseth(unittest.TestCase):

    def setUp(self):
        self.utilization_cls = HopsUtilizationGlennTinseth
        self.hop = centennial
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
            }
        ]

        # Additions
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.final_volume = 5.0
        self.boil_time = 60.0
        self.hop_addition = HopAddition(self.hop,
                                        boil_time=self.boil_time,
                                        weight=0.57,
                                        utilization_cls=self.utilization_cls)

    def test_str(self):
        self.assertEquals(str(self.hop_addition.utilization_cls),
                          "Glenn Tinseth")

    def test_get_ibus(self):
        ibu = self.hop_addition.get_ibus(self.sg,
                                         self.final_volume)
        self.assertEquals(round(ibu, 2), 28.52)

    def test_get_bigness_factor(self):
        bf = self.hop_addition.utilization_cls.get_bigness_factor(self.sg)
        self.assertEquals(round(bf, 2), 0.99)

    def test_get_boil_time_factor(self):
        bf = self.hop_addition.utilization_cls.get_boil_time_factor(
                self.boil_time)
        self.assertEquals(round(bf, 2), 0.22)

    def test_get_percent_utilization(self):
        utilization = self.hop_addition.utilization_cls.get_percent_utilization(  # nopep8
                self.sg, self.boil_time)
        self.assertEquals(round(utilization * 100, 2), 21.69)
