
from ..constants import FC_DIFF_TWO_ROW
from ..constants import LITERS_OF_WORT_AT_SG
from ..constants import MOISTURE_CORRECTION
from ..constants import MOISTURE_FINISHED_MALT
from ..constants import PPG_TO_HWE_CONVERSION
from ..constants import SUCROSE_PLATO
from ..constants import SUCROSE_PPG
from ..validators import validate_percentage
from .sugar import gu_to_sg


def dry_to_liquid_malt_weight(malt):
    """
    Source: http://www.weekendbrewer.com/brewingformulas.htm
    """
    return malt * 1.25


def liquid_to_dry_malt_weight(malt):
    """
    Source: http://www.weekendbrewer.com/brewingformulas.htm
    """
    return malt / 1.25


def grain_to_liquid_malt_weight(grain):
    """
    Source: http://www.weekendbrewer.com/brewingformulas.htm
    """
    return grain * 0.75


def liquid_malt_to_grain_weight(malt):
    return malt / 0.75


def dry_malt_to_grain_weight(malt):
    return malt * 5.0 / 3.0


def grain_to_dry_malt_weight(malt):
    return malt * 3.0 / 5.0


def specialty_grain_to_liquid_malt_weight(grain):
    """
    Source: http://www.weekendbrewer.com/brewingformulas.htm
    """
    return grain * 0.89


def liquid_malt_to_specialty_grain_weight(malt):
    return malt / 0.89


def fine_grind_to_coarse_grind(fine_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Fine Grind to Coarse Grind

    fine_grind is a percentage from the malt bill
    fc_diff is the F/C difference percentage from the malt bill
    """
    validate_percentage(fine_grind)
    validate_percentage(fc_diff)
    return fine_grind - fc_diff


def coarse_grind_to_fine_grind(coarse_grind, fc_diff=FC_DIFF_TWO_ROW):
    """
    Coarse Grind to Fine Grind

    coarse_grind is a percentage from the malt bill
    fc_diff is the F/C difference percentage from the malt bill
    """
    validate_percentage(coarse_grind)
    validate_percentage(fc_diff)
    return coarse_grind + fc_diff


def dry_basis_to_as_is_basis(dry_basis,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    Dry Basis to As-Is Basis

    dry_basis is a percentage from the malt bill in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    """
    validate_percentage(dry_basis)
    validate_percentage(moisture_content)
    return dry_basis * (1.0 - moisture_content)


def as_is_basis_to_dry_basis(as_is,
                             moisture_content=MOISTURE_FINISHED_MALT):
    """
    As-Is Basis to Dry Basis

    asi_is is a percentage from the malt bill in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    """
    validate_percentage(as_is)
    validate_percentage(moisture_content)
    return as_is / (1.0 - moisture_content)


def sg_from_dry_basis(dbcg,
                      moisture_content=MOISTURE_FINISHED_MALT,
                      moisture_correction=MOISTURE_CORRECTION,
                      brew_house_efficiency=0.90):
    """
    dbcg is Dry Basis Coarse Grain in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    moisture_correction is a percentage correction in decimal form
    brew_house_efficiency is the efficiency in decimal form

    Returns: Specific Gravity available from Malt
    """
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
    dbcg is Dry Basis Coars Grain in decimal form
    moisture_content is a percentage of moisture content in finished malt
      in decimal form
    moisture_correction is a percentage correction in decimal form
    brew_house_efficiency is the efficiency in decimal form

    Returns: Degrees Plato available from Malt
    """
    validate_percentage(dbcg)
    validate_percentage(moisture_content)
    validate_percentage(moisture_correction)
    validate_percentage(brew_house_efficiency)
    return ((dbcg - moisture_content - moisture_correction) *
            brew_house_efficiency * SUCROSE_PLATO)


def basis_to_hwe(basis_percentage):
    """
    basis_percentage in decimal form

    Return Hot Water Extract as Ldeg/kg, dry basis

    Ldeg/kg means how many litres of wort with a specific gravity of 1.001 you
    could produce from a kilogram of the fermentable

    For example, if you had a kilogram of sucrose, you could make up 386 litres
    of wort with a specific gravity of 1.001.
    """
    validate_percentage(basis_percentage)
    return basis_percentage * LITERS_OF_WORT_AT_SG


def hwe_to_basis(hwe):
    return hwe / LITERS_OF_WORT_AT_SG


def ppg_to_hwe(ppg):
    return ppg * PPG_TO_HWE_CONVERSION


def hwe_to_ppg(hwe):
    return hwe / PPG_TO_HWE_CONVERSION
