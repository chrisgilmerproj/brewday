from .constants import GRAIN_TYPE_LIST
from .constants import HOP_TYPE_LIST
from .constants import IMPERIAL_UNITS
from .constants import SI_UNITS


def validate_grain_type(grain_type):
    if grain_type in GRAIN_TYPE_LIST:
        return grain_type
    raise Exception("Unkown grain type '{}', must use {}".format(
        grain_type, ', '.join(GRAIN_TYPE_LIST)))


def validate_hop_type(hop_type):
    if hop_type in HOP_TYPE_LIST:
        return hop_type
    raise Exception("Unkown hop type '{}', must use {}".format(
        hop_type, ', '.join(HOP_TYPE_LIST)))


def validate_percentage(percent):
    if 0.0 <= percent <= 1.0:
        return percent
    raise Exception("Percentage values should be in decimal format")


def validate_units(units):
    if units in [IMPERIAL_UNITS, SI_UNITS]:
        return units
    raise Exception("Unkown units '{}', must use {} or {}".format(
        units, IMPERIAL_UNITS, SI_UNITS))


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


def validate_optional_fields(data, optional_fields, data_field='data'):
    """
    Validate fields which are optional as part of the data.

    data: a python dict
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
