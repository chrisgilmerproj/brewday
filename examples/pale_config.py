#! /usr/bin/env python

import os

from brew.parsers import parse_recipe


def main():

    recipe = {
        'name': 'Pale Ale',
        'start_volume': 7.0,
        'final_volume': 5.0,
        'grains': [
            {'name': 'pale malt 2-row us',
             'grain_data': {
                 'color': 1.8,
                 'ppg': 37,
             },
             'weight': 13.96},
            {'name': 'caramel crystal malt 20l',
             'grain_data': {
                 'color': 20.0,
                 'ppg': 35,
             },
             'weight': 0.78},
        ],
        'hops': [
            {'name': 'centennial',
             'hop_data': {
                 'percent_alpha_acids': 0.14,
             },
             'weight': 0.57,
             'boil_time': 60.0},
            {'name': 'cascade us',
             'hop_data': {
                 'percent_alpha_acids': 0.07,
             },
             'weight': 0.76,
             'boil_time': 5.0},
        ],
        'yeast': {
            'name': 'Wyeast 1056',
            'yeast_data': {
                'percent_attenuation': 0.75,
            },
        },
        'recipe_data': {
            'percent_brew_house_yield': 0.70,
            'units': 'imperial',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    beer = parse_recipe(recipe, data_dir)
    beer.format()


if __name__ == "__main__":
    main()
