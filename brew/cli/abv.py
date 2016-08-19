
from brew.constants import HYDROMETER_ADJUSTMENT_TEMP
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.utilities.abv import alcohol_by_volume_alternative
from brew.utilities.abv import alcohol_by_volume_standard
from brew.utilities.sugar import hydrometer_adjustment
from brew.utilities.sugar import refractometer_adjustment


def get_abv(og, fg,
            og_temp=HYDROMETER_ADJUSTMENT_TEMP,
            fg_temp=HYDROMETER_ADJUSTMENT_TEMP,
            alternative=False,
            refractometer=False,
            units=IMPERIAL_UNITS,
            verbose=False):
    # Gravity is required for calculation
    if not og:
        raise Exception("Original gravity required")
    if not fg:
        raise Exception("Final gravity required")

    # Ensure the gravity units are not mixed up
    if og < fg:
        raise Exception("Original Gravity must be higher than Final Gravity")

    if units not in [IMPERIAL_UNITS, SI_UNITS]:
        raise Exception("Units must be in either {} or {}".format(IMPERIAL_UNITS,  # nopep8
                                                                  SI_UNITS))

    # Adjust the gravity based on temperature
    og = hydrometer_adjustment(og, og_temp, units=units)
    fg = hydrometer_adjustment(fg, fg_temp, units=units)

    # Adjust the final gravity if using a refractometer
    if refractometer:
        fg = refractometer_adjustment(og, fg)

    # Calculate the ABV
    if alternative:
        abv = alcohol_by_volume_alternative(og, fg)
    else:
        abv = alcohol_by_volume_standard(og, fg)

    if verbose:
        out = []
        t_unit = 'F' if units == IMPERIAL_UNITS else 'C'
        out.append("OG     : {:0.3f}".format(og))
        out.append("OG Adj : {:0.3f}".format(og))
        out.append("OG Temp: {:0.2f} {}".format(og_temp, t_unit))
        out.append("FG     : {:0.3f}".format(fg))
        out.append("FG Adj : {:0.3f}".format(fg))
        out.append("FG Temp: {:0.2f} {}".format(fg_temp, t_unit))
        out.append("ABV    : {:0.2f} %".format(abv))
        return '\n'.join(out)
    else:
        return abv
