import json
import string
import textwrap

from .constants import GRAIN_TYPE_CEREAL
from .constants import GRAIN_TYPE_DME
from .constants import GRAIN_TYPE_LME
from .constants import GRAIN_TYPE_SPECIALTY
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import KG_PER_POUND
from .constants import POUND_PER_KG
from .constants import SI_TYPES
from .constants import SI_UNITS
from .utilities.malt import dry_to_liquid_malt_weight
from .utilities.malt import dry_malt_to_grain_weight
from .utilities.malt import grain_to_dry_malt_weight
from .utilities.malt import grain_to_liquid_malt_weight
from .utilities.malt import hwe_to_basis
from .utilities.malt import hwe_to_ppg
from .utilities.malt import liquid_malt_to_grain_weight
from .utilities.malt import liquid_to_dry_malt_weight
from .utilities.malt import specialty_grain_to_liquid_malt_weight
from .utilities.malt import ppg_to_hwe
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units


__all__ = ['Grain', 'GrainAddition']


class Grain(object):
    """
    A representation of a type of grain.
    """

    def __init__(self, name,
                 short_name=None,
                 color=None,
                 ppg=None,
                 hwe=None):
        """
        Color - The color of the grain in SRM
        PPG - The potential points points per gallon.
        Hot Water Extract - The international unit for the total soluble
            extract of a malt, based on specific gravity. HWE is measured as
            liter*degrees per kilogram, and is equivalent to
            points/pound/gallon (PPG) when you apply metric conversion factors
            for volume and weight. The combined conversion factor is
            8.3454 X PPG = HWE.
        """
        self.name = name
        self.short_name = short_name or name
        self.color = float(color)
        if ppg and hwe:
            raise Exception("Cannot provide both ppg and hwe")
        if ppg:
            self.ppg = float(ppg)
            self.hwe = ppg_to_hwe(self.ppg)
        elif hwe:
            self.hwe = float(hwe)
            self.ppg = hwe_to_ppg(self.hwe)

    def __str__(self):
        return string.capwords(self.name)

    def __repr__(self):
        out = "{0}('{1}'".format(type(self).__name__, self.name)
        if self.short_name:
            out = "{0}, short_name='{1}'".format(out, self.short_name)
        if self.color:
            out = "{0}, color={1}".format(out, self.color)
        if self.hwe:
            out = "{0}, hwe={1}".format(out,
                                                      round(self.hwe, 2))  # nopep8
        out = "{0})".format(out)
        return out

    def to_dict(self):
        return {'name': self.name,
                'short_name': self.short_name,
                'color': round(self.color, 1),
                'ppg': round(self.ppg, 2),
                'hwe': round(self.hwe, 2),
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def format(self):
        msg = textwrap.dedent("""\
                {name} Grain
                -----------------------------------
                Color:             {color} degL
                PPG:               {ppg:0.2f}
                Hot Water Extract: {hwe:0.2f}""".format(
            **self.to_dict()))
        return msg

    def get_working_yield(self, percent_brew_house_yield):
        """
        Working Yield
        Working Yield is the product of the Hot Water Extract multiplied by the
        Brew House Yield.  This product will provide the percent of extract
        collected from the malt.

        WY =    (HWE as-is)(BHY)
        """
        validate_percentage(percent_brew_house_yield)
        return (hwe_to_basis(self.hwe) *
                percent_brew_house_yield)


class GrainAddition(object):
    """
    A representation of the grain as added to a Recipe.
    """

    def __init__(self, grain,
                 weight=None,
                 grain_type=GRAIN_TYPE_CEREAL,
                 units=IMPERIAL_UNITS):
        """
        Weight - The weight of the grain to add
        Grain Type - The type of grain being used
        """
        self.grain = grain
        self.weight = weight
        self.grain_type = grain_type

        # Manage units
        self.set_units(units)

    def set_units(self, units):
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def change_units(self):
        """
        Change units from one type to the other return new instance
        """
        if self.units == IMPERIAL_UNITS:
            weight = self.weight * KG_PER_POUND
            units = SI_UNITS
        elif self.units == SI_UNITS:
            weight = self.weight * POUND_PER_KG
            units = IMPERIAL_UNITS
        return GrainAddition(self.grain,
                             weight=weight,
                             units=units)

    def __str__(self):
        return "{grain}, weight {weight} {weight_large}".format(
            grain=self.grain,
            weight=self.weight,
            **self.types)

    def __repr__(self):
        out = "{0}({1}".format(type(self).__name__, repr(self.grain))
        if self.weight:
            out = "{0}, weight={1}".format(out, self.weight)
        if self.grain_type:
            out = "{0}, grain_type='{1}'".format(out, self.grain_type)
        out = "{0})".format(out)
        return out

    def get_cereal_weight(self):
        """
        Get the weight of the addition in cereal weight
        """
        if self.grain_type == GRAIN_TYPE_CEREAL:
            return self.weight
        elif self.grain_type == GRAIN_TYPE_DME:
            return dry_malt_to_grain_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_LME:
            return liquid_malt_to_grain_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_SPECIALTY:
            return self.weight

    def get_lme_weight(self):
        """
        Get the weight of the addition in Liquid Malt Extract weight
        """
        if self.grain_type == GRAIN_TYPE_CEREAL:
            return grain_to_liquid_malt_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_DME:
            return dry_to_liquid_malt_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_LME:
            return self.weight
        elif self.grain_type == GRAIN_TYPE_SPECIALTY:
            return specialty_grain_to_liquid_malt_weight(self.weight)

    def get_dry_weight(self):
        """
        Get the weight of the addition in Dry Malt Extract weight
        """
        if self.grain_type == GRAIN_TYPE_CEREAL:
            return grain_to_dry_malt_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_DME:
            return self.weight
        elif self.grain_type == GRAIN_TYPE_LME:
            return liquid_to_dry_malt_weight(self.weight)
        elif self.grain_type == GRAIN_TYPE_SPECIALTY:
            lme = specialty_grain_to_liquid_malt_weight(self.weight)
            return liquid_to_dry_malt_weight(lme)

    def get_weight_map(self):
        return {
            'grain_weight': round(self.get_cereal_weight(), 2),
            'lme_weight': round(self.get_lme_weight(), 2),
            'dry_weight': round(self.get_dry_weight(), 2),
        }

    def to_dict(self):
        grain_data = self.grain.to_dict()
        return {'name': grain_data.pop('name'),
                'data': grain_data,
                'weight': round(self.weight, 2),
                'grain_type': self.grain_type,
                'units': self.units,
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, grain_data):
        required_fields = [('name', str),
                           ('weight', float),
                           ]
        optional_fields = [('color', (int, float)),
                           ('ppg', (int, float)),
                           ('hwe', (int, float)),
                           ('grain_type', str),
                           ('units', str),
                           ]
        validate_required_fields(grain_data, required_fields)
        validate_optional_fields(grain_data, optional_fields)

    def format(self):
        kwargs = {}
        kwargs.update(self.to_dict())
        kwargs.update(self.types)
        msg = textwrap.dedent("""\
                {name} Addition
                -----------------------------------
                Grain Type:        {grain_type}
                Weight:            {weight:0.2f} {weight_large}""".format(
            **kwargs))
        return msg
