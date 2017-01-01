#! /usr/bin/env python
# -*- coding: utf-8 -*-

from brew.grains import Grain
from brew.hops import Hop
from brew.recipes import RecipeBuilder

"""
Design a beer from base ingredients.
"""


def main():
    # Define Grains
    pale = Grain(u'pale 2-row',
                 color=2.0,
                 ppg=37.0)
    crystal = Grain(u'crystal C20',
                    color=20.0,
                    ppg=35.0)
    grain_list = [pale, crystal]

    # Define Hops
    centennial = Hop(name=u'centennial',
                     percent_alpha_acids=0.14)
    cascade = Hop(name=u'cascade',
                  percent_alpha_acids=0.07)
    hop_list = [centennial, cascade]

    # Define Builder
    builder = RecipeBuilder(name=u'Pale Ale',
                            grain_list=grain_list,
                            hop_list=hop_list,
                            target_ibu=33.0,
                            target_og=1.05,
                            percent_brew_house_yield=0.70,
                            start_volume=7.0,
                            final_volume=5.0,
                            )

    # Get Grain Bill
    percent_list = [0.90, 0.10]
    grain_additions = builder.get_grain_additions(percent_list)
    for grain_add in grain_additions:
        print(grain_add.format())
        print(u'')

    # Get Hop Bill
    percent_list = [0.8827, 0.1173]
    boil_time_list = [60.0, 5.0]
    hop_additions = builder.get_hop_additions(percent_list, boil_time_list)
    for hop_add in hop_additions:
        print(hop_add.format())
        print(u'')


if __name__ == "__main__":
    main()
