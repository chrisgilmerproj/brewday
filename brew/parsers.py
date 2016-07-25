import json
import os

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.utilities.sugar import sg_to_gu
from brew.yeasts import Yeast


class JSONParser(object):

    def __init__(self, data_dir):
        self.data_dir = data_dir

    @classmethod
    def format_name(cls, name):
        return name.lower().replace(' ', '_').replace('-', '_')

    @classmethod
    def read_json_file(cls, filename):
        data = None
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
        return data

    def get_item_json(self, dir_suffix, item_name):
        item_dir = os.path.join(self.data_dir, dir_suffix)
        item_list = [item[:-5] for item in os.listdir(item_dir)]

        name = self.format_name(item_name)
        if name not in item_list:
            raise Exception('Item from {} dir not found: {}'.format(dir_suffix,
                                                                    name))

        item_filename = os.path.join(item_dir, '{}.json'.format(name))
        return self.read_json_file(item_filename)


def parse_cereals(recipe, parser):
    """
    Parse grains data from a recipe

    Grain must have the following top level attributes:
    - name       (str)
    - weight     (float)
    - grain_data (dict) (optional)

    Additionally grains may contain override data in the 'grain_data'
    attribute with the following keys:
    - color (float)
    - ppg   (int)
    """
    # Create Grains
    grain_additions = []
    for cereal_data in recipe['grains']:
        GrainAddition.validate(cereal_data)
        try:
            cereal_json = parser.get_item_json('cereals/',
                                               cereal_data['name'])
        except Exception:
            continue

        color = None
        if 'grain_data' in cereal_data and 'color' in cereal_data['grain_data']:  # nopep8
            color = cereal_data['grain_data']['color']
        else:
            color = float(cereal_json['color'][:-4])

        ppg = None
        if 'grain_data' in cereal_data and 'ppg' in cereal_data['grain_data']:
            ppg = cereal_data['grain_data']['ppg']
        else:
            ppg = sg_to_gu(float(cereal_json['potential'][:-3]))
        grain = Grain(cereal_json['name'],
                      color=color,
                      ppg=ppg)
        grain_add = GrainAddition(grain, weight=float(cereal_data['weight']))
        grain_additions.append(grain_add)

    return grain_additions


def parse_hops(recipe, parser):
    """
    Parse hops data from a recipe

    Hops must have the following top level attributes:
    - name      (str)
    - weight    (float)
    - boil_time (float)
    - hop_data  (dict) (optional)

    Additionally hops may contain override data in the 'hop_data' attribute
    with the following keys:
    - percent_alpha_acids (float)
    """
    # Create Grains
    hop_additions = []
    for hop_data in recipe['hops']:
        HopAddition.validate(hop_data)
        try:
            hop_json = parser.get_item_json('hops/', hop_data['name'])  # nopep8
        except Exception:
            continue

        alpha_acids = None
        if 'hop_data' in hop_data and 'percent_alpha_acids' in hop_data['hop_data']:  # nopep8
            alpha_acids = hop_data['hop_data']['percent_alpha_acids']
        else:
            alpha_acids = float(hop_json['alpha_acid_composition'].split('%')[0]) / 100.  # nopep8

        hop = Hop(hop_json['name'],
                  percent_alpha_acids=alpha_acids)
        hop_add = HopAddition(hop,
                              weight=float(hop_data['weight']),
                              boil_time=hop_data['boil_time'])
        hop_additions.append(hop_add)
    return hop_additions


def parse_yeast(recipe, parser):
    """
    Parse yeast data from a recipe

    Yeast must have the following top level attributes:
    - name       (str)
    - yeast_data (dict) (optional)

    Additionally yeast may contain override data in the 'yeast_data' attribute
    with the following keys:
    - percent_attenuation (float)
    """
    yeast_data = recipe['yeast']
    Yeast.validate(yeast_data)
    try:
        yeast_json = parser.get_item_json('yeast/', yeast_data['name'])  # nopep8
    except Exception:
        return Yeast(yeast_data['name'])

    attenuation = None
    if 'yeast_data' in yeast_data and 'percent_attenuation' in yeast_data['yeast_data']:  # nopep8
        attenuation = yeast_data['yeast_data']['percent_attenuation']
    else:
        attenuation = yeast_json['attenuation'][0]

    return Yeast(yeast_data['name'],
                 percent_attenuation=attenuation)


def parse_recipe(recipe, data_dir):
    """
    Parse a recipe from a python Dict

    recipe: a python dict describing the recipe
    data_dir: a path to a directory holding data to parse for construcitng the
              recipe

    A recipe must have the following top level attributes:
    - name         (str)
    - start_volume (float)
    - final_volume (float)
    - grains       (list(dict))
    - hops         (list(dict))
    - yeast        (dict)

    Additionally the recipe may contain override data in the 'recipe_data'
    attribute with the following keys:
    - percent_brew_house_yield (float)
    - units                    (str)

    All other fields will be ignored and may be used for other metadata.

    The dict objects in the grains, hops, and yeast values are required to have
    the key 'name' and the remaining attributes will be looked up in the data
    directory if they are not provided.
    """
    parser = JSONParser(data_dir)
    Recipe.validate(recipe)

    grain_additions = parse_cereals(recipe, parser)
    hop_additions = parse_hops(recipe, parser)
    yeast = parse_yeast(recipe, parser)

    recipe_kwargs = {
        'grain_additions': grain_additions,
        'hop_additions': hop_additions,
        'yeast': yeast,
        'start_volume': recipe['start_volume'],
        'final_volume': recipe['final_volume'],
    }
    if 'recipe_data' in recipe:
        if 'percent_brew_house_yield' in recipe['recipe_data']:
            recipe_kwargs['percent_brew_house_yield'] = \
                recipe['recipe_data']['percent_brew_house_yield']
        if 'units' in recipe['recipe_data']:
            recipe_kwargs['units'] = recipe['recipe_data']['units']

    beer = Recipe(recipe['name'],
                  **recipe_kwargs)
    return beer
