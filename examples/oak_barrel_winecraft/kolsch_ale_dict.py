#! /usr/bin/env python

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
"""  # nopep8

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        'name': "Kolsch Ale (Extract)",
        'start_volume': 2.5,
        'final_volume': 5.0,
        'grains': [
            {'name': 'Pilsner Liquid Extract',
             'weight': 3.25,
             'grain_type': 'lme'},
            {'name': 'Munich Liquid Extract',
             'data': {
                 'color': 10.0,
                 'ppg': 36,
             },
             'weight': 3.25,
             'grain_type': 'lme'},
            {'name': 'White Wheat Malt',
             'weight': 0.25,
             'grain_type': 'specialty'},
            {'name': 'Caramel Crystal Malt 10l',
             'weight': 0.25,
             'grain_type': 'specialty'},
        ],
        'hops': [
            {'name': 'Vanguard',
             'weight': 1.0,
             'boil_time': 60.0},
            {'name': 'hersbrucker',
             'weight': 1.0,
             'boil_time': 0.0},
        ],
        'yeast': {
            'name': 'White Labs Wlp029',
        },
        'data': {
            'percent_brew_house_yield': 0.70,
            'units': 'imperial',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    loader = JSONDataLoader(data_dir)
    beer = parse_recipe(recipe, loader)
    print(beer.format())


if __name__ == "__main__":
    main()
