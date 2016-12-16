# -*- coding: utf-8 -*-
"""
Yeast Pitch Calculator

This replicates other calculators found here:
    - http://www.brewersfriend.com/yeast-pitch-rate-and-starter-calculator/

"""  # noqa

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
        method=u'stir plate',
        og=1.05,
        fv=5.0,
        sg=1.036,
        sv=0.53,
        target_pitch_rate=1.42,
        yeast_type=u'liquid',
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
    cells_needed = data[u'cells_needed']
    data.update(model.types)
    msg = textwrap.dedent(u"""\
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

    if data[u'cells'] <= 0:
        msg_list.append(u"\nNo cells available for further calculation")
        return u'\n'.join(msg_list)

    data = model.get_starter_volume(available_cells=data[u'cells'],
                                    starter_volume=sv,
                                    original_gravity=sg)
    end_cell_count = data[u'end_cell_count']
    data.update(model.types)
    msg = textwrap.dedent(u"""\

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
        msg_list.append(u"\nStarter has enough cells")
    else:
        msg_list.append(u"\nStarter DOES NOT HAVE enough cells")

    resulting_pitch_rate = model.get_resulting_pitch_rate(
        starter_cell_count=end_cell_count,
        original_gravity=sg,
        final_volume=fv)
    data.update(model.types)
    msg = textwrap.dedent(u"""\

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
    return(u'\n'.join(msg_list))


def get_parser():
    parser = argparse.ArgumentParser(description=u'Yeast Pitch Calculator')
    parser.add_argument(u'--og', metavar=u'O', type=float,
                        default=1.05,
                        help=u'Wort Original Gravity (default: %(default)s)')
    parser.add_argument(u'--fv', metavar=u'V', type=float,
                        default=5.0,
                        help=u'Wort Final Volume (default: %(default)s)')
    parser.add_argument(u'--sg', metavar=u'O', type=float,
                        default=1.036,
                        help=u'Starter Original Gravity (default: %(default)s)')  # noqa
    parser.add_argument(u'--sv', metavar=u'V', type=float,
                        default=2.0 * GAL_PER_LITER,
                        help=u'Starter Volume (default: %(default)s)')
    parser.add_argument(u'--target-pitch-rate', metavar=u'T', type=float,
                        default=1.42,
                        help=u'Target Pitch Rate (default: %(default)s)')
    parser.add_argument(u'--type', metavar=u'T', type=str,
                        default=u'liquid',
                        help=u'Yeast Type (default: %(default)s)')
    parser.add_argument(u'-c', u'--cells', metavar=u'C', type=int,
                        default=100,
                        help=u'Number of cells per container in Billions')
    parser.add_argument(u'-n', u'--num', metavar=u'N', type=int,
                        default=1,
                        help=u'Number of containers (default: %(default)s)')
    parser.add_argument(u'-d', u'--days', metavar=u'D', type=int,
                        default=0,
                        help=u'Number of days since yeast manufacture (default: %(default)s)')  # noqa
    parser.add_argument(u'--model', metavar=u'M', type=str,
                        default=u'white',
                        help=u'Model of yeast growth, white or kaiser (default: %(default)s)')  # noqa
    parser.add_argument(u'--method', metavar=u'M', type=str,
                        default=u'stir plate',
                        help=u'Method of growth (default: %(default)s)')  # noqa
    parser.add_argument(u'--units', metavar=u'U', type=str,
                        default=IMPERIAL_UNITS,
                        help=u'Units to use (default: %(default)s)')
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
        print(u"Units must be in either {} or {}".format(IMPERIAL_UNITS,
                                                         SI_UNITS))
        sys.exit(1)

    model_cls = None
    if args.model == u'white':
        model_cls = WhiteYeastModel
    elif args.model == u'kaiser':
        model_cls = KaiserYeastModel
    else:
        print(u"Unknown Yeast Growth Model '{}', must be 'white' or 'kaiser'".format(args.model))  # noqa
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
