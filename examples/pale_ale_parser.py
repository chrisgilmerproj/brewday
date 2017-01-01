#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from brew.parsers import JSONDataLoader
from brew.parsers import parse_recipe

"""
Build a recipe using data parsers.
"""


def main():

    recipe = {
        u'name': u'Pale Ale',
        u'start_volume': 7.0,
        u'final_volume': 5.0,
        u'grains': [
            {u'name': u'pale malt 2-row us',
             u'data': {
                 u'color': 1.8,
                 u'ppg': 37,
             },
             u'weight': 13.96},
            {u'name': u'caramel crystal malt 20l',
             u'data': {
                 u'color': 20.0,
                 u'ppg': 35,
             },
             u'weight': 0.78},
        ],
        u'hops': [
            {u'name': u'centennial',
             u'data': {
                 u'percent_alpha_acids': 0.14,
             },
             u'weight': 0.57,
             u'boil_time': 60.0},
            {u'name': u'cascade us',
             u'data': {
                 u'percent_alpha_acids': 0.07,
             },
             u'weight': 0.76,
             u'boil_time': 5.0},
        ],
        u'yeast': {
            u'name': u'Wyeast 1056',
            u'data': {
                u'percent_attenuation': 0.75,
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
