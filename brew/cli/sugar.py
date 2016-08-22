
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
    if sugar_out and sugar_out in ['b', 'p', 's']:
        if sugar_out == 'b':
            return brix
        elif sugar_out == 'p':
            return plato
        elif sugar_out == 's':
            return sg
    else:
        out = textwrap.dedent("""\
        SG\tPlato\tBrix
        {:0.3f}\t{:0.1f}\t{:0.1f}""".format(sg, plato, brix))
        return out


def get_parser():
    parser = argparse.ArgumentParser(description='Sugar Conversion')
    parser.add_argument('-b', '--brix', metavar='B', type=float,
                        help='Degrees Brix')
    parser.add_argument('-p', '--plato', metavar='P', type=float,
                        help='Degrees Plato')
    parser.add_argument('-s', '--sg', metavar='S', type=float,
                        help='Specific Gravity')
    parser.add_argument('-o', '--out', metavar='O', type=str,
                        help='Desired Output (b, p, s accepted)')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if sum(bool(arg) for arg in [args.brix, args.plato, args.sg]) != 1:
        print("Must provide only one of Brix, Plato or Specific Gravity")
        sys.exit(1)
    print(get_sugar_conversion(args.brix, args.plato, args.sg, args.out))
