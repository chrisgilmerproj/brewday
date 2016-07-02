import math

from ..constants import GAL_PER_LITER
from ..constants import LITER_PER_GAL
from ..constants import IMPERIAL_UNITS
from ..constants import SI_UNITS
from .sugar import plato_to_sg
from .sugar import sg_to_gu
from .sugar import sg_to_plato

"""
1 billion cells growth per gram of extract (B/g) =
    13.3 Million cells / (ml * P)

Ale:    0.75 M / (ml * P) = 0.71  B / (G * SG)
Lager:  1.50 M / (ml * P) = 1.42  B / (G * SG)
Hybrid: 1.00 M / (ml * P) = 0.948 B / (G * SG)
"""


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

    def __init__(self, method):
        if method not in self.METHOD_TO_GROWTH_ADJ.keys():
            raise Exception("Method '{}' not allowed for yeast model".format(
                method))
        self.method = method
        self.adjustment = self.METHOD_TO_GROWTH_ADJ[method]

    def get_inoculation_rate(self, growth_rate):
        raise NotImplementedError

    def get_growth_rate(self, inoculation_rate):
        raise NotImplementedError

    def get_yeast_pitch_rate(self,
                             original_gravity=1.050,
                             final_volume=5.0,
                             target_pitch_rate=1.42,
                             yeast_type='liquid',
                             cells_per_pack=100,
                             num_packs=1,
                             days_since_manufacture=30,
                             units=IMPERIAL_UNITS):
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
        viability = 1.0 - days_since_manufacture * (0.2 / 30.0)
        cells = cells_per_pack * num_packs * viability

        if units == IMPERIAL_UNITS:
            modifier = sg_to_gu(original_gravity)
        elif units == SI_UNITS:
            modifier = sg_to_plato(original_gravity)
        pitch_rate_as_is = cells / final_volume / modifier
        pitch_rate_cells = target_pitch_rate * final_volume * modifier

        return {'original_gravity': original_gravity,
                'final_volume': final_volume,
                'target_pitch_rate': target_pitch_rate,
                'viability': round(viability, 2),
                'cells': round(cells, 2),
                'pitch_rate_as_is': round(pitch_rate_as_is, 2),
                'pitch_rate_cells': round(pitch_rate_cells, 2),
                }

    def get_starter_volume(self, pitch_rate, cells):
        growth_rate = pitch_rate / cells
        inoculation_rate = self.get_inoculation_rate(growth_rate)
        starter_volume = cells / inoculation_rate
        return {'growth_rate': round(growth_rate, 2),
                'inoculation_rate': round(inoculation_rate, 2),
                'starter_volume': round(starter_volume, 2),
                }


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

    def __init__(self, method='stir plate'):
        return super(KaiserYeastModel, self).__init__(method)

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
        'no agitation': 1.0,
        'shaking': 0.5,
        'stir plate': 0.0,
    }

    def __init__(self, method='stir plate'):
        return super(WhiteYeastModel, self).__init__(method)

    def get_inoculation_rate(self, growth_rate):
        a, b, c = self.INOCULATION_CONST
        return 10 ** (math.log10(b / (growth_rate - a))/-c)

    def get_growth_rate(self, inoculation_rate):
        """
        initial_cells - Billion / gram extract (B/g)

        G = (12.54793776 * x^-0.4594858324) - 0.9994994906
        """  # nopep8
        if inoculation_rate > 200:
            raise Exception("Yeast will not grow at more than 200 M/ml")
        a, b, c = self.INOCULATION_CONST
        growth_rate = a + b * inoculation_rate ** c - self.adjustment
        if growth_rate > 6:
            raise Exception("Model does not allow for growth greater than 6")
        return growth_rate
