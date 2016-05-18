#! /usr/bin/python

import math
import string


def fahrenheit_to_celsius(temp):
    return (temp - 32.0) / 1.8


def celsius_to_fahrenheit(temp):
    return(temp * 1.8) + 32.0


class Beer(object):
    """
    Learn to Brew Website:
    http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """

    def __init__(self, name='beer',
                 grain_list=None,
                 hop_list=None,
                 percent_brew_house_yield=70.0,
                 gallons_of_beer=5.0,
                 target_degrees_plato=None,
                 mash_temp=None,
                 malt_temp=None,
                 liquor_to_grist_ratio=3.0 / 1.0,
                 percent_color_loss=30.0,
                 target_ibu=None,
                 units='us'):
        self.name = name
        self.grain_list = grain_list
        self.hop_list = hop_list
        self.percent_brew_house_yield = percent_brew_house_yield  # %
        self.gallons_of_beer = gallons_of_beer  # G
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
        """
        Specific Gravity (S.G.)
        S.G. is the density of a liquid or solid compared to that of water.
        The simple formula for S.G. is:

        S.G. = 1 + 0.004 x Plato

        The more precise calculation of S.G. is:

        S.G. = [(Plato) / (258.6 - (Plato/258.2 x 227.1))] + 1

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (self.target_degrees_plato / (258.6 - ((self.target_degrees_plato / 258.2) * 227.1))) + 1

    def get_degrees_plato(self):
        """
        Plato
        Degrees Plato is the weight of the extract in a 100gram solution at 64 degrees Fahrenheit.

        Plato = [(S.G. - 1) x 1000] / 4

        The more precise calculation of Plato is:

        Plato = -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3

        Source: http://www.brewersfriend.com/2012/10/31/on-the-relationship-between-plato-and-specific-gravity/
        """
        sg = self.get_specific_gravity()
        # return (sg - 1.0) * 1000 / 4
        return -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3

    def get_brew_house_yield(self, plato_actual, gal_actual):
        """
        Brew House Yield (BHY)
        Brew house yield is a measurement that tells the efficiency of the
        brewing.  The actual degrees Plato from the brew and the actual gallons
        collected out of the kettle are needed to calculate the BHY.

        BHY  =  [(Pactual)(galactual)(BHYtarget)] / [(Ptarget)(galtarget)]

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return ((plato_actual)(gal_actual)(self.percent_brew_house_yield)) / ((self.target_degrees_plato)(self.gallons_of_beer))

    def get_extract_weight(self):
        """
        Weight of Extract
        The weight of extract is the amount of malt extract present in the wort.

        Lbs extract =   [(8.32 pounds/gal wort)(gal wort)(S.G.)(P)] / 100

        8.32 in the above formula is the weight of one gallon of water.
        To find the weight of a gallon of wort, multiply the specific gravity
        of the wort by 8.32 pounds.

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (8.32 * self.gallons_of_beer * self.get_specific_gravity() * self.target_degrees_plato) / 100.0

    def get_working_yield(self, grain):
        """
        Working Yield
        Working Yield is the product of the Hot Water Extract multiplied by the
        Brew House Yield.  This product will provide the percent of extract
        collected from the malt.

        WY =    (HWE as-is)(BHY)

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return grain.hot_water_extract * self.percent_brew_house_yield

    def get_pounds_malt(self, grain):
        """
        Pounds of Malt
        It is imperative that you measure your recipes by the percent of extract
        taken from the malt rather than the weight of the malt.  Do this will
        all you to compensate for the Working Yield and help you accurately
        measure your malt bills.  For example, an recipe may call for 5% of
        caramel 20.  This does not me that you ad 0.5 pounds of caramel 20 malt
        in a 10 lb recipe. Instead, this means that you will have 5% of the
        total extract come from the caramel 20 malt.  Use the following formula
        to calculate the weight of malt based on a percent of extract.

        Lbs malt = (Lbs extract)(% Extract) / WY

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return self.get_extract_weight() * grain.percent_extract / self.get_working_yield(grain)

    def get_total_grain_weight(self):
        """
        Convenience method to get total grain weight
        """
        return sum([self.get_pounds_malt(g) for g in self.grain_list])

    def get_strike_temp(self):
        """
        Strike Water Temp
        As you know when you are mashing, your strike water has to be warmer
        than the target mash temperature because the cool malt will cool the
        temperature of the water.  To correctly calculate the temperature of
        the strike water, use the following formula.

        Strike Temp =  [((0.4)(T mash-T malt)) / L:G] +  T mash

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (((0.4) * (self.mash_temp - self.malt_temp)) / self.liquor_to_grist_ratio) + self.mash_temp

    def get_mash_water_volume(self):
        """
        Mash Water Volume
        To calculate the mash water volume you will need to know your liquor to
        grist ratio.  The term liquor refers to the mash water and grist refers
        to the milled malt.  We need to calculate the appropriate amount of
        water to allow for enzyme action and starch conversion take place.

        gallons H2O =  (Lbs malt)(L:G)(1gallon H2O) / 8.32 pounds water

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return self.get_total_grain_weight() * self.liquor_to_grist_ratio / 8.32

    def get_hops_weight(self, hop):
        """
        Weight of Hops
        IBUs or International Bittering Units measures a bitterness unit for hops.
        IBUs are the measurement in parts per million (ppm) of iso-alpha acids
        in the beer.   For example, an IPA with 75 IBUs has 75 milligrams of
        isomerized alpha acids per liter. The equation used to calculate the
        weight of hops for the boil is as follows.

        Ounces hops = (IBU Target)(galbeer)(IBU%) / (%a-acid)(%Utilization)(7494)

        The IBU target equals the total bitterness for the beer.  (e.g. an IPA
        may have an IBU target of 75 IBUs)  The percent IBU is equal to the
        percent of IBUs from each hop addition.  You may wish for your first hop
        addition to contribute 95% of the total IBUs.  This would make your
        IBU% 95%.  The %a-acid is the amount of alpha acid in the hops and can
        be found on the hop packaging.  The % Utilization is a measurement of
        the percentage of alpha acid units that will isomerize in the boil.
        The following chart outlines the typical utilizations and hop boil times.

        60 min = 30% utilization
        30 min = 15%
        5   min = 2.5%

        The 7494 is a conversion factor and used to cancel the units in the
        equation. For the hops equation, the units for the % must be expressed
        in decimal form.  (e.g. 10%= .10)

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return (self.target_ibu * self.gallons_of_beer * (hop.percent_contribution / 100.0)) / ((hop.percent_alpha_acids / 100.0) * (hop.percent_utilization / 100.0) * 7494)

    def get_wort_color(self, grain):
        """
        Calculation of Wort and Beer Color

        Color of Wort = S [(% extract)(L of malt)(P wort / 8P reference)]

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        return grain.percent_extract / 100.0 * grain.color * self.target_degrees_plato / 8

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
        """
        return self.get_total_wort_color() * (1.0 - self.percent_color_loss / 100.0)

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
        Ounces hops = (40 IBU Target)(5 galbeer)(95% IBU) / (14% a-acid)(32% Utilization)(7494)

        Cascade Hops = 0.76 oz
        Ounces hops = (40 IBU Target)(5 galbeer)(5% IBU) / (7% a-acid)(2.5% Utilization)(7494)

        Color of Wort = 5.07 degrees Lovibond
        Color of Wort 2Row = (95% extract)(2L of malt)(14P wort / 8P reference) = 3.32
        Color of Wort C10 = (5% extract)(20L of malt)(14P wort / 8P reference) = 1.75
        (3.32 + 1.75 = 5.07)

        Color of Beer = 3.5 degrees Lovibond
        Color of Beer = (5.07 color of wort)(1 - 30% color loss)

        If you make this recipe, add one ounce of Cascade in the sedondary for an excellent dry hop aroma!

        Source: http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
        """
        sg = self.get_specific_gravity()
        deg_plato = self.get_degrees_plato()
        pounds_extract = self.get_extract_weight()
        strike_temp = self.get_strike_temp()
        mash_water_vol = self.get_mash_water_volume()
        total_wort_color = self.get_total_wort_color()
        beer_color = self.get_beer_color()
        total_grain_weight = self.get_total_grain_weight()

        print
        print string.capwords(self.name)
        print '-' * len(self.name)
        print 'Specific Gravity:   {:0.3f}'.format(sg)
        print 'Degrees Plato:      {:0.3f} degP'.format(deg_plato)
        print 'Extract Weight:     {:0.2f} lbs'.format(pounds_extract)
        print 'Strike Temperature: {:0.2f} degF'.format(strike_temp)
        print 'Mash Water Volume:  {:0.2f} gallons'.format(mash_water_vol)
        print 'Total Grain Weight: {:0.2f} lbs'.format(total_grain_weight)
        print 'Total Wort Color:   {0:0.2f} degL'.format(total_wort_color)
        print 'Beer Color:         {0:0.2f} degL'.format(beer_color)
        print

        for grain in self.grain_list:
            wy = self.get_working_yield(grain)
            pounds_lme = self.get_pounds_malt(grain)
            pounds_dry = grain.get_liquid_to_dry_malt_weight(pounds_lme)
            pounds_grain = grain.get_liquid_malt_to_grain_weight(pounds_lme)
            wort_color = self.get_wort_color(grain)
            print grain.format()
            print 'Working Yield:     {0:0.2f} %'.format(wy)
            print 'Weight DME:        {0:0.2f} lbs'.format(pounds_dry)
            print 'Weight LME:        {0:0.2f} lbs'.format(pounds_lme)
            print 'Weight Grain:      {0:0.2f} lbs'.format(pounds_grain)
            print 'Color:             {0:0.2f} degL'.format(wort_color)
            print

        for hop in self.hop_list:
            hops_weight = self.get_hops_weight(hop)
            ibus = self.get_ibu_real_beer(hop)
            utilization = hop.get_percent_utilization(sg, hop.boil_time)
            print hop.format()
            print 'Weight:       {0:0.2f} oz'.format(hops_weight)
            print 'IBUs:         {0:0.2f}'.format(ibus)
            print 'Utilization:  {0:0.2f} %'.format(utilization)
            print

        # self.hop_list[0].print_utilization_table()

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

        Source: http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
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

        Source: http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
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
        """
        correction = 1.313454 - 0.132674 * (temp ** 1) + \
                    (2.057793 * 10 ** -3) * (temp ** 2) - \
                    (2.627634 * 10 ** -6) * (temp ** 3)
        return self.get_specific_gravity() + (correction * 0.001)

    def get_ibu_jackie_rager(self, hop):
        """
        Source: http://www.rooftopbrew.net/ibu.php
        """
        woz = self.get_hops_weight(hop)
        return (woz * (hop.percent_utilization / 100.0) * (hop.percent_alpha_acids / 100.0) * 7489) / (self.gallons_of_beer * self.get_specific_gravity())

    def get_ibu_glenn_tinseth(self, hop):
        """
        Source: http://www.rooftopbrew.net/ibu.php
        """
        #woz = self.get_hops_weight(hop)

    def get_ibu_real_beer(self, hop):
        """
        Source: http://www.realbeer.com/hops/research.html
        """
        woz = self.get_hops_weight(hop)
        return (woz * (hop.percent_utilization / 100.0) * (hop.percent_alpha_acids / 100.0) * 7490) / (self.gallons_of_beer * self.get_specific_gravity())


class Grain(object):

    def __init__(self, name=None,
                 short_name=None,
                 color=None,
                 hot_water_extract=None,
                 percent_extract=None):
        self.name = name
        self.short_name = short_name or name
        self.color = color
        self.hot_water_extract = hot_water_extract
        self.percent_extract = percent_extract

    def __repr__(self):
        return self.name

    def format(self):
        msg = """{0} Grain
{1}
Color:             {2} degL
Hot Water Extract: {3}
Extract:           {4} %""".format(string.capwords(self.name),
                                   '-' * (len(self.name) + 6),
                                   self.color,
                                   self.hot_water_extract,
                                   self.percent_extract)
        return msg

    @classmethod
    def get_dry_to_liquid_malt_weight(cls, malt):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return malt * 1.25

    @classmethod
    def get_liquid_to_dry_malt_weight(cls, malt):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return malt * 1.0 / 1.25

    @classmethod
    def get_grain_to_liquid_malt_weight(cls, grain):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return grain * 0.75

    @ classmethod
    def get_liquid_malt_to_grain_weight(cls, malt):
        return malt * 1.0 / 0.75

    @classmethod
    def get_specialty_grain_to_liquid_malt_weight(cls, grain):
        """
        Source: http://www.weekendbrewer.com/brewingformulas.htm
        """
        return grain * 0.89

    @classmethod
    def get_liquid_malt_to_specialty_grain_weight(cls, malt):
        return malt * 1.0 / 0.89


class Hop(object):

    def __init__(self, name=None,
                 short_name=None,
                 boil_time=None,
                 percent_alpha_acids=None,
                 percent_ibus=None,
                 percent_utilization=None,
                 percent_contribution=None):
        self.name = name
        self.short_name = short_name or name
        self.boil_time = boil_time
        self.percent_alpha_acids = percent_alpha_acids
        self.percent_ibus = percent_ibus
        self.percent_utilization = percent_utilization
        self.percent_contribution = percent_contribution

    def __repr__(self):
        return "{0}, alpha {1}%".format(self.name.capitalize(),
                                        self.percent_alpha_acids)

    def format(self):
        msg = """{0} Hops
{1}
Alpha Acids:  {2} %
IBUs:         {3} %
Utilization:  {4} %
Contribution: {5} %
Boil Time:    {6} min""".format(string.capwords(self.name),
                                '-' * (len(self.name) + 6),
                                self.percent_alpha_acids,
                                self.percent_ibus,
                                self.percent_utilization,
                                self.percent_contribution,
                                self.boil_time,)
        return msg

    @classmethod
    def get_bigness_factor(cls, sg):
        """
        Source: http://www.realbeer.com/hops/research.html
        """
        return 1.65 * 0.000125 ** (sg - 1)

    @classmethod
    def get_boil_time_factor(cls, boil_time):
        """
        Source: http://www.realbeer.com/hops/research.html
        """
        return (1 - math.exp(-0.04 * boil_time)) / 4.15

    @classmethod
    def get_percent_utilization(cls, sg, boil_time):
        """
        The Bigness factor accounts for reduced utilization due to higher wort
        gravities. Use an average gravity value for the entire boil to account
        for changes in the wort volume.

        Bigness factor = 1.65 * 0.000125^(wort gravity - 1)

        The Boil Time factor accounts for the change in utilization due to
        boil time:

        Boil Time factor = (1 - e^(-0.04 * time in mins)) / 4.15

        Source: http://www.realbeer.com/hops/research.html
        """
        bigness_factor = cls.get_bigness_factor(sg)
        boil_time_factor = cls.get_boil_time_factor(boil_time)
        return bigness_factor * boil_time_factor * 100

    @classmethod
    def print_utilization_table(cls):
        """
        Percent Alpha Acid Utilization - Boil Time vs Wort Original Gravity

        Source: http://www.realbeer.com/hops/research.html
        """
        boil_time_list = range(0, 60, 3) + range(60, 130, 10)
        gravity_list = range(1030, 1140, 10)

        title = 'Percent Alpha Acid Utilization - Boil Time vs Wort Original Gravity'
        size = 92
        print title.center(size)
        print str('=' * len(title)).center(size)
        print
        print ' '.join([' ' * 4] + ['{0:7.3f}'.format(l/1000.0) for l in gravity_list])
        print '-' * size
        for boil_time in boil_time_list:
            line = []
            line.append(str(boil_time).rjust(4))
            for sg in gravity_list:
                aau = cls.get_percent_utilization(sg / 1000.0, boil_time)
                line.append('{0:7.3f}'.format(aau))
            print ' '.join([item for item in line])
        print


if __name__ == "__main__":

    # Define Grains
    pale = Grain(name='pale 2-row',
                 short_name='2-row',
                 hot_water_extract=0.76,
                 color=2.0,
                 percent_extract=95.0)
    crystal = Grain(name='crystal C20',
                    short_name='C20',
                    hot_water_extract=0.70,
                    color=20.0,
                    percent_extract=5.0)
    grain_list = [pale, crystal]

    # Define Hops
    centennial = Hop(name='centennial',
                     boil_time=60.0,
                     percent_alpha_acids=14.0,
                     percent_ibus=80.0,
                     percent_utilization=32.0,
                     percent_contribution=95.0)
    cascade = Hop(name='cascade',
                  boil_time=5.0,
                  percent_alpha_acids=7.0,
                  percent_ibus=20.0,
                  percent_utilization=2.5,
                  percent_contribution=5.0)
    hop_list = [centennial, cascade]

    # Define Beer
    beer = Beer(name='pale ale',
                grain_list=grain_list,
                hop_list=hop_list,
                percent_brew_house_yield=70.0,  # %
                gallons_of_beer=5.0,  # G
                target_degrees_plato=14.0,  # P
                mash_temp=152.0,  # F
                malt_temp=60.0,  # F
                liquor_to_grist_ratio=3.0 / 1.0,
                percent_color_loss=30.0,  # %
                target_ibu=40.0)

    beer.format()
