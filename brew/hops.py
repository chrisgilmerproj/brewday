import json
import math
import textwrap

from .constants import HOP_TYPE_PELLET
from .constants import HOP_UTILIZATION_SCALE_PELLET
from .constants import HOPS_CONSTANT_IMPERIAL
from .constants import HOPS_CONSTANT_SI
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import MG_PER_OZ
from .constants import OZ_PER_MG
from .constants import SI_TYPES
from .constants import SI_UNITS
from .validators import validate_hop_type
from .validators import validate_percentage
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
                'percent_alpha_acids': self.percent_alpha_acids,
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


class HopsUtilization(object):
    """
    http://www.boondocks-brewing.com/hops
    """

    def __init__(self, hop_addition,
                 units=IMPERIAL_UNITS):
        self.hop_addition = hop_addition

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
            units = SI_UNITS
        elif self.units == SI_UNITS:
            units = IMPERIAL_UNITS
        return HopsUtilization(self.hop_addition,
                               units=units)

    def get_ibus(self, sg, final_volume):
        hops_constant = HOPS_CONSTANT_IMPERIAL
        if self.units == SI_UNITS:
            hops_constant = HOPS_CONSTANT_SI
        utilization = self.get_percent_utilization(
                sg, self.hop_addition.boil_time)
        # Utilization is 10% higher for pellet vs whole/plug
        if self.hop_addition.hop_type == HOP_TYPE_PELLET:
            utilization *= HOP_UTILIZATION_SCALE_PELLET
        num = (self.hop_addition.weight * utilization *
               self.hop_addition.hop.percent_alpha_acids *
               hops_constant)
        return num / final_volume

    @classmethod
    def get_percent_utilization(cls, sg, boil_time):
        raise NotImplementedError

    @classmethod
    def get_utilization_table(cls, gravity_list, boil_time_list, sig=3):
        table = []
        for boil_time in boil_time_list:
            line = []
            for sg in gravity_list:
                aau = cls.get_percent_utilization(sg / 1000.0, boil_time)
                line.append(round(aau, sig))
            table.append(line)
        return table

    @classmethod
    def print_utilization_table(cls):
        """
        Percent Alpha Acid Utilization - Boil Time vs Wort Original Gravity

        Source: http://www.realbeer.com/hops/research.html
        """
        gravity_list = list(range(1030, 1140, 10))
        boil_time_list = list(range(0, 60, 3)) + list(range(60, 130, 10))
        table = cls.get_utilization_table(gravity_list, boil_time_list)

        title = 'Percent Alpha Acid Utilization - ' \
                'Boil Time vs Wort Original Gravity'
        table_size = 92

        out = []
        out.append(title.center(table_size))
        out.append(str('=' * len(title)).center(table_size))
        out.append('\n')
        out.append(' '.join([' ' * 4] + ['{0:7.3f}'.format(l/1000.0)
                   for l in gravity_list]))
        out.append('-' * table_size)
        for index, line in enumerate(table):
            boil_time = boil_time_list[index]
            out.append('{0} {1}'.format(
                str(boil_time).rjust(4),
                ' '.join(['{0:7.3f}'.format(aau) for aau in line])))
        print('\n'.join(out))


class HopsUtilizationJackieRager(HopsUtilization):
    """
    Jackie Rager

    Best for extract and partial mash brewing.

    Source: http://www.rooftopbrew.net/ibu.php
    """

    def __str__(self):
        return "Jackie Rager"

    @classmethod
    def get_c_gravity(cls, sg):
        """
        Cgravity is a constant to adjust the boil size when dealing with
        specific gravity greater than 1.050 in the calculation of IBUs.
        """
        cgravity = 1
        if sg > 1.050:
            cgravity += (sg - 1.050)/0.2
        return cgravity

    @classmethod
    def get_percent_utilization(cls, sg, boil_time):
        num = (18.11 + 13.86 * math.tanh((boil_time - 31.32) / 18.27)) / 100.0
        return num / cls.get_c_gravity(sg)


class HopsUtilizationGlennTinseth(HopsUtilization):
    """
    Glenn Tinseth

    Best for all grain brewing.

    Source: http://www.realbeer.com/hops/research.html
    Source: http://www.rooftopbrew.net/ibu.php
    """

    def __str__(self):
        return "Glenn Tinseth"

    @classmethod
    def get_bigness_factor(cls, sg):
        return 1.65 * 0.000125 ** (sg - 1)

    @classmethod
    def get_boil_time_factor(cls, boil_time):
        return (1 - math.exp(-0.04 * boil_time)) / 4.15

    @classmethod
    def get_percent_utilization(cls, sg, boil_time):
        """
        The Bigness factor accounts for reduced utilization due to higher wort
        gravities. Use an average gravity value for the entire boil to account
        for changes in the wort volume.

        Bigness factor = 1.65 * 0.000125^(wort gravity - 1)

        The Boil Time factor accounts for the change in utilization due to
        boil time:

        Boil Time factor = (1 - e^(-0.04 * time in mins)) / 4.15

        Source: http://www.realbeer.com/hops/research.html
        """
        bigness_factor = cls.get_bigness_factor(sg)
        boil_time_factor = cls.get_boil_time_factor(boil_time)
        return bigness_factor * boil_time_factor


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
        return {'hop': self.hop.to_dict(),
                'weight': self.weight,
                'boil_time': self.boil_time,
                'hop_type': self.hop_type,
                'utilization_cls': str(self.utilization_cls),
                'utilization_cls_kwargs': self.utilization_cls_kwargs,
                'units': self.units,
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def format(self):
        kwargs = {}
        kwargs.update(self.to_dict())
        kwargs.update(self.types)
        msg = textwrap.dedent("""\
                {hop[name]} Addition
                -----------------------------------
                Weight:       {weight:0.2f} {weight_small}
                Boil Time:    {boil_time:0.2f} min
                Hop Type:     {hop_type}""".format(
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
