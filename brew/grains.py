# -*- coding: utf-8 -*-
import json
import sys
import textwrap

from .constants import GRAIN_TYPE_CEREAL
from .constants import GRAIN_TYPE_DME
from .constants import GRAIN_TYPE_LME
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import KG_PER_POUND
from .constants import POUND_PER_KG
from .constants import PPG_CEREAL
from .constants import PPG_DME
from .constants import PPG_LME
from .constants import SI_TYPES
from .constants import SI_UNITS
from .constants import WEIGHT_TOLERANCE
from .exceptions import GrainException
from .utilities.malt import hwe_to_basis
from .utilities.malt import hwe_to_ppg
from .utilities.malt import ppg_to_hwe
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units

__all__ = [u'Grain', u'GrainAddition']


class Grain(object):
    """
    A representation of a type of grain.
    """

    def __init__(self, name,
                 color=None,
                 ppg=None,
                 hwe=None):
        """
        :param str name: The name of the grain
        :param float color: The color of the grain in SRM
        :param float ppg: The potential points per gallon
        :param float hwe: The hot water extract value
        :raises GrainException: If color is not provided
        :raises GrainException: If ppg or hwe is not provided
        :raises GrainException: If both ppg and hwe are provided
        """
        self.name = name
        if color is None:
            raise GrainException(u"{}: Must provide color value".format(
                self.name))
        self.color = float(color)
        if ppg and hwe:
            raise GrainException(u"{}: Cannot provide both ppg and hwe".format(
                self.name))
        if ppg:
            self.ppg = float(ppg)
            self.hwe = ppg_to_hwe(self.ppg)
        elif hwe:
            self.hwe = float(hwe)
            self.ppg = hwe_to_ppg(self.hwe)
        else:
            raise GrainException(u"{}: Must provide ppg or hwe".format(
                self.name))

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return self.name

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.name)
        if self.color:
            out = u"{0}, color={1}".format(out, self.color)
        if self.hwe:
            out = u"{0}, hwe={1}".format(out,
                                         round(self.hwe, 2))
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # Short name does not need to match
        if (self.name == other.name) and \
           (self.ppg == other.ppg) and \
           (self.color == other.color):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {u'name': self.name,
                u'color': round(self.color, 1),
                u'ppg': round(self.ppg, 2),
                u'hwe': round(self.hwe, 2),
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def format(self):
        msg = textwrap.dedent(u"""\
                {name} Grain
                -----------------------------------
                Color:             {color} degL
                PPG:               {ppg:0.2f}
                Hot Water Extract: {hwe:0.2f}""".format(
            **self.to_dict()))
        return msg

    def get_working_yield(self, brew_house_yield):
        """
        Get Working Yield

        :param float brew_house_yield: The Percent Brew House Yield
        :return: The working yield
        :rtype: float
        """
        validate_percentage(brew_house_yield)
        return (hwe_to_basis(self.hwe) *
                brew_house_yield)

    def convert_to_cereal(self, ppg=None):
        if not ppg:
            raise GrainException(u'Must provide PPG to convert to cereal')
        return Grain(self.name, color=self.color, ppg=ppg)

    def convert_to_lme(self, ppg=PPG_LME):
        return Grain(self.name, color=self.color, ppg=ppg)

    def convert_to_dme(self, ppg=PPG_DME):
        return Grain(self.name, color=self.color, ppg=ppg)


class GrainAddition(object):
    """
    A representation of the grain as added to a Recipe.
    """

    def __init__(self, grain,
                 weight=None,
                 grain_type=GRAIN_TYPE_CEREAL,
                 units=IMPERIAL_UNITS):
        """
        :param Grain grain: The Grain object
        :param float weight: The weight of the grain addition
        :param str grain_type: The type of the grain being used
        :param str units: The units
        """
        self.grain = grain
        self.weight = weight
        self.grain_type = grain_type

        # Manage units
        self.set_units(units)

    def set_units(self, units):
        """
        Set the units and unit types

        :param str units: The units
        """
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def change_units(self):
        """
        Change units of the class from one type to the other

        :return: Grain Addition in new unit type
        :rtype: GrainAddition
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
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return u"{grain}, weight {weight} {weight_large}".format(
            grain=self.grain,
            weight=self.weight,
            **self.types)

    def __repr__(self):
        out = u"{0}({1}".format(type(self).__name__, repr(self.grain))
        if self.weight:
            out = u"{0}, weight={1}".format(out, self.weight)
        if self.grain_type:
            out = u"{0}, grain_type='{1}'".format(out, self.grain_type)
        out = u"{0}, units='{1}'".format(out, self.units)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (abs(1.0 - self.weight / other.weight) < WEIGHT_TOLERANCE) and \
           (self.grain_type == other.grain_type) and \
           (self.units == other.units) and \
           (self.grain == other.grain):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_cereal_weight(self, ppg=PPG_CEREAL):
        """
        Get the weight of the addition in cereal weight

        :param float ppg: The potential points per gallon
        :return: Cereal weight
        :rtype: float
        """
        return self.convert_to_cereal(ppg=ppg).weight

    def get_lme_weight(self):
        """
        Get the weight of the addition in Liquid Malt Extract weight

        :return: LME weight
        :rtype: float
        """
        return self.convert_to_lme().weight

    def get_dme_weight(self):
        """
        Get the weight of the addition in Dry Malt Extract weight

        :return: Dry weight
        :rtype: float
        """
        return self.convert_to_dme().weight

    def get_weight_map(self):
        """
        Get map of grain weights by type

        :return: Grain weights
        :rtype: dict
        """
        return {
            u'grain_weight': round(self.get_cereal_weight(), 2),
            u'lme_weight': round(self.get_lme_weight(), 2),
            u'dry_weight': round(self.get_dme_weight(), 2),
        }

    def convert_to_cereal(self, ppg=None, brew_house_yield=1.0):
        """
        Convert Grain Addition to GRAIN_TYPE_CEREAL

        :param float ppg: The potential points per gallon
        :param float brew_house_yield: The brew house yield as a percentage
        :return: GrainAddition of type GRAIN_TYPE_CEREAL
        :rtype: GrainAddition
        """
        if self.grain_type == GRAIN_TYPE_CEREAL:
            return self
        if not ppg:
            raise GrainException('Must provide PPG to convert to cereal')

        validate_percentage(brew_house_yield)
        new_grain = self.grain.convert_to_cereal(ppg=ppg)
        ppg_factor = self.grain.ppg / new_grain.ppg

        # When converting away from cereal BHY works in reverse
        weight = self.weight * ppg_factor / brew_house_yield
        return GrainAddition(
            new_grain,
            weight=weight,
            grain_type=GRAIN_TYPE_CEREAL,
            units=self.units)

    def convert_to_lme(self, ppg=PPG_LME, brew_house_yield=1.0):
        """
        Convert Grain Addition to GRAIN_TYPE_LME

        :param float ppg: The potential points per gallon
        :param float brew_house_yield: The brew house yield as a percentage
        :return: GrainAddition of type GRAIN_TYPE_LME
        :rtype: GrainAddition
        """
        if self.grain_type == GRAIN_TYPE_LME:
            return self

        # BHY applies to cereal grains
        validate_percentage(brew_house_yield)
        if self.grain_type == GRAIN_TYPE_DME:
            brew_house_yield = 1.0
        new_grain = self.grain.convert_to_lme(ppg=ppg)
        ppg_factor = self.grain.ppg / new_grain.ppg
        weight = self.weight * ppg_factor * brew_house_yield
        return GrainAddition(
            new_grain,
            weight=weight,
            grain_type=GRAIN_TYPE_LME,
            units=self.units)

    def convert_to_dme(self, ppg=PPG_DME, brew_house_yield=1.0):
        """
        Convert Grain Addition to GRAIN_TYPE_DME

        :param float ppg: The potential points per gallon
        :param float brew_house_yield: The brew house yield as a percentage
        :return: GrainAddition of type GRAIN_TYPE_DME
        :rtype: GrainAddition
        """
        if self.grain_type == GRAIN_TYPE_DME:
            return self

        # BHY applies to cereal grains
        validate_percentage(brew_house_yield)
        if self.grain_type == GRAIN_TYPE_LME:
            brew_house_yield = 1.0
        new_grain = self.grain.convert_to_dme(ppg=ppg)
        ppg_factor = self.grain.ppg / new_grain.ppg
        weight = self.weight * ppg_factor * brew_house_yield
        return GrainAddition(
            new_grain,
            weight=weight,
            grain_type=GRAIN_TYPE_DME,
            units=self.units)

    @property
    def gu(self):
        return self.get_gravity_units()

    def get_gravity_units(self):
        """
        Get the gravity units for the Grain Addition
        :return: Gravity Units as PPG or HWE depending on units
        :rtype: float
        """
        # Pick the attribute based on units
        if self.units == IMPERIAL_UNITS:
            attr = u'ppg'
        if self.units == SI_UNITS:
            attr = u'hwe'

        return getattr(self.grain, attr) * self.weight

    def to_dict(self):
        grain_data = self.grain.to_dict()
        return {u'name': grain_data.pop('name'),
                u'data': grain_data,
                u'weight': round(self.weight, 2),
                u'grain_type': self.grain_type,
                u'units': self.units,
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, grain_data):
        required_fields = [(u'name', str),
                           (u'weight', float),
                           ]
        optional_fields = [(u'color', (int, float)),
                           (u'ppg', (int, float)),
                           (u'hwe', (int, float)),
                           (u'grain_type', str),
                           (u'units', str),
                           ]
        validate_required_fields(grain_data, required_fields)
        validate_optional_fields(grain_data, optional_fields)

    def format(self):
        kwargs = {}
        kwargs.update(self.to_dict())
        kwargs.update(self.types)
        msg = textwrap.dedent(u"""\
                {name} Addition
                -----------------------------------
                Grain Type:        {grain_type}
                Weight:            {weight:0.2f} {weight_large}""".format(
            **kwargs))
        return msg
