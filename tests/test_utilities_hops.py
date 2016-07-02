import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.hops import HopAddition
from brew.utilities.hops import HopsUtilization
from brew.utilities.hops import HopsUtilizationGlennTinseth
from brew.utilities.hops import HopsUtilizationJackieRager
from brew.utilities.sugar import plato_to_sg
from fixtures import centennial


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
