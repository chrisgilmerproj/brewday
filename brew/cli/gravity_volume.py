# -*- coding: utf-8 -*-
import argparse
import sys

from brew.utilities.sugar import sg_to_gu
from brew.utilities.sugar import gu_to_sg


def get_gravity(original_volume, final_volume, gravity):
    """
    Convert gravity at original volume to gravity at final volume
    """
    return gu_to_sg(sg_to_gu(gravity) * original_volume / final_volume)


def get_parser():
    parser = argparse.ArgumentParser(description=u'Gravity-Volume Conversion')
    parser.add_argument(u'-o', u'--original-volume', metavar=u'V', type=float,
                        required=True, help=u'Original Volume')
    parser.add_argument(u'-f', u'--final-volume', metavar=u'V', type=float,
                        required=True, help=u'Final Volume')
    parser.add_argument(u'-g', u'--gravity', metavar=u'G', type=float,
                        required=True, help=u'Gravity')
    return parser


def main(parser_fn=get_parser, parser_kwargs=None):
    parser = None
    if not parser_kwargs:
        parser = parser_fn()
    else:
        parser = parser_fn(**parser_kwargs)
    args = parser.parse_args()
    if not all([args.original_volume,
                args.final_volume,
                args.gravity]):
        print("Please provide all arguments")
        sys.exit(1)
    out = get_gravity(args.original_volume,
                      args.final_volume,
                      args.gravity)
    print("{:0.3f}".format(out))


if __name__ == "__main__":
    main()
