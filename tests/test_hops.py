import textwrap
import unittest

from brew.hops import HopAddition
from brew.hops import HopsUtilization
from brew.hops import HopsUtilizationGlennTinseth
from brew.hops import HopsUtilizationJackieRager
from brew.utilities import plato_to_sg

from fixtures import cascade
from fixtures import centennial


class TestHops(unittest.TestCase):

    def setUp(self):

        # Define Hops
        self.hop = centennial

    def test_str(self):
        out = str(self.hop)
        self.assertEquals(out, 'Centennial, alpha 14.0%')

    def test_repr(self):
        out = repr(self.hop)
        self.assertEquals(out, "Hop('centennial', percent_alpha_acids=14.0)")

    def test_format(self):
        out = self.hop.format()
        msg = textwrap.dedent("""Centennial Hops
                                 ---------------
                                 Alpha Acids:  14.0 %""")
        self.assertEquals(out, msg)


class TestHopAdditions(unittest.TestCase):

    def setUp(self):
        self.hop1 = centennial
        self.hop2 = cascade
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
                'percent_contribution': 95.0,
            },
            {
                'boil_time': 5.0,
                'weight': 0.76,
                'percent_contribution': 5.0,
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

    def test_str(self):
        out = str(self.hop_addition1)
        self.assertEquals(
            out, 'Centennial, alpha 14.0%, weight 0.57 oz, boil time 60.0 min')

    def test_repr(self):
        out = repr(self.hop_addition1)
        self.assertEquals(
            out, "HopAddition(Hop('centennial', percent_alpha_acids=14.0))")

    def test_format(self):
        out = self.hop_addition1.format()
        msg = textwrap.dedent("""Centennial, alpha 14.0%
                                 ------------------------
                                 Weight:       0.57 oz
                                 Contribution: 95.00 %
                                 Boil Time:    60.00 min""")
        self.assertEquals(out, msg)

    def test_get_hops_weight(self):
        hops_weight = self.hop_addition1.get_hops_weight(
                        self.sg,
                        self.target_ibu,
                        self.final_volume)
        self.assertEquals(round(hops_weight, 2), 0.61)

        hops_weight = self.hop_addition2.get_hops_weight(
                        self.sg,
                        self.target_ibu,
                        self.final_volume)
        self.assertEquals(round(hops_weight, 2), 0.34)


class TestHopsUtilization(unittest.TestCase):

    def setUp(self):
        self.utilization_cls = HopsUtilization
        self.hop = centennial
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
                'percent_contribution': 95.0,
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
                                        percent_contribution=95.0,
                                        utilization_cls=self.utilization_cls)

    def test_get_ibus_raises(self):
        with self.assertRaises(NotImplementedError):
            self.hop_addition.get_ibus(self.sg, self.final_volume)

    def test_get_percent_utilization_raises(self):
        with self.assertRaises(NotImplementedError):
            self.hop_addition.utilization_cls.get_percent_utilization(
                    self.sg, self.final_volume)


class TestHopsUtilizationJackieRager(unittest.TestCase):

    def setUp(self):
        self.utilization_cls = HopsUtilizationJackieRager
        self.hop = centennial
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
                'percent_contribution': 95.0,
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
                                        percent_contribution=95.0,
                                        utilization_cls=self.utilization_cls)

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
        self.assertEquals(round(ibu, 2), 35.62)

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
                'percent_contribution': 95.0,
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
                                        percent_contribution=95.0,
                                        utilization_cls=self.utilization_cls)

    def test_get_ibus(self):
        ibu = self.hop_addition.get_ibus(self.sg,
                                         self.final_volume)
        self.assertEquals(round(ibu, 2), 25.93)

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
