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

    def test_format_utilization_table(self):
        out = self.utilization_cls.format_utilization_table()
        expected = ("""\
            Percent Alpha Acid Utilization - Boil Time vs Wort Original Gravity
            ===================================================================
       1.030   1.040   1.050   1.060   1.070   1.080   1.090   1.100   1.110   1.120   1.130
--------------------------------------------------------------------------------------------
   0   0.051   0.051   0.051   0.049   0.047   0.045   0.043   0.041   0.039   0.038   0.037
   3   0.054   0.054   0.054   0.052   0.049   0.047   0.045   0.044   0.042   0.040   0.039
   6   0.059   0.059   0.059   0.056   0.053   0.051   0.049   0.047   0.045   0.044   0.042
   9   0.065   0.065   0.065   0.062   0.059   0.056   0.054   0.052   0.050   0.048   0.046
  12   0.072   0.072   0.072   0.069   0.066   0.063   0.060   0.058   0.056   0.054   0.052
  15   0.082   0.082   0.082   0.078   0.075   0.072   0.069   0.066   0.063   0.061   0.059
  18   0.095   0.095   0.095   0.090   0.086   0.082   0.079   0.076   0.073   0.070   0.068
  21   0.110   0.110   0.110   0.105   0.100   0.096   0.092   0.088   0.085   0.082   0.079
  24   0.128   0.128   0.128   0.122   0.117   0.112   0.107   0.103   0.099   0.095   0.092
  27   0.149   0.149   0.149   0.142   0.135   0.129   0.124   0.119   0.115   0.110   0.106
  30   0.171   0.171   0.171   0.163   0.156   0.149   0.143   0.137   0.132   0.127   0.122
  33   0.194   0.194   0.194   0.185   0.176   0.169   0.162   0.155   0.149   0.144   0.138
  36   0.216   0.216   0.216   0.206   0.196   0.188   0.180   0.173   0.166   0.160   0.154
  39   0.236   0.236   0.236   0.225   0.215   0.205   0.197   0.189   0.182   0.175   0.169
  42   0.254   0.254   0.254   0.242   0.231   0.221   0.212   0.203   0.195   0.188   0.181
  45   0.269   0.269   0.269   0.256   0.245   0.234   0.224   0.215   0.207   0.199   0.192
  48   0.281   0.281   0.281   0.268   0.256   0.245   0.234   0.225   0.216   0.208   0.201
  51   0.291   0.291   0.291   0.277   0.264   0.253   0.242   0.233   0.224   0.215   0.208
  54   0.298   0.298   0.298   0.284   0.271   0.259   0.249   0.239   0.229   0.221   0.213
  57   0.304   0.304   0.304   0.290   0.276   0.264   0.253   0.243   0.234   0.225   0.217
  60   0.308   0.308   0.308   0.294   0.280   0.268   0.257   0.247   0.237   0.228   0.220
  70   0.316   0.316   0.316   0.301   0.287   0.275   0.263   0.253   0.243   0.234   0.226
  80   0.318   0.318   0.318   0.303   0.289   0.277   0.265   0.255   0.245   0.236   0.227
  90   0.319   0.319   0.319   0.304   0.290   0.278   0.266   0.255   0.246   0.236   0.228
 100   0.320   0.320   0.320   0.304   0.290   0.278   0.266   0.256   0.246   0.237   0.228
 110   0.320   0.320   0.320   0.304   0.291   0.278   0.266   0.256   0.246   0.237   0.228
 120   0.320   0.320   0.320   0.304   0.291   0.278   0.266   0.256   0.246   0.237   0.228""")  # nopep8
        self.assertEquals(out, expected)


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
