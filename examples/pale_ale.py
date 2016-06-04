#! /usr/bin/env python

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe


if __name__ == "__main__":

    # Define Grains
    pale = Grain(name='pale 2-row',
                 short_name='2-row',
                 color=2.0,
                 hot_water_extract=0.76)
    crystal = Grain(name='crystal C20',
                    short_name='C20',
                    color=20.0,
                    hot_water_extract=0.70)
    grain_list = [pale, crystal]

    pale_add = GrainAddition(pale,
                             percent_extract=95)

    crystal_add = GrainAddition(crystal,
                                percent_extract=5.0)
    grain_additions = [pale_add, crystal_add]

    # Define Hops
    centennial = Hop(name='centennial',
                     percent_alpha_acids=14.0)
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0,
                                 percent_contribution=95.0)
    cascade = Hop(name='cascade',
                  percent_alpha_acids=7.0)
    cascade_add = HopAddition(cascade,
                              weight=0.76,
                              boil_time=5.0,
                              percent_contribution=5.0)
    hop_additions = [centennial_add, cascade_add]

    # Define Beer
    beer = Recipe(name='pale ale',
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  percent_brew_house_yield=70.0,  # %
                  start_volume=7.0,  # G
                  final_volume=5.0,  # G
                  target_sg=1.057,  # SG
                  target_ibu=40.0)

    beer.format()
