import math
import string
import textwrap

from .constants import HOPS_CONSTANT_IMPERIAL
from .constants import HOPS_CONSTANT_SI
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import SI_TYPES
from .constants import SI_UNITS
from .validators import validate_percentage
from .validators import validate_units


def get_percent_ibus(hop, total_ibus):
    """Get the percentage the hops contributes to total ibus"""
    pass


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

    def format(self):
        msg = textwrap.dedent("""\
                {0} Hops
                {1}
                Alpha Acids:  {2} %""".format(
                    string.capwords(self.name),
                    '-' * (len(self.name) + 5),
                    self.percent_alpha_acids))
        return msg


class HopsUtilization(object):
    """
    http://www.boondocks-brewing.com/hops
    """

    def __init__(self, hop_addition,
                 units=IMPERIAL_UNITS):
        self.hop_addition = hop_addition
        self.units = validate_units(units)

    def get_ibus(self, sg, final_volume):
        hops_constant = HOPS_CONSTANT_IMPERIAL
        if self.units == SI_UNITS:
            hops_constant = HOPS_CONSTANT_SI
        utilization = self.get_percent_utilization(
                sg, self.hop_addition.boil_time)
        num = (self.hop_addition.weight * utilization *
               self.hop_addition.hop.percent_alpha_acids *
               hops_constant)
        return num / (final_volume)

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


# class HopsUtilizationMarkGaretz(HopsUtilization):
#
#     def __init__(self, hop_addition,
#                  final_volume=None,
#                  boil_volume=None,
#                  starting_gravity=None,
#                  desired_ibus=None,
#                  elevation=SEA_LEVEL,
#                  ):
#         self.hop_addition = hop_addition
#         self.final_volume = final_volume
#         self.boil_volume = boil_volume
#
#     def concentration_factor(self):
#         return self.final_volume / self.boil_volume
#
#     def boil_gravity(self):
#         cf = self.get_concentration_factor()
#         return (cf * (self.starting_gravity - 1)) + 1
#
#     def gravity_factor(self):
#         bg = self.boil_gravity()
#         return (bg - 1.050) / 0.2 + 1
#
#     def hopping_rate_factor(self):
#         cf = self.get_concentration_factor()
#         return ((cf * self.desired_ibus)/260) + 1
#
#     def temperature_factor(self, elevation):
#         """ elevation in feet """
#         return ((self.elevation / 550) * 0.02) + 1
#
#     def yeast_factor(self):
#         return 1
#
#     def pellet_factor(self):
#         return 1
#
#     def bag_factor(self):
#         return 1
#
#     def filter_factor(self):
#         return 1
#
#     def combined_adjustments(self):
#         gf = self.gravity_factor()
#         hf = self.hopping_rate_factor()
#         tf = self.temperature_factor()
#         yf = self.yeast_factor()
#         pf = self.pellet_factor()
#         bf = self.bag_factor()
#         ff = self.filter_factor()
#         return gf * hf * tf * yf * pf * bf * ff
#
#     def get_percent_utilization(self, sg, boil_time):
#         ca = self.combined_adjustments()
#         return 10000.0 / ca


# TODO: Hopville, Daniels, Mosher, Yooper


class HopAddition(object):

    def __init__(self, hop,
                 weight=None,
                 boil_time=None,
                 percent_contribution=None,
                 utilization_cls=HopsUtilizationJackieRager,
                 utilization_cls_kwargs=None,
                 units=IMPERIAL_UNITS):
        self.hop = hop
        self.weight = weight
        self.boil_time = boil_time
        self.percent_contribution = validate_percentage(percent_contribution)
        utilization_kwargs = utilization_cls_kwargs or {}
        self.utilization_cls = utilization_cls(self, **utilization_kwargs)

        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def __str__(self):
        return "{hop}, weight {weight} {weight_small}, boil time {boil_time} min".format(  # nopep8
                hop=self.hop,
                weight=self.weight,
                boil_time=self.boil_time,
                weight_small=self.types['weight_small'])

    def __repr__(self):
        out = "{0}({1}".format(type(self).__name__, repr(self.hop))
        out = "{0})".format(out)
        return out

    def format(self):
        msg = textwrap.dedent("""\
                {hop}
                ------------------------
                Weight:       {weight:0.2f} {weight_small}
                Contribution: {percent_contribution:0.2f} %
                Boil Time:    {boil_time:0.2f} min""".format(
                    hop=self.hop,
                    weight=self.weight,
                    percent_contribution=self.percent_contribution,
                    boil_time=self.boil_time,
                    weight_small=self.types['weight_small'],
                    ))
        return msg

    def get_ibus(self, sg, final_volume):
        return self.utilization_cls.get_ibus(sg, final_volume)

    def get_hops_weight(self, sg, target_ibu, final_volume):
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
        hops_constant = HOPS_CONSTANT_IMPERIAL
        if self.units == SI_UNITS:
            hops_constant = HOPS_CONSTANT_SI
        num = (target_ibu * final_volume *
               self.percent_contribution)
        den = (self.hop.percent_alpha_acids *
               self.utilization_cls.get_percent_utilization(
                   sg, self.boil_time) * hops_constant)
        return num / den
