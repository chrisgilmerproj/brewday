# -*- coding: utf-8 -*-

from ..constants import GRAIN_TYPE_DME
from ..constants import GRAIN_TYPE_LME
from .sugar import sg_to_gu

__all__ = [
    u'calculate_brew_house_yield',
]


def calculate_brew_house_yield(wort_volume, sg, grain_additions):
    """
    Calculate Brew House Yield

    :param float wort_volume: The volume of the wort
    :param float sg: THe specific gravity of the wort
    :param list grain_additions: A list of grain additions in the wort
    :type grain_additions: list of GrainAddition objects
    :return: The brew house yield as a percentage

    Brew House Yield is a function of the wort volume, the measured specific
    gravity, and the grain additions used to make the wort.  This equation is
    thrown off by use of LME or DME since both have 100% efficiency in a brew.
    A better measure is to look at just the grains that needed to be steeped
    seperately and measure the specific gravity of that process.
    """
    total_gu = sum([grain_add.gu for grain_add in grain_additions])
    return (sg_to_gu(sg) * wort_volume) / total_gu
