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
from .utilities.color import calculate_mcu
from .utilities.color import calculate_srm
from .utilities.color import calculate_srm_daniels
from .utilities.color import calculate_srm_morey
from .utilities.color import calculate_srm_mosher
from .utilities.color import srm_to_ebc
from .utilities.malt import liquid_malt_to_grain_weight
from .utilities.sugar import gu_to_sg
from .utilities.sugar import sg_to_plato
from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields
from .validators import validate_units


class Recipe(object):
    """
    Recipe Calculations

    Many equations came from these sources:
    - http://www.learntobrew.com/beer-calculations/
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
            self.hop_lookup[hop_add.hop.name] = hop_add
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

    def get_malt_weight(self, grain_add):
        """
        Pounds of Malt
        It is imperative that you measure your recipes by the percent of
        extract taken from the malt rather than the weight of the malt.  Do
        this will all you to compensate for the Working Yield and help you
        accurately measure your malt bills.  For example, an recipe may call
        for 5% of caramel 20.  This does not me that you ad 0.5 pounds of
        caramel 20 malt in a 10 lb recipe. Instead, this means that you will
        have 5% of the total extract come from the caramel 20 malt.  Use the
        following formula to calculate the weight of malt based on a percent
        of extract.

        Lbs malt = (Lbs extract)(% Extract) / WY
        """
        return (self.get_extract_weight() *
                self.get_percent_malt_bill(grain_add) /
                grain_add.grain.get_working_yield(self.percent_brew_house_yield))  # nopep8

    def get_percent_malt_bill(self, grain_add):
        return grain_add.get_cereal_weight() / self.get_total_grain_weight()

    def get_total_grain_weight(self):
        return sum([g.get_cereal_weight() for g in self.grain_additions])

    def get_total_malt_weight(self):
        """
        Convenience method to get total malt weight
        """
        return sum([self.get_malt_weight(g) for g in self.grain_additions])

    def get_percent_ibus(self, hop_add):
        """Get the percentage the hops contributes to total ibus"""
        sg = self.get_boil_gravity()
        fv = self.final_volume
        return hop_add.get_ibus(sg, fv) / self.get_total_ibu()

    def get_total_ibu(self):
        """
        Convenience method to get total IBU
        """
        sg = self.get_boil_gravity()
        fv = self.final_volume
        return sum([hop_add.get_ibus(sg, fv)
                   for hop_add in self.hop_additions])

    def get_bu_to_gu(self):
        """
        Returns ratio of Bitterness Units to Original Gravity Units
        """
        return self.get_total_ibu() / self.get_original_gravity_units()

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
        return (self.get_total_malt_weight() * liquor_to_grist_ratio /
                water_weight)

    def get_wort_color_mcu(self, grain_add):
        """
        Calculation of Wort and Beer Color

        Color of Wort = S [(% extract)(L of malt)(P wort / 8P reference)]

        TODO:
        http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
        http://brewwiki.com/index.php/Estimating_Color
        """  # nopep8
        malt_weight = self.get_malt_weight(grain_add)
        grain_weight = liquid_malt_to_grain_weight(malt_weight)
        return calculate_mcu(grain_weight,
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
                'morey': srm_morey,
                'daniels': srm_daniels,
                'mosher': srm_mosher,
            },
            'ebc': {
                'morey': srm_to_ebc(srm_morey),
                'daniels': srm_to_ebc(srm_daniels),
                'mosher': srm_to_ebc(srm_mosher),
            },
        }

    def to_dict(self):
        og = self.get_original_gravity()
        bg = self.get_boil_gravity()
        fg = self.get_final_gravity()
        recipe_dict = {
            'name': string.capwords(self.name),
            'start_volume': self.start_volume,
            'final_volume': self.final_volume,
            'data': {
                'percent_brew_house_yield': self.percent_brew_house_yield,
                'original_gravity': og,
                'boil_gravity': bg,
                'final_gravity': fg,
                'abv_standard': alcohol_by_volume_standard(og, fg),
                'abv_alternative': alcohol_by_volume_alternative(og, fg),
                'extract_weight': self.get_extract_weight(),
                'total_wort_color_map': self.get_total_wort_color_map(),
                'total_grain_weight': self.get_total_grain_weight(),
                'total_ibu': self.get_total_ibu(),
                'bu_to_gu': self.get_bu_to_gu(),
                'units': self.units,
            },
            'grains': [],
            'hops': [],
            'yeast': {},
        }

        for grain_add in self.grain_additions:
            grain = grain_add.to_dict()
            weight_map = grain_add.get_weight_map()
            wort_color_srm = self.get_wort_color(grain_add)
            grain['data'].update({
                'working_yield': grain_add.grain.get_working_yield(self.percent_brew_house_yield),  # nopep8
                'wort_color_srm': wort_color_srm,
                'wort_color_ebc': srm_to_ebc(wort_color_srm),
            })
            grain['data'].update(weight_map)
            recipe_dict['grains'].append(grain)

        for hop_add in self.hop_additions:
            hop = hop_add.to_dict()

            utilization = hop_add.utilization_cls.get_percent_utilization(
                bg, hop_add.boil_time)
            # Utilization is 10% higher for pellet vs whole/plug
            if hop_add.hop_type == HOP_TYPE_PELLET:
                utilization *= HOP_UTILIZATION_SCALE_PELLET

            hop['data'].update({
                'ibus': hop_add.get_ibus(og, self.final_volume),
                'utilization': utilization,
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

            Brew House Yield:   {data[percent_brew_house_yield]:0.2f}
            Start Volume:       {start_volume:0.1f}
            Final Volume:       {final_volume:0.1f}

            Original Gravity:   {data[original_gravity]:0.3f}
            Boil Gravity:       {data[boil_gravity]:0.3f}
            Final Gravity:      {data[final_gravity]:0.3f}

            ABV Standard:       {data[abv_standard]:0.2f} %
            ABV Alternative:    {data[abv_alternative]:0.2f} %

            IBU:                {data[total_ibu]:0.2f} ibu
            BU/GU:              {data[bu_to_gu]:0.2f}

            Morey   (SRM/EBC):  {data[total_wort_color_map][srm][morey]:0.2f} degL / {data[total_wort_color_map][ebc][morey]:0.2f}
            Daneils (SRM/EBC):  {data[total_wort_color_map][srm][daniels]:0.2f} degL / {data[total_wort_color_map][ebc][daniels]:0.2f}
            Mosher  (SRM/EBC):  {data[total_wort_color_map][srm][mosher]:0.2f} degL / {data[total_wort_color_map][ebc][mosher]:0.2f}

            Extract Weight:     {data[extract_weight]:0.2f} {weight_large}
            Total Grain Weight: {data[total_grain_weight]:0.2f} {weight_large}

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

            msg += grain_add.format()
            msg += textwrap.dedent("""\

                    Weight DME:        {data[dry_weight]:0.2f} {weight_large}
                    Weight LME:        {data[lme_weight]:0.2f} {weight_large}
                    Weight Grain:      {data[grain_weight]:0.2f} {weight_large}
                    Working Yield:     {data[working_yield]:0.2f} %
                    SRM:               {data[wort_color_srm]:0.2f} degL
                    EBC:               {data[wort_color_ebc]:0.2f}

                    """.format(**grain_kwargs))

        msg += textwrap.dedent("""\
            Hops
            ===================================

            """)

        for hop_data in recipe_data['hops']:
            hop_kwargs = {}
            hop_kwargs.update(hop_data)
            hop_kwargs.update(self.types)

            hop_name = hop_data['name']
            hop = self.hop_lookup[hop_name]

            msg += hop.format()
            msg += textwrap.dedent("""\

                    IBUs:         {data[ibus]:0.2f}
                    Utilization:  {data[utilization]:0.2f} %
                    Util Cls:     {utilization_cls}

                    """.format(**hop_kwargs))

        msg += textwrap.dedent("""\
            Yeast
            ===================================

            """)

        msg += self.yeast.format()
        return msg
