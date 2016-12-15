#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Oak Barrel Winecraft

Kolsch Ale

Used by permission of Oak Barrel Winecraft. All rights reserved.

You can purchase this kit at their store:

- http://oakbarrel.com/

Original Stats:

OG:      1.045
FG:      1.008 - 1.012
ADF:     72 % - 78 %
IBU:
Color:
Alcohol: 4.3% ABV
Boil:    60 min
Pre-Boil Volume:  2.5 G
Pre-Boil Gravity: 
"""  # noqa

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        u'name': u"Kölsch Ale (Extract)",
        u'start_volume': 2.5,
        u'final_volume': 5.0,
        u'grains': [
            {u'name': u'Pilsner Liquid Extract',
             u'weight': 3.25,
             u'grain_type': u'lme'},
            {u'name': u'Munich Liquid Extract',
             u'data': {
                 u'color': 10.0,
                 u'ppg': 36,
             },
             u'weight': 3.25,
             u'grain_type': u'lme'},
            {u'name': u'White Wheat Malt',
             u'weight': 0.25,
             u'grain_type': u'specialty'},
            {u'name': u'Caramel Crystal Malt 10l',
             u'weight': 0.25,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'Vanguard',
             u'weight': 1.0,
             u'boil_time': 60.0},
            {u'name': u'hersbrucker',
             u'weight': 1.0,
             u'boil_time': 0.0},
        ],
        u'yeast': {
            u'name': u'White Labs Wlp029',
        },
        u'data': {
            u'percent_brew_house_yield': 0.70,
            u'units': u'imperial',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    loader = JSONDataLoader(data_dir)
    beer = parse_recipe(recipe, loader)
    print(beer.format())


if __name__ == "__main__":
    main()
