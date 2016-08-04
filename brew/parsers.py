import glob
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
    DATA = {}

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

    def get_item(self, dir_suffix, item_name):
        item_dir = os.path.join(self.data_dir, dir_suffix)

        # Cache the directory
        if dir_suffix not in self.DATA:
            self.DATA[dir_suffix] = {}
            for item in glob.glob('{}*.json'.format(item_dir)):
                filename = os.path.basename(item)[:-5]
                self.DATA[dir_suffix][filename] = {}

        name = self.format_name(item_name)
        if name not in self.DATA[dir_suffix]:
            raise Exception('Item from {} dir not found: {}'.format(dir_suffix,
                                                                    name))

        # Cache file data
        if not self.DATA[dir_suffix][name]:
            item_filename = os.path.join(item_dir, '{}.json'.format(name))
            data = self.read_json_file(item_filename)
            self.DATA[dir_suffix][name] = data
            return data
        else:
            return self.DATA[dir_suffix][name]


def parse_cereals(recipe, parser):
    """
    Parse grains data from a recipe

    Grain must have the following top level attributes:
    - name       (str)
    - weight     (float)
    - grain_data (dict) (optional)

    Additionally grains may contain override data in the 'data'
    attribute with the following keys:
    - color (float)
    - ppg   (int)
    """
    # Create Grains
    grain_additions = []
    for cereal_data in recipe['grains']:
        GrainAddition.validate(cereal_data)

        cereal_json = {}
        try:
            cereal_json = parser.get_item('cereals/', cereal_data['name'])
        except Exception:
            pass

        name = cereal_json.get('name', cereal_data['name'])
        color = None
        ppg = None

        if 'data' in cereal_data:
            color = cereal_data['data'].get('color', None)
            ppg = cereal_data['data'].get('ppg', None)

        if not color:
            color = float(cereal_json['color'][:-4])

        if not ppg:
            ppg = sg_to_gu(float(cereal_json['potential'][:-3]))

        grain = Grain(name, color=color, ppg=ppg)
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

    Additionally hops may contain override data in the 'data' attribute
    with the following keys:
    - percent_alpha_acids (float)
    """
    # Create Grains
    hop_additions = []
    for hop_data in recipe['hops']:
        HopAddition.validate(hop_data)
        try:
            hop_json = parser.get_item('hops/', hop_data['name'])  # nopep8
        except Exception:
            continue

        alpha_acids = None
        if 'data' in hop_data and 'percent_alpha_acids' in hop_data['data']:  # nopep8
            alpha_acids = hop_data['data']['percent_alpha_acids']
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

    Additionally yeast may contain override data in the 'data' attribute
    with the following keys:
    - percent_attenuation (float)
    """
    yeast_data = recipe['yeast']
    Yeast.validate(yeast_data)
    try:
        yeast_json = parser.get_item('yeast/', yeast_data['name'])  # nopep8
    except Exception:
        return Yeast(yeast_data['name'])

    attenuation = None
    if 'data' in yeast_data and 'percent_attenuation' in yeast_data['data']:  # nopep8
        attenuation = yeast_data['data']['percent_attenuation']
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

    Additionally the recipe may contain override data in the 'data'
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
    if 'data' in recipe:
        if 'percent_brew_house_yield' in recipe['data']:
            recipe_kwargs['percent_brew_house_yield'] = \
                recipe['data']['percent_brew_house_yield']
        if 'units' in recipe['data']:
            recipe_kwargs['units'] = recipe['data']['units']

    beer = Recipe(recipe['name'],
                  **recipe_kwargs)
    return beer
