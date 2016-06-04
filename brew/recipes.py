#! /usr/bin/python

import string
import textwrap

from .constants import IMPERIAL_UNITS
from .constants import SI_UNITS
from .utilities import sg_to_plato


class Recipe(object):
    """
    Learn to Brew Website:
    http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """

    def __init__(self, name='beer',
                 grain_additions=None,
                 hop_additions=None,
                 percent_brew_house_yield=70.0,
                 start_volume=7.0,
                 final_volume=5.0,
                 target_sg=None,
                 target_ibu=None,
                 units=IMPERIAL_UNITS):
        self.name = name
        self.grain_additions = grain_additions
        self.hop_additions = hop_additions

        self.percent_brew_house_yield = percent_brew_house_yield  # %
        self.start_volume = start_volume  # G
        self.final_volume = final_volume  # G
        self.target_sg = target_sg  # SG
        self.target_degrees_plato = sg_to_plato(self.target_sg)  # P

        self.target_ibu = target_ibu

        # TODO: Make this work
        # US = Gallons, degF
        # Metric = Liters, degC
        if units not in [IMPERIAL_UNITS, SI_UNITS]:
            self.units = IMPERIAL_UNITS
        else:
            self.units = units

    def __str__(self):
        return self.name

    def get_total_gravity_units(self):
        return ((self.target_sg - 1.0) * 1000) * self.final_volume

    def get_starting_sg(self):
        total_gu = self.get_total_gravity_units()
        starting_gu = total_gu / self.start_volume
        return 1.0 + starting_gu / 1000

    def get_starting_plato(self):
        return sg_to_plato(self.get_starting_sg())

    def get_brew_house_yield(self, plato_actual, vol_actual):
        """
        Brew House Yield (BHY)
        Brew house yield is a measurement that tells the efficiency of the
        brewing.  The actual degrees Plato from the brew and the actual gallons
        collected out of the kettle are needed to calculate the BHY.

        BHY  =  [(Pactual)(galactual)(BHYtarget)] / [(Ptarget)(galtarget)]

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        num = plato_actual * vol_actual * self.percent_brew_house_yield
        den = self.target_degrees_plato * self.final_volume
        return num / den

    def get_extract_weight(self):
        """
        Weight of Extract
        The weight of extract is the amount of malt extract present in the
        wort.

        Lbs extract =   [(8.32 pounds/gal wort)(gal wort)(S.G.)(P)] / 100

        8.32 in the above formula is the weight of one gallon of water.
        To find the weight of a gallon of wort, multiply the specific gravity
        of the wort by 8.32 pounds.

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (8.32 * self.final_volume * self.target_sg *
                self.target_degrees_plato) / 100.0

    def get_working_yield(self, grain_add):
        """
        Working Yield
        Working Yield is the product of the Hot Water Extract multiplied by the
        Brew House Yield.  This product will provide the percent of extract
        collected from the malt.

        WY =    (HWE as-is)(BHY)

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return grain_add.grain.hot_water_extract * self.percent_brew_house_yield

    def get_pounds_malt(self, grain_add):
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

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (self.get_extract_weight() * grain_add.percent_extract /
                self.get_working_yield(grain_add))

    def get_total_grain_weight(self):
        """
        Convenience method to get total grain weight
        """
        return sum([self.get_pounds_malt(g) for g in self.grain_additions])

    def get_total_ibu(self):
        """
        Convenience method to get total IBU
        """
        sg = self.target_sg
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

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return ((((0.4) * (mash_temp - malt_temp)) /
                liquor_to_grist_ratio) + mash_temp)

    def get_mash_water_volume(self, liquor_to_grist_ratio):
        """
        Mash Water Volume
        To calculate the mash water volume you will need to know your liquor to
        grist ratio.  The term liquor refers to the mash water and grist refers
        to the milled malt.  We need to calculate the appropriate amount of
        water to allow for enzyme action and starch conversion take place.

        gallons H2O =  (Lbs malt)(L:G)(1gallon H2O) / 8.32 pounds water

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (self.get_total_grain_weight() * liquor_to_grist_ratio /
                8.32)

    def get_wort_color(self, grain_add):
        """
        Calculation of Wort and Beer Color

        Color of Wort = S [(% extract)(L of malt)(P wort / 8P reference)]

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return ((grain_add.percent_extract / 100.0) * grain_add.grain.color *
                (self.target_degrees_plato / 8))

    def get_total_wort_color(self):
        """
        Convenience method to get total wort color
        """
        return sum([self.get_wort_color(g) for g in self.grain_additions])

    def get_beer_color(self, percent_color_loss=30.0):
        """
        We allow for a 30% loss of color during fermentation to calculate the color of beer.
        Color of Beer = (color of wort)(1 - % color loss)

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        # nopep8
        """
        return (self.get_total_wort_color() *
                (1.0 - percent_color_loss / 100.0))

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

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html  # nopep8
        """
        sg = self.target_sg
        deg_plato = self.target_degrees_plato
        pounds_extract = self.get_extract_weight()
        total_wort_color = self.get_total_wort_color()
        beer_color = self.get_beer_color()
        total_grain_weight = self.get_total_grain_weight()
        total_ibu = self.get_total_ibu()

        print(textwrap.dedent("""\
            {0}
            -----------------------------------
            Specific Gravity:   {1:0.3f}
            Degrees Plato:      {2:0.3f} degP
            Extract Weight:     {3:0.2f} lbs
            Total Grain Weight: {4:0.2f} lbs
            Total IBU:          {5:0.2f} ibu
            Total Wort Color:   {6:0.2f} degL
            Beer Color:         {7:0.2f} degL
            """.format(string.capwords(self.name),
                       sg,
                       deg_plato,
                       pounds_extract,
                       total_grain_weight,
                       total_ibu,
                       total_wort_color,
                       beer_color)))

        for grain_add in self.grain_additions:
            wy = self.get_working_yield(grain_add)
            pounds_lme = self.get_pounds_malt(grain_add)
            pounds_dry = grain_add.grain.get_liquid_to_dry_malt_weight(
                    pounds_lme)
            pounds_grain = grain_add.grain.get_liquid_malt_to_grain_weight(
                    pounds_lme)
            wort_color = self.get_wort_color(grain_add)
            print(grain_add.format())
            print(textwrap.dedent("""\
                    Working Yield:     {0:0.2f} %
                    Weight DME:        {1:0.2f} lbs
                    Weight LME:        {2:0.2f} lbs
                    Weight Grain:      {3:0.2f} lbs
                    Color:             {4:0.2f} degL
                    """.format(wy,
                               pounds_dry,
                               pounds_lme,
                               pounds_grain,
                               wort_color)))

        for hop in self.hop_additions:
            hops_weight = hop.get_hops_weight(sg,
                                              self.target_ibu,
                                              self.final_volume)
            ibus = hop.get_ibus(sg, self.final_volume)
            utilization = hop.utilization_cls.get_percent_utilization(
                    sg, hop.boil_time) * 100.0
            print(hop.format())
            print(textwrap.dedent("""\
                    Weight:       {0:0.2f} oz
                    IBUs:         {1:0.2f}
                    Utilization:  {2:0.2f} %
                    """.format(hops_weight,
                               ibus,
                               utilization)))

        self.hop_additions[0].utilization_cls.print_utilization_table()
