
from ..constants import HYDROMETER_ADJUSTMENT_TEMP
from ..constants import IMPERIAL_UNITS
from ..constants import SI_UNITS
from ..validators import validate_units
from .temperature import celsius_to_fahrenheit


__all__ = [
    'sg_to_gu',
    'gu_to_sg',
    'plato_to_sg',
    'sg_to_plato',
    'brix_to_sg',
    'sg_to_brix',
    'brix_to_plato',
    'plato_to_brix',
    'hydrometer_adjustment',
    'refractometer_adjustment',
]


def sg_to_gu(sg):
    """
    Specific Gravity to Gravity Units
    """
    return (sg - 1) * 1000.0


def gu_to_sg(gu):
    """
    Gravity Units to Specific Gravity
    """
    return 1 + (gu / 1000.0)


def plato_to_sg(deg_plato):
    """
    Degrees Plato to Specific Gravity

    Specific Gravity (S.G.)
    S.G. is the density of a liquid or solid compared to that of water.
    The simple formula for S.G. is:

    S.G. = 1 + 0.004 x Plato

    The more precise calculation of S.G. is:

    S.G. = [(Plato) / (258.6 - (Plato/258.2 x 227.1))] + 1

    Source:
    http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """
    return (deg_plato / (258.6 - ((deg_plato / 258.2) * 227.1))) + 1.0


def sg_to_plato(sg):
    """
    Specific Gravity to Degrees Plato

    Degrees Plato is the weight of the extract in a 100gram solution at
    64 degrees Fahrenheit.

    Plato = [(S.G. - 1) x 1000] / 4

    The more precise calculation of Plato is:

    Plato = -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3

    Source:
    http://www.brewersfriend.com/2012/10/31/on-the-relationship-between-plato-and-specific-gravity/
    """
    # return (sg - 1.0) * 1000 / 4
    return ((135.997 * sg - 630.272) * sg + 1111.14) * sg - 616.868


def brix_to_sg(brix):
    """
    Degrees Brix to Specific Gravity

    Source:
    http://www.brewersfriend.com/brix-converter/
    """
    return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1


def sg_to_brix(sg):
    """
    Specific Gravity to Degrees Brix

    Source:
    http://en.wikipedia.org/wiki/Brix
    http://www.brewersfriend.com/brix-converter/
    """
    if sg > 1.17874:
        raise Exception("Above 40 degBx this function no longer works")
    return (((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622)


def brix_to_plato(brix):
    """
    Degrees Brix to Degrees Plato

    The difference between the degBx and degP as calculated from the respective
    polynomials is:

        degP - degBx = (((-2.81615*sg + 8.79724)*sg - 9.1626)*sg + 3.18213)

    The difference is generally less than +/-0.0005 degBx or degP with the
    exception being for weak solutions.

    https://en.wikipedia.org/wiki/Brix
    """
    return sg_to_plato(brix_to_sg(brix))


def plato_to_brix(plato):
    """
    Degrees Plato to Degrees Brix
    """
    return sg_to_brix(plato_to_sg(plato))


def hydrometer_adjustment(sg, temp, units=IMPERIAL_UNITS):
    """
    Adjust the Hydrometer if the temperature deviates from 59degF.

    http://hbd.org/brewery/library/HydromCorr0992.html
    Correction(@59F) = 1.313454 - 0.132674*T + 2.057793e-3*T**2 - 2.627634e-6*T**3
        where T is in degrees F.

    Sources:
    http://www.brewersfriend.com/hydrometer-temp/
    http://www.topdownbrew.com/SGCorrection.html
    http://hbd.org/brewery/library/HydromCorr0992.html
    http://www.primetab.com/formulas.html
    """  # nopep8
    validate_units(units)
    if units == SI_UNITS:
        if temp < 0.0 or 100.0 < temp:
            raise Exception("Correction does not work outside temps 0 - 100C")
        temp = celsius_to_fahrenheit(temp)
    elif units == IMPERIAL_UNITS:
        if temp < 0.0 or 212.0 < temp:
            raise Exception("Correction does not work outside temps 0 - 212F")

    if temp == HYDROMETER_ADJUSTMENT_TEMP:
        return sg

    correction = (1.313454 - 0.132674 * (temp ** 1) +
                  (2.057793 * 10 ** -3) * (temp ** 2) -
                  (2.627634 * 10 ** -6) * (temp ** 3))
    return sg + (correction * 0.001)


def refractometer_adjustment(og, fg):
    """
    Adjust the Refractometer for the presence of alcohol.

    NOTE: This calculation assumes using Brix or Plato, so the input will be
    converted from SG to Plato and then converted back.

    Returns: Final Gravity

    Sources:
    http://seanterrill.com/2011/04/07/refractometer-fg-results/
    """
    og_brix = sg_to_brix(og)
    fg_brix = sg_to_brix(fg)

    new_fg = (1.0000 -
              0.0044993 * og_brix + 0.011774 * fg_brix +
              0.00027581 * (og_brix ** 2) - 0.0012717 * (fg_brix ** 2) -
              0.0000072800 * (og_brix ** 3) + 0.000063293 * (fg_brix ** 3))
    return brix_to_sg(new_fg)
