import math
import string


class Hop(object):

    def __init__(self, name=None,
                 short_name=None,
                 boil_time=None,
                 percent_alpha_acids=None,
                 percent_ibus=None,
                 percent_utilization=None,
                 percent_contribution=None):
        self.name = name
        self.short_name = short_name or name
        self.boil_time = boil_time
        self.percent_alpha_acids = percent_alpha_acids
        self.percent_ibus = percent_ibus
        self.percent_utilization = percent_utilization
        self.percent_contribution = percent_contribution

    def __repr__(self):
        return "{0}, alpha {1}%".format(self.name.capitalize(),
                                        self.percent_alpha_acids)

    def format(self):
        msg = """{0} Hops
{1}
Alpha Acids:  {2} %
IBUs:         {3} %
Utilization:  {4} %
Contribution: {5} %
Boil Time:    {6} min""".format(string.capwords(self.name),
                                '-' * (len(self.name) + 6),
                                self.percent_alpha_acids,
                                self.percent_ibus,
                                self.percent_utilization,
                                self.percent_contribution,
                                self.boil_time,)
        return msg

    @classmethod
    def get_bigness_factor(cls, sg):
        """
        Source: http://www.realbeer.com/hops/research.html
        """
        return 1.65 * 0.000125 ** (sg - 1)

    @classmethod
    def get_boil_time_factor(cls, boil_time):
        """
        Source: http://www.realbeer.com/hops/research.html
        """
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
        print title.center(size)
        print str('=' * len(title)).center(size)
        print
        print ' '.join([' ' * 4] + ['{0:7.3f}'.format(l/1000.0)
                       for l in gravity_list])
        print '-' * size
        for boil_time in boil_time_list:
            line = []
            line.append(str(boil_time).rjust(4))
            for sg in gravity_list:
                aau = cls.get_percent_utilization(sg / 1000.0, boil_time)
                line.append('{0:7.3f}'.format(aau))
            print ' '.join([item for item in line])
        print
