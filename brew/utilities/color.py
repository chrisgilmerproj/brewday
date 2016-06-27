
from ..constants import GAL_PER_LITER
from ..constants import IMPERIAL_UNITS
from ..constants import POUND_PER_KG
from ..constants import SI_UNITS
from ..validators import validate_units


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


def calculate_mcu(grain_weight, beer_color, final_volume,
                  units=IMPERIAL_UNITS):
    """
    Return MCU

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters

    http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
    """  # nopep8
    validate_units(units)
    if units == SI_UNITS:
        grain_weight = grain_weight * POUND_PER_KG
        final_volume = final_volume * GAL_PER_LITER

    mcu = grain_weight * beer_color / final_volume
    return mcu


def calculate_srm_mosher(mcu):
    """
    Mosher Equation

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters
    """  # nopep8
    if mcu < 7.0:
        raise Exception("Mosher equation does not work for MCU < 7.0")
    srm = (mcu * 0.3) + 4.7
    return srm


def calculate_srm_daniels(mcu):
    """
    Daniels Equation

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters
    """  # nopep8
    # if mcu < 11.0:
    #     raise Exception("Daniels equation does not work for MCU < 11.0")
    srm = (mcu * 0.2) + 8.4
    return srm


def calculate_srm_daniels_power(mcu):
    """
    Daniels Power Equation based on work by Druey

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters
    """  # nopep8
    srm = 1.73 * (mcu ** 0.64) - 0.27
    if srm > 50.0:
        raise Exception("Daniels Power equation does not work above SRM 50")
    return srm


def calculate_srm_noonan_power(mcu):
    """
    Noonan Power Equation based on work by Druey

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters
    """  # nopep8
    srm = 15.03 * (mcu ** 0.27) - 15.53
    if srm > 50.0:
        raise Exception("Noonan Power equation does not work above SRM 50")
    return srm


def calculate_srm_morey_hybrid(mcu):
    """
    A hybrid approach used by Morey.  Assumptions:

    1. SRM is approximately equal to MCU for values from 0 to 10.
    2. Homebrew is generally darker than commercial beer.
    3. Base on the previous qualitative postulate, I assumed that Ray Daniels'
       predicted relationship exists for beers with color greater than 10.
    4. Since Mosher's equation predicts darker color than Daniels' model for
       values of MCU greater than 37, I assumed that Mosher's approximation
       governed beer color for all values more than 37 MCUs.
    5. Difference in color for beers greater than 40 SRM are essentially
       impossible to detect visually; therefore, I limited the analysis to SRM
       of 50 and less.

    http://babblehomebrewers.com/attachments/article/61/beercolor.pdf
    """
    if 0 < mcu < 10:
        return mcu
    elif 10 <= mcu < 37:
        return calculate_srm_daniels(mcu)
    elif 37 <= mcu < 50:
        return calculate_srm_mosher(mcu)
    else:
        raise Exception("Morey Hybrid does not work above SRM 50")


def calculate_srm_morey(mcu):
    """
    Morey Equation
    http://www.morebeer.com/brewingtechniques/beerslaw/morey.html

    grain_weight - in lbs or kg
    beer_color - in deg Lovibond
    final_volume - in gal or liters

    http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
    """  # nopep8
    srm = 1.4922 * (mcu ** 0.6859)
    if srm > 50.0:
        raise Exception("Morey equation does not work above SRM 50")
    return srm


def calculate_srm(mcu):
    """
    General srm calculation uses the Morey Power Equation
    """
    return calculate_srm_morey(mcu)


def lovibond_to_srm(lovibond):
    """
    Convert deg Lovibond to SRM
    https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return 1.3546 * lovibond - 0.76


def srm_to_lovibond(srm):
    """
    Convert SRM to deg Lovibond
    https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return (srm + 0.76) / 1.3546


def srm_to_a430(srm, dilution=1.0):
    """
    Get attenuation at A430 from SRM and dilution
    https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return srm / (12.7 * dilution)


def ebc_to_a430(ebc, dilution=1.0):
    """
    Get attenuation at A430 from EBC and dilution
    https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return ebc / (25 * dilution)
