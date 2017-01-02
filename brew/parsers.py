# -*- coding: utf-8 -*-
import glob
import json
import os
import warnings

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.yeasts import Yeast

__all__ = [
    u'DataLoader',
    u'JSONDataLoader',
    u'parse_cereals',
    u'parse_hops',
    u'parse_yeast',
    u'parse_recipe',
]


class DataLoader(object):
    """
    Base class for loading data from data files inside the data_dir.
    """
    #: A local cache of loaded data
    DATA = {}
    #: The expected file extension (json, xml, csv)
    EXT = ''

    def __init__(self, data_dir):
        """
        :param str data_dir: The directory where the data resides
        """
        if not os.path.isdir(data_dir):
            raise Exception(u"Directory '{}' does not exist".format(data_dir))
        self.data_dir = data_dir

    @classmethod
    def format_name(cls, name):
        """
        Reformat a given name to match the filename of a data file.
        """
        return name.lower().replace(u' ', u'_').replace(u'-', u'_')

    @classmethod
    def read_data(cls, filename):
        """
        :param str filename: The filename of the file to read
        :raises NotImplementedError: Must be supplied in inherited class
        """
        raise NotImplementedError

    def get_item(self, dir_suffix, item_name):
        """
        :param str dir_suffix: The directory name suffix
        :param str item_name: The name of the item to load
        :return: The item as a python dict
        :raises Exception: If item directory does not exist
        :raises Warning: If item not found in the directory
        """
        item_dir = os.path.join(self.data_dir, dir_suffix)
        if not os.path.isdir(item_dir):
            raise Exception(u"Item directory '{}' does not exist".format(item_dir))  # noqa

        # Cache the directory
        if dir_suffix not in self.DATA:
            self.DATA[dir_suffix] = {}
            for item in glob.glob('{}*.{}'.format(item_dir, self.EXT)):
                ext_len = len(self.EXT) + 1
                filename = os.path.basename(item)[:-ext_len]
                self.DATA[dir_suffix][filename] = {}

        name = self.format_name(item_name)
        if name not in self.DATA[dir_suffix]:
            warnings.warn(u'Item from {} dir not found: {}'.format(dir_suffix,  # noqa
                                                                   name))
            return {}

        # Cache file data
        if not self.DATA[dir_suffix][name]:
            item_filename = os.path.join(item_dir, '{}.{}'.format(name, self.EXT))  # noqa
            data = self.read_data(item_filename)
            self.DATA[dir_suffix][name] = data
            return data
        else:
            return self.DATA[dir_suffix][name]


class JSONDataLoader(DataLoader):
    """
    Load data from JSON files inside the data_dir.
    """
    #: The JSON file extension
    EXT = 'json'

    @classmethod
    def read_data(cls, filename):
        """
        :param str filename: The filename of the file to read
        :return: The data loaded from a JSON file
        """
        data = None
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
        return data


def parse_cereals(cereal, loader, dir_suffix='cereals/'):
    """
    Parse grains data from a recipe

    :param dict cereal: A representation of a cereal
    :param DataLoader loader: A class to load additional information

    Grain must have the following top level attributes:

    * name   (str)
    * weight (float)
    * data   (dict) (optional)

    Additionally grains may contain override data in the 'data'
    attribute with the following keys:

    * color (float)
    * ppg   (int)
    """
    GrainAddition.validate(cereal)

    cereal_data = loader.get_item(dir_suffix, cereal[u'name'])

    name = cereal_data.get(u'name', cereal[u'name'])
    color = None
    ppg = None

    if u'data' in cereal:
        color = cereal[u'data'].get(u'color', None)
        ppg = cereal[u'data'].get(u'ppg', None)

    if not color:
        color = cereal_data.get(u'color', None)

    if not ppg:
        ppg = cereal_data.get(u'ppg', None)

    grain_obj = Grain(name, color=color, ppg=ppg)

    grain_add_kwargs = {
        u'weight': float(cereal[u'weight']),
    }
    if u'grain_type' in cereal:
        grain_add_kwargs[u'grain_type'] = cereal[u'grain_type']
    if u'units' in cereal:
        grain_add_kwargs[u'units'] = cereal[u'units']
    return GrainAddition(grain_obj, **grain_add_kwargs)


def parse_hops(hop, loader, dir_suffix='hops/'):
    """
    Parse hops data from a recipe

    :param dict hops: A representation of a hop
    :param DataLoader loader: A class to load additional information

    Hops must have the following top level attributes:

    * name      (str)
    * weight    (float)
    * boil_time (float)
    * data      (dict) (optional)

    Additionally hops may contain override data in the 'data' attribute
    with the following keys:

    * percent_alpha_acids (float)
    """
    HopAddition.validate(hop)

    hop_data = loader.get_item(dir_suffix, hop[u'name'])

    name = hop_data.get(u'name', hop[u'name'])
    alpha_acids = None

    if u'data' in hop:
        alpha_acids = hop[u'data'].get(u'percent_alpha_acids', None)

    if not alpha_acids:
        alpha_acids = hop_data.get(u'percent_alpha_acids', None)

    hop_obj = Hop(name, percent_alpha_acids=alpha_acids)
    hop_add_kwargs = {
        u'weight': float(hop[u'weight']),
        u'boil_time': hop[u'boil_time'],
    }
    if u'hop_type' in hop:
        hop_add_kwargs[u'hop_type'] = hop[u'hop_type']
    if u'units' in hop:
        hop_add_kwargs[u'units'] = hop[u'units']
    return HopAddition(hop_obj, **hop_add_kwargs)


def parse_yeast(yeast, loader, dir_suffix='yeast/'):
    """
    Parse yeast data from a recipe

    :param dict hops: A representation of a yeast
    :param DataLoader loader: A class to load additional information

    Yeast must have the following top level attributes:

    * name (str)
    * data (dict) (optional)

    Additionally yeast may contain override data in the 'data' attribute
    with the following keys:

    * percent_attenuation (float)
    """
    Yeast.validate(yeast)

    yeast_data = loader.get_item(dir_suffix, yeast[u'name'])  # noqa

    name = yeast_data.get(u'name', yeast[u'name'])
    attenuation = None

    if u'data' in yeast:
        attenuation = yeast[u'data'].get(u'percent_attenuation', None)

    if not attenuation:
        attenuation = yeast_data.get(u'percent_attenuation', None)

    return Yeast(name, percent_attenuation=attenuation)


def parse_recipe(recipe, loader,
                 cereals_loader=None,
                 hops_loader=None,
                 yeast_loader=None,
                 cereals_dir_suffix='cereals/',
                 hops_dir_suffix='hops/',
                 yeast_dir_suffix='yeast/'):
    """
    Parse a recipe from a python Dict

    :param dict recipe: A representation of a recipe
    :param DataLoader loader: A class to load additional information
    :param DataLoader cereal_loader: A class to load additional information specific to cereals
    :param DataLoader hops_loader: A class to load additional information specific to hops
    :param DataLoader yeast_loader: A class to load additional information specific to yeast

    A recipe must have the following top level attributes:

    * name         (str)
    * start_volume (float)
    * final_volume (float)
    * grains       (list(dict))
    * hops         (list(dict))
    * yeast        (dict)

    Additionally the recipe may contain override data in the 'data'
    attribute with the following keys:

    * percent_brew_house_yield (float)
    * units                    (str)

    All other fields will be ignored and may be used for other metadata.

    The dict objects in the grains, hops, and yeast values are required to have
    the key 'name' and the remaining attributes will be looked up in the data
    directory if they are not provided.
    """  # noqa
    if cereals_loader is None:
        cereals_loader = loader
    if hops_loader is None:
        hops_loader = loader
    if yeast_loader is None:
        yeast_loader = loader

    Recipe.validate(recipe)

    grain_additions = []
    for grain in recipe[u'grains']:
        grain_additions.append(parse_cereals(grain, cereals_loader,
                                             dir_suffix=cereals_dir_suffix))

    hop_additions = []
    for hop in recipe[u'hops']:
        hop_additions.append(parse_hops(hop, hops_loader,
                                        dir_suffix=hops_dir_suffix))

    yeast = parse_yeast(recipe[u'yeast'], yeast_loader,
                        dir_suffix=yeast_dir_suffix)

    recipe_kwargs = {
        u'grain_additions': grain_additions,
        u'hop_additions': hop_additions,
        u'yeast': yeast,
        u'start_volume': recipe[u'start_volume'],
        u'final_volume': recipe[u'final_volume'],
    }
    if u'data' in recipe:
        if u'percent_brew_house_yield' in recipe[u'data']:
            recipe_kwargs[u'percent_brew_house_yield'] = \
                recipe[u'data'][u'percent_brew_house_yield']
        if u'units' in recipe[u'data']:
            recipe_kwargs[u'units'] = recipe[u'data'][u'units']

    beer = Recipe(recipe[u'name'],
                  **recipe_kwargs)
    return beer
