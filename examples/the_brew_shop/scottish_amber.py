#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Brew Shop

Scottish Amber

Used by permission of The Brew Shop. All rights reserved.

You can purchase this kit at their store:

- http://thebrewshopbend.com/

Original Stats:

OG:
FG:
ADF:
IBU:
Color:
Alcohol:
Boil:    60 min
Pre-Boil Volume:
Pre-Boil Gravity: 
"""  # noqa

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe
from brew.utilities.efficiency import calculate_brew_house_yield  # noqa


def main():

    recipe = {
        u'name': u"Scottish Amber (Extract)",
        u'start_volume': 5.0,
        u'final_volume': 5.0,
        u'grains': [
            {u'name': u'Pale Liquid Extract',
             u'weight': 7.0,
             u'grain_type': u'lme'},
            {u'name': u'Caramel Crystal Malt 80l',
             u'weight': 1.0,
             u'grain_type': u'specialty'},
            {u'name': u'Smoked Malt',
             # Rausch means "Smoked"
             u'weight': 1.0,
             u'data': {
                 u'color': 6.0},
             u'grain_type': u'specialty'},
            {u'name': u'Victory Malt',
             u'weight': 1.0,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'Perle',
             u'weight': 1.0,
             u'boil_time': 60.0},
            {u'name': u'Perle',
             u'weight': 1.0,
             u'boil_time': 30.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 1728',
        },
        u'data': {
            u'brew_house_yield': 0.458,
            u'units': u'imperial',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    loader = JSONDataLoader(data_dir)
    beer = parse_recipe(recipe, loader)
    print(beer.format())


if __name__ == "__main__":
    main()
