import textwrap

from brew.utilities.sugar import brix_to_plato
from brew.utilities.sugar import brix_to_sg
from brew.utilities.sugar import plato_to_brix
from brew.utilities.sugar import plato_to_sg
from brew.utilities.sugar import sg_to_brix
from brew.utilities.sugar import sg_to_plato


def get_sugar_conversion(brix_in, plato_in, sg_in, sugar_out):
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

    brix = round(brix, 3)
    plato = round(plato, 3)
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
        {:0.3f}\t{:0.3f}\t{:0.3f}""".format(sg, plato, brix))
        return out
