# -*- coding: utf-8 -*-
import argparse
import sys
import textwrap

from brew.utilities.sugar import brix_to_plato
from brew.utilities.sugar import brix_to_sg
from brew.utilities.sugar import plato_to_brix
from brew.utilities.sugar import plato_to_sg
from brew.utilities.sugar import sg_to_brix
from brew.utilities.sugar import sg_to_plato


def get_sugar_conversion(brix_in, plato_in, sg_in, sugar_out):
    """
    Convert one sugar unit to another or print all.

    brix_in - Degrees Brix Input
    plato_in - Degrees Plato Input
    sg_in - Specific Gravity Input
    sugar_out - Type of conversion ('b', 'p', 's', or None)
    """
    brix, plato, sg = 0.0, 0.0, 0.0
    if brix_in:
        brix = brix_in
        plato = brix_to_plato(brix_in)
        sg = brix_to_sg(brix_in)
    elif plato_in:
        brix = plato_to_brix(plato_in)
        plato = plato_in
        sg = plato_to_sg(plato_in)
    elif sg_in:
        brix = sg_to_brix(sg_in)
        plato = sg_to_plato(sg_in)
        sg = sg_in

    brix = round(brix, 1)
    plato = round(plato, 1)
    sg = round(sg, 3)
    if sugar_out and sugar_out in [u'b', u'p', u's']:
        if sugar_out == u'b':
            return brix
        elif sugar_out == u'p':
            return plato
        elif sugar_out == u's':
            return sg
    else:
        out = textwrap.dedent(u"""\
        SG\tPlato\tBrix
        {:0.3f}\t{:0.1f}\t{:0.1f}""".format(sg, plato, brix))
        return out


def get_parser():
    parser = argparse.ArgumentParser(description=u'Sugar Conversion')
    parser.add_argument(u'-b', u'--brix', metavar=u'B', type=float,
                        help=u'Degrees Brix')
    parser.add_argument(u'-p', u'--plato', metavar=u'P', type=float,
                        help=u'Degrees Plato')
    parser.add_argument(u'-s', u'--sg', metavar=u'S', type=float,
                        help=u'Specific Gravity')
    parser.add_argument(u'-o', u'--out', metavar=u'O', type=str,
                        help=u'Desired Output (b, p, s accepted)')
    return parser


def main(parser_fn=get_parser, parser_kwargs=None):
    parser = None
    if not parser_kwargs:
        parser = parser_fn()
    else:
        parser = parser_fn(**parser_kwargs)
    args = parser.parse_args()

    if sum(bool(arg) for arg in [args.brix, args.plato, args.sg]) != 1:
        print(u"Must provide only one of Brix, Plato or Specific Gravity")
        sys.exit(1)
    print(get_sugar_conversion(args.brix, args.plato, args.sg, args.out))


if __name__ == "__main__":
    main()
