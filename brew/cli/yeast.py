
"""
Yeast Pitch Calculator

This replicates other calculators found here:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/

"""  # nopep8

import argparse
import sys
import textwrap

from brew.constants import GAL_PER_LITER
from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.utilities.yeast import KaiserYeastModel
from brew.utilities.yeast import WhiteYeastModel


def get_yeast_pitch_calculation(
        model_cls=WhiteYeastModel,
        method='stir plate',
        og=1.05,
        fv=5.0,
        sg=1.036,
        sv=0.53,
        target_pitch_rate=1.42,
        yeast_type='liquid',
        cells=100,
        num=1,
        days=0,
        units=IMPERIAL_UNITS):
    msg_list = []

    model = model_cls(method, units=units)
    data = model.get_yeast_pitch_rate(original_gravity=og,
                                      final_volume=fv,
                                      target_pitch_rate=target_pitch_rate,
                                      yeast_type=yeast_type,
                                      cells_per_pack=cells,
                                      num_packs=num,
                                      days_since_manufacture=days)
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
    msg_list.append(msg)

    if data['cells'] <= 0:
        msg_list.append("\nNo cells available for further calculation")
        return '\n'.join(msg_list)

    data = model.get_starter_volume(available_cells=data['cells'],
                                    starter_volume=sv,
                                    original_gravity=sg)
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
    msg_list.append(msg)

    if cells_needed < end_cell_count:
        msg_list.append("\nStarter has enough cells")
    else:
        msg_list.append("\nStarter DOES NOT HAVE enough cells")

    resulting_pitch_rate = model.get_resulting_pitch_rate(
        starter_cell_count=end_cell_count,
        original_gravity=sg,
        final_volume=fv)
    data.update(model.types)
    msg = textwrap.dedent("""\

            Resulting Pitch Rate
            -----------------------------------
            Starter Cell Count    {starter_cell_count} B
            Original Gravity      {original_gravity}
            Final Volume          {final_volume} {volume}
            Pitch Rate            {resulting_pitch_rate}""".format(
        starter_cell_count=end_cell_count,
        original_gravity=sg,
        final_volume=fv,
        resulting_pitch_rate=resulting_pitch_rate,
        **model.types))
    msg_list.append(msg)
    return('\n'.join(msg_list))


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


def main(parser_fn=get_parser, parser_kwargs=None):
    parser = None
    if not parser_kwargs:
        parser = parser_fn()
    else:
        parser = parser_fn(**parser_kwargs)
    args = parser.parse_args()

    # Check on output
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
        out = get_yeast_pitch_calculation(
            model_cls=model_cls,
            method=args.method,
            og=args.og,
            fv=args.fv,
            sg=args.sg,
            sv=args.sv,
            target_pitch_rate=args.target_pitch_rate,
            yeast_type=args.type,
            cells=args.cells,
            num=args.num,
            days=args.days,
            units=args.units)
        print(out)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
