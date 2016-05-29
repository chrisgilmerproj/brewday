import math
import string

from .constants import HOPS_CONSTANT_US


def get_percent_ibus(hop, total_ibus):
    """Get the percentage the hops contributes to total ibus"""
    pass


class Hop(object):

    def __init__(self, name=None,
                 short_name=None,
                 percent_alpha_acids=None,
                 percent_utilization=None):
        self.name = name
        self.short_name = short_name or name
        self.percent_alpha_acids = percent_alpha_acids
        self.percent_utilization = percent_utilization

    def __repr__(self):
        return "{0}, alpha {1}%".format(self.name.capitalize(),
                                        self.percent_alpha_acids)

    def format(self):
        msg = """{0} Hops
{1}
Alpha Acids:  {2} %
Utilization:  {3} %""".format(string.capwords(self.name),
                              '-' * (len(self.name) + 6),
                              self.percent_alpha_acids,
                              self.percent_utilization)
        return msg


class HopsUtilization(object):
    """
    http://www.boondocks-brewing.com/hops
    """

    def __init__(self, hop_addition):
        self.hop_addition = hop_addition

    def get_ibus(self, sg, gallons_of_beer):
        utilization = self.get_percent_utilization(
                sg, self.hop_addition.boil_time)
        num = (self.hop_addition.weight * utilization *
               (self.hop_addition.hop.percent_alpha_acids / 100.0) *
               HOPS_CONSTANT_US)
        return num / (gallons_of_beer)

    @classmethod
    def get_percent_utilization(cls, sg, boil_time):
        raise NotImplementedError

    @classmethod
    def print_utilization_table(cls):
        """
        Percent Alpha Acid Utilization - Boil Time vs Wort Original Gravity

        Source: http://www.realbeer.com/hops/research.html
        """
        boil_time_list = range(0, 60, 3) + range(60, 130, 10)
        gravity_list = range(1030, 1140, 10)

        title = 'Percent Alpha Acid Utilization - ' \
                'Boil Time vs Wort Original Gravity'
        size = 92
        print(title.center(size))
        print(str('=' * len(title)).center(size))
        print('\n')
        print(' '.join([' ' * 4] + ['{0:7.3f}'.format(l/1000.0)
                       for l in gravity_list]))
        print('-' * size)
        for boil_time in boil_time_list:
            line = []
            line.append(str(boil_time).rjust(4))
            for sg in gravity_list:
                aau = cls.get_percent_utilization(sg / 1000.0, boil_time)
                line.append('{0:7.3f}'.format(aau))
            print(' '.join([item for item in line]))
        print('\n')


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


class HopAddition(object):

    def __init__(self, hop,
                 weight=None,
                 boil_time=None,
                 percent_contribution=None,
                 utilization_cls=HopsUtilizationJackieRager):
        self.hop = hop
        self.weight = weight
        self.boil_time = boil_time
        self.percent_contribution = percent_contribution
        self.utilization_cls = utilization_cls(self)

    def format(self):
        msg = """{0}
Weight:       {1} %
Contribution: {2} %
Boil Time:    {3} min""".format(self.hop,
                                self.weight,
                                self.percent_contirubtion,
                                self.boil_time)
        return msg

    def get_ibus(self, sg, gallons_of_beer):
        return self.utilization_cls.get_ibus(sg, gallons_of_beer)

    def get_hops_weight(self, target_ibu, gallons_of_beer):
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
        num = (target_ibu * gallons_of_beer *
               (self.percent_contribution / 100.0))
        den = ((self.hop.percent_alpha_acids / 100.0) *
               (self.hop.percent_utilization / 100.0) * HOPS_CONSTANT_US)
        return num / den
