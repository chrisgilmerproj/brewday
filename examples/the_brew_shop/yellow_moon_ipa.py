#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Brew Shop

Yellow Moon IPA

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
        u'name': u"Yellow Moon IPA (Extract)",
        u'start_volume': 4.0,
        u'final_volume': 5.0,
        u'grains': [
            {u'name': u'Pale Liquid Extract',
             u'weight': 7.0,
             u'grain_type': u'lme'},
            {u'name': u'Caramel Crystal Malt 20l',
             u'weight': 1.0,
             u'grain_type': u'specialty'},
            {u'name': u'Munich Malt',
             u'weight': 0.5,
             u'grain_type': u'specialty'},
            {u'name': u'Cara Pils Dextrine',
             u'weight': 0.5,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'Centennial',
             u'weight': 1.0,
             u'boil_time': 60.0},
            {u'name': u'Centennial',
             u'weight': 1.0,
             u'boil_time': 30.0},
            {u'name': u'Cascade US',
             u'weight': 1.0,
             u'boil_time': 10.0},
            {u'name': u'Cascade US',
             u'weight': 1.0,
             u'boil_time': 0.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 1056',
        },
        u'data': {
            u'brew_house_yield': 0.425,
            u'units': u'imperial',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    loader = JSONDataLoader(data_dir)
    beer = parse_recipe(recipe, loader)
    print(beer.format())


if __name__ == "__main__":
    main()
