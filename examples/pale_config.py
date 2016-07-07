#! /usr/bin/env python

import json
import os

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.utilities.sugar import sg_to_gu
from brew.yeasts import Yeast


def format_name(name):
    return name.replace(' ', '_').replace('-', '_')


def read_json_file(filename):
    data = None
    with open(filename, 'r') as data_file:
        data = json.loads(data_file.read())
    return data


def parse_cereals(recipe, data_dir):
    # Look up cereal data
    cereal_dir = os.path.join(data_dir, 'cereals/')
    cereal_list = [cereal[:-5] for cereal in os.listdir(cereal_dir)]

    # Create Grains
    grain_additions = []
    for cereal_data in recipe['grains']:
        name = format_name(cereal_data['name'])
        if name not in cereal_list:
            print('Cereal not found: {}'.format(name))
            continue

        cereal_filename = os.path.join(cereal_dir, '{}.json'.format(name))
        grain_json = read_json_file(cereal_filename)
        grain = Grain(grain_json['name'],
                      color=float(grain_json['color'][:-4]),
                      ppg=sg_to_gu(float(grain_json['potential'][:-3])))
        grain_add = GrainAddition(grain, weight=float(cereal_data['weight']))
        grain_additions.append(grain_add)

    return grain_additions


def parse_hops(recipe, data_dir):
    # Look up hop data
    hop_dir = os.path.join(data_dir, 'hops/')
    hop_list = [hop[:-5] for hop in os.listdir(hop_dir)]

    # Create Grains
    hop_additions = []
    for hop_data in recipe['hops']:
        name = format_name(hop_data['name'])
        if name not in hop_list:
            print('Hop not found: {}'.format(name))
            continue

        hop_filename = os.path.join(hop_dir, '{}.json'.format(name))
        hop_json = read_json_file(hop_filename)
        alpha_acids = float(hop_json['alpha_acid_composition'].split('%')[0]) / 100.  # nopep8
        hop = Hop(hop_json['name'],
                  percent_alpha_acids=alpha_acids)
        hop_add = HopAddition(hop,
                              weight=float(hop_data['weight']),
                              boil_time=hop_data['boil_time'])
        hop_additions.append(hop_add)
    return hop_additions


def parse_yeast(recipe, data_dir):
    # yeast_dir = os.path.join(data_dir, 'yeast/')
    return Yeast(recipe['yeast']['name'])


def main():

    recipe = {
        'name': 'Pale Ale',
        'start_volume': 7.0,
        'final_volume': 5.0,
        'grains': [
            {'name': 'pale malt 2-row us',
             'weight': 13.96},
            {'name': 'caramel crystal malt 20l',
             'weight': 0.78},
        ],
        'hops': [
            {'name': 'centennial',
             'weight': 0.57,
             'boil_time': 60.0},
            {'name': 'cascade us',
             'weight': 0.76,
             'boil_time': 5.0},
        ],
        'yeast': {
            'name': 'Danstar',
        },
    }

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    grain_additions = parse_cereals(recipe, data_dir)
    hop_additions = parse_hops(recipe, data_dir)
    yeast = parse_yeast(recipe, data_dir)

    beer = Recipe(recipe['name'],
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  yeast=yeast,
                  start_volume=recipe['start_volume'],
                  final_volume=recipe['final_volume'],
                  )
    beer.format()


if __name__ == "__main__":
    main()