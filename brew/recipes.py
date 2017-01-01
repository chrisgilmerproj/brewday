# -*- coding: utf-8 -*-
import json
import sys
import textwrap

from .constants import BOIL_EVAPORATION
from .constants import GAL_PER_LITER
from .constants import GRAIN_TYPE_DME
from .constants import GRAIN_TYPE_LME
from .constants import HOP_TYPE_PELLET
from .constants import HOP_UTILIZATION_SCALE_PELLET
from .constants import HOPS_CONSTANT_IMPERIAL
from .constants import HOPS_CONSTANT_SI
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import LITER_PER_GAL
from .constants import SI_TYPES
from .constants import SI_UNITS
from .constants import WATER_WEIGHT_IMPERIAL
from .constants import WATER_WEIGHT_SI
from .grains import GrainAddition
from .hops import HopAddition
from .utilities.abv import alcohol_by_volume_alternative
from .utilities.abv import alcohol_by_volume_standard
from .utilities.abv import alcohol_by_weight
from .utilities.abv import final_gravity_from_abv_standard
from .utilities.color import calculate_mcu
from .utilities.color import calculate_srm
from .utilities.color import calculate_srm_daniels
from .utilities.color import calculate_srm_morey
from .utilities.color import calculate_srm_mosher
from .utilities.color import srm_to_ebc
from .utilities.hops import HopsUtilizationGlennTinseth
from .utilities.sugar import gu_to_sg
from .utilities.sugar import sg_to_gu
from .utilities.sugar import sg_to_plato
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units

__all__ = [u'Recipe', u'RecipeBuilder']


class Recipe(object):
    """
    A representation of a Recipe that can be brewed to make beer.
    """
    grain_lookup = {}
    hop_lookup = {}

    def __init__(self, name,
                 grain_additions=None,
                 hop_additions=None,
                 yeast=None,
                 percent_brew_house_yield=0.70,
                 start_volume=7.0,
                 final_volume=5.0,
                 units=IMPERIAL_UNITS):
        """
        :param str name: The name of the recipe
        :param grain_additions: A list of Grain Additions
        :type grain_additions: list of GrainAddition objects
        :param hop_additions: A list of Hop Additions
        :type hop_additions: list of HopAddition objects
        :param float percent_brew_house_yield: The brew house yield
        :param float start_volume: The starting volume of the wort
        :param float final_volume: The final volume of the wort
        :param str units: The units
        :raises Exception: If the units of any GrainAddition is not the same as the units of the Recipe
        :raises Exception: If the units of any HopAddition is not the same as the units of the Recipe
        """  # noqa
        self.name = name
        if grain_additions is None:
            grain_additions = []
        self.grain_additions = grain_additions
        if hop_additions is None:
            hop_additions = []
        self.hop_additions = hop_additions
        self.yeast = yeast

        self.percent_brew_house_yield = validate_percentage(percent_brew_house_yield)  # noqa
        self.start_volume = start_volume
        self.final_volume = final_volume

        # Manage units
        self.set_units(units)

        # For each grain and hop:
        # 1. Add to lookup
        # 2. Ensure all units are the same
        for grain_add in self.grain_additions:
            self.grain_lookup[grain_add.grain.name] = grain_add
            if grain_add.units != self.units:
                raise Exception(u"Grain addition units must be in '{}' not '{}'".format(  # noqa
                    self.units, grain_add.units))
        for hop_add in self.hop_additions:
            # The same hops may be used several times, so we must distinguish
            hop_key = u'{}_{}'.format(hop_add.hop.name, hop_add.boil_time)
            self.hop_lookup[hop_key] = hop_add
            if hop_add.units != self.units:
                raise Exception(u"Hop addition units must be in '{}' not '{}'".format(  # noqa
                    self.units, hop_add.units))

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return self.name

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.name)
        if self.grain_additions:
            out = u"{0}, grain_additions=[{1}]".format(out, u', '.join([repr(h) for h in self.grain_additions]))  # noqa
        if self.hop_additions:
            out = u"{0}, hop_additions=[{1}]".format(out, u', '.join([repr(h) for h in self.hop_additions]))  # noqa
        if self.yeast:
            out = u"{0}, yeast={1}".format(out, repr(self.yeast))
        if self.percent_brew_house_yield:
            out = u"{0}, percent_brew_house_yield={1}".format(out, self.percent_brew_house_yield)  # noqa
        if self.start_volume:
            out = u"{0}, start_volume={1}".format(out, self.start_volume)
        if self.final_volume:
            out = u"{0}, final_volume={1}".format(out, self.final_volume)
        if self.units:
            out = u"{0}, units={1}".format(out, self.units)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.name == other.name) and \
           (self.grain_additions == other.grain_additions) and \
           (self.hop_additions == other.hop_additions) and \
           (self.yeast == other.yeast) and \
           (self.percent_brew_house_yield ==
               other.percent_brew_house_yield) and \
           (self.start_volume == other.start_volume) and \
           (self.final_volume == other.final_volume) and \
           (self.units == other.units):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_units(self, units):
        """
        Set the units and unit types

        :param str units: The units
        """
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def change_units(self):
        """
        Change units of the class from one type to the other

        :return: Recipe in new unit type
        :rtype: Recipe
        """
        if self.units == IMPERIAL_UNITS:
            start_volume = self.start_volume * LITER_PER_GAL
            final_volume = self.final_volume * LITER_PER_GAL
            units = SI_UNITS
        elif self.units == SI_UNITS:
            start_volume = self.start_volume * GAL_PER_LITER
            final_volume = self.final_volume * GAL_PER_LITER
            units = IMPERIAL_UNITS
        return Recipe(self.name,
                      grain_additions=[ga.change_units() for ga in
                                       self.grain_additions],
                      hop_additions=[ha.change_units() for ha in
                                     self.hop_additions],
                      yeast=self.yeast,
                      percent_brew_house_yield=self.percent_brew_house_yield,
                      start_volume=start_volume,
                      final_volume=final_volume,
                      units=units)

    def get_total_points(self):
        """
        Get the total points of the recipe

        :return: PPG or HWE depending on the units of the Recipe
        :rtype: float
        """
        # Pick the attribute based on units
        if self.units == IMPERIAL_UNITS:
            attr = u'ppg'
        if self.units == SI_UNITS:
            attr = u'hwe'

        total_points = 0
        for grain_add in self.grain_additions:
            # DME and LME are 100% efficient in disolving in water
            # Cereal extraction depends on brew house yield
            efficiency = self.percent_brew_house_yield
            if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
                efficiency = 1.0
            total_points += getattr(grain_add.grain, attr) * grain_add.weight * efficiency  # noqa
        return total_points

    def get_original_gravity_units(self):
        """
        Get the original gravity units

        :return: The original gravity units
        :rtype: float
        """
        return self.get_total_points() / self.final_volume

    def get_original_gravity(self):
        """
        Get the original specific gravity

        :return: The original specific gravity
        :rtype: float
        """
        return gu_to_sg(self.get_original_gravity_units())

    @property
    def og(self):
        return self.get_original_gravity()

    def get_boil_gravity_units(self, evaporation=BOIL_EVAPORATION):  # noqa
        """
        Get the boil gravity units

        :param float evaporation: Percent water evaporation during boil
        :return: The boil gravity units
        :rtype: float
        """
        return self.get_total_points() / ((1.0 - evaporation) * self.start_volume)  # noqa

    def get_boil_gravity(self, evaporation=BOIL_EVAPORATION):  # noqa
        """
        Get the boil specific gravity

        :param float evaporation: Percent water evaporation during boil
        :return: The boil specific gravity
        :rtype: float
        """
        return gu_to_sg(self.get_boil_gravity_units(evaporation=evaporation))

    @property
    def bg(self):
        return self.get_boil_gravity()

    def get_final_gravity_units(self):
        """
        Get the final gravity units

        :return: The final gravity units
        :rtype: float
        """
        return self.get_original_gravity_units() * (1.0 - self.yeast.percent_attenuation)  # noqa

    def get_final_gravity(self):
        """
        Get the final specific gravity

        :return: The final specific gravity
        :rtype: float
        """
        return gu_to_sg(self.get_final_gravity_units())

    @property
    def fg(self):
        return self.get_final_gravity()

    def get_degrees_plato(self):
        """
        Get the degrees plato

        :return: The degrees plato of the wort
        :rtype: float
        """
        return sg_to_plato(self.get_boil_gravity())

    @property
    def plato(self):
        return self.get_degrees_plato()

    def get_brew_house_yield(self, plato_actual, vol_actual):
        """
        Get the Brew House Yield

        :param float plato_actual: The actual degrees Plato
        :param float vol_actual: The actual volume collected from the kettle
        :return: Brew House Yield
        :rtyle: float
        """
        num = plato_actual * vol_actual * self.percent_brew_house_yield
        den = self.plato * self.final_volume
        return num / den

    def get_extract_weight(self):
        """
        Get the weight of the extract

        :return: The weight of extract
        :rtype: float
        """
        water_density = WATER_WEIGHT_IMPERIAL
        if self.units == SI_UNITS:
            water_density = WATER_WEIGHT_SI
        return (water_density * self.final_volume * self.get_boil_gravity() *
                (self.plato / 100.0))

    def get_percent_malt_bill(self, grain_add):
        """
        Get Percent Malt Bill

        :param GrainAddition grain_add: The Grain Addition
        :return: The percent extract the addition adds to the bill
        :rtype: float

        To ensure different additions are measured equally each is
        converted to dry weight.
        """
        return self.get_grain_add_dry_weight(grain_add) / self.get_total_dry_weight()  # noqa

    def get_grain_add_dry_weight(self, grain_add):
        """
        Get Grain Addition as DME

        :param GrainAddition grain_add: The Grain Addition
        :return: The weight of the grain as DME
        :rtype: float

        When converting Grain to DME its important to remember
        that you can't get 100% efficiency from grains.  Multiplying by
        the brew house yield will decrease the size of the DME
        accordingly.
        """
        if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
            return grain_add.get_dry_weight()
        else:
            return grain_add.get_dry_weight() * self.percent_brew_house_yield  # noqa

    def get_total_dry_weight(self):
        """
        Get total DME weight

        :return: The total weight of the DME
        :rtype: float
        """
        weights = []
        for grain_add in self.grain_additions:
            weights.append(self.get_grain_add_dry_weight(grain_add))
        return sum(weights)

    def get_grain_add_cereal_weight(self, grain_add):
        """
        Get Grain Addition as Cereal

        :param GrainAddition grain_add: The Grain Addition
        :return: The weight of the grain as Cereal
        :rtype: float

        When converting DME or LME to grain its important to remember
        that you can't get 100% efficiency from grains.  Dividing by
        the brew house yield will increase the size of the grain
        accordingly.
        """
        if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
            return grain_add.get_cereal_weight() / self.percent_brew_house_yield  # noqa
        else:
            return grain_add.get_cereal_weight()

    def get_total_grain_weight(self):
        """
        Get total Cereal weight

        :return: The total weight of the Cereal
        :rtype: float
        """
        weights = []
        for grain_add in self.grain_additions:
            weights.append(self.get_grain_add_cereal_weight(grain_add))
        return sum(weights)

    def get_percent_ibus(self, hop_add):
        """
        Get the percentage the hops contributes to total ibus

        :param HopAddition hop_add: The Hop Addition
        :return: The percent the hops contributes to total ibus
        :rtype: float
        """
        bg = self.get_boil_gravity()
        fv = self.final_volume
        return hop_add.get_ibus(bg, fv) / self.get_total_ibu()

    def get_total_ibu(self):
        """
        Convenience method to get total IBU for the recipe

        :return: The total IBU for the Recipe
        :rtype: float
        """
        bg = self.get_boil_gravity()
        fv = self.final_volume
        return sum([hop_add.get_ibus(bg, fv)
                   for hop_add in self.hop_additions])

    @property
    def ibu(self):
        return self.get_total_ibu()

    def get_bu_to_gu(self):
        """
        Get BU to GU Ratio

        :return: Ratio of Bitterness Units to Original Gravity Units
        :rtype: float
        """
        return self.get_total_ibu() / self.get_boil_gravity_units()

    @classmethod
    def get_strike_temp(cls, mash_temp, malt_temp, liquor_to_grist_ratio):
        """
        Get Strike Water Temperature

        :param float mash_temp: Mash Temperature
        :param float malt_temp: Malt Temperature
        :param float liquor_to_grist_ratio: The Liquor to Grist Ratio
        :return: The strike water temperature
        :rtype: float
        """
        return (((0.4 * (mash_temp - malt_temp)) /
                liquor_to_grist_ratio) + mash_temp)

    def get_mash_water_volume(self, liquor_to_grist_ratio):
        """
        Get the Mash Water Volume

        :param float liquor_to_grist_ratio: The Liquor to Grist Ratio
        :return: The mash water volume
        :rtype: float
        """
        water_weight = WATER_WEIGHT_IMPERIAL
        if self.units == SI_UNITS:
            water_weight = WATER_WEIGHT_SI
        return (self.get_total_dry_weight() * liquor_to_grist_ratio /
                water_weight)

    @property
    def abv(self):
        return alcohol_by_volume_standard(self.og, self.fg)

    def get_wort_color_mcu(self, grain_add):
        """
        Get the Wort Color in Malt Color Units

        :param GrainAddition grain_add: The Grain Addition to calculate
        :return: The MCU of the Grain Addition
        :rtype: float
        """  # noqa
        weight = self.get_grain_add_cereal_weight(grain_add)
        return calculate_mcu(weight,
                             grain_add.grain.color,
                             self.final_volume,
                             units=self.units)

    def get_wort_color(self, grain_add):
        """
        Get the Wort Color in SRM

        :param GrainAddition grain_add: The Grain Addition to calculate
        :return: The SRM of the Grain Addition
        :rtype: float
        """
        mcu = self.get_wort_color_mcu(grain_add)
        return calculate_srm(mcu)

    def get_total_wort_color(self):
        """
        Get the Total Color of the Wort in SRM using Morey Power Equation

        :return: The total color of the wort in SRM
        :rtype: float
        """
        mcu = sum([self.get_wort_color_mcu(ga) for ga in self.grain_additions])
        return calculate_srm(mcu)

    @property
    def color(self):
        return self.get_total_wort_color()

    def get_total_wort_color_map(self):
        """
        Get a map of wort color by method

        :return: A map of wort color in SRM and EBC by method (Morey, Daniels, and Mosher)
        :rtype: dict
        """  # noqa
        mcu = sum([self.get_wort_color_mcu(ga) for ga in self.grain_additions])

        srm_morey = u'N/A'
        srm_daniels = u'N/A'
        srm_mosher = u'N/A'

        ebc_morey = u'N/A'
        ebc_daniels = u'N/A'
        ebc_mosher = u'N/A'

        try:
            srm_morey = calculate_srm_morey(mcu)
            ebc_morey = round(srm_to_ebc(srm_morey), 1)
            srm_morey = round(srm_morey, 1)
        except Exception:
            pass

        try:
            srm_daniels = calculate_srm_daniels(mcu)
            ebc_daniels = round(srm_to_ebc(srm_daniels), 1)
            srm_daniels = round(srm_daniels, 1)
        except Exception:
            pass

        try:
            srm_mosher = calculate_srm_mosher(mcu)
            ebc_mosher = round(srm_to_ebc(srm_mosher), 1)
            srm_mosher = round(srm_mosher, 1)
        except Exception:
            pass

        return {
            u'srm': {
                u'morey': srm_morey,
                u'daniels': srm_daniels,
                u'mosher': srm_mosher,
            },
            u'ebc': {
                u'morey': ebc_morey,
                u'daniels': ebc_daniels,
                u'mosher': ebc_mosher,
            },
        }

    def to_dict(self):
        og = self.og
        bg = self.bg
        fg = self.fg
        abv_standard = self.abv
        abv_alternative = alcohol_by_volume_alternative(og, fg)
        recipe_dict = {
            u'name': self.name,
            u'start_volume': round(self.start_volume, 2),
            u'final_volume': round(self.final_volume, 2),
            u'data': {
                u'percent_brew_house_yield': round(self.percent_brew_house_yield, 3),  # noqa
                u'original_gravity': round(og, 3),
                u'boil_gravity': round(bg, 3),
                u'final_gravity': round(fg, 3),
                u'abv_standard': round(abv_standard, 4),
                u'abv_alternative': round(abv_alternative, 4),
                u'abw_standard': round(alcohol_by_weight(abv_standard), 4),
                u'abw_alternative': round(alcohol_by_weight(abv_alternative), 4),  # noqa
                u'total_wort_color_map': self.get_total_wort_color_map(),
                u'total_ibu': round(self.get_total_ibu(), 1),
                u'bu_to_gu': round(self.get_bu_to_gu(), 1),
                u'units': self.units,
            },
            u'grains': [],
            u'hops': [],
            u'yeast': {},
        }

        for grain_add in self.grain_additions:
            grain = grain_add.to_dict()
            wort_color_srm = self.get_wort_color(grain_add)
            wort_color_ebc = srm_to_ebc(wort_color_srm)
            working_yield = round(grain_add.grain.get_working_yield(self.percent_brew_house_yield), 3)  # noqa
            percent_malt_bill = round(self.get_percent_malt_bill(grain_add), 3)
            grain[u'data'].update({
                u'working_yield': working_yield,
                u'percent_malt_bill': percent_malt_bill,
                u'wort_color_srm': round(wort_color_srm, 1),
                u'wort_color_ebc': round(wort_color_ebc, 1),
            })
            recipe_dict[u'grains'].append(grain)

        for hop_add in self.hop_additions:
            hop = hop_add.to_dict()

            ibus = hop_add.get_ibus(bg, self.final_volume)

            utilization = hop_add.utilization_cls.get_percent_utilization(
                bg, hop_add.boil_time)
            # Utilization is 10% higher for pellet vs whole/plug
            if hop_add.hop_type == HOP_TYPE_PELLET:
                utilization *= HOP_UTILIZATION_SCALE_PELLET

            hop[u'data'].update({
                u'ibus': round(ibus, 1),
                u'utilization': round(utilization, 3),
            })
            recipe_dict[u'hops'].append(hop)

        recipe_dict[u'yeast'] = self.yeast.to_dict()

        return recipe_dict

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, recipe):
        required_fields = [(u'name', str),
                           (u'start_volume', (int, float)),
                           (u'final_volume', (int, float)),
                           (u'grains', (list, tuple)),
                           (u'hops', (list, tuple)),
                           (u'yeast', dict),
                           ]
        optional_fields = [(u'percent_brew_house_yield', float),
                           (u'units', str),
                           ]
        validate_required_fields(recipe, required_fields)
        validate_optional_fields(recipe, optional_fields)

    def format(self):
        recipe_data = self.to_dict()
        kwargs = {}
        kwargs.update(recipe_data)
        kwargs.update(self.types)

        msg = u""
        msg += textwrap.dedent(u"""\
            {name}
            ===================================

            Brew House Yield:   {data[percent_brew_house_yield]:0.1%}
            Start Volume:       {start_volume:0.1f}
            Final Volume:       {final_volume:0.1f}

            Boil Gravity:       {data[boil_gravity]:0.3f}
            Original Gravity:   {data[original_gravity]:0.3f}
            Final Gravity:      {data[final_gravity]:0.3f}

            ABV / ABW Standard: {data[abv_standard]:0.2%} / {data[abw_standard]:0.2%}
            ABV / ABW Alt:      {data[abv_alternative]:0.2%} / {data[abw_alternative]:0.2%}

            IBU:                {data[total_ibu]:0.1f} ibu
            BU/GU:              {data[bu_to_gu]:0.1f}

            Morey   (SRM/EBC):  {data[total_wort_color_map][srm][morey]} degL / {data[total_wort_color_map][ebc][morey]}
            Daniels (SRM/EBC):  {data[total_wort_color_map][srm][daniels]} degL / {data[total_wort_color_map][ebc][daniels]}
            Mosher  (SRM/EBC):  {data[total_wort_color_map][srm][mosher]} degL / {data[total_wort_color_map][ebc][mosher]}

            """.format(**kwargs))  # noqa

        msg += textwrap.dedent(u"""\
            Grains
            ===================================

            """)

        for grain_data in recipe_data[u'grains']:
            grain_kwargs = {}
            grain_kwargs.update(grain_data)
            grain_kwargs.update(self.types)

            grain_name = grain_data[u'name']
            grain_add = self.grain_lookup[grain_name]
            if grain_add.units != self.units:
                grain_add = grain_add.change_units()

            msg += grain_add.format()
            msg += textwrap.dedent(u"""\

                    Percent Malt Bill: {data[percent_malt_bill]:0.1%}
                    Working Yield:     {data[working_yield]:0.1%}
                    SRM/EBC:           {data[wort_color_srm]:0.1f} degL / {data[wort_color_ebc]:0.1f}

                    """.format(**grain_kwargs))  # noqa

        msg += textwrap.dedent(u"""\
            Hops
            ===================================

            """)

        for hop_data in recipe_data[u'hops']:
            hop_kwargs = {}
            hop_kwargs.update(hop_data)
            hop_kwargs.update(self.types)

            hop_key = u'{}_{}'.format(hop_data[u'name'],
                                      hop_data[u'boil_time'])
            hop = self.hop_lookup[hop_key]
            if hop.units != self.units:
                hop = hop.change_units()

            msg += hop.format()
            msg += textwrap.dedent(u"""\

                    IBUs:         {data[ibus]:0.1f}
                    Utilization:  {data[utilization]:0.1%}

                    """.format(**hop_kwargs))

        msg += textwrap.dedent(u"""\
            Yeast
            ===================================

            """)

        msg += self.yeast.format()
        return msg


class RecipeBuilder(object):
    """
    A class for building recipes
    """
    grain_lookup = {}
    hop_lookup = {}

    def __init__(self, name,
                 grain_list=None,
                 hop_list=None,
                 target_ibu=33.0,
                 target_og=1.050,
                 percent_brew_house_yield=0.70,
                 start_volume=7.0,
                 final_volume=5.0,
                 units=IMPERIAL_UNITS):
        """
        :param str name: The name of the recipe
        :param grain_list: A list of Grains
        :type grain_list: list of Grain objects
        :param hop_list: A list of Hops
        :type hop_list: list of Hop objects
        :param float target_ibu: The IBU Target
        :param float target_og: The Original Gravity Target
        :param float percent_brew_house_yield: The brew house yield
        :param float start_volume: The starting volume of the wort
        :param float final_volume: The final volume of the wort
        :param str units: The units
        """  # noqa
        self.name = name
        if grain_list is None:
            grain_list = []
        self.grain_list = grain_list
        if hop_list is None:
            hop_list = []
        self.hop_list = hop_list

        self.target_ibu = target_ibu
        self.target_og = target_og
        self.percent_brew_house_yield = validate_percentage(percent_brew_house_yield)  # noqa
        self.start_volume = start_volume
        self.final_volume = final_volume

        # Manage units
        self.set_units(units)

        # For each grain and hop:
        # Add to lookup
        for grain in self.grain_list:
            self.grain_lookup[grain.name] = grain
        for hop in self.hop_list:
            self.hop_lookup[hop.name] = hop

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return self.name

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.name)
        if self.grain_list:
            out = u"{0}, grain_list=[{1}]".format(out, u', '.join([repr(h) for h in self.grain_list]))  # noqa
        if self.hop_list:
            out = u"{0}, hop_list=[{1}]".format(out, u', '.join([repr(h) for h in self.hop_list]))  # noqa
        if self.target_og:
            out = u"{0}, target_og={1}".format(out, self.target_og)  # noqa
        if self.percent_brew_house_yield:
            out = u"{0}, percent_brew_house_yield={1}".format(out, self.percent_brew_house_yield)  # noqa
        if self.start_volume:
            out = u"{0}, start_volume={1}".format(out, self.start_volume)
        if self.final_volume:
            out = u"{0}, final_volume={1}".format(out, self.final_volume)
        if self.units:
            out = u"{0}, units={1}".format(out, self.units)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.name == other.name) and \
           (self.grain_list == other.grain_list) and \
           (self.hop_list == other.hop_list) and \
           (self.target_og == other.target_og) and \
           (self.percent_brew_house_yield ==
               other.percent_brew_house_yield) and \
           (self.start_volume == other.start_volume) and \
           (self.final_volume == other.final_volume) and \
           (self.units == other.units):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_units(self, units):
        """
        Set the units and unit types

        :param str units: The units
        """
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def change_units(self):
        """
        Change units of the class from one type to the other

        :return: RecipeBuilder in new unit type
        :rtype: RecipeBuilder
        """
        if self.units == IMPERIAL_UNITS:
            start_volume = self.start_volume * LITER_PER_GAL
            final_volume = self.final_volume * LITER_PER_GAL
            units = SI_UNITS
        elif self.units == SI_UNITS:
            start_volume = self.start_volume * GAL_PER_LITER
            final_volume = self.final_volume * GAL_PER_LITER
            units = IMPERIAL_UNITS
        return RecipeBuilder(
            self.name,
            grain_list=self.grain_list,
            hop_list=self.hop_list,
            target_og=self.target_og,
            percent_brew_house_yield=self.percent_brew_house_yield,
            start_volume=start_volume,
            final_volume=final_volume,
            units=units)

    def get_grain_additions(self, percent_list):
        """
        Calculate GrainAdditions from list of percentages

        :param list percent_list: A list of percentages mapped to each Grain
        :return: A list of Grain Additions
        :rtype: list(GrainAddition)
        :raises Exception: If sum of percentages does not equal 1.0
        :raises Exception: If length of percent_list does not match length of self.grain_list
        """  # noqa
        for percent in percent_list:
            validate_percentage(percent)

        if sum(percent_list) != 1.0:
            raise Exception(u"Percentages must sum to 1.0")

        if len(percent_list) != len(self.grain_list):
            raise Exception(u"The length of percent_list must equal length of self.grain_list")  # noqa

        # Pick the attribute based on units
        if self.units == IMPERIAL_UNITS:
            attr = u'ppg'
        if self.units == SI_UNITS:
            attr = u'hwe'

        gu = sg_to_gu(self.target_og)
        total_points = gu * self.final_volume

        grain_additions = []
        for index, grain in enumerate(self.grain_list):
            efficiency = self.percent_brew_house_yield
            weight = (percent_list[index] * total_points) / (getattr(grain, attr) * efficiency)  # noqa
            grain_add = GrainAddition(grain, weight=weight, units=self.units)
            grain_additions.append(grain_add)
        return grain_additions

    def get_hop_additions(self, percent_list, boil_time_list,
                          hop_type=HOP_TYPE_PELLET,
                          utilization_cls=HopsUtilizationGlennTinseth):
        """
        Calculate HopAdditions from list of boil times

        :param list boil_time_list: A list of boil times mapped to each Hop
        :param HopsUtilization utilization_cls: The utilization class used for calculation
        :return: A list of Hop Additions
        :rtype: list(HopAddition)
        :raises Exception: If sum of percentages does not equal 1.0
        :raises Exception: If length of percent_list does not match length of self.grain_list
        :raises Exception: If length of boil_time_list does not match length of self.hop_list
        """  # noqa
        for percent in percent_list:
            validate_percentage(percent)

        if sum(percent_list) != 1.0:
            raise Exception(u"Percentages must sum to 1.0")

        if len(percent_list) != len(self.grain_list):
            raise Exception(u"The length of percent_list must equal length of self.grain_list")  # noqa

        if len(boil_time_list) != len(self.hop_list):
            raise Exception(u"The length of boil_time_list must equal length of self.hop_list")  # noqa

        hops_constant = HOPS_CONSTANT_IMPERIAL
        if self.units == SI_UNITS:
            hops_constant = HOPS_CONSTANT_SI

        hop_additions = []
        for index, hop in enumerate(self.hop_list):
            percent = percent_list[index]
            boil_time = boil_time_list[index]

            # Calculate utilization from boil gravity
            bg = gu_to_sg(sg_to_gu(self.target_og) * self.final_volume / self.start_volume)  # noqa
            utilization = utilization_cls.get_percent_utilization(bg, boil_time)  # noqa
            if hop_type == HOP_TYPE_PELLET:
                utilization *= HOP_UTILIZATION_SCALE_PELLET

            num = (self.target_ibu * percent * self.final_volume)
            den = (utilization * hop.percent_alpha_acids * hops_constant)
            weight = num / den
            hop_add = HopAddition(hop,
                                  weight=weight,
                                  boil_time=boil_time,
                                  hop_type=hop_type,
                                  utilization_cls=utilization_cls,
                                  units=self.units)
            hop_additions.append(hop_add)
        return hop_additions

    def get_yeast_attenuation(self, abv):
        """
        Estimate yeast attenuation given a target abv

        :param float abv: Alcohol by Volume
        :return: Yeast Attenuation Percentage
        :rtype: float

        This uses the ABV Standard Equation
        """
        validate_percentage(abv)
        fg = final_gravity_from_abv_standard(self.target_og, abv)
        attenuation = 1.0 - sg_to_gu(fg) / sg_to_gu(self.target_og)
        return attenuation
