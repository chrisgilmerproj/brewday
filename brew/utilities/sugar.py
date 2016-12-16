# -*- coding: utf-8 -*-
from ..constants import HYDROMETER_ADJUSTMENT_TEMP
from ..constants import IMPERIAL_UNITS
from ..constants import SI_UNITS
from ..validators import validate_units
from .temperature import celsius_to_fahrenheit

__all__ = [
    u'sg_to_gu',
    u'gu_to_sg',
    u'plato_to_sg',
    u'sg_to_plato',
    u'brix_to_sg',
    u'sg_to_brix',
    u'brix_to_plato',
    u'plato_to_brix',
    u'apparent_extract_to_real_extract',
    u'hydrometer_adjustment',
    u'refractometer_adjustment',
]


def sg_to_gu(sg):
    """
    Specific Gravity to Gravity Units

    :param float sg: Specific Gravity
    :return: Gravity Units
    :rtype: float
    """
    return (sg - 1) * 1000.0


def gu_to_sg(gu):
    """
    Gravity Units to Specific Gravity

    :param float gu: Gravity Units
    :return: Specific Gravity
    :rtype: float
    """
    return 1 + (gu / 1000.0)


def plato_to_sg(deg_plato):
    """
    Degrees Plato to Specific Gravity

    :param float deg_plato: Degrees Plato
    :return: Specific Gravity
    :rtype: float

    The simple formula for S.G. is:

    :math:`\\text{SG} = 1 + 0.004 \\times \\text{Plato}`

    The more precise calculation of SG is:

    :math:`\\text{SG} = \\frac{Plato}{258.6 - \\big(\\frac{Plato}{258.2} \\times 227.1\\big)} + 1`

    Source:

    * http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """  # noqa
    return (deg_plato / (258.6 - ((deg_plato / 258.2) * 227.1))) + 1.0


def sg_to_plato(sg):
    """
    Specific Gravity to Degrees Plato

    :param float sg: Specific Gravity
    :return: Degrees Plato
    :rtype: float

    :math:`\\text{Plato} = \\frac{\\big(\\text{SG} - 1\\big) \\times 1000}{4}`

    The more precise calculation of Plato is:

    :math:`\\text{Plato} = -616.868 + 1111.14 \\times sg - 630.272 \\times sg^2 + 135.997 \\times sg^3`

    Source:

    * http://www.brewersfriend.com/2012/10/31/on-the-relationship-between-plato-and-specific-gravity/
    """  # noqa
    # return (sg - 1.0) * 1000 / 4
    return ((135.997 * sg - 630.272) * sg + 1111.14) * sg - 616.868


def brix_to_sg(brix):
    """
    Degrees Brix to Specific Gravity

    :param float brix: Degrees Brix
    :return: Specific Gravity
    :rtype: float

    Source:

    * http://www.brewersfriend.com/brix-converter/
    """
    return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1


def sg_to_brix(sg):
    """
    Specific Gravity to Degrees Brix

    :param float sg: Specific Gravity
    :return: Degrees Brix
    :rtype: float

    Source:

    * http://en.wikipedia.org/wiki/Brix
    * http://www.brewersfriend.com/brix-converter/
    """
    if sg > 1.17874:
        raise Exception(u"Above 40 degBx this function no longer works")
    return (((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622)


def brix_to_plato(brix):
    """
    Degrees Brix to Degrees Plato

    :param float brix: Degrees Brix
    :return: Degrees Plato
    :rtype: float

    The difference between the degBx and degP as calculated from the respective
    polynomials is:

    :math:`\\text{degP} - \\text{degBx} = \\big(\\big(\\big(-2.81615*sg + 8.79724\\big) \\times sg - 9.1626\\big) \\times sg + 3.18213\\big)`

    The difference is generally less than +/-0.0005 degBx or degP with the
    exception being for weak solutions.

    Source:

    * https://en.wikipedia.org/wiki/Brix
    """  # noqa
    return sg_to_plato(brix_to_sg(brix))


def plato_to_brix(plato):
    """
    Degrees Plato to Degrees Brix

    :param float brix: Degrees Plato
    :return: Degrees Brix
    :rtype: float
    """
    return sg_to_brix(plato_to_sg(plato))


def apparent_extract_to_real_extract(original_extract, apparent_extract):
    """
    Apparent Extract to Real Extract in degrees Plato

    :param float original_extract: Original degrees Plato
    :param float apparent_extract: Apparent degrees Plato of finished beer
    :return: Real degrees Plato of finished beer
    :rtype: float

    Source:

    * Formula from Balling: De Clerck, Jean, A Textbook Of Brewing, Chapman & Hall Ltd., 1958
    """  # noqa
    attenuation_coeff = 0.22 + 0.001 * original_extract
    real_extract = (attenuation_coeff * original_extract + apparent_extract) / (1 + attenuation_coeff)  # noqa
    return real_extract


def hydrometer_adjustment(sg, temp, units=IMPERIAL_UNITS):
    """
    Adjust the Hydrometer if the temperature deviates from 59degF.

    :param float sg: Specific Gravity
    :param float temp: Temperature
    :param str units: The units
    :return: Specific Gravity corrected for temperature
    :rtype: float
    :raises Exception: If temperature outside freezing to boiling range of water

    The correction formula is from Lyons (1992), who used the following formula
    to fit data from the Handbook of Chemistry and Physics (CRC):

    :math:`\\text{Correction(@59F)} = 1.313454 - 0.132674 \\times T + 2.057793e^{-3} \\times T^2 - 2.627634e^{-6} \\times T^3`

    where T is in degrees F.

    Sources:

    * http://www.topdownbrew.com/SGCorrection.html
    * http://hbd.org/brewery/library/HydromCorr0992.html
    * http://www.brewersfriend.com/hydrometer-temp/
    * http://www.primetab.com/formulas.html
    """  # noqa
    validate_units(units)
    if units == SI_UNITS:
        if temp < 0.0 or 100.0 < temp:
            raise Exception(u"Correction does not work outside temps 0 - 100C")
        temp = celsius_to_fahrenheit(temp)
    elif units == IMPERIAL_UNITS:
        if temp < 0.0 or 212.0 < temp:
            raise Exception(u"Correction does not work outside temps 0 - 212F")

    if temp == HYDROMETER_ADJUSTMENT_TEMP:
        return sg

    correction = (1.313454 - 0.132674 * (temp ** 1) +
                  (2.057793 * 10 ** -3) * (temp ** 2) -
                  (2.627634 * 10 ** -6) * (temp ** 3))
    return sg + (correction * 0.001)


def refractometer_adjustment(og, fg):
    """
    Adjust the Refractometer for the presence of alcohol.

    :param float og: Original Gravity
    :param float fg: Final Gravity
    :return: Final Gravity adjusted
    :rtype: float

    NOTE: This calculation assumes using Brix or Plato, so the input will be
    converted from SG to Plato and then converted back.

    Sources:

    * http://seanterrill.com/2011/04/07/refractometer-fg-results/
    """
    og_brix = sg_to_brix(og)
    fg_brix = sg_to_brix(fg)

    new_fg = (1.0000 -
              0.0044993 * og_brix + 0.011774 * fg_brix +
              0.00027581 * (og_brix ** 2) - 0.0012717 * (fg_brix ** 2) -
              0.0000072800 * (og_brix ** 3) + 0.000063293 * (fg_brix ** 3))
    return brix_to_sg(new_fg)
