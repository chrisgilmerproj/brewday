import string
import textwrap

from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import KG_PER_POUND
from .constants import POUND_PER_KG
from .constants import SI_TYPES
from .constants import SI_UNITS
from .utilities.malt import hwe_to_basis
from .validators import validate_percentage
from .validators import validate_units


class Grain(object):
    """
    Grain

    Color - The color of the grain in SRM

    Hot Water Extract - The international unit for the total soluble extract
    of a malt, based on specific gravity. HWE is measured as liter*degrees per
    kilogram, and is equivalent to points/pound/gallon (PPG) when you apply
    metric conversion factors for volume and weight. The combined conversion
    factor is 8.3454 X PPG = HWE.

    Percent Extract - The percentage this grain contributes to the beer recipe.
    """

    def __init__(self, name,
                 short_name=None,
                 color=None,
                 hot_water_extract=None):
        self.name = name
        self.short_name = short_name or name
        self.color = color
        self.hot_water_extract = hot_water_extract

    def __str__(self):
        return string.capwords(self.name)

    def __repr__(self):
        out = "{0}('{1}'".format(type(self).__name__, self.name)
        if self.short_name:
            out = "{0}, short_name='{1}'".format(out, self.short_name)
        if self.color:
            out = "{0}, color={1}".format(out, self.color)
        if self.hot_water_extract:
            out = "{0}, hot_water_extract={1}".format(out,
                                                      round(self.hot_water_extract, 2))  # nopep8
        out = "{0})".format(out)
        return out

    def format(self):
        msg = textwrap.dedent("""\
                {0} Grain
                {1}
                Color:             {2} degL
                Hot Water Extract: {3}""".format(
                    string.capwords(self.name),
                    '-' * (len(self.name) + 6),
                    self.color,
                    round(self.hot_water_extract, 2)))
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
        return (hwe_to_basis(self.hot_water_extract) *
                percent_brew_house_yield)


class GrainAddition(object):

    def __init__(self, grain,
                 weight=None,
                 units=IMPERIAL_UNITS):
        self.grain = grain
        self.weight = weight

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
        out = "{0})".format(out)
        return out

    def format(self):
        msg = textwrap.dedent("""\
                {grain} Addition
                ----------------
                Malt Bill:         {weight} {weight_large}""".format(
                    grain=self.grain,
                    weight=self.weight,
                    **self.types))
        return msg
