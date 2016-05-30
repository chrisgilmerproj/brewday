import string
import textwrap


class Grain(object):

    def __init__(self, name=None,
                 short_name=None,
                 color=None,
                 hot_water_extract=None,
                 percent_extract=None):
        self.name = name
        self.short_name = short_name or name
        self.color = color
        self.hot_water_extract = hot_water_extract
        self.percent_extract = percent_extract

    def __str__(self):
        return self.name

    def format(self):
        msg = textwrap.dedent("""{0} Grain
                                 {1}
                                 Color:             {2} degL
                                 Hot Water Extract: {3}
                                 Extract:           {4} %""".format(
                                     string.capwords(self.name),
                                     '-' * (len(self.name) + 6),
                                     self.color,
                                     self.hot_water_extract,
                                     self.percent_extract))
        return msg

    @classmethod
    def get_dry_to_liquid_malt_weight(cls, malt):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return malt * 1.25

    @classmethod
    def get_liquid_to_dry_malt_weight(cls, malt):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return malt * 1.0 / 1.25

    @classmethod
    def get_grain_to_liquid_malt_weight(cls, grain):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return grain * 0.75

    @ classmethod
    def get_liquid_malt_to_grain_weight(cls, malt):
        return malt / 0.75

    @classmethod
    def get_specialty_grain_to_liquid_malt_weight(cls, grain):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return grain * 0.89

    @classmethod
    def get_liquid_malt_to_specialty_grain_weight(cls, malt):
        return malt / 0.89
