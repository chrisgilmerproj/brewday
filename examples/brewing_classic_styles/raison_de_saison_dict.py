#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brewing Classic Styles: 80 Winning Recipes Anyone Can Brew
by Jamil Zainasheff and John J. Palmer

Raison de Saison

Used by permission of Brewers Publications (2007). All rights reserved.

You can purchase the book here:

- http://www.brewerspublications.com/books/brewing-classic-styles-80-winning-recipes-anyone-can-brew/

Original Stats:

OG:      1.060 (14.8P)
FG:      1.008 ( 2.0P)
ADF:     86%
IBU:     27
Color:   5 SRM (10 EBC)
Alcohol: 6.9% ABV (5.4% ABW)
Boil:    60 min
Pre-Boil Volume:  7 Gal (26.5L)
Pre-Boil Gravity: 1.051 (12.7P)
"""  # noqa

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        u'name': u"Raison de Saison (Extract)",
        u'start_volume': 7.0,
        u'final_volume': 6.0,
        u'grains': [
            {u'name': u'Pilsner Liquid Extract',
             u'data': {
                 u'color': 2.3,
                 u'ppg': 37,
             },
             u'weight': 7.7,
             u'grain_type': u'lme'},
            {u'name': u'Cane Beet Sugar',
             u'weight': 1.0,
             u'grain_type': u'dme'},
            {u'name': u'Wheat Liquid Extract',
             u'data': {
                 u'color': 4.0,
                 u'ppg': 37,
             },
             u'weight': 0.75,
             u'grain_type': u'lme'},
            {u'name': u'munich liquid malt extract',
             u'data': {
                 u'color': 9.0,
                 u'ppg': 37,
             },
             u'weight': 0.5,
             u'grain_type': u'lme'},
            {u'name': u'Caramunich Malt',
             u'data': {
                 u'color': 60.0,
             },
             u'weight': 0.125,
             u'grain_type': u'specialty'},
        ],
        u'hops': [
            {u'name': u'Hallertau US',
             u'data': {
                 u'percent_alpha_acids': 0.05,
             },
             u'weight': 1.7,
             u'boil_time': 60.0},
            {u'name': u'Hallertau US',
             u'data': {
                 u'percent_alpha_acids': 0.05,
             },
             u'weight': 0.75,
             u'boil_time': 0.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 3724',
            u'data': {
                u'percent_attenuation': 0.86,
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
