#! /usr/bin/python

import string
import textwrap

from .constants import GAL_PER_LITER
from .constants import IMPERIAL_TYPES
from .constants import IMPERIAL_UNITS
from .constants import LITER_PER_GAL
from .constants import SI_TYPES
from .constants import SI_UNITS
from .constants import WATER_WEIGHT_IMPERIAL
from .constants import WATER_WEIGHT_SI
from .utilities.abv import alcohol_by_volume_standard
from .utilities.color import calculate_mcu
from .utilities.color import calculate_srm
from .utilities.color import srm_to_ebc
from .utilities.malt import liquid_malt_to_grain_weight
from .utilities.malt import liquid_to_dry_malt_weight
from .utilities.malt import grain_to_liquid_malt_weight
from .utilities.sugar import gu_to_sg
from .utilities.sugar import sg_to_plato
from .validators import validate_percentage
from .validators import validate_units


class Recipe(object):
    """
    Recipe Calculations

    Many equations came from these sources:
    - http://www.learntobrew.com/beer-calculations/
    """

    def __init__(self, name,
                 grain_additions=None,
                 hop_additions=None,
                 yeast_attenuation=0.75,
                 percent_brew_house_yield=0.70,
                 start_volume=7.0,
                 final_volume=5.0,
                 units=IMPERIAL_UNITS):
        self.name = name
        self.grain_additions = grain_additions
        self.hop_additions = hop_additions
        self.yeast_attenuation = validate_percentage(yeast_attenuation)

        self.percent_brew_house_yield = validate_percentage(percent_brew_house_yield)  # nopep8 %
        self.start_volume = start_volume  # G
        self.final_volume = final_volume  # G

        # Manage units
        self.set_units(units)

        # Ensure all units are the same
        for grain_add in self.grain_additions:
            if grain_add.units != self.units:
                raise Exception("Grain addition units must be in '{}' not '{}'".format(  # nopep8
                    self.units, grain_add.units))
        for hop_add in self.hop_additions:
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
                      yeast_attenuation=self.yeast_attenuation,
                      percent_brew_house_yield=self.percent_brew_house_yield,
                      start_volume=start_volume,
                      final_volume=final_volume,
                      units=units)

    def get_original_gravity_units(self):
        total_points = 0
        if self.units == IMPERIAL_UNITS:
            for grain_add in self.grain_additions:
                total_points += grain_add.grain.ppg * grain_add.weight
        if self.units == SI_UNITS:
            for grain_add in self.grain_additions:
                total_points += grain_add.grain.hwe * grain_add.weight
        return total_points * self.percent_brew_house_yield / self.final_volume

    def get_original_gravity(self):
        return gu_to_sg(self.get_original_gravity_units())

    def get_boil_gravity_units(self):
        total_points = 0
        if self.units == IMPERIAL_UNITS:
            for grain_add in self.grain_additions:
                total_points += grain_add.grain.ppg * grain_add.weight
        if self.units == SI_UNITS:
            for grain_add in self.grain_additions:
                total_points += grain_add.grain.hwe * grain_add.weight
        return total_points * self.percent_brew_house_yield / self.start_volume

    def get_boil_gravity(self):
        return gu_to_sg(self.get_boil_gravity_units())

    def get_final_gravity_units(self):
        return self.get_original_gravity_units() * (1.0 - self.yeast_attenuation)  # nopep8

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
        return grain_add.weight / self.get_total_grain_weight()

    def get_total_grain_weight(self):
        return sum([g.weight for g in self.grain_additions])

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

    def get_beer_color(self, percent_color_loss=0.30):
        """
        We allow for a 30% loss of color during fermentation to calculate the color of beer.
        Color of Beer = (color of wort)(1 - % color loss)
        """  # nopep8
        validate_percentage(percent_color_loss)
        return (self.get_total_wort_color() * (1.0 - percent_color_loss))

    def format(self):
        """
        PALE ALE ANSWERS:

        Specific Gravity = 1.057
        S.G. = [(14P) / (258.6 - (14P/258.2 x 227.1))] +1

        Lbs extract = 6.16 pounds
        Lbs extract =   [(8.32 pounds/gal wort)(5gal wort)(1.057 S.G.)(14 P)] / 100

        Working Yield of 2-Row = 0.53
        WY =    (0.76 HWE as-is)(70% BHY)

        Working Yield of C20 = 0.49
        WY =    (0.70 HWE as-is)(70% BHY)

        Lbs of 2-Row = 11.04 pounds
        Lbs malt = (6.15Lbs extract)(95% Extract) / 0.53 WY

        Lbs of C20 = 0.63 pounds
        Lbs malt = (6.15 Lbs extract)(5% Extract) / 0.49 WY

        Total Grain Weight = 11.67 pounds

        Strike Temperature = 164 degrees F
        Strike Temp =  [((0.4)(152 T mash- 60 T malt)) / 3 L:G] +  152 T mash

        Mash Water Volume = 4.2 Gallons
        gallons H2O =  (11.67 Lbs malt)(3 L:G)(1gallon H2O) / 8.32 pounds water

        Centennial Hops = 0.0.57 oz
        Ounces hops = (40 IBU Target)(5 galbeer)(95% IBU) / (14% a-acid)(32% Utilization)(7489)

        Cascade Hops = 0.76 oz
        Ounces hops = (40 IBU Target)(5 galbeer)(5% IBU) / (7% a-acid)(2.5% Utilization)(7489)

        Color of Wort = 5.07 degrees Lovibond
        Color of Wort 2Row = (95% extract)(2L of malt)(14P wort / 8P reference) = 3.32
        Color of Wort C10 = (5% extract)(20L of malt)(14P wort / 8P reference) = 1.75
        (3.32 + 1.75 = 5.07)

        Color of Beer = 3.5 degrees Lovibond
        Color of Beer = (5.07 color of wort)(1 - 30% color loss)

        If you make this recipe, add one ounce of Cascade in the sedondary for an excellent dry hop aroma!
        """  # nopep8
        og = self.get_original_gravity()
        bg = self.get_boil_gravity()
        fg = self.get_final_gravity()
        abv = alcohol_by_volume_standard(og, fg)
        extract_weight = self.get_extract_weight()
        total_wort_color = self.get_total_wort_color()
        beer_color = self.get_beer_color()
        total_grain_weight = self.get_total_grain_weight()
        total_ibu = self.get_total_ibu()

        print(textwrap.dedent("""\
            {name}
            -----------------------------------
            Start Volume:       {start_volume:0.1f}
            Final Volume:       {final_volume:0.1f}
            Original Gravity:   {og:0.3f}
            Boil Gravity:       {bg:0.3f}
            Final Gravity:      {fg:0.3f}
            ABV Standard:       {abv:0.2f} %
            Yeast Attenuation:  {yeast_attenuation:0.2f} %
            Extract Weight:     {extract_weight:0.2f} {weight_large}
            Total Grain Weight: {total_grain_weight:0.2f} {weight_large}
            Total IBU:          {total_ibu:0.2f} ibu
            Total Wort Color:   {total_wort_color:0.2f} degL
            Beer Color SRM:     {beer_color_srm:0.2f} degL
            Beer Color EBC:     {beer_color_ebc:0.2f} degL
            """.format(name=string.capwords(self.name),
                       start_volume=self.start_volume,
                       final_volume=self.final_volume,
                       og=og,
                       bg=bg,
                       fg=fg,
                       abv=abv,
                       yeast_attenuation=self.yeast_attenuation,
                       extract_weight=extract_weight,
                       total_grain_weight=total_grain_weight,
                       total_ibu=total_ibu,
                       total_wort_color=total_wort_color,
                       beer_color_srm=beer_color,
                       beer_color_ebc=srm_to_ebc(beer_color),
                       **self.types
                       )))

        for grain_add in self.grain_additions:
            wy = grain_add.grain.get_working_yield(self.percent_brew_house_yield)  # nopep8
            grain_weight = grain_add.weight
            lme_weight = grain_to_liquid_malt_weight(grain_weight)
            dry_weight = liquid_to_dry_malt_weight(
                    lme_weight)
            wort_color = self.get_wort_color(grain_add)
            print(grain_add.format())
            print(textwrap.dedent("""\
                    Working Yield:     {wy:0.2f} %
                    Weight DME:        {dry_weight:0.2f} {weight_large}
                    Weight LME:        {lme_weight:0.2f} {weight_large}
                    Weight Grain:      {grain_weight:0.2f} {weight_large}
                    Color:             {wort_color:0.2f} degL
                    """.format(wy=wy,
                               dry_weight=dry_weight,
                               lme_weight=lme_weight,
                               grain_weight=grain_weight,
                               wort_color=wort_color,
                               **self.types
                               )))

        for hop in self.hop_additions:
            ibus = hop.get_ibus(bg, self.final_volume)
            utilization = hop.utilization_cls.get_percent_utilization(
                    bg, hop.boil_time)
            print(hop.format())
            print(textwrap.dedent("""\
                    IBUs:         {ibus:0.2f}
                    Utilization:  {utilization:0.2f} %
                    """.format(ibus=ibus,
                               utilization=utilization,
                               **self.types
                               )))
