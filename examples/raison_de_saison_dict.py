#! /usr/bin/env python

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
"""  # nopep8

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        'name': "Raison de Saison (Extract)",
        'start_volume': 7.0,
        'final_volume': 6.0,
        'grains': [
            {'name': 'Pilsner Liquid Extract',
             'data': {
                 'color': 2.3,
                 'ppg': 37,
             },
             'weight': 7.7,
             'grain_type': 'lme'},
            {'name': 'Cane Beet Sugar',
             'weight': 1.0,
             'grain_type': 'dme'},
            {'name': 'Wheat Liquid Extract',
             'data': {
                 'color': 4.0,
                 'ppg': 37,
             },
             'weight': 0.75,
             'grain_type': 'lme'},
            {'name': 'munich liquid malt extract',
             'data': {
                 'color': 9.0,
                 'ppg': 37,
             },
             'weight': 0.5,
             'grain_type': 'lme'},
            {'name': 'Caramunich Malt',
             'data': {
                 'color': 60.0,
             },
             'weight': 0.125,
             'grain_type': 'specialty'},
        ],
        'hops': [
            {'name': 'Hallertau US',
             'data': {
                 'percent_alpha_acids': 0.05,
             },
             'weight': 1.7,
             'boil_time': 60.0},
            {'name': 'Hallertau US',
             'data': {
                 'percent_alpha_acids': 0.05,
             },
             'weight': 0.75,
             'boil_time': 0.0},
        ],
        'yeast': {
            'name': 'Wyeast 3724',
            'data': {
                'percent_attenuation': 0.86,
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
