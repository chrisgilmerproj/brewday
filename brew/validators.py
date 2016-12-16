# -*- coding: utf-8 -*-
from .constants import GRAIN_TYPE_LIST
from .constants import HOP_TYPE_LIST
from .constants import IMPERIAL_UNITS
from .constants import SI_UNITS

__all__ = [
    u'validate_grain_type',
    u'validate_hop_type',
    u'validate_percentage',
    u'validate_units',
    u'validate_required_fields',
    u'validate_optional_fields',
]


def validate_grain_type(grain_type):
    """
    Validate a grain type

    :param str grain_type: Type of Grain
    :return: grain type
    :rtype: str
    :raises Exception: If grain type is unknown
    """
    if grain_type in GRAIN_TYPE_LIST:
        return grain_type
    raise Exception(u"Unkown grain type '{}', must use {}".format(
        grain_type, u', '.join(GRAIN_TYPE_LIST)))


def validate_hop_type(hop_type):
    """
    Validate a hop type

    :param str hop_type: Type of Grain
    :return: hop type
    :rtype: str
    :raises Exception: If hop type is unknown
    """
    if hop_type in HOP_TYPE_LIST:
        return hop_type
    raise Exception(u"Unkown hop type '{}', must use {}".format(
        hop_type, u', '.join(HOP_TYPE_LIST)))


def validate_percentage(percent):
    """
    Validate decimal percentage

    :param float percent: Percentage between 0.0 and 1.0
    :return: percentage
    :rtype: float
    :raises Exception: If decimal percentage not between 0.0 and 1.0
    """
    if 0.0 <= percent <= 1.0:
        return percent
    raise Exception(u"Percentage values should be in decimal format")


def validate_units(units):
    """
    Validate units

    :param str units: Unit type
    :return: units
    :rtype: str
    :raises Exception: If units is unknown
    """
    if units in [IMPERIAL_UNITS, SI_UNITS]:
        return units
    raise Exception(u"Unkown units '{}', must use {} or {}".format(
        units, IMPERIAL_UNITS, SI_UNITS))


def validate_required_fields(data, required_fields):
    """
    Validate fields which are required as part of the data.

    :param dict data: A python dictionary to check for required fields
    :param list(tuple) required_fields: Values and types to check for in data
    :raises Exception: Required field is missing from data
    :raises Exception: Required field is of the wrong type

    The format is a list of tuples where the first element is a string with
    a value that should be a key found in the data dict and
    where the second element is a python type or list/tuple of
    python types to check the field against.
    """
    for field, field_type in required_fields:
        if field not in data:
            raise Exception(u"Required field '{}' missing from data".format(
                field))
        if field_type == str:
            try:
                field_type = unicode
            except NameError:
                field_type = str
        if not isinstance(data[field], field_type):
            raise Exception(u"Required field '{}' is not of type '{}'".format(
                field, field_type))


def validate_optional_fields(data, optional_fields, data_field=u'data'):
    """
    Validate fields which are optional as part of the data.

    :param dict data: A python dictionary to check for required fields
    :param list(tuple) optional_fields: Values and types to check for in data
    :param str data_field: The key in the data dictionary containing the optional fields
    :raises Exception: Optional field is of the wrong type

    The format is a list of tuples where the first element is a string with
    a value that should be a key found in the data dict and
    where the second element is a python type or list/tuple of
    python types to check the field against.
    """  # noqa
    # If no optional data field present then return
    if data_field not in data:
        return
    for field, field_type in optional_fields:
        if field in data[data_field]:
            if field_type == str:
                try:
                    field_type = unicode
                except NameError:
                    field_type = str
            # With optional fields only check the type as they are overrides
            # and not all overrides need to be present
            if not isinstance(data[data_field][field], field_type):
                raise Exception(u"Optional field '{}' in '{}' is not of type '{}'".format(  # noqa
                    field, data_field, field_type))
