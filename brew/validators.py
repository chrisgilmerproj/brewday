from .constants import HOP_TYPE_LIST
from .constants import IMPERIAL_UNITS
from .constants import SI_UNITS


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
