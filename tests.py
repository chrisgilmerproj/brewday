import unittest

from brew import Beer, Grain, Hop


class TestBeer(unittest.TestCase):

    def setUp(self):
        # Define Grains
        pale = Grain(name='pale 2-row',
                     short_name='2-row',
                     hot_water_extract=0.76,
                     color=2,
                     percent_extract=95)
        crystal = Grain(name='crystal C20',
                        short_name='C20',
                        hot_water_extract=0.70,
                        color=20,
                        percent_extract=5.0)
        self.grain_list = [pale, crystal]

        # Define Hops
        centennial = Hop(name='centennial',
                         boil_time=60.0,
                         percent_alpha_acids=14.0,
                         percent_ibus=80.0,
                         percent_utilization=32.0,
                         percent_contribution=95.0)
        cascade = Hop(name='cascade',
                      boil_time=5.0,
                      percent_alpha_acids=7.0,
                      percent_ibus=20.0,
                      percent_utilization=2.5,
                      percent_contribution=5.0)
        self.hop_list = [centennial, cascade]

        # Define Beers
        self.beer = Beer(name='pale ale',
                         grain_list=self.grain_list,
                         hop_list=self.hop_list,
                         percent_brew_house_yield=70.0,  # %
                         gallons_of_beer=5.0,  # G
                         target_degrees_plato=14.0,  # P
                         mash_temp=152.0,  # F
                         malt_temp=60.0,  # F
                         liquor_to_grist_ratio=3.0 / 1.0,
                         percent_color_loss=30.0,  # %
                         target_ibu=40.0)

    def test_get_specific_gravity(self):
        sg = self.beer.get_specific_gravity()
        self.assertEquals(round(sg, 3), 1.057)

    def test_get_degrees_plato(self):
        deg_plato = self.beer.get_degrees_plato()
        self.assertEquals(round(deg_plato, 3), 14.003)

    def test_get_extract_weight(self):
        pounds_extract = self.beer.get_extract_weight()
        self.assertEquals(round(pounds_extract, 2), 6.16)

    def test_get_working_yield(self):
        wy = self.beer.get_working_yield(self.grain_list[0])
        self.assertEquals(round(wy, 2), 53.20)
        wy = self.beer.get_working_yield(self.grain_list[1])
        self.assertEquals(round(wy, 2), 49.00)

    def test_get_pounds_malt(self):
        pounds_malt = self.beer.get_pounds_malt(self.grain_list[0])
        self.assertEquals(round(pounds_malt, 2), 10.99)
        pounds_malt = self.beer.get_pounds_malt(self.grain_list[1])
        self.assertEquals(round(pounds_malt, 2), 0.63)

    def test_get_total_grain_weight(self):
        total_grain_weight = self.beer.get_total_grain_weight()
        self.assertEquals(round(total_grain_weight, 2), 11.62)

    def test_get_strike_temp(self):
        strike_temp = self.beer.get_strike_temp()
        self.assertEquals(round(strike_temp, 2), 164.27)

    def test_get_mash_water_volume(self):
        mash_water_vol = self.beer.get_mash_water_volume()
        self.assertEquals(round(mash_water_vol, 2), 4.19)

    def test_get_hops_weight(self):
        hops_weight = self.beer.get_hops_weight(self.hop_list[0])
        self.assertEquals(round(hops_weight, 2), 0.57)
        hops_weight = self.beer.get_hops_weight(self.hop_list[1])
        self.assertEquals(round(hops_weight, 2), 0.76)

    def test_get_wort_color(self):
        wort_color = self.beer.get_wort_color(self.grain_list[0])
        self.assertEquals(round(wort_color, 2), 3.32)
        wort_color = self.beer.get_wort_color(self.grain_list[1])
        self.assertEquals(round(wort_color, 2), 1.75)

    def test_get_total_wort_color(self):
        total_wort_color = self.beer.get_total_wort_color()
        self.assertEquals(round(total_wort_color, 2), 5.07)

    def test_get_beer_color(self):
        beer_color = self.beer.get_beer_color()
        self.assertEquals(round(beer_color, 2), 3.55)

    def test_get_alcohol_by_volume_standard(self):
        abv = self.beer.get_alcohol_by_volume_standard(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.78)

    def test_get_alcohol_by_volume_alternative(self):
        abv = self.beer.get_alcohol_by_volume_alternative(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.95)

    def test_get_hydrometer_adjustment(self):
        sg = self.beer.get_hydrometer_adjustment(float(70))
        self.assertEquals(round(sg, 3), 1.058)

    def test_get_ibu_real_beer(self):
        ibu = self.beer.get_ibu_real_beer(self.hop_list[0])
        self.assertEquals(round(ibu, 2), 35.94)
        ibu = self.beer.get_ibu_real_beer(self.hop_list[1])
        self.assertEquals(round(ibu, 2), 1.89)

    def test_get_percent_utilization(self):
        utilization = self.beer.get_percent_utilization(self.hop_list[0])
        self.assertEquals(round(utilization, 2), 0.22)
        utilization = self.beer.get_percent_utilization(self.hop_list[1])
        self.assertEquals(round(utilization, 2), 0.04)


if __name__ == '__main__':
    unittest.main(verbosity=2)
