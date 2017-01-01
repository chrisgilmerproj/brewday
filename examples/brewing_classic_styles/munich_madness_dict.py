#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brewing Classic Styles: 80 Winning Recipes Anyone Can Brew
by Jamil Zainasheff and John J. Palmer

Munich Madness

Used by permission of Brewers Publications (2007). All rights reserved.

You can purchase the book here:

- http://www.brewerspublications.com/books/brewing-classic-styles-80-winning-recipes-anyone-can-brew/

Original Stats:

OG:      1.055 (13.6P)
FG:      1.015 ( 3.7P)
ADF:     73%
IBU:     27
Color:   11 SRM (21 EBC)
Alcohol: 5.4% ABV (4.2% ABW)
Boil:    60 min
Pre-Boil Volume:  7 Gal (26.5L)
Pre-Boil Gravity: 1.047 (11.7P)
"""  # noqa

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        u'name': u"Munich Madness (All Grain)",
        u'start_volume': 7.0,
        u'final_volume': 6.0,
        u'grains': [
            {u'name': u'Pilsner 2 row Ger',
             u'data': {
                 u'color': 2.3,
             },
             u'weight': 5.0},
            {u'name': u'Munich Malt 10L',
             u'data': {
                 u'color': 9.0,
             },
             u'weight': 4.0},
            {u'name': u'Vienna Malt',
             u'weight': 3.0},
            {u'name': u'Caramunich Malt',
             u'data': {
                 u'color': 60.0,
             },
             u'weight': 1.0,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'Hallertau US',
             u'data': {
                 u'percent_alpha_acids': 0.04,
             },
             u'weight': 1.5,
             u'boil_time': 60.0},
            {u'name': u'Hallertau US',
             u'data': {
                 u'percent_alpha_acids': 0.04,
             },
             u'weight': 0.5,
             u'boil_time': 20.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 2206',
            u'data': {
                u'percent_attenuation': 0.73,
            },
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
