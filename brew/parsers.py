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


class DataLoader(object):
    """
    Base class for loading data from data files inside the data_dir.
    """
    DATA = {}
    EXT = ''

    def __init__(self, data_dir):
        self.data_dir = data_dir

    @classmethod
    def format_name(cls, name):
        """
        Reformat a given name to match the filename of a data file.
        """
        return name.lower().replace(' ', '_').replace('-', '_')

    @classmethod
    def read_data(cls, filename):
        raise NotImplementedError

    def get_item(self, dir_suffix, item_name):
        item_dir = os.path.join(self.data_dir, dir_suffix)

        # Cache the directory
        if dir_suffix not in self.DATA:
            self.DATA[dir_suffix] = {}
            for item in glob.glob('{}*.{}'.format(item_dir, self.EXT)):
                ext_len = len(self.EXT) + 1
                filename = os.path.basename(item)[:-ext_len]
                self.DATA[dir_suffix][filename] = {}

        name = self.format_name(item_name)
        if name not in self.DATA[dir_suffix]:
            raise Exception('Item from {} dir not found: {}'.format(dir_suffix,
                                                                    name))

        # Cache file data
        if not self.DATA[dir_suffix][name]:
            item_filename = os.path.join(item_dir, '{}.{}'.format(name, self.EXT))  # nopep8
            data = self.read_data(item_filename)
            self.DATA[dir_suffix][name] = data
            return data
        else:
            return self.DATA[dir_suffix][name]


class JSONDataLoader(DataLoader):
    """
    Load data from JSON files inside the data_dir.
    """
    EXT = 'json'

    @classmethod
    def read_data(cls, filename):
        data = None
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
        return data


def parse_cereals(cereal, loader):
    """
    Parse grains data from a recipe

    Grain must have the following top level attributes:
    - name   (str)
    - weight (float)
    - data   (dict) (optional)

    Additionally grains may contain override data in the 'data'
    attribute with the following keys:
    - color (float)
    - ppg   (int)
    """
    GrainAddition.validate(cereal)

    cereal_data = {}
    try:
        cereal_data = loader.get_item('cereals/', cereal['name'])
    except Exception:
        pass

    name = cereal_data.get('name', cereal['name'])
    color = None
    ppg = None

    if 'data' in cereal:
        color = cereal['data'].get('color', None)
        ppg = cereal['data'].get('ppg', None)

    if not color:
        color = float(cereal_data['color'][:-4])

    if not ppg:
        ppg = sg_to_gu(float(cereal_data['potential'][:-3]))

    grain_obj = Grain(name, color=color, ppg=ppg)

    grain_add_kwargs = {
        'weight': float(cereal['weight']),
    }
    if 'grain_type' in cereal:
        grain_add_kwargs['grain_type'] = cereal['grain_type']
    if 'units' in cereal:
        grain_add_kwargs['units'] = cereal['units']
    return GrainAddition(grain_obj, **grain_add_kwargs)


def parse_hops(hop, loader):
    """
    Parse hops data from a recipe

    Hops must have the following top level attributes:
    - name      (str)
    - weight    (float)
    - boil_time (float)
    - data      (dict) (optional)

    Additionally hops may contain override data in the 'data' attribute
    with the following keys:
    - percent_alpha_acids (float)
    """
    HopAddition.validate(hop)

    hop_data = {}
    try:
        hop_data = loader.get_item('hops/', hop['name'])
    except Exception:
        pass

    name = hop_data.get('name', hop['name'])
    alpha_acids = None

    if 'data' in hop:
        alpha_acids = hop['data'].get('percent_alpha_acids', None)

    if not alpha_acids:
        alpha_acids = float(hop_data['alpha_acid_composition'].split('%')[0]) / 100.  # nopep8

    hop_obj = Hop(name, percent_alpha_acids=alpha_acids)
    hop_add_kwargs = {
        'weight': float(hop['weight']),
        'boil_time': hop['boil_time'],
    }
    if 'hop_type' in hop:
        hop_add_kwargs['hop_type'] = hop['hop_type']
    if 'units' in hop:
        hop_add_kwargs['units'] = hop['units']
    return HopAddition(hop_obj, **hop_add_kwargs)


def parse_yeast(yeast, loader):
    """
    Parse yeast data from a recipe

    Yeast must have the following top level attributes:
    - name (str)
    - data (dict) (optional)

    Additionally yeast may contain override data in the 'data' attribute
    with the following keys:
    - percent_attenuation (float)
    """
    Yeast.validate(yeast)

    yeast_data = {}
    try:
        yeast_data = loader.get_item('yeast/', yeast['name'])  # nopep8
    except Exception:
        return Yeast(yeast['name'])

    name = yeast_data.get('name', yeast['name'])
    attenuation = None

    if 'data' in yeast:
        attenuation = yeast['data'].get('percent_attenuation', None)

    if not attenuation:
        attenuation = yeast_data['attenuation'][0]

    return Yeast(name, percent_attenuation=attenuation)


def parse_recipe(recipe, loader):
    """
    Parse a recipe from a python Dict

    recipe: a python dict describing the recipe
    loader: a data loader class that loads data from data files

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
    Recipe.validate(recipe)

    grain_additions = []
    for grain in recipe['grains']:
        grain_additions.append(parse_cereals(grain, loader))

    hop_additions = []
    for hop in recipe['hops']:
        hop_additions.append(parse_hops(hop, loader))

    yeast = parse_yeast(recipe['yeast'], loader)

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
