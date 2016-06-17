from .constants import IMPERIAL_UNITS
from .constants import SI_UNITS


def validate_percentage(percent):
    if 0.0 <= percent <= 1.0:
        return percent
    else:
        raise Exception("Percentage values should be in decimal format")


def validate_units(units):
    if units in [IMPERIAL_UNITS, SI_UNITS]:
        return units
    else:
        raise Exception("Unkown units '{}', must use {} or {}".format(
            units, IMPERIAL_UNITS, SI_UNITS))
