# -*- coding: utf-8 -*-

from .sugar import sg_to_gu
from ..constants import PPG_DME

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


def get_wort_correction(boil_gravity, boil_volume,
                        final_gravity, final_volume,
                        efficiency=PPG_DME):
    """
    Get amount of sugar to add to correct wort

    Calculate how much additional DME or LME must be added to correct the boil
    to hit target final gravity.

    :param float boil_gravity: The gravity of the boil in GU
    :param float boil_volume: The volume of the boil
    :param float final_gravity: The desired final gravity in GU
    :param float final_volume: The desired final volume
    :param float efficiency: The efficiency of the medium to add
    """
    return (final_gravity * final_volume - boil_gravity * boil_volume) / efficiency  # noqa
