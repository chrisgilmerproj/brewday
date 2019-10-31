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
    pale = Grain(u"Pale Malt (2 Row) US", color=1.8, ppg=37)
    pale_add = GrainAddition(pale, weight=10.8)
    crystal60 = Grain(u"Caramel/Crystal Malt - 60L", color=60.0, ppg=34)
    crystal60_add = GrainAddition(crystal60, weight=1.2)
    crystal20 = Grain(u"Caramel/Crystal Malt - 20L", color=20.0, ppg=35)
    crystal20_add = GrainAddition(crystal20, weight=0.6)
    carapils = Grain(u"Carapils/Dextrine Malt", color=1.8, ppg=33)
    carapils_add = GrainAddition(carapils, weight=0.6)
    chocolate = Grain(u"Chocolate Malt", color=350.0, ppg=29)
    chocolate_add = GrainAddition(chocolate, weight=0.6)
    black_patent = Grain(u"Black Patent Malt", color=525.0, ppg=27)
    black_patent_add = GrainAddition(black_patent, weight=0.15)
    flaked_oats = Grain(u"Flaked Oats", color=2.2.0, ppg=33)
    flaked_oats_add = GrainAddition(flaked_oats, weight=0.6)
    
    grain_additions = [pale_add, crystal60_add, crystal20_add, carapils_add, 
                      chocolate_add, black_patent_add, flaked_oats_add]

    # Define Hops
    ekg = Hop(u"East Kent Goldings", percent_alpha_acids=5.0)
    ekg_add = HopAddition(ekg, weight=1.0, boil_time=60.0)
    liberty = Hop(u"Liberty", percent_alpha_acids=4.0)
    liberty1_add = HopAddition(liberty, weight=1.0, boil_time=30.0)
    willamette = Hop(u"Willamette", percent_alpha_acids=4.5)
    willamette_add = HopAddition(willamette, weight=1.0, boil_time=15.0)
    liberty2_add = HopAddition(liberty, weight=1.0, boil_time=0.0)
    
    hop_additions = [ekg_add, liberty1_add, willamette_add, liberty2_add]

    # Define Yeast
    yeast = Yeast(u"Danstar Windsor Ale Yeast")

    # Define Recipe
    beer = Recipe(
        u"brown ale",
        grain_additions=grain_additions,
        hop_additions=hop_additions,
        yeast=yeast,
        brew_house_yield=0.65,  # %
        start_volume=7.5,  # G
        final_volume=5.5,  # G
    )
    print(beer.format())


if __name__ == "__main__":
    main()
