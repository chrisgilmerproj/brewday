#! /usr/bin/env python
# -*- coding: utf-8 -*-

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.yeasts import Yeast

"""
Build a recipe from known ingredients.
"""


def main():
    # Define Grains
    pale = Grain(u'Pale Malt (2 Row) US',
                 color=1.8,
                 ppg=37)
    pale_add = GrainAddition(pale,
                             weight=13.96)
    crystal = Grain(u'Caramel/Crystal Malt - 20L',
                    color=20.0,
                    ppg=35)
    crystal_add = GrainAddition(crystal,
                                weight=0.78)
    grain_additions = [pale_add, crystal_add]

    # Define Hops
    centennial = Hop(u'Centennial',
                     percent_alpha_acids=0.14)
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0)
    cascade = Hop(u'Cascade (US)',
                  percent_alpha_acids=0.07)
    cascade_add = HopAddition(cascade,
                              weight=0.76,
                              boil_time=5.0)
    hop_additions = [centennial_add, cascade_add]

    # Define Yeast
    yeast = Yeast(u'Wyeast 1056')

    # Define Recipe
    beer = Recipe(u'pale ale',
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  yeast=yeast,
                  percent_brew_house_yield=0.70,  # %
                  start_volume=7.0,  # G
                  final_volume=5.0,  # G
                  )
    print(beer.format())


if __name__ == "__main__":
    main()
