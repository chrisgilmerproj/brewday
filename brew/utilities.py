from .constants import FC_DIFF_TWO_ROW
from .constants import GAL_PER_LITER
from .constants import HYDROMETER_ADJUSTMENT_TEMP
from .constants import IMPERIAL_UNITS
from .constants import LITERS_OF_WORT_AT_SG
from .constants import MOISTURE_CORRECTION
from .constants import MOISTURE_FINISHED_MALT
from .constants import POUND_PER_KG
from .constants import SI_UNITS
from .constants import SUCROSE_PLATO
from .constants import SUCROSE_PPG
from .validators import validate_percentage
from .validators import validate_units


def fahrenheit_to_celsius(temp):
    """
    Convert degrees Fahrenheit  to degrees Celsius
    """
    return (temp - 32.0) / 1.8


def celsius_to_fahrenheit(temp):
    """
    Convert degrees Celsius to degrees Fahrenheit
    """
    return(temp * 1.8) + 32.0


def sg_to_gu(sg):
    return (sg - 1) * 1000.0


def gu_to_sg(gu):
    return 1 + (gu / 1000.0)


def plato_to_sg(deg_plato):
    """
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
    Plato
    Degrees Plato is the weight of the extract in a 100gram solution at
    64 degrees Fahrenheit.

    Plato = [(S.G. - 1) x 1000] / 4

    The more precise calculation of Plato is:

    Plato = -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3

    Source:
    http://www.brewersfriend.com/2012/10/31/on-the-relationship-between-plato-and-specific-gravity/
    """
    # return (sg - 1.0) * 1000 / 4
    return ((135.997*sg - 630.272)*sg + 1111.14)*sg - 616.868


def brix_to_sg(brix):
    """
    Source:
    Brew Your Own Magazine
    http://www.brewersfriend.com/brix-converter/
    """
    return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1


def sg_to_brix(sg):
    """
    Source:
    http://en.wikipedia.org/wiki/Brix
    http://www.brewersfriend.com/brix-converter/
    """
    if sg > 1.17874:
        raise Exception("Above 40 degBx this function no longer works")
    return (((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622)


def brix_to_plato(brix):
    """
    The difference between the degBx and degP as calculated from the respective
    polynomials is:

        degP - degBx = (((-2.81615*sg + 8.79724)*sg - 9.1626)*sg + 3.18213)

    The difference is generally less than +/-0.0005 degBx or degP with the
    exception being for weak solutions.

    https://en.wikipedia.org/wiki/Brix
    """
    return sg_to_plato(brix_to_sg(brix))


def plato_to_brix(plato):
    return sg_to_brix(plato_to_sg(plato))


def hydrometer_adjustment(sg, temp, units=IMPERIAL_UNITS):
    """
    Adjust for the temperature if it deviates from 59degF.

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
    Adjust for the presence of alcohol in the refractometer reading

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


def alcohol_by_volume_standard(og, fg):
    """
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
    """  # nopep8
    return (og - fg) * 131.25


def alcohol_by_volume_alternative(og, fg):
    """
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
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)


def fine_grind_to_coarse_grind(fine_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Fine Grind to Coarse Grind

    fine_grind is a percentage from the malt bill
    fc_diff is the F/C difference percentage from the malt bill
    """
    validate_percentage(fine_grind)
    validate_percentage(fc_diff)
    return fine_grind - fc_diff


def coarse_grind_to_fine_grind(coarse_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Coarse Grind to Fine Grind

    coarse_grind is a percentage from the malt bill
    fc_diff is the F/C difference percentage from the malt bill
    """
    validate_percentage(coarse_grind)
    validate_percentage(fc_diff)
    return coarse_grind + fc_diff


def dry_basis_to_as_is_basis(dry_basis,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    Dry Basis to As-Is Basis

    dry_basis is a percentage from the malt bill in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    """
    validate_percentage(dry_basis)
    validate_percentage(moisture_content)
    return dry_basis * (1.0 - moisture_content)


def as_is_basis_to_dry_basis(as_is,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    As-Is Basis to Dry Basis

    asi_is is a percentage from the malt bill in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    """
    validate_percentage(as_is)
    validate_percentage(moisture_content)
    return as_is / (1.0 - moisture_content)


def sg_from_dry_basis(dbcg,
                      moisture_content=MOISTURE_FINISHED_MALT,
                      moisture_correction=MOISTURE_CORRECTION,
                      brew_house_efficiency=0.90):
    """
    dbcg is Dry Basis Coars Grain in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    moisture_correction is a percentage correction in decimal form
    brew_house_efficiency is the efficiency in decimal form

    Returns: Specific Gravity available from Malt
    """
    validate_percentage(dbcg)
    validate_percentage(moisture_content)
    validate_percentage(moisture_correction)
    validate_percentage(brew_house_efficiency)
    gu = ((dbcg - moisture_content - moisture_correction) *
          brew_house_efficiency * SUCROSE_PPG)
    return gu_to_sg(gu)


def plato_from_dry_basis(dbcg,
                         moisture_content=MOISTURE_FINISHED_MALT,
                         moisture_correction=MOISTURE_CORRECTION,
                         brew_house_efficiency=0.90):
    """
    dbcg is Dry Basis Coars Grain in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    moisture_correction is a percentage correction in decimal form
    brew_house_efficiency is the efficiency in decimal form

    Returns: Degrees Plato available from Malt
    """
    validate_percentage(dbcg)
    validate_percentage(moisture_content)
    validate_percentage(moisture_correction)
    validate_percentage(brew_house_efficiency)
    return ((dbcg - moisture_content - moisture_correction) *
            brew_house_efficiency * SUCROSE_PLATO)


def basis_to_hwe(basis_percentage):
    """
    basis_percentage in decimal form

    Return Hot Water Extract as Ldeg/kg, dry basis

    Ldeg/kg means how many litres of wort with a specific gravity of 1.001 you
    could produce from a kilogram of the fermentable

    For example, if you had a kilogram of sucrose, you could make up 386 litres
    of wort with a specific gravity of 1.001.
    """
    validate_percentage(basis_percentage)
    return basis_percentage * LITERS_OF_WORT_AT_SG


def hwe_to_basis(hwe):
    return hwe / LITERS_OF_WORT_AT_SG


def srm_to_ebc(srm):
    """
    Convert SRM to EBC Color
    """
    return srm * 1.97


def ebc_to_srm(ebc):
    """
    Convert EBC to SRM Color
    """
    return ebc / 1.97


def calculate_srm(grain_weight, beer_color, vol, units=IMPERIAL_UNITS):
    """
    Morey Equation

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    vol - in gal or liters

    http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
    """  # nopep8
    validate_units(units)
    if units == SI_UNITS:
        grain_weight = grain_weight * POUND_PER_KG
        vol = vol * GAL_PER_LITER

    mcu = grain_weight * beer_color / vol
    srm = 1.4922 * (mcu ** 0.6859)
    if srm > 50.0:
        raise Exception("Morey equation does not work above SRM 50")
    return srm
