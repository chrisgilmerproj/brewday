import json
import os

from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.utilities.sugar import sg_to_gu
from brew.yeasts import Yeast


def validate_required_fields(data, required_fields):
    """
    Validate fields which are required as part of the data.

    data: a python dict
    required_fields: a list of tuples where the first element is a string with
                     a value that should be a key found in the data dict and
                     where the second element is a python type or list/tuple of
                     python types to check the field against.
    """
    for field, field_type in required_fields:
        if field not in data:
            raise Exception("Required field '{}' missing from recipe".format(
                field))
        if not isinstance(data[field], field_type):
            raise Exception("Required field '{}' is not of type '{}'".format(
                field, field_type))


def validate_optional_fields(data, data_field, optional_fields):
    """
    Validate fields which are optional as part of the data.

    data: a python dict
    data_field: the name of the key in the data that holds the optional data
    optional_fields: a list of tuples where the first element is a string with
                     a value that should be a key found in the data dict and
                     where the second element is a python type or list/tuple of
                     python types to check the field against.
    """
    # If no optional data field present then return
    if data_field not in data:
        return
    for field, field_type in optional_fields:
        if field in data[data_field]:
            # With optional fields only check the type as they are overrides
            # and not all overrides need to be present
            if not isinstance(data[data_field][field], field_type):
                raise Exception("Optional field '{}' in '{}' is not of type '{}'".format(  # nopep8
                    field, data_field, field_type))


def validate_recipe(recipe):
    required_fields = [('name', str),
                       ('start_volume', (int, float)),
                       ('final_volume', (int, float)),
                       ('grains', (list, tuple)),
                       ('hops', (list, tuple)),
                       ('yeast', dict),
                       ]
    validate_required_fields(recipe, required_fields)


def validate_grains(grain_data):
    required_fields = [('name', str),
                       ('weight', float),
                       ]
    data_field = 'grain_data'
    optional_fields = [('color', float),
                       ('ppg', int),
                       ]
    validate_required_fields(grain_data, required_fields)
    validate_optional_fields(grain_data, data_field, optional_fields)


def validate_hops(hop_data):
    required_fields = [('name', str),
                       ('weight', float),
                       ('boil_time', float),
                       ]
    data_field = 'hop_data'
    optional_fields = [('percent_alpha_acids', float),
                       ]
    validate_required_fields(hop_data, required_fields)
    validate_optional_fields(hop_data, data_field, optional_fields)


def validate_yeast(yeast_data):
    required_fields = [('name', str),
                       ]
    data_field = 'yeast_data'
    optional_fields = [('percent_attenuation', float),
                       ]
    validate_required_fields(yeast_data, required_fields)
    validate_optional_fields(yeast_data, data_field, optional_fields)


def format_name(name):
    return name.lower().replace(' ', '_').replace('-', '_')


def read_json_file(filename):
    data = None
    with open(filename, 'r') as data_file:
        data = json.loads(data_file.read())
    return data


def get_item_json(data_dir, dir_suffix, item_name):
    item_dir = os.path.join(data_dir, dir_suffix)
    item_list = [item[:-5] for item in os.listdir(item_dir)]

    name = format_name(item_name)
    if name not in item_list:
        raise Exception('Item from {} dir not found: {}'.format(dir_suffix,
                                                                name))

    item_filename = os.path.join(item_dir, '{}.json'.format(name))
    return read_json_file(item_filename)


def parse_cereals(recipe, data_dir):
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
        validate_grains(cereal_data)
        try:
            cereal_json = get_item_json(data_dir,
                                        'cereals/',
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


def parse_hops(recipe, data_dir):
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
        validate_hops(hop_data)
        try:
            hop_json = get_item_json(data_dir, 'hops/', hop_data['name'])
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


def parse_yeast(recipe, data_dir):
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
    validate_yeast(yeast_data)
    try:
        yeast_json = get_item_json(data_dir, 'yeast/', yeast_data['name'])
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

    All other fields will be ignored and may be used for other metadata.

    The dict objects in the grains, hops, and yeast values are required to have
    the key 'name' and the remaining attributes will be looked up in the data
    directory if they are not provided.
    """
    validate_recipe(recipe)

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
    return beer
