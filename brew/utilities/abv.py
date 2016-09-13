from ..constants import ALCOHOL_SPECIFIC_GRAVITY
from .sugar import apparent_extract_to_real_extract


__all__ = [
    'apparent_attenuation',
    'real_attenuation',
    'real_attenuation_from_apparent_extract',
    'alcohol_by_volume_standard',
    'alcohol_by_volume_alternative',
    'alcohol_by_weight',
]


def apparent_attenuation(original_extract, apparent_extract):
    return (original_extract - apparent_extract) / original_extract


def real_attenuation(original_extract, real_extract):
    return (original_extract - real_extract) / original_extract


def real_attenuation_from_apparent_extract(original_extract, apparent_extract):
    real_extract = apparent_extract_to_real_extract(original_extract,
                                                    apparent_extract)
    return real_attenuation(original_extract, real_extract)


def alcohol_by_volume_standard(og, fg):
    """
    Alcohol by Volume Standard Calculation

    Most brewing sites use this basic formula:

    ABV = (og - fg) * 131.25

    This equation was created before the computer age.  It is easy to do by
    hand, and over time became the accepted formula for home brewers!

    Variations on this equation which report within tenths of each other
    come from The Joy of Homebrewing Method by Charlie Papazian, Bee Lee's
    Method, Beer Advocate Method. Some variations use 131 instead of 131.25.
    The resulting difference is pretty minor.

    Source:
    - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    - http://www.brewmorebeer.com/calculate-percent-alcohol-in-beer/

      46.07 g/mol C2H6O       1.0
     ------------------- x -------- * 100 * (og - fg)
      44.0095 g/mol CO2     0.7936
    """  # nopep8
    ABV_CONST = 131.25
    return (og - fg) * ABV_CONST / 100.0


def alcohol_by_volume_alternative(og, fg):
    """
    Alcohol by Volume Alternative Calculation

    Alternate Formula:

    A more complex equation which attempts to provide greater accuracy at higher gravities is:

    ABV =(76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)

    The alternate equation reports a higher ABV for higher gravity beers.
    This equation is just a different take on it. Scientists rarely agree
    when it comes to equations. There will probably be another equation for
    ABV down the road.

    The complex formula, and variations on it come from
    Ritchie Products Ltd, (Zymurgy, Summer 1995, vol. 18, no. 2)
    -Michael L. Hall's article Brew by the Numbers: Add Up What's in Your
    Beer, and Designing Great Beers by Daniels.

    Source:
    - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    """  # nopep8
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794) / 100.0


def alcohol_by_weight(abv):
    """
    Alcohol by Weight from ABV
    """
    return abv * ALCOHOL_SPECIFIC_GRAVITY
