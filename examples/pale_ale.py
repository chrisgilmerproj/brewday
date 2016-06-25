#! /usr/bin/env python

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe

if __name__ == "__main__":

    # Define Grains
    pale = Grain('pale 2-row',
                 short_name='2-row',
                 color=1.8,
                 ppg=37)
    pale_add = GrainAddition(pale,
                             weight=13.96)
    crystal = Grain('crystal C20',
                    short_name='C20',
                    color=20.0,
                    ppg=35)
    # OG 32.74
    crystal_add = GrainAddition(crystal,
                                weight=0.78)
    grain_list = [pale, crystal]
    grain_additions = [pale_add, crystal_add]

    # Define Hops
    centennial = Hop(name='centennial',
                     percent_alpha_acids=0.14)
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0,
                                 percent_contribution=0.05)
    cascade = Hop(name='cascade',
                  percent_alpha_acids=0.07)
    cascade_add = HopAddition(cascade,
                              weight=0.76,
                              boil_time=5.0,
                              percent_contribution=0.05)
    hop_list = [centennial, cascade]
    hop_additions = [centennial_add, cascade_add]

    # Define Beer
    beer = Recipe(name='pale ale',
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  percent_brew_house_yield=0.70,  # %
                  start_volume=7.0,  # G
                  final_volume=5.0,  # G
                  target_sg=1.057,  # SG
                  target_ibu=40.0)

    beer.format()
    # Efficiency 70%
    # Boil: 7.0 Gal
    # Fermenter: 5.5 Gal
    # Final: 5.0 Gal
    # BG 1.054 (boil gravity)
    # OG 1.069
    # FG 1.017
    # ABV 6.81 (Standard)
    # IBU 30.03 (Tinseth)
    # SRM 5.89 (Morey)

    # Pale 2-row 13.96 lbs
    #     37 PPG, 1.8L, OG 32.87
    # Crystal 20 0.78 lbs
    #     35 PPG, 20L, 1.74 OG

    # Centennial: 0.57 oz, 14AA, 60 min
    #     33.85 IBU, 0.311 Util, 8.0 AAUs
    # Cascade:    0.76 oz,  7AA,  5 min
    #     4.50 IBU, 0.062 Util, 5.3 AAUs
