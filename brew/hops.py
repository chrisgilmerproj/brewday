# -*- coding: utf-8 -*-
import json
import sys
import textwrap

from .constants import HOP_TYPE_PELLET
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import MG_PER_OZ
from .constants import OZ_PER_MG
from .constants import SI_TYPES
from .constants import SI_UNITS
from .constants import WEIGHT_TOLERANCE
from .utilities.hops import HopsUtilizationGlennTinseth
from .validators import validate_hop_type
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units

__all__ = [u'Hop', u'HopAddition']


class Hop(object):
    """
    A representation of a type of Hop.
    """

    def __init__(self, name,
                 percent_alpha_acids=None):
        """
        :param str name: The name of the hop
        :param float percent_alpha_acids: The percent alpha acids in the hop
        :raises Exception: If percent_alpha_acids is not provided
        """
        self.name = name
        if percent_alpha_acids is None:
            raise Exception(u"Must provide percent alpha acids")
        self.percent_alpha_acids = validate_percentage(percent_alpha_acids)

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return u"{0}, alpha {1:0.1%}".format(self.name.capitalize(),
                                             self.percent_alpha_acids)

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.name)
        if self.percent_alpha_acids:
            out = u"{0}, percent_alpha_acids={1}".format(
                out, self.percent_alpha_acids)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.name == other.name) and \
           (self.percent_alpha_acids == other.percent_alpha_acids):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {u'name': self.name,
                u'percent_alpha_acids': round(self.percent_alpha_acids, 3),
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def format(self):
        msg = textwrap.dedent(u"""\
                {name} Hops
                -----------------------------------
                Alpha Acids:  {percent_alpha_acids:0.1%}""".format(
            **self.to_dict()))
        return msg


class HopAddition(object):
    """
    A representation of the Hop as added to a Recipe.
    """

    def __init__(self, hop,
                 weight=None,
                 boil_time=None,
                 hop_type=HOP_TYPE_PELLET,
                 utilization_cls=HopsUtilizationGlennTinseth,
                 utilization_cls_kwargs=None,
                 units=IMPERIAL_UNITS):
        """
        :param Hop hop: The Hop object
        :param float weight: The weight of the hop addition
        :param float boil_time: The amount of time the hop is boiled
        :param float hop_type: The type of the hop being used
        :param HopsUtilization utilization_cls: The utilization class used for calculation
        :param dict utilization_cls_kwargs: The kwargs to initialize the utilization_cls object
        :param str units: The units
        """  # noqa
        self.hop = hop
        self.weight = weight
        self.boil_time = boil_time
        self.hop_type = validate_hop_type(hop_type)
        self.utilization_cls_kwargs = utilization_cls_kwargs or {}
        self.utilization_cls = utilization_cls(self, **self.utilization_cls_kwargs)  # noqa

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

        :return: Hop Addition in new unit type
        :rtype: HopAddition
        """
        if self.units == IMPERIAL_UNITS:
            weight = self.weight * MG_PER_OZ
            units = SI_UNITS
        elif self.units == SI_UNITS:
            weight = self.weight * OZ_PER_MG
            units = IMPERIAL_UNITS
        return HopAddition(self.hop,
                           weight=weight,
                           boil_time=self.boil_time,
                           utilization_cls_kwargs={u'units': units},
                           units=units)

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return u"{hop}, {weight} {weight_small}, {boil_time} min, {hop_type}".format(  # noqa
                hop=self.hop,
                weight=self.weight,
                boil_time=self.boil_time,
                hop_type=self.hop_type,
                **self.types)

    def __repr__(self):
        out = u"{0}({1}".format(type(self).__name__, repr(self.hop))
        if self.weight:
            out = u"{0}, weight={1}".format(out, self.weight)
        if self.boil_time:
            out = u"{0}, boil_time={1}".format(out, self.boil_time)
        if self.hop_type:
            out = u"{0}, hop_type='{1}'".format(out, self.hop_type)
        if self.utilization_cls:
            out = u"{0}, utilization_cls={1}".format(out, type(self.utilization_cls).__name__)  # noqa
        if self.utilization_cls_kwargs:
            out = u"{0}, utilization_cls_kwargs={1}".format(out, str(self.utilization_cls_kwargs))  # noqa
        out = u"{0}, units='{1}'".format(out, self.units)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.hop == other.hop) and \
           (self.boil_time == other.boil_time) and \
           (abs(1.0 - self.weight / other.weight) < WEIGHT_TOLERANCE) and \
           (self.hop_type == other.hop_type) and \
           (self.units == other.units):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        hop_data = self.hop.to_dict()
        return {u'name': hop_data.pop(u'name'),
                u'data': hop_data,
                u'weight': round(self.weight, 2),
                u'boil_time': round(self.boil_time, 1),
                u'hop_type': self.hop_type,
                u'utilization_cls': str(self.utilization_cls),
                u'utilization_cls_kwargs': self.utilization_cls_kwargs,
                u'units': self.units,
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, hop_data):
        required_fields = [(u'name', str),
                           (u'weight', float),
                           (u'boil_time', float),
                           ]
        optional_fields = [(u'percent_alpha_acids', float),
                           (u'hop_type', str),
                           (u'units', str),
                           ]
        validate_required_fields(hop_data, required_fields)
        validate_optional_fields(hop_data, optional_fields)

    def format(self):
        kwargs = {}
        kwargs.update(self.to_dict())
        kwargs.update(self.types)
        msg = textwrap.dedent(u"""\
                {name} Addition
                -----------------------------------
                Hop Type:     {hop_type}
                AA %:         {data[percent_alpha_acids]:0.1%}
                Weight:       {weight:0.2f} {weight_small}
                Boil Time:    {boil_time:0.1f} min""".format(
            **kwargs))
        return msg

    def get_ibus(self, sg, final_volume):
        """
        Get the IBUs

        :param float sg: The specific gravity of the wort
        :param float final_volume: The final volume of the wort
        :return: The IBUs of the wort
        :rtype: float
        """
        return self.utilization_cls.get_ibus(sg, final_volume)

    def get_alpha_acid_units(self):
        """
        Get Alpha Acid Units

        :return: alpha acid units
        :rtype: float
        """
        alpha_acids = self.hop.percent_alpha_acids * 100
        if self.units == IMPERIAL_UNITS:
            return self.weight * alpha_acids
        elif self.units == SI_UNITS:
            return self.weight * OZ_PER_MG * alpha_acids
