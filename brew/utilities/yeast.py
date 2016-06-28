
from ..constants import IMPERIAL_UNITS
from ..constants import SI_UNITS
from .sugar import sg_to_gu

"""
1 billion cells growth per gram of extract (B/g) =
    13.3 Million cells / (ml * P)

Ale:    0.75 M / (ml * P) = 0.71  B / (G * SG)
Lager:  1.50 M / (ml * P) = 1.42  B / (G * SG)
Hybrid: 1.00 M / (ml * P) = 0.948 B / (G * SG)
"""


def pitch_rate_conversion(pitch_rate, units=IMPERIAL_UNITS):
    if units == IMPERIAL_UNITS:
        pass
    elif units == SI_UNITS:
        pass


def stir_plate_growth(initial_cells):
    """
    Stir Plage Growth

    initial_cells - Billion / gram extract (B/g)
    Sources:
    - http://braukaiser.com/blog/blog/2012/11/03/estimating-yeast-growth/
    """
    if initial_cells < 1.4:
        return 1.4
    if 1.4 <= initial_cells < 3.5:
        return 2.33 - 0.67 * initial_cells
    else:
        return 0.0


def get_inoculation_rate(growth_rate):
    """
    exponential: y = 3.4485e^-0.018x
                 R^2 = 0.9613

    power      : y = 29.466x^-0.905
                 R^2 = 0.9394

    Sources:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/
    - White, Chris, and Jamil Zainasheff. Yeast: The Practical Guide to Beer
      Fermentation. Boulder, CO: Brewers Publications, 2010. 139-44. Print.
    """


def get_growth_rate(inoculation_rate):
    """
    exponential: y = 132.79e^-0.758x
                 R^2 = 0.95234

    power      : y = 41.418x^-1.038
                 R^2 = 0.9394

    G = (12.54793776 * x^-0.4594858324) - 0.9994994906

    Sources:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/
    - White, Chris, and Jamil Zainasheff. Yeast: The Practical Guide to Beer
      Fermentation. Boulder, CO: Brewers Publications, 2010. 139-44. Print.
    """


def yeast_pitch_rate(original_gravity=1.050,
                     start_volume=5.0,
                     target_pitch_rate=1.42,
                     yeast_type='liquid',
                     cells_per_pack=100,
                     num_packs=1,
                     days_since_manufacture=30,
                     units=IMPERIAL_UNITS):
    """
    Determine yeast pitch rate

    original_gravity  - specific gravity of original beer
    start_volume      - volume of the batch
    target_pitch_rate - million cells / (ml * degP)
    yeast_type        - liquid, dry
    cells_per_pack    - Billions of cells
    num_packs         - how many in units
    days_since_manufacture - the older the yeast the less viable
    units             - imperial, metric

    Yeast Viability: lose 20% viability / month or 0.66% / day

    Sources:
    - http://beersmith.com/blog/2011/01/10/yeast-starters-for-home-brewing-beer-part-2/
    """  # nopep8
    gu = sg_to_gu(original_gravity)
    pitch_rate = target_pitch_rate * gu * start_volume

    viability = 1.0 - days_since_manufacture * (0.2 / 30.0)
    cells = cells_per_pack * num_packs * viability
    growth_rate = pitch_rate / cells
    return {'pitch_rate': round(pitch_rate, 2),
            'viability': round(viability, 2),
            'cells': round(cells, 2),
            'growth_rate': round(growth_rate, 2),
            }
