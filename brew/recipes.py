#! /usr/bin/python

import json
import string
import textwrap

from .constants import GRAIN_TYPE_DME
from .constants import GRAIN_TYPE_LME
from .constants import GAL_PER_LITER
from .constants import HOP_TYPE_PELLET
from .constants import HOP_UTILIZATION_SCALE_PELLET
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import LITER_PER_GAL
from .constants import SI_TYPES
from .constants import SI_UNITS
from .constants import WATER_WEIGHT_IMPERIAL
from .constants import WATER_WEIGHT_SI
from .utilities.abv import alcohol_by_volume_alternative
from .utilities.abv import alcohol_by_volume_standard
from .utilities.abv import alcohol_by_weight
from .utilities.color import calculate_mcu
from .utilities.color import calculate_srm
from .utilities.color import calculate_srm_daniels
from .utilities.color import calculate_srm_morey
from .utilities.color import calculate_srm_mosher
from .utilities.color import srm_to_ebc
from .utilities.sugar import gu_to_sg
from .utilities.sugar import sg_to_plato
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units


__all__ = ['Recipe']


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
        self.name = name
        self.grain_additions = grain_additions
        self.hop_additions = hop_additions
        self.yeast = yeast

        self.percent_brew_house_yield = validate_percentage(percent_brew_house_yield)  # nopep8 %
        self.start_volume = start_volume  # G
        self.final_volume = final_volume  # G

        # Manage units
        self.set_units(units)

        # For each grain and hop:
        # 1. Add to lookup
        # 2. Ensure all units are the same
        for grain_add in self.grain_additions:
            self.grain_lookup[grain_add.grain.name] = grain_add
            if grain_add.units != self.units:
                raise Exception("Grain addition units must be in '{}' not '{}'".format(  # nopep8
                    self.units, grain_add.units))
        for hop_add in self.hop_additions:
            # The same hops may be used several times, so we must distinguish
            hop_key = '{}_{}'.format(hop_add.hop.name, hop_add.boil_time)
            self.hop_lookup[hop_key] = hop_add
            if hop_add.units != self.units:
                raise Exception("Hop addition units must be in '{}' not '{}'".format(  # nopep8
                    self.units, hop_add.units))

    def __str__(self):
        return self.name

    def set_units(self, units):
        self.units = validate_units(units)
        if self.units == IMPERIAL_UNITS:
            self.types = IMPERIAL_TYPES
        elif self.units == SI_UNITS:
            self.types = SI_TYPES

    def change_units(self):
        """
        Change units from one type to the other return new instance
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
        # Pick the attribute based on units
        if self.units == IMPERIAL_UNITS:
            attr = 'ppg'
        if self.units == SI_UNITS:
            attr = 'hwe'

        total_points = 0
        for grain_add in self.grain_additions:
            # DME and LME are 100% efficient in disolving in water
            # Cereal extraction depends on brew house yield
            efficiency = self.percent_brew_house_yield
            if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
                efficiency = 1.0
            total_points += getattr(grain_add.grain, attr) * grain_add.weight * efficiency  # nopep8
        return total_points

    def get_original_gravity_units(self):
        return self.get_total_points() / self.final_volume

    def get_original_gravity(self):
        return gu_to_sg(self.get_original_gravity_units())

    def get_boil_gravity_units(self):
        return self.get_total_points() / self.start_volume

    def get_boil_gravity(self):
        return gu_to_sg(self.get_boil_gravity_units())

    def get_final_gravity_units(self):
        return self.get_original_gravity_units() * (1.0 - self.yeast.percent_attenuation)  # nopep8

    def get_final_gravity(self):
        return gu_to_sg(self.get_final_gravity_units())

    def get_degrees_plato(self):
        return sg_to_plato(self.get_boil_gravity())

    def get_brew_house_yield(self, plato_actual, vol_actual):
        """
        Brew House Yield (BHY)
        Brew house yield is a measurement that tells the efficiency of the
        brewing.  The actual degrees Plato from the brew and the actual gallons
        collected out of the kettle are needed to calculate the BHY.

        BHY  =  [(Pactual)(galactual)(BHYtarget)] / [(Ptarget)(galtarget)]
        """
        num = plato_actual * vol_actual * self.percent_brew_house_yield
        den = self.get_degrees_plato() * self.final_volume
        return num / den

    def get_extract_weight(self):
        """
        Weight of Extract
        The weight of extract is the amount of malt extract present in the
        wort.

        Lbs extract = (density of water) * (gal of wort) * (SG) * (P/100)

        The weight of one gallon of water in the above formula is 8.32 lbs/gal

        To find the weight of a gallon of wort, multiply the specific gravity
        of the wort by the density of water.

        Plato is a percentage of sugars by weight.  So 10 Plato means solution
        is 10% sugars.  In this equation we convert the degrees plato to a
        decimal number between 0.0 and 1.0 by dividing it by 100.  This is
        multiplied by the  weight of a gallon of wort.
        """
        water_density = WATER_WEIGHT_IMPERIAL
        if self.units == SI_UNITS:
            water_density = WATER_WEIGHT_SI
        return (water_density * self.final_volume * self.get_boil_gravity() *
                (self.get_degrees_plato() / 100.0))

    def get_percent_malt_bill(self, grain_add):
        """
        Percent malt bill is how much extract each grain addition adds to the
        recipe. To ensure different additions are measured equally each is
        converted to dry weight.
        """
        return self.get_grain_add_dry_weight(grain_add) / self.get_total_dry_weight()  # nopep8

    def get_grain_add_dry_weight(self, grain_add):
        """
        When converting Grain to DME its important to remember
        that you can't get 100% efficiency from grains.  Multiplying by
        the brew house yield will decrease the size of the DME
        accordingly.
        """
        if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
            return grain_add.get_dry_weight()
        else:
            return grain_add.get_dry_weight() * self.percent_brew_house_yield  # nopep8

    def get_total_dry_weight(self):
        weights = []
        for grain_add in self.grain_additions:
            weights.append(self.get_grain_add_dry_weight(grain_add))
        return sum(weights)

    def get_grain_add_cereal_weight(self, grain_add):
        """
        When converting DME or LME to grain its important to remember
        that you can't get 100% efficiency from grains.  Dividing by
        the brew house yield will increase the size of the grain
        accordingly.
        """
        if grain_add.grain_type in [GRAIN_TYPE_DME, GRAIN_TYPE_LME]:
            return grain_add.get_cereal_weight() / self.percent_brew_house_yield  # nopep8
        else:
            return grain_add.get_cereal_weight()

    def get_total_grain_weight(self):
        weights = []
        for grain_add in self.grain_additions:
            weights.append(self.get_grain_add_cereal_weight(grain_add))
        return sum(weights)

    def get_percent_ibus(self, hop_add):
        """
        Get the percentage the hops contributes to total ibus
        """
        bg = self.get_boil_gravity()
        fv = self.final_volume
        return hop_add.get_ibus(bg, fv) / self.get_total_ibu()

    def get_total_ibu(self):
        """
        Convenience method to get total IBU for the recipe
        """
        bg = self.get_boil_gravity()
        fv = self.final_volume
        return sum([hop_add.get_ibus(bg, fv)
                   for hop_add in self.hop_additions])

    def get_bu_to_gu(self):
        """
        Returns ratio of Bitterness Units to Original Gravity Units
        """
        return self.get_total_ibu() / self.get_boil_gravity_units()

    @classmethod
    def get_strike_temp(cls, mash_temp, malt_temp, liquor_to_grist_ratio):
        """
        Strike Water Temp
        As you know when you are mashing, your strike water has to be warmer
        than the target mash temperature because the cool malt will cool the
        temperature of the water.  To correctly calculate the temperature of
        the strike water, use the following formula.

        Strike Temp =  [((0.4)(T mash-T malt)) / L:G] +  T mash
        """
        return (((0.4 * (mash_temp - malt_temp)) /
                liquor_to_grist_ratio) + mash_temp)

    def get_mash_water_volume(self, liquor_to_grist_ratio):
        """
        Mash Water Volume
        To calculate the mash water volume you will need to know your liquor to
        grist ratio.  The term liquor refers to the mash water and grist refers
        to the milled malt.  We need to calculate the appropriate amount of
        water to allow for enzyme action and starch conversion take place.

        gallons H2O =  (Lbs malt)(L:G)(1gallon H2O) / 8.32 pounds water
        """
        water_weight = WATER_WEIGHT_IMPERIAL
        if self.units == SI_UNITS:
            water_weight = WATER_WEIGHT_SI
        return (self.get_total_dry_weight() * liquor_to_grist_ratio /
                water_weight)

    def get_wort_color_mcu(self, grain_add):
        """
        Calculation of Wort and Beer Color

        Color of Wort = S [(% extract)(L of malt)(P wort / 8P reference)]

        Source:
        http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
        http://brewwiki.com/index.php/Estimating_Color
        """  # nopep8
        weight = self.get_grain_add_cereal_weight(grain_add)
        return calculate_mcu(weight,
                             grain_add.grain.color,
                             self.final_volume,
                             units=self.units)

    def get_wort_color(self, grain_add):
        mcu = self.get_wort_color_mcu(grain_add)
        return calculate_srm(mcu)

    def get_total_wort_color(self):
        """
        Convenience method to get total wort color
        """
        mcu = sum([self.get_wort_color_mcu(ga) for ga in self.grain_additions])
        return calculate_srm(mcu)

    def get_total_wort_color_map(self):
        """
        Convenience method to get total wort color
        """
        mcu = sum([self.get_wort_color_mcu(ga) for ga in self.grain_additions])
        srm_morey = calculate_srm_morey(mcu)
        srm_daniels = calculate_srm_daniels(mcu)
        srm_mosher = calculate_srm_mosher(mcu)

        return {
            'srm': {
                'morey': round(srm_morey, 1),
                'daniels': round(srm_daniels, 1),
                'mosher': round(srm_mosher, 1),
            },
            'ebc': {
                'morey': round(srm_to_ebc(srm_morey), 1),
                'daniels': round(srm_to_ebc(srm_daniels), 1),
                'mosher': round(srm_to_ebc(srm_mosher), 1),
            },
        }

    def to_dict(self):
        og = self.get_original_gravity()
        bg = self.get_boil_gravity()
        fg = self.get_final_gravity()
        abv_standard = alcohol_by_volume_standard(og, fg)
        abv_alternative = alcohol_by_volume_alternative(og, fg)
        recipe_dict = {
            'name': string.capwords(self.name),
            'start_volume': round(self.start_volume, 2),
            'final_volume': round(self.final_volume, 2),
            'data': {
                'percent_brew_house_yield': round(self.percent_brew_house_yield, 2),  # nopep8
                'original_gravity': round(og, 3),
                'boil_gravity': round(bg, 3),
                'final_gravity': round(fg, 3),
                'abv_standard': round(abv_standard, 2),
                'abv_alternative': round(abv_alternative, 2),
                'abw_standard': round(alcohol_by_weight(abv_standard), 2),
                'abw_alternative': round(alcohol_by_weight(abv_alternative), 2),  # nopep8
                'total_wort_color_map': self.get_total_wort_color_map(),
                'total_ibu': round(self.get_total_ibu(), 1),
                'bu_to_gu': round(self.get_bu_to_gu(), 1),
                'units': self.units,
            },
            'grains': [],
            'hops': [],
            'yeast': {},
        }

        for grain_add in self.grain_additions:
            grain = grain_add.to_dict()
            wort_color_srm = self.get_wort_color(grain_add)
            wort_color_ebc = srm_to_ebc(wort_color_srm)
            working_yield = round(grain_add.grain.get_working_yield(self.percent_brew_house_yield), 2)  # nopep8
            percent_malt_bill = round(self.get_percent_malt_bill(grain_add), 2)
            grain['data'].update({
                'working_yield': working_yield,
                'percent_malt_bill': percent_malt_bill,
                'wort_color_srm': round(wort_color_srm, 1),
                'wort_color_ebc': round(wort_color_ebc, 1),
            })
            recipe_dict['grains'].append(grain)

        for hop_add in self.hop_additions:
            hop = hop_add.to_dict()

            ibus = hop_add.get_ibus(bg, self.final_volume)

            utilization = hop_add.utilization_cls.get_percent_utilization(
                bg, hop_add.boil_time)
            # Utilization is 10% higher for pellet vs whole/plug
            if hop_add.hop_type == HOP_TYPE_PELLET:
                utilization *= HOP_UTILIZATION_SCALE_PELLET

            hop['data'].update({
                'ibus': round(ibus, 1),
                'utilization': round(utilization, 2),
            })
            recipe_dict['hops'].append(hop)

        recipe_dict['yeast'] = self.yeast.to_dict()

        return recipe_dict

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, recipe):
        required_fields = [('name', str),
                           ('start_volume', (int, float)),
                           ('final_volume', (int, float)),
                           ('grains', (list, tuple)),
                           ('hops', (list, tuple)),
                           ('yeast', dict),
                           ]
        optional_fields = [('percent_brew_house_yield', float),
                           ('units', str),
                           ]
        validate_required_fields(recipe, required_fields)
        validate_optional_fields(recipe, optional_fields)

    def format(self):
        recipe_data = self.to_dict()
        kwargs = {}
        kwargs.update(recipe_data)
        kwargs.update(self.types)

        msg = ""
        msg += textwrap.dedent("""\
            {name}
            ===================================

            Brew House Yield:   {data[percent_brew_house_yield]:0.2f} %
            Start Volume:       {start_volume:0.1f}
            Final Volume:       {final_volume:0.1f}

            Original Gravity:   {data[original_gravity]:0.3f}
            Boil Gravity:       {data[boil_gravity]:0.3f}
            Final Gravity:      {data[final_gravity]:0.3f}

            ABV / ABW Standard: {data[abv_standard]:0.2f} % / {data[abw_standard]:0.2f} %
            ABV / ABW Alt:      {data[abv_alternative]:0.2f} % / {data[abw_alternative]:0.2f} %

            IBU:                {data[total_ibu]:0.1f} ibu
            BU/GU:              {data[bu_to_gu]:0.1f}

            Morey   (SRM/EBC):  {data[total_wort_color_map][srm][morey]:0.1f} degL / {data[total_wort_color_map][ebc][morey]:0.1f}
            Daneils (SRM/EBC):  {data[total_wort_color_map][srm][daniels]:0.1f} degL / {data[total_wort_color_map][ebc][daniels]:0.1f}
            Mosher  (SRM/EBC):  {data[total_wort_color_map][srm][mosher]:0.1f} degL / {data[total_wort_color_map][ebc][mosher]:0.1f}

            """.format(**kwargs))  # nopep8

        msg += textwrap.dedent("""\
            Grains
            ===================================

            """)

        for grain_data in recipe_data['grains']:
            grain_kwargs = {}
            grain_kwargs.update(grain_data)
            grain_kwargs.update(self.types)

            grain_name = grain_data['name']
            grain_add = self.grain_lookup[grain_name]
            if grain_add.units != self.units:
                grain_add = grain_add.change_units()

            msg += grain_add.format()
            msg += textwrap.dedent("""\

                    Percent Malt Bill: {data[percent_malt_bill]:0.2f} %
                    Working Yield:     {data[working_yield]:0.2f} %
                    SRM/EBC:           {data[wort_color_srm]:0.1f} degL / {data[wort_color_ebc]:0.1f}

                    """.format(**grain_kwargs))  # nopep8

        msg += textwrap.dedent("""\
            Hops
            ===================================

            """)

        for hop_data in recipe_data['hops']:
            hop_kwargs = {}
            hop_kwargs.update(hop_data)
            hop_kwargs.update(self.types)

            hop_key = '{}_{}'.format(hop_data['name'],
                                     hop_data['boil_time'])
            hop = self.hop_lookup[hop_key]
            if hop.units != self.units:
                hop = hop.change_units()

            msg += hop.format()
            msg += textwrap.dedent("""\

                    IBUs:         {data[ibus]:0.1f}
                    Utilization:  {data[utilization]:0.2f} %

                    """.format(**hop_kwargs))

        msg += textwrap.dedent("""\
            Yeast
            ===================================

            """)

        msg += self.yeast.format()
        return msg
