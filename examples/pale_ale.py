#! /usr/bin/env python

from brew.grains import Grain
from brew.hops import Hop
from brew.recipes import Recipe


if __name__ == "__main__":

    # Define Grains
    pale = Grain(name='pale 2-row',
                 short_name='2-row',
                 hot_water_extract=0.76,
                 color=2.0,
                 percent_extract=95.0)
    crystal = Grain(name='crystal C20',
                    short_name='C20',
                    hot_water_extract=0.70,
                    color=20.0,
                    percent_extract=5.0)
    grain_list = [pale, crystal]

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
    hop_list = [centennial, cascade]

    # Define Beer
    beer = Recipe(name='pale ale',
                  grain_list=grain_list,
                  hop_list=hop_list,
                  percent_brew_house_yield=70.0,  # %
                  gallons_of_beer=5.0,  # G
                  target_degrees_plato=14.0,  # P
                  mash_temp=152.0,  # F
                  malt_temp=60.0,  # F
                  liquor_to_grist_ratio=3.0 / 1.0,
                  percent_color_loss=30.0,  # %
                  target_ibu=40.0)

    beer.format()
