import math

from ..constants import GAL_PER_LITER
from ..constants import IMPERIAL_TYPES
from ..constants import IMPERIAL_UNITS
from ..constants import LITER_PER_GAL
from ..constants import OZ_PER_G
from ..constants import SI_TYPES
from ..constants import SI_UNITS
from ..validators import validate_units
from .sugar import plato_to_sg
from .sugar import sg_to_gu
from .sugar import sg_to_plato


__all__ = [
    'PITCH_RATE_MAP',
    'pitch_rate_conversion',
    'YeastModel',
    'KaiserYeastModel',
    'WhiteYeastModel',
]


"""
1 billion cells growth per gram of extract (B/g) =
    13.3 Million cells / (ml * P)

Ale:    0.75 M / ml / P = 0.71  B / G / SG
Lager:  1.50 M / ml / P = 1.42  B / G / SG
Hybrid: 1.00 M / ml / P = 0.948 B / G / SG
"""

# Pitch rate in M / ml / P
PITCH_RATE_MAP = {
    'MFG Recommended  (Ale, fresh yeast only)': 0.35,
    'MFG Recommended+ (Ale, fresh yeast only)': 0.55,
    'Pro Brewer (Ale, LG)': 0.75,
    'Pro Brewer (Ale)': 1.0,
    'Pro Brewer (Ale, HG)': 1.25,
    'Pro Brewer (Lager, LG)': 1.5,
    'Pro Brewer (Lager)': 1.75,
    'Pro Brewer (Lager, HG)': 2.0,
}


def pitch_rate_conversion(pitch_rate, units=IMPERIAL_UNITS):
    """
    Pitch Rate Conversion

    Input should be given in:
    Imperial: B / (Gal * GU)
    SI:       B / (L * P)

    Note: 1 M / (ml * P) == 1B / (L * P)
    """
    plato_per_gu = sg_to_gu(plato_to_sg(1))
    if units == IMPERIAL_UNITS:
        return pitch_rate * GAL_PER_LITER * plato_per_gu
    elif units == SI_UNITS:
        return pitch_rate * LITER_PER_GAL / plato_per_gu


class YeastModel(object):
    METHOD_TO_GROWTH_ADJ = {
        'no agitation': 0.0,
        'shaking': 0.0,
        'stir plate': 0.0,
    }

    def __init__(self, method, units=IMPERIAL_UNITS):
        if method not in self.METHOD_TO_GROWTH_ADJ.keys():
            raise Exception("Method '{}' not allowed for yeast model".format(
                method))
        self.method = method
        self.adjustment = self.METHOD_TO_GROWTH_ADJ[method]
        self.set_units(units)

    def set_units(self, units):
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def get_inoculation_rate(self, growth_rate):
        raise NotImplementedError

    def get_growth_rate(self, inoculation_rate):
        raise NotImplementedError

    def get_viability(self, days_since_manufacture):
        """
        Yeast viability drops 21% each month or 0.7% per day from the date of
        manufacture.  Assume linear change.
        """
        viability = 1.0 - days_since_manufacture * (0.21 / 30.0)
        if viability < 0:
            return 0.0
        return viability

    def get_yeast_pitch_rate(self,
                             original_gravity=1.050,
                             final_volume=5.0,
                             target_pitch_rate=1.42,
                             yeast_type='liquid',
                             cells_per_pack=100,
                             num_packs=1,
                             days_since_manufacture=30):
        """
        Determine yeast pitch rate

        original_gravity  - specific gravity of original beer
        final_volume      - volume of the batch post fermentation
        target_pitch_rate - million cells / (ml * degP)
        yeast_type        - liquid, dry
        cells_per_pack    - Billions of cells
        num_packs         - how many in units
        days_since_manufacture - the older the yeast the less viable
        units             - imperial, metric

        Yeast Viability: lose 20% viability / month or 0.66% / day

        Imperial: B / Gal / GU
        Metric:   M / ml  / Plato

        Sources:
        - http://beersmith.com/blog/2011/01/10/yeast-starters-for-home-brewing-beer-part-2/
        """  # nopep8
        viability = self.get_viability(days_since_manufacture)

        cells = cells_per_pack * num_packs * viability

        if self.units == IMPERIAL_UNITS:
            modifier = sg_to_gu(original_gravity)
        elif self.units == SI_UNITS:
            modifier = sg_to_plato(original_gravity)
        pitch_rate_as_is = cells / final_volume / modifier
        pitch_rate_cells = target_pitch_rate * final_volume * modifier

        if cells <= 0.0:
            required_growth_rate = 0.0
        else:
            required_growth_rate = pitch_rate_cells / cells

        return {'original_gravity': original_gravity,
                'final_volume': final_volume,
                'target_pitch_rate': target_pitch_rate,
                'viability': round(viability, 2),
                'cells': round(cells, 2),
                'pitch_rate_as_is': round(pitch_rate_as_is, 2),
                'pitch_rate_cells': round(pitch_rate_cells, 2),
                'cells_needed': round(pitch_rate_cells - cells, 2),
                'required_growth_rate': round(required_growth_rate, 2),
                'units': self.units,
                }

    def get_starter_volume(self,
                           available_cells,
                           starter_volume=2.0 * GAL_PER_LITER,
                           original_gravity=1.036):
        """
        Calculate the number of cells given a stater volume and gravity
        """
        GPL = 2.845833  # g/P/L grams of extract per point of gravity per liter of starter  # nopep8
        dme = GPL * sg_to_gu(original_gravity) * starter_volume  # in grams
        if self.units == IMPERIAL_UNITS:
            inoculation_rate = available_cells / (starter_volume * LITER_PER_GAL)  # nopep8
            dme = dme * OZ_PER_G * LITER_PER_GAL
        elif self.units == SI_UNITS:
            inoculation_rate = available_cells / starter_volume
        growth_rate = self.get_growth_rate(inoculation_rate)
        end_cell_count = available_cells * (growth_rate + 1)

        return {'available_cells': round(available_cells, 2),
                'starter_volume': round(starter_volume, 2),
                'original_gravity': original_gravity,
                'dme': round(dme, 2),
                'inoculation_rate': round(inoculation_rate, 2),
                'growth_rate': round(growth_rate, 2),
                'end_cell_count': round(end_cell_count, 2),
                'units': self.units,
                }

    def get_resulting_pitch_rate(self,
                                 starter_cell_count,
                                 original_gravity=1.036,
                                 final_volume=5.0):
        if self.units == IMPERIAL_UNITS:
            modifier = sg_to_gu(original_gravity)
        elif self.units == SI_UNITS:
            modifier = sg_to_plato(original_gravity)
        pitch_rate = starter_cell_count / final_volume / modifier
        return pitch_rate


class KaiserYeastModel(YeastModel):
    """
    Kaiser Yeast Model

    Only works for Stir Plage Growth

    Sources:
    - http://braukaiser.com/blog/blog/2012/11/03/estimating-yeast-growth/
    """
    METHOD_TO_GROWTH_ADJ = {
        'stir plate': 0.0,
    }

    def __init__(self, method='stir plate', units=IMPERIAL_UNITS):
        return super(KaiserYeastModel, self).__init__(method, units=units)

    def get_inoculation_rate(self, growth_rate):
        if 0 < growth_rate < 1.4:
            return (2.33 - growth_rate) / 0.67
        elif 1.4 <= growth_rate:
            return 1.4

    def get_growth_rate(self, initial_cells):
        """
        initial_cells - Billion / gram extract (B/g)
        """
        if initial_cells < 1.4:
            return 1.4 + self.adjustment
        elif 1.4 <= initial_cells < 3.5:
            return 2.33 - 0.67 * initial_cells + self.adjustment
        else:
            return 0.0 + self.adjustment


class WhiteYeastModel(YeastModel):
    """
    Sources:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/
    - White, Chris, and Jamil Zainasheff. Yeast: The Practical Guide to Beer
      Fermentation. Boulder, CO: Brewers Publications, 2010. 139-44. Print.
    """

    # Linear Regression Least Squares
    INOCULATION_CONST = [-0.999499, 12.547938, -0.459486]
    METHOD_TO_GROWTH_ADJ = {
        'no agitation': 0.0,
        'shaking': 0.5,
        'stir plate': 1.0,
    }

    def __init__(self, method='no agitation', units=IMPERIAL_UNITS):
        return super(WhiteYeastModel, self).__init__(method, units=units)

    def get_inoculation_rate(self, growth_rate):
        a, b, c = self.INOCULATION_CONST
        return 10 ** (math.log10(b / (growth_rate - a)) / -c)

    def get_growth_rate(self, inoculation_rate):
        """
        initial_cells - Billion / gram extract (B/g)

        G = (12.54793776 * x^-0.4594858324) - 0.9994994906
        """  # nopep8
        # if inoculation_rate > 200:
        #     raise Exception("Yeast will not grow at more than 200 M/ml")
        a, b, c = self.INOCULATION_CONST
        growth_rate = a + b * inoculation_rate ** c + self.adjustment
        # if growth_rate > 6:
        #     raise Exception("Model does not allow for growth greater than 6")
        return growth_rate
