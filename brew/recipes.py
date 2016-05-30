#! /usr/bin/python

import string

from .utilities import plato_to_sg
from .utilities import sg_to_plato


class Recipe(object):
    """
    Learn to Brew Website:
    http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """

    def __init__(self, name='beer',
                 grain_list=None,
                 hop_additions=None,
                 percent_brew_house_yield=70.0,
                 final_volume=5.0,
                 target_degrees_plato=None,
                 mash_temp=None,
                 malt_temp=None,
                 liquor_to_grist_ratio=3.0 / 1.0,
                 percent_color_loss=30.0,
                 target_ibu=None,
                 units='us'):
        self.name = name
        self.grain_list = grain_list
        self.hop_additions = hop_additions
        self.percent_brew_house_yield = percent_brew_house_yield  # %
        self.final_volume = final_volume  # G
        self.target_degrees_plato = target_degrees_plato  # P
        self.mash_temp = mash_temp  # F
        self.malt_temp = malt_temp  # F
        self.liquor_to_grist_ratio = liquor_to_grist_ratio
        self.percent_color_loss = percent_color_loss  # %
        self.target_ibu = target_ibu

        # TODO: Make this work
        # US = Gallons, degF
        # Metric = Liters, degC
        if units not in ['us', 'metric']:
            self.units = 'us'
        else:
            self.units = units

    def __repr__(self):
        return self.name

    def get_specific_gravity(self):
        return plato_to_sg(self.target_degrees_plato)

    def get_degrees_plato(self):
        return sg_to_plato(self.get_specific_gravity())

    def get_brew_house_yield(self, plato_actual, gal_actual):
        """
        Brew House Yield (BHY)
        Brew house yield is a measurement that tells the efficiency of the
        brewing.  The actual degrees Plato from the brew and the actual gallons
        collected out of the kettle are needed to calculate the BHY.

        BHY  =  [(Pactual)(galactual)(BHYtarget)] / [(Ptarget)(galtarget)]

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        num = plato_actual * gal_actual * self.percent_brew_house_yield
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
        return (8.32 * self.final_volume * self.get_specific_gravity() *
                self.target_degrees_plato) / 100.0

    def get_working_yield(self, grain):
        """
        Working Yield
        Working Yield is the product of the Hot Water Extract multiplied by the
        Brew House Yield.  This product will provide the percent of extract
        collected from the malt.

        WY =    (HWE as-is)(BHY)

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return grain.hot_water_extract * self.percent_brew_house_yield

    def get_pounds_malt(self, grain):
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
        return (self.get_extract_weight() * grain.percent_extract /
                self.get_working_yield(grain))

    def get_total_grain_weight(self):
        """
        Convenience method to get total grain weight
        """
        return sum([self.get_pounds_malt(g) for g in self.grain_list])

    def get_total_ibu(self):
        """
        Convenience method to get total IBU
        """
        sg = self.get_specific_gravity()
        gal = self.final_volume
        return sum([hop_add.get_ibus(sg, gal)
                   for hop_add in self.hop_additions])

    def get_strike_temp(self):
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
        return ((((0.4) * (self.mash_temp - self.malt_temp)) /
                self.liquor_to_grist_ratio) + self.mash_temp)

    def get_mash_water_volume(self):
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
        return (self.get_total_grain_weight() * self.liquor_to_grist_ratio /
                8.32)

    def get_wort_color(self, grain):
        """
        Calculation of Wort and Beer Color

        Color of Wort = S [(% extract)(L of malt)(P wort / 8P reference)]

        Source:
        - http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return ((grain.percent_extract / 100.0) * grain.color *
                (self.target_degrees_plato / 8))

    def get_total_wort_color(self):
        """
        Convenience method to get total wort color
        """
        return sum([self.get_wort_color(g) for g in self.grain_list])

    def get_beer_color(self):
        """
        We allow for a 30% loss of color during fermentation to calculate the color of beer.
        Color of Beer = (color of wort)(1 - % color loss)

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        # nopep8
        """
        return (self.get_total_wort_color() *
                (1.0 - self.percent_color_loss / 100.0))

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
        sg = self.get_specific_gravity()
        deg_plato = self.get_degrees_plato()
        pounds_extract = self.get_extract_weight()
        strike_temp = self.get_strike_temp()
        mash_water_vol = self.get_mash_water_volume()
        total_wort_color = self.get_total_wort_color()
        beer_color = self.get_beer_color()
        total_grain_weight = self.get_total_grain_weight()
        total_ibu = self.get_total_ibu()

        print('\n')
        print(string.capwords(self.name))
        print('-' * len(self.name))
        print('Specific Gravity:   {:0.3f}'.format(sg))
        print('Degrees Plato:      {:0.3f} degP'.format(deg_plato))
        print('Extract Weight:     {:0.2f} lbs'.format(pounds_extract))
        print('Strike Temperature: {:0.2f} degF'.format(strike_temp))
        print('Mash Water Volume:  {:0.2f} gallons'.format(mash_water_vol))
        print('Total Grain Weight: {:0.2f} lbs'.format(total_grain_weight))
        print('Total IBU:          {:0.2f} ibu'.format(total_ibu))
        print('Total Wort Color:   {0:0.2f} degL'.format(total_wort_color))
        print('Beer Color:         {0:0.2f} degL'.format(beer_color))
        print('\n')

        for grain in self.grain_list:
            wy = self.get_working_yield(grain)
            pounds_lme = self.get_pounds_malt(grain)
            pounds_dry = grain.get_liquid_to_dry_malt_weight(pounds_lme)
            pounds_grain = grain.get_liquid_malt_to_grain_weight(pounds_lme)
            wort_color = self.get_wort_color(grain)
            print(grain.format())
            print('Working Yield:     {0:0.2f} %'.format(wy))
            print('Weight DME:        {0:0.2f} lbs'.format(pounds_dry))
            print('Weight LME:        {0:0.2f} lbs'.format(pounds_lme))
            print('Weight Grain:      {0:0.2f} lbs'.format(pounds_grain))
            print('Color:             {0:0.2f} degL'.format(wort_color))
            print('\n')

        for hop in self.hop_additions:
            hops_weight = hop.get_hops_weight(sg,
                                              self.target_ibu,
                                              self.final_volume)
            ibus = hop.get_ibus(sg, self.final_volume)
            utilization = hop.utilization_cls.get_percent_utilization(
                    sg, hop.boil_time) * 100.0
            print(hop.format())
            print('Weight:       {0:0.2f} oz'.format(hops_weight))
            print('IBUs:         {0:0.2f}'.format(ibus))
            print('Utilization:  {0:0.2f} %'.format(utilization))
            print('\n')

        self.hop_additions[0].utilization_cls.print_utilization_table()

    def get_alcohol_by_volume_standard(self, og, fg):
        """
        Most brewing sites use this basic formula:

        ABV = (og - fg) * 131.25

        This equation was created before the computer age.  It is easy to do by
        hand, and over time became the accepted formula for home brewers!

        Variations on this equation which report within tenths of each other
        come from The Joy of Homebrewing Method by Charlie Papazian, Bee Lee's
        Method, Beer Advocate Method. Some variations use 131 instead of 131.25.
        The resulting difference is pretty minor.

        Source:
        - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/  # nopep8
        """
        return (og - fg) * 131.25

    def get_alcohol_by_volume_alternative(self, og, fg):
        """
        Alternate Formula:

        A more complex equation which attempts to provide greater accuracy at higher gravities is:

        ABV =(76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)

        The alternate equation reports a higher ABV for higher gravity beers.
        This equation is just a different take on it. Scientists rarely agree
        when it comes to equations. There will probably be another equation for
        ABV down the road.

        The complex formula, and variations on it come from
        Ritchie Products Ltd, (Zymurgy, Summer 1995, vol. 18, no. 2)
        -Michael L. Hall's article Brew by the Numbers: Add Up What's in Your
        Beer, and Designing Great Beers by Daniels.

        Source:
        - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/  # nopep8
        """
        return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)

    def get_hydrometer_adjustment(self, temp):
        """
        Correction(@59F) = 1.313454 - 0.132674*T + 2.057793e-3*T**2 - 2.627634e-6*T**3
            where T is in degrees F.

        Sources:
        http://www.brewersfriend.com/hydrometer-temp/
        http://merrycuss.com/calc/sgcorrection.html
        http://hbd.org/brewery/library/HydromCorr0992.html
        http://www.primetab.com/formulas.html
        # nopep8
        """
        correction = (1.313454 - 0.132674 * (temp ** 1) +
                      (2.057793 * 10 ** -3) * (temp ** 2) -
                      (2.627634 * 10 ** -6) * (temp ** 3))
        return self.get_specific_gravity() + (correction * 0.001)
