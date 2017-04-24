# -*- coding: utf-8 -*-

from .sugar import sg_to_gu

__all__ = [
    u'calculate_brew_house_yield',
]


def calculate_brew_house_yield(wort_volume, sg, grain_additions):

    gravity_units = 0.0
    for grain_add in grain_additions:
        gravity_units += grain_add.grain.ppg * grain_add.weight
    return sg_to_gu(sg) * wort_volume / gravity_units
