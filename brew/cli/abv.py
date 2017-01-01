# -*- coding: utf-8 -*-
import argparse
import sys

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
    """
    Get Alcohol by Volume for CLI Utility

    og - Original Specific Gravity
    fg - Final Specific Gravity
    og_temp - Temperature of reading for og
    fg_temp - Temperature of reading for fg
    alternative - Use alternative ABV calculation
    refractometer - Adjust for using a refractometer for readings
    units - Type of units to use in calculations
    verbose - Return verbose information about calculations
    """
    # Gravity is required for calculation
    if not og:
        raise Exception(u"Original gravity required")
    if not fg:
        raise Exception(u"Final gravity required")

    # Ensure the gravity units are not mixed up
    if og < fg:
        raise Exception(u"Original Gravity must be higher than Final Gravity")

    if units not in [IMPERIAL_UNITS, SI_UNITS]:
        raise Exception(u"Units must be in either {} or {}".format(IMPERIAL_UNITS,  # noqa
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
        t_unit = u'F' if units == IMPERIAL_UNITS else u'C'
        out.append(u"OG     : {:0.3f}".format(og))
        out.append(u"OG Adj : {:0.3f}".format(og))
        out.append(u"OG Temp: {:0.2f} {}".format(og_temp, t_unit))
        out.append(u"FG     : {:0.3f}".format(fg))
        out.append(u"FG Adj : {:0.3f}".format(fg))
        out.append(u"FG Temp: {:0.2f} {}".format(fg_temp, t_unit))
        out.append(u"ABV    : {:0.2%}".format(abv))
        return u'\n'.join(out)
    else:
        return abv


def get_parser():
    parser = argparse.ArgumentParser(description=u'ABV Calculator')
    parser.add_argument(u'-o', u'--og', metavar=u'O', type=float,
                        required=True,
                        help=u'Original Gravity')
    parser.add_argument(u'-f', u'--fg', metavar=u'F', type=float,
                        required=True,
                        help=u'Final Gravity')
    parser.add_argument(u'--og-temp', metavar=u'T', type=float,
                        default=HYDROMETER_ADJUSTMENT_TEMP,
                        help=u'Original Gravity Temperature (default: %(default)s)')  # noqa
    parser.add_argument(u'--fg-temp', metavar=u'T', type=float,
                        default=HYDROMETER_ADJUSTMENT_TEMP,
                        help=u'Final Gravity Temperature (default: %(default)s)')  # noqa
    parser.add_argument(u'-a', u'--alternative', action=u'store_true',
                        default=False,
                        help=u'Use alternative ABV equation')
    parser.add_argument(u'-r', u'--refractometer', action=u'store_true',
                        default=False,
                        help=u'Adjust the Final Gravity if using a Refractometer reading')  # noqa
    parser.add_argument(u'--units', metavar=u"U", type=str,
                        default=IMPERIAL_UNITS,
                        help=u'Units to use (default: %(default)s)')
    parser.add_argument(u'-v', u'--verbose', action=u'store_true',
                        default=False,
                        help=u'Verbose Output')
    return parser


def main(parser_fn=get_parser, parser_kwargs=None):
    parser = None
    if not parser_kwargs:
        parser = parser_fn()
    else:
        parser = parser_fn(**parser_kwargs)
    args = parser.parse_args()
    try:
        out = get_abv(args.og, args.fg,
                      og_temp=args.og_temp,
                      fg_temp=args.fg_temp,
                      alternative=args.alternative,
                      refractometer=args.refractometer,
                      units=args.units,
                      verbose=args.verbose)
        if args.verbose:
            print(out)
        else:
            print(u"{:0.2%}".format(out))
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
