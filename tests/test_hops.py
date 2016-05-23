import unittest

from brew.hops import Hop
from brew.utilities import plato_to_sg


class TestRecipe(unittest.TestCase):

    def setUp(self):

        # Define Hops
        centennial = Hop(name='centennial',
                         boil_time=60.0,
                         weight=0.57,
                         percent_alpha_acids=14.0,
                         percent_ibus=80.0,
                         percent_utilization=32.0,
                         percent_contribution=95.0)
        cascade = Hop(name='cascade',
                      boil_time=5.0,
                      weight=0.76,
                      percent_alpha_acids=7.0,
                      percent_ibus=20.0,
                      percent_utilization=2.5,
                      percent_contribution=5.0)
        self.hop_list = [centennial, cascade]
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.target_ibu = 40.0
        self.gallons_of_beer = 5.0

    def test_get_hops_weight(self):
        hops_weight = self.hop_list[0].get_hops_weight(self.target_ibu,
                                                       self.gallons_of_beer)
        self.assertEquals(round(hops_weight, 2), 0.57)
        hops_weight = self.hop_list[1].get_hops_weight(self.target_ibu,
                                                       self.gallons_of_beer)
        self.assertEquals(round(hops_weight, 2), 0.76)

    def test_get_ibu_real_beer(self):
        ibu = self.hop_list[0].get_ibu_real_beer(self.sg,
                                                 self.gallons_of_beer)
        self.assertEquals(round(ibu, 2), 36.98)
        ibu = self.hop_list[1].get_ibu_real_beer(self.sg,
                                                 self.gallons_of_beer)
        self.assertEquals(round(ibu, 2), 1.93)

    def test_get_ibu_glenn_tinseth(self):
        ibu = self.hop_list[0].get_ibu_glenn_tinseth(self.sg,
                                                     self.gallons_of_beer)
        self.assertEquals(round(ibu, 2), 25.93)
        ibu = self.hop_list[1].get_ibu_glenn_tinseth(self.sg,
                                                     self.gallons_of_beer)
        self.assertEquals(round(ibu, 2), 3.45)

    def test_get_percent_utilization(self):
        utilization = self.hop_list[0].get_percent_utilization(
                self.sg, self.hop_list[0].boil_time)
        self.assertEquals(round(utilization * 100, 2), 21.69)
        utilization = self.hop_list[1].get_percent_utilization(
                self.sg, self.hop_list[1].boil_time)
        self.assertEquals(round(utilization * 100, 2), 4.32)
