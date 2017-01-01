# -*- coding: utf-8 -*-
from ..constants import FC_DIFF_TWO_ROW
from ..constants import LITERS_OF_WORT_AT_SG
from ..constants import MOISTURE_CORRECTION
from ..constants import MOISTURE_FINISHED_MALT
from ..constants import PPG_TO_HWE_CONVERSION
from ..constants import SUCROSE_PLATO
from ..constants import SUCROSE_PPG
from ..validators import validate_percentage
from .sugar import gu_to_sg

__all__ = [
    u'dry_to_liquid_malt_weight',
    u'liquid_to_dry_malt_weight',
    u'grain_to_liquid_malt_weight',
    u'liquid_malt_to_grain_weight',
    u'dry_malt_to_grain_weight',
    u'grain_to_dry_malt_weight',
    u'specialty_grain_to_liquid_malt_weight',
    u'liquid_malt_to_specialty_grain_weight',
    u'fine_grind_to_coarse_grind',
    u'coarse_grind_to_fine_grind',
    u'dry_basis_to_as_is_basis',
    u'as_is_basis_to_dry_basis',
    u'sg_from_dry_basis',
    u'plato_from_dry_basis',
    u'basis_to_hwe',
    u'hwe_to_basis',
    u'ppg_to_hwe',
    u'hwe_to_ppg',
]


def dry_to_liquid_malt_weight(malt):
    """
    DME to LME Weight

    :param float malt: Weight of DME
    :return: LME Weight
    :rtype: float

    Source:

    * http://www.weekendbrewer.com/brewingformulas.htm
    """
    return malt * 1.25


def liquid_to_dry_malt_weight(malt):
    """
    LME to DME Weight

    :param float malt: Weight of LME
    :return: DME Weight
    :rtype: float
    """
    return malt / 1.25


def grain_to_liquid_malt_weight(grain):
    """
    Grain to LME Weight

    :param float grain: Weight of Grain
    :return: LME Weight
    :rtype: float
    """
    return grain * 0.75


def liquid_malt_to_grain_weight(malt):
    """
    LME to Grain Weight

    :param float malt: Weight of LME
    :return: Grain Weight
    :rtype: float
    """
    return malt / 0.75


def dry_malt_to_grain_weight(malt):
    """
    DME to Grain Weight

    :param float malt: Weight of DME
    :return: Grain Weight
    :rtype: float
    """
    return malt * 5.0 / 3.0


def grain_to_dry_malt_weight(malt):
    """
    Grain to DME Weight

    :param float grain: Weight of Grain
    :return: DME Weight
    :rtype: float
    """
    return malt * 3.0 / 5.0


def specialty_grain_to_liquid_malt_weight(grain):
    """
    Specialty Grain to LME Weight

    :param float grain: Weight of Specialty Grain
    :return: LME Weight
    :rtype: float
    """
    return grain * 0.89


def liquid_malt_to_specialty_grain_weight(malt):
    """
    LME to Specialty Grain Weight

    :param float grain: Weight of LME
    :return: Specialty Grain Weight
    :rtype: float
    """
    return malt / 0.89


def fine_grind_to_coarse_grind(fine_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Fine Grind to Coarse Grind Percentage

    :param float fine_grind: A percentage from the malt bill
    :param float fc_diff: The F/C difference percentage from the malt bill
    :return: Coarse Grind Percentage
    :rtype: float
    """
    validate_percentage(fine_grind)
    validate_percentage(fc_diff)
    return fine_grind - fc_diff


def coarse_grind_to_fine_grind(coarse_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Coarse Grind to Fine Grind Percentage

    :param float coarse_grind: A percentage from the malt bill
    :param float fc_diff: The F/C difference percentage from the malt bill
    :return: Fine Grind Percentage
    :rtype: float
    """
    validate_percentage(coarse_grind)
    validate_percentage(fc_diff)
    return coarse_grind + fc_diff


def dry_basis_to_as_is_basis(dry_basis,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    Dry Basis to As-Is Basis Percentage

    :param float dry_basis: A percentage from the malt bill in decimal form
    :param float moisture_content: A percentage of moisture content in finished malt in decimal form
    :return: As-Is Basis
    :rtype: float
    """  # noqa
    validate_percentage(dry_basis)
    validate_percentage(moisture_content)
    return dry_basis * (1.0 - moisture_content)


def as_is_basis_to_dry_basis(as_is,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    As-Is Basis to Dry Basis Percentage

    :param float as_is: A percentage from the malt bill in decimal form
    :param float moisture_content: A percentage of moisture content in finished malt in decimal form
    :return: Dry Basis
    :rtype: float
    """  # noqa
    validate_percentage(as_is)
    validate_percentage(moisture_content)
    return as_is / (1.0 - moisture_content)


def sg_from_dry_basis(dbcg,
                      moisture_content=MOISTURE_FINISHED_MALT,
                      moisture_correction=MOISTURE_CORRECTION,
                      brew_house_efficiency=0.90):
    """
    Specific Gravity from Dry Basis Percentage

    :param float dbcg: Dry Basis Coarse Grain in decimal form
    :param float moisture_content: A percentage of moisture content in finished malt in decimal form
    :param float moisture_correction: A percentage correction in decimal form
    :param float brew_house_efficiency: The efficiency in decimal form
    :return: Specific Gravity available from Malt
    :rtype: float
    """  # noqa
    validate_percentage(dbcg)
    validate_percentage(moisture_content)
    validate_percentage(moisture_correction)
    validate_percentage(brew_house_efficiency)
    gu = ((dbcg - moisture_content - moisture_correction) *
          brew_house_efficiency * SUCROSE_PPG)
    return gu_to_sg(gu)


def plato_from_dry_basis(dbcg,
                         moisture_content=MOISTURE_FINISHED_MALT,
                         moisture_correction=MOISTURE_CORRECTION,
                         brew_house_efficiency=0.90):
    """
    Degrees Plato from Dry Basis Percentage

    :param float dbcg: Dry Basis Coarse Grain in decimal form
    :param float moisture_content: A percentage of moisture content in finished malt in decimal form
    :param float moisture_correction: A percentage correction in decimal form
    :param float brew_house_efficiency: The efficiency in decimal form
    :return: Specific Gravity available from Malt
    :rtype: float
    """  # noqa
    validate_percentage(dbcg)
    validate_percentage(moisture_content)
    validate_percentage(moisture_correction)
    validate_percentage(brew_house_efficiency)
    return ((dbcg - moisture_content - moisture_correction) *
            brew_house_efficiency * SUCROSE_PLATO)


def basis_to_hwe(basis_percentage):
    """
    Basis Percentage to Hot Water Extract

    :param float basis_percentage: Basis as percentage
    :return: Hot Water Extract as Ldeg/kg, dry basis
    :rtype: float

    Ldeg/kg means how many litres of wort with a specific gravity of 1.001 you
    could produce from a kilogram of the fermentable

    For example, if you had a kilogram of sucrose, you could make up 386 litres
    of wort with a specific gravity of 1.001.
    """
    validate_percentage(basis_percentage)
    return basis_percentage * LITERS_OF_WORT_AT_SG


def hwe_to_basis(hwe):
    """
    Hot Water Extract to Basis Percentage

    :param float hwe: Hot Water Extract as Ldeg/kg, dry basis
    :return: Basis as percentage
    :rtype: float
    """
    return hwe / LITERS_OF_WORT_AT_SG


def ppg_to_hwe(ppg):
    """
    Points Per Gallon to Hot Water Extract

    :param float ppg: Points Per Gallon
    :return: Hot Water Extract
    :rtype: float
    """
    return ppg * PPG_TO_HWE_CONVERSION


def hwe_to_ppg(hwe):
    """
    Hot Water Extract to Points Per Gallon

    :param float hwe: Hot Water Extract
    :return: Points Per Gallon
    :rtype: float
    """
    return hwe / PPG_TO_HWE_CONVERSION
