# -*- coding: utf-8 -*-
from ..constants import ABV_CONST
from ..constants import ALCOHOL_SPECIFIC_GRAVITY
from .sugar import apparent_extract_to_real_extract

__all__ = [
    u'apparent_attenuation',
    u'real_attenuation',
    u'real_attenuation_from_apparent_extract',
    u'alcohol_by_volume_standard',
    u'final_gravity_from_abv_standard',
    u'alcohol_by_volume_alternative',
    u'alcohol_by_weight',
]


def apparent_attenuation(original_extract, apparent_extract):
    """
    Apparent Attenuation

    :param float original_extract: Original degrees Plato
    :param float apparent_extract: Apparent degrees Plato of finished beer
    :return: The percent of apparent attenuation
    :rtype: float

    Source:

    * Formula from Balling: De Clerck, Jean, A Textbook Of Brewing, Chapman & Hall Ltd., 1958
    * http://beersmith.com/blog/2010/09/07/apparent-and-real-attenuation-for-beer-brewers-part-1/
    * http://beersmith.com/blog/2010/09/14/apparent-and-real-attenuation-for-beer-brewers-part-2/
    """  # noqa
    return (original_extract - apparent_extract) / original_extract


def real_attenuation(original_extract, real_extract):
    """
    Real Attenuation

    :param float original_extract: Original degrees Plato
    :param float real_extract: Real degrees Plato of finished beer
    :return: The percent of real attenuation
    :rtype: float
    """
    return (original_extract - real_extract) / original_extract


def real_attenuation_from_apparent_extract(original_extract, apparent_extract):
    """
    Real Attenuation from Apparent Extract

    :param float original_extract: Original degrees Plato
    :param float apparent_extract: Apparent degrees Plato of finished beer
    :return: The percent of real attenuation
    :rtype: float
    """
    real_extract = apparent_extract_to_real_extract(original_extract,
                                                    apparent_extract)
    return real_attenuation(original_extract, real_extract)


def alcohol_by_volume_standard(og, fg):
    """
    Alcohol by Volume Standard Calculation

    :param float og: Original Gravity
    :param float fg: Final Gravity
    :return: Alcohol by Volume decimal percentage
    :rtype: float

    Most brewing sites use this basic formula:

    :math:`\\text{ABV} = \\big(\\text{og} - \\text{fg}\\big) \\times 131.25`

    This equation was created before the computer age.  It is easy to do by
    hand, and over time became the accepted formula for home brewers!

    Variations on this equation which report within tenths of each other
    come from The Joy of Homebrewing Method by Charlie Papazian, Bee Lee's
    Method, Beer Advocate Method. Some variations use 131 instead of 131.25.
    The resulting difference is pretty minor.

    Source:

    * http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    * http://www.brewmorebeer.com/calculate-percent-alcohol-in-beer/

    :math:`\\text{ABV} = \\frac{46.07 \\text{g/mol C2H6O}}{44.0095 \\text{g/mol CO2}} \\times \\frac{1.0}{0.7936} \\times 100 \\times (og - fg)`
    """  # noqa
    return (og - fg) * ABV_CONST / 100.0


def final_gravity_from_abv_standard(og, abv):
    """
    Final Gravity from ABV Standard

    :param float og: Original Gravity
    :param float abv: Alcohol by Volume decimal percentage
    :return: Final Gravity
    :rtype: float
    """
    return og - (abv * 100.0) / ABV_CONST


def alcohol_by_volume_alternative(og, fg):
    """
    Alcohol by Volume Alternative Calculation

    :param float og: Original Gravity
    :param float fg: Final Gravity
    :return: Alcohol by Volume decimal percentage
    :rtype: float

    Alternate Formula:

    A more complex equation which attempts to provide greater accuracy at higher gravities is:

    :math:`\\text{ABV} = \\frac{76.08 \\times \\big( \\text{og} - \\text{fg} \\big)}{1.775 - \\text{og}} \\times \\frac{\\text{fg}}{0.794}`

    The alternate equation reports a higher ABV for higher gravity beers.
    This equation is just a different take on it. Scientists rarely agree
    when it comes to equations. There will probably be another equation for
    ABV down the road.

    The complex formula, and variations on it come from:

    * Ritchie Products Ltd, (Zymurgy, Summer 1995, vol. 18, no. 2)
    * Michael L. Hall's article Brew by the Numbers: Add Up What's in Your Beer, and Designing Great Beers by Daniels.

    Source:

    * http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    """  # noqa
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794) / 100.0


def alcohol_by_weight(abv):
    """
    Alcohol by Weight from ABV

    :param float abv: Alcohol by Volume
    :return: Alcohol by Weight
    :rtype: float
    """
    return abv * ALCOHOL_SPECIFIC_GRAVITY
