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


def parse_cereals():
    # Look up cereal data
    cereal_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/cereals/'))
    cereal_list = [cereal[:-5] for cereal in os.listdir(cereal_dir)]

    # Create Grains
    grain_additions = []
    for cereal_data in recipe['grains']:
        name = cereal_data['name'].replace(' ', '_').replace('-', '_')
        if name in cereal_list:
            cereal_filename = os.path.join(cereal_dir, '{}.json'.format(name))
            with open(cereal_filename, 'r') as cereal_file:
                grain_json = json.loads(cereal_file.read())
                grain = Grain(grain_json['name'],
                              color=float(grain_json['color'][:-4]),
                              ppg=sg_to_gu(float(grain_json['potential'][:-3])))  # nopep8
                grain_add = GrainAddition(grain, weight=float(cereal_data['weight']))  # nopep8
                grain_additions.append(grain_add)
        else:
            print 'Cereal not found: {}'.format(name)

    return grain_additions


def parse_hops():
    # Look up hop data
    hop_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/hops/'))
    hop_list = [hop[:-5] for hop in os.listdir(hop_dir)]

    # Create Grains
    hop_additions = []
    for hop_data in recipe['hops']:
        name = hop_data['name'].replace(' ', '_').replace('-', '_')
        if name in hop_list:
            hop_filename = os.path.join(hop_dir, '{}.json'.format(name))
            with open(hop_filename, 'r') as hop_file:
                hop_json = json.loads(hop_file.read())
                alpha_acids = float(hop_json['alpha_acid_composition'].split('%')[0]) / 100.  # nopep8
                hop = Hop(hop_json['name'],
                          percent_alpha_acids=alpha_acids)
                hop_add = HopAddition(hop,
                                      weight=float(hop_data['weight']),
                                      boil_time=hop_data['boil_time'])
                hop_additions.append(hop_add)
        else:
            print 'Hop not found: {}'.format(name)
    return hop_additions


def main():
    grain_additions = parse_cereals()
    hop_additions = parse_hops()
    yeast = Yeast(recipe['yeast']['name'])

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
