
"""
Yeast Pitch Calculator

This replicates other calculators found here:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/

"""  # nopep8

import argparse
import textwrap
import sys

from brew.constants import GAL_PER_LITER
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.utilities.yeast import KaiserYeastModel
from brew.utilities.yeast import WhiteYeastModel


def get_yeast_pitch_calculation(args):
    if args.units not in [IMPERIAL_UNITS, SI_UNITS]:
        print("Units must be in either {} or {}".format(IMPERIAL_UNITS,
                                                        SI_UNITS))
        sys.exit(1)

    model_cls = None
    if args.model == 'white':
        model_cls = WhiteYeastModel
    elif args.model == 'kaiser':
        model_cls = KaiserYeastModel
    else:
        print("Unknown Yeast Growth Model '{}', must be 'white' or 'kaiser'".format(args.model))  # nopep8
        sys.exit(1)

    try:
        model = model_cls(args.method, units=args.units)
    except Exception as e:
        print(e)
        sys.exit(1)
    data = model.get_yeast_pitch_rate(original_gravity=args.og,
                                      final_volume=args.fv,
                                      target_pitch_rate=args.target_pitch_rate,
                                      yeast_type=args.type,
                                      cells_per_pack=args.cells,
                                      num_packs=args.num,
                                      days_since_manufacture=args.days)
    cells_needed = data['cells_needed']
    data.update(model.types)
    msg = textwrap.dedent("""\
            Yeast Pitch Calculator
            -----------------------------------
            Original Gravity      {original_gravity:0.3f}
            Final Volume          {final_volume:0.2f} {volume}
            Target Pitch Rate     {target_pitch_rate}
            Viability             {viability} %
            Cells                 {cells:0.0f} B
            Pitch Rate As-Is      {pitch_rate_as_is:0.2f}
            Pitch Rate Cells      {pitch_rate_cells:0.0f} B
            Cells Needed          {cells_needed} B
            Required Growth Rate  {required_growth_rate}
            Units                 {units}""".format(**data))
    print(msg)

    if data['cells'] <= 0:
        print("\nNo cells available for further calculation")
        sys.exit(1)

    data = model.get_starter_volume(available_cells=data['cells'],
                                    starter_volume=args.sv,
                                    original_gravity=args.sg)
    end_cell_count = data['end_cell_count']
    data.update(model.types)
    msg = textwrap.dedent("""\

            Starter Volume
            -----------------------------------
            Available Cells       {available_cells:0.0f}
            Starter Volume        {starter_volume:0.2f} {volume}
            Original Gravity      {original_gravity:0.3f}
            DME Required          {dme:0.2f} {weight_small}
            Inoculation Rate      {inoculation_rate}
            Growth Rate           {growth_rate}
            End Cell Count        {end_cell_count} B
            Units                 {units}""".format(**data))
    print(msg)

    if cells_needed < end_cell_count:
        print("\nStarter has enough cells")
    else:
        print("\nStarter DOES NOT HAVE enough cells")

    resulting_pitch_rate = model.get_resulting_pitch_rate(
        starter_cell_count=end_cell_count,
        original_gravity=args.sg,
        final_volume=args.fv)
    data.update(model.types)
    msg = textwrap.dedent("""\

            Resulting Pitch Rate
            -----------------------------------
            Starter Cell Count    {starter_cell_count} B
            Original Gravity      {original_gravity}
            Final Volume          {final_volume} {volume}
            Pitch Rate            {resulting_pitch_rate}""".format(
        starter_cell_count=end_cell_count,
        original_gravity=args.sg,
        final_volume=args.fv,
        resulting_pitch_rate=resulting_pitch_rate,
        **model.types))
    print(msg)


def get_parser():
    parser = argparse.ArgumentParser(description='Yeast Pitch Calculator')
    parser.add_argument('--og', metavar='O', type=float,
                        default=1.05,
                        help='Wort Original Gravity (default: %(default)s)')
    parser.add_argument('--fv', metavar='V', type=float,
                        default=5.0,
                        help='Wort Final Volume (default: %(default)s)')
    parser.add_argument('--sg', metavar='O', type=float,
                        default=1.036,
                        help='Starter Original Gravity (default: %(default)s)')
    parser.add_argument('--sv', metavar='V', type=float,
                        default=2.0 * GAL_PER_LITER,
                        help='Starter Volume (default: %(default)s)')
    parser.add_argument('--target-pitch-rate', metavar='T', type=float,
                        default=1.42,
                        help='Target Pitch Rate (default: %(default)s)')
    parser.add_argument('--type', metavar='T', type=str,
                        default='liquid',
                        help='Yeast Type (default: %(default)s)')
    parser.add_argument('-c', '--cells', metavar='C', type=int,
                        default=100,
                        help='Number of cells per container in Billions')
    parser.add_argument('-n', '--num', metavar='N', type=int,
                        default=1,
                        help='Number of containers (default: %(default)s)')
    parser.add_argument('-d', '--days', metavar='D', type=int,
                        default=0,
                        help='Number of days since yeast manufacture (default: %(default)s)')  # nopep8
    parser.add_argument('--model', metavar='M', type=str,
                        default='white',
                        help='Model of yeast growth, white or kaiser (default: %(default)s)')  # nopep8
    parser.add_argument('--method', metavar='M', type=str,
                        default='stir plate',
                        help='Method of growth (default: %(default)s)')  # nopep8
    parser.add_argument('--units', metavar="U", type=str,
                        default=IMPERIAL_UNITS,
                        help='Units to use (default: %(default)s)')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    get_yeast_pitch_calculation(args)
