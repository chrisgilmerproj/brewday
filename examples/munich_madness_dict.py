#! /usr/bin/env python

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
"""  # nopep8

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        'name': "Munich Madness (All Grain)",
        'start_volume': 7.0,
        'final_volume': 6.0,
        'grains': [
            {'name': 'Pilsner 2 row Ger',
             'data': {
                 'color': 2.3,
             },
             'weight': 5.0},
            {'name': 'Munich Malt 10L',
             'data': {
                 'color': 9.0,
             },
             'weight': 4.0},
            {'name': 'Vienna Malt',
             'weight': 3.0},
            {'name': 'Caramunich Malt',
             'data': {
                 'color': 60.0,
             },
             'weight': 1.0,
             'grain_type': 'specialty'},
        ],
        'hops': [
            {'name': 'Hallertau US',
             'data': {
                 'percent_alpha_acids': 0.04,
             },
             'weight': 1.5,
             'boil_time': 60.0},
            {'name': 'Hallertau US',
             'data': {
                 'percent_alpha_acids': 0.04,
             },
             'weight': 0.5,
             'boil_time': 20.0},
        ],
        'yeast': {
            'name': 'Wyeast 2206',
            'data': {
                'percent_attenuation': 0.73,
            },
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
