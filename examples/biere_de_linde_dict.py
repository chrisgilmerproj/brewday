#! /usr/bin/env python

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
"""  # nopep8

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe


def main():

    recipe = {
        'name': "Biere de l'Inde (Extract)",
        'start_volume': 7.0,
        'final_volume': 6.0,
        'grains': [
            {'name': 'English Pale Ale Liquid Extract',
             'data': {
                 'color': 3.5,
                 'ppg': 37,
             },
             'weight': 8.7,
             'grain_type': 'lme'},
            {'name': 'wheat liquid extract',
             'data': {
                 'color': 4.0,
                 'ppg': 37,
             },
             'weight': 0.5,
             'grain_type': 'lme'},
            {'name': 'biscuit malt',
             'data': {
                 'color': 25.0,
             },
             'weight': 0.5,
             'grain_type': 'specialty'},
            {'name': 'caramel crystal malt 40l',
             'weight': 0.5,
             'grain_type': 'specialty'},
            {'name': 'caramel crystal malt 120l',
             'weight': 0.375,
             'grain_type': 'specialty'},
        ],
        'hops': [
            {'name': 'challenger',
             'data': {
                 'percent_alpha_acids': 0.08,
             },
             'weight': 1.43,
             'boil_time': 60.0},
            {'name': 'fuggle',
             'data': {
                 'percent_alpha_acids': 0.05,
             },
             'weight': 1.5,
             'boil_time': 10.0},
            {'name': 'east kent golding',
             'data': {
                 'percent_alpha_acids': 0.05,
             },
             'weight': 1.5,
             'boil_time': 0.0},
        ],
        'yeast': {
            'name': 'Wyeast 1028',
            'data': {
                'percent_attenuation': 0.74,
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
