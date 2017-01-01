#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brewing Classic Styles: 80 Winning Recipes Anyone Can Brew
by Jamil Zainasheff and John J. Palmer

Biere de l'Inde

Used by permission of Brewers Publications (2007). All rights reserved.

You can purchase the book here:

- http://www.brewerspublications.com/books/brewing-classic-styles-80-winning-recipes-anyone-can-brew/

Original Stats:

OG:      1.062 (15.2P)
FG:      1.015 ( 4.0P)
ADF:     74%
IBU:     50
Color:   11 SRM (22 EBC)
Alcohol: 6.2% ABV (4.8% ABW)
Boil:    60 min
Pre-Boil Volume:  7 Gal (26.5L)
Pre-Boil Gravity: 1.053 (13.0P)
"""  # noqa

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        u'name': u"Biere de l'Inde (Extract)",
        u'start_volume': 7.0,
        u'final_volume': 6.0,
        u'grains': [
            {u'name': u'English Pale Ale Liquid Extract',
             u'data': {
                 u'color': 3.5,
                 u'ppg': 37,
             },
             u'weight': 8.7,
             u'grain_type': u'lme'},
            {u'name': u'wheat liquid extract',
             u'data': {
                 u'color': 4.0,
                 u'ppg': 37,
             },
             u'weight': 0.5,
             u'grain_type': u'lme'},
            {u'name': u'biscuit malt',
             u'data': {
                 u'color': 25.0,
             },
             u'weight': 0.5,
             u'grain_type': u'specialty'},
            {u'name': u'caramel crystal malt 40l',
             u'weight': 0.5,
             u'grain_type': u'specialty'},
            {u'name': u'caramel crystal malt 120l',
             u'weight': 0.375,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'challenger',
             u'data': {
                 u'percent_alpha_acids': 0.08,
             },
             u'weight': 1.43,
             u'boil_time': 60.0},
            {u'name': u'fuggle',
             u'data': {
                 u'percent_alpha_acids': 0.05,
             },
             u'weight': 1.5,
             u'boil_time': 10.0},
            {u'name': u'east kent golding',
             u'data': {
                 u'percent_alpha_acids': 0.05,
             },
             u'weight': 1.5,
             u'boil_time': 0.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 1028',
            u'data': {
                u'percent_attenuation': 0.74,
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
