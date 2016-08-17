import json
import textwrap

from .constants import HOP_TYPE_PELLET
from .constants import HOPS_CONSTANT_IMPERIAL
from .constants import HOPS_CONSTANT_SI
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import MG_PER_OZ
from .constants import OZ_PER_MG
from .constants import SI_TYPES
from .constants import SI_UNITS
from .utilities.hops import HopsUtilizationGlennTinseth
from .validators import validate_hop_type
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units


class Hop(object):

    def __init__(self, name,
                 percent_alpha_acids=None):
        self.name = name
        self.percent_alpha_acids = validate_percentage(percent_alpha_acids)

    def __str__(self):
        return "{0}, alpha {1}%".format(self.name.capitalize(),
                                        self.percent_alpha_acids)

    def __repr__(self):
        out = "{0}('{1}'".format(type(self).__name__, self.name)
        if self.percent_alpha_acids:
            out = "{0}, percent_alpha_acids={1}".format(
                out, self.percent_alpha_acids)
        out = "{0})".format(out)
        return out

    def to_dict(self):
        return {'name': self.name,
                'percent_alpha_acids': round(self.percent_alpha_acids, 2),
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def format(self):
        msg = textwrap.dedent("""\
                {name} Hops
                -----------------------------------
                Alpha Acids:  {percent_alpha_acids} %""".format(
            **self.to_dict()))
        return msg


class HopAddition(object):

    def __init__(self, hop,
                 weight=None,
                 boil_time=None,
                 hop_type=HOP_TYPE_PELLET,
                 utilization_cls=HopsUtilizationGlennTinseth,
                 utilization_cls_kwargs=None,
                 units=IMPERIAL_UNITS):
        self.hop = hop
        self.weight = weight
        self.boil_time = boil_time
        self.hop_type = validate_hop_type(hop_type)
        self.utilization_cls_kwargs = utilization_cls_kwargs or {}
        self.utilization_cls = utilization_cls(self, **self.utilization_cls_kwargs)  # nopep8

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
            weight = self.weight * MG_PER_OZ
            units = SI_UNITS
        elif self.units == SI_UNITS:
            weight = self.weight * OZ_PER_MG
            units = IMPERIAL_UNITS
        return HopAddition(self.hop,
                           weight=weight,
                           boil_time=self.boil_time,
                           utilization_cls_kwargs={'units': units},
                           units=units)

    def __str__(self):
        return "{hop}, {weight} {weight_small}, {boil_time} min, {hop_type}".format(  # nopep8
                hop=self.hop,
                weight=self.weight,
                boil_time=self.boil_time,
                hop_type=self.hop_type,
                **self.types)

    def __repr__(self):
        out = "{0}({1}".format(type(self).__name__, repr(self.hop))
        if self.weight:
            out = "{0}, weight={1}".format(out, self.weight)
        if self.boil_time:
            out = "{0}, boil_time={1}".format(out, self.boil_time)
        if self.hop_type:
            out = "{0}, hop_type='{1}'".format(out, self.hop_type)
        if self.utilization_cls:
            out = "{0}, utilization_cls={1}".format(out, type(self.utilization_cls).__name__)  # nopep8
        if self.utilization_cls_kwargs:
            out = "{0}, utilization_cls_kwargs={1}".format(out, self.utilization_cls_kwargs)  # nopep8
        if self.units:
            out = "{0}, units='{1}'".format(out, self.units)
        out = "{0})".format(out)
        return out

    def to_dict(self):
        hop_data = self.hop.to_dict()
        return {'name': hop_data.pop('name'),
                'data': hop_data,
                'weight': round(self.weight, 2),
                'boil_time': round(self.boil_time, 1),
                'hop_type': self.hop_type,
                'utilization_cls': str(self.utilization_cls),
                'utilization_cls_kwargs': self.utilization_cls_kwargs,
                'units': self.units,
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, hop_data):
        required_fields = [('name', str),
                           ('weight', float),
                           ('boil_time', float),
                           ]
        optional_fields = [('percent_alpha_acids', float),
                           ('hop_type', str),
                           ('units', str),
                           ]
        validate_required_fields(hop_data, required_fields)
        validate_optional_fields(hop_data, optional_fields)

    def format(self):
        kwargs = {}
        kwargs.update(self.to_dict())
        kwargs.update(self.types)
        msg = textwrap.dedent("""\
                {name} Addition
                -----------------------------------
                Hop Type:     {hop_type}
                AA %:         {data[percent_alpha_acids]:0.2f} %
                Weight:       {weight:0.2f} {weight_small}
                Boil Time:    {boil_time:0.1f} min""".format(
            **kwargs))
        return msg

    def get_ibus(self, sg, final_volume):
        return self.utilization_cls.get_ibus(sg, final_volume)

    def get_alpha_acid_units(self):
        """
        Alpha Acid Units

        Defined as ounces of hops * alpha acids
        """
        alpha_acids = self.hop.percent_alpha_acids * 100
        if self.units == IMPERIAL_UNITS:
            return self.weight * alpha_acids
        elif self.units == SI_UNITS:
            return self.weight * OZ_PER_MG * alpha_acids

    def get_hops_weight(self, sg, target_ibu, final_volume,
                        percent_contribution):
        """
        Weight of Hops
        IBUs or International Bittering Units measures a bitterness unit for hops.
        IBUs are the measurement in parts per million (ppm) of iso-alpha acids
        in the beer.   For example, an IPA with 75 IBUs has 75 milligrams of
        isomerized alpha acids per liter. The equation used to calculate the
        weight of hops for the boil is as follows.

        Ounces hops = (IBU Target)(galbeer)(IBU%) / (%a-acid)(%Utilization)(7489)

        The IBU target equals the total bitterness for the beer.  (e.g. an IPA
        may have an IBU target of 75 IBUs)  The percent IBU is equal to the
        percent of IBUs from each hop addition.  You may wish for your first hop
        addition to contribute 95% of the total IBUs.  This would make your
        IBU% 95%.  The %a-acid is the amount of alpha acid in the hops and can
        be found on the hop packaging.  The % Utilization is a measurement of
        the percentage of alpha acid units that will isomerize in the boil.
        The following chart outlines the typical utilizations and hop boil times.

        60 min = 30% utilization
        30 min = 15%
        5   min = 2.5%

        The 7489 is a conversion factor and used to cancel the units in the
        equation, converting oz/gallon to mg/l. For the hops equation, the
        units for the % must be expressed in decimal form.  (e.g. 10%= .10)

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        # nopep8
        """
        validate_percentage(percent_contribution)

        hops_constant = HOPS_CONSTANT_IMPERIAL
        if self.units == SI_UNITS:
            hops_constant = HOPS_CONSTANT_SI

        utilization = self.utilization_cls.get_percent_utilization(
            sg, self.boil_time)

        num = (target_ibu * final_volume)
        den = (utilization * self.hop.percent_alpha_acids * hops_constant)
        return num / den * percent_contribution
