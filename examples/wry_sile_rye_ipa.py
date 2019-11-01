#! /usr/bin/env python
# -*- coding: utf-8 -*-

from brew.grains import Grain, GrainAddition
from brew.hops import Hop, HopAddition
from brew.recipes import Recipe
from brew.yeasts import Yeast

"""
Build a recipe from known ingredients.
"""


def main():
    # Define Grains
    pale = Grain(u"Pale Malt (2 Row) US", color=1.8, ppg=37)
    rye = Grain(u"Rye Malt", color=3.5, ppg=38)
    crystal = Grain(u"Caramel/Crystal - 60L", color=60, ppg=34)
    carapils = Grain(u"Carapils/Dextrine Malt", color=1.8, ppg=33)
    flaked_wheat = Grain(u"Flaked Wheat", color=2, ppg=34)

    pale_add = GrainAddition(pale, weight=13.96)
    rye_add = GrainAddition(rye, weight=3.0)
    crystal_add = GrainAddition(crystal, weight=1.25)
    carapils_add = GrainAddition(carapils, weight=0.5)
    flaked_wheat_add = GrainAddition(flaked_wheat, weight=0.5)

    grain_additions = [pale_add, rye_add, crystal_add, carapils_add, flaked_wheat_add]

    # Define Hops
    mt_hood = Hop(u"Mount Hood", percent_alpha_acids=0.048)
    columbus = Hop(u"Columbus", percent_alpha_acids=0.15)


    mt_hood_add_01 = HopAddition(mt_hood, weight=1.0, boil_time=60.0)
    columbus_add_01 = HopAddition(columbus, weight=1.0, boil_time=60.0)
    mt_hood_add_02 = HopAddition(mt_hood, weight=0.5, boil_time=30.0)
    mt_hood_add_03 = HopAddition(mt_hood, weight=1.5, boil_time=1.0)
    columbus_add_02 = HopAddition(columbus, weight=1.0, boil_time=0.0)

    hop_additions = [mt_hood_add_01, columbus_add_01, mt_hood_add_02, mt_hood_add_03, columbus_add_02]

    # Define Yeast
    yeast = Yeast(u"Wyeast 1450", percent_attenuation=0.75)

    # Define Recipe
    beer = Recipe(
        u"pale ale",
        grain_additions=grain_additions,
        hop_additions=hop_additions,
        yeast=yeast,
        brew_house_yield=0.70,  # %
        start_volume=7.5,  # G
        final_volume=5.5,  # G
    )
    print(beer.format())


if __name__ == "__main__":
    main()
