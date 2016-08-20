import math

from ..constants import HOP_TYPE_PELLET
from ..constants import HOP_UTILIZATION_SCALE_PELLET
from ..constants import HOPS_CONSTANT_IMPERIAL
from ..constants import HOPS_CONSTANT_SI
from ..constants import IMPERIAL_TYPES
from ..constants import IMPERIAL_UNITS
from ..constants import SI_TYPES
from ..constants import SI_UNITS
from ..validators import validate_units


__all__ = [
    'HopsUtilization',
    'HopsUtilizationJackieRager',
    'HopsUtilizationGlennTinseth',
]


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
    def format_utilization_table(cls):
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
        out.append(' '.join([' ' * 4] + ['{0:7.3f}'.format(l / 1000.0)
                   for l in gravity_list]))
        out.append('-' * table_size)
        for index, line in enumerate(table):
            boil_time = boil_time_list[index]
            out.append('{0} {1}'.format(
                str(boil_time).rjust(4),
                ' '.join(['{0:7.3f}'.format(aau) for aau in line])))
        return '\n'.join([o.rstrip() for o in out if o != '\n'])


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
            cgravity += (sg - 1.050) / 0.2
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
