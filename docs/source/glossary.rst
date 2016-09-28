Glossary
========

.. glossary::

    Alpha Acid Units (AAU)
        Defined as ounces of hops * alpha acids

    Boil Volume
        The volume of the wort during the boil.

    Brew House Yield (BHY)
        Brew house yield is a measurement that tells the efficiency of the
        brewing.  The actual degrees Plato from the brew and the actual gallons
        collected out of the kettle are needed to calculate the BHY.

        :math:`\text{BHY} = \frac{\text{Pactual} \times \text{galactual} \times \text{BHYtarget}}{\text{Ptarget} \times \text{galtarget}}`

    Cereal
        A type of whole grain used for brewing.

    DME
        Dry Malt Extract

    Final Volume
        The volume of the wort at the finish of the boil.

    Gravity Units (GU)
        The gravity units of a recipe is defined as the total points of the
        recipe (as measured in PPG or HWE depending on units) divided by the
        volume of the wort.

        :math:`\text{GU} = \text{PPG} \div \text{Wort Volume}`

    Hot Water Extract
        The international unit for the total soluble
        extract of a malt, based on specific gravity. HWE is measured as
        liter*degrees per kilogram, and is equivalent to
        points/pound/gallon (PPG) when you apply metric conversion factors
        for volume and weight. The combined conversion factor is:

        :math:`\text{HWE} = 8.3454 \times \text{PPG}`

    International Bitterness Units (IBUs)
        IBUs or International Bittering Units measures a bitterness unit for hops.
        IBUs are the measurement in parts per million (ppm) of iso-alpha acids
        in the beer.   For example, an IPA with 75 IBUs has 75 milligrams of
        isomerized alpha acids per liter. The equation used to calculate the
        weight of hops for the boil is as follows.

        :math:`\text{Ounces hops} = \frac{\text{IBU Target} \times \text{galbeer} \times \text{IBU%}}{\text{%a-acid} \times \text{%Utilization} \times 7489}`

        The IBU target equals the total bitterness for the beer.  (e.g. an IPA
        may have an IBU target of 75 IBUs)  The percent IBU is equal to the
        percent of IBUs from each hop addition.  You may wish for your first hop
        addition to contribute 95% of the total IBUs.  This would make your
        IBU% 95%.  The %a-acid is the amount of alpha acid in the hops and can
        be found on the hop packaging.  The % Utilization is a measurement of
        the percentage of alpha acid units that will isomerize in the boil.
        The following chart outlines the typical utilizations and hop boil times.

        ========= ===========
        Boil Time Utilization
        ========= ===========
        60 min    30%
        30 min    15%
        5  min    2.5%
        ========= ===========

        The 7489 is a conversion factor and used to cancel the units in the
        equation, converting oz/gallon to mg/l. For the hops equation, the
        units for the % must be expressed in decimal form.  (e.g. 10%= .10)

        Source:

        * http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html

    LME
        Liquid Malt Extract

    Malt Color Units (MCU)
        The color of malt as a function of weight, beer color, and wort volume.

        :math:`\text{MCU} = \frac{\text{grain weight} \times \text{beer color in SRM}}{\text{wort volume}}`

    Mash Water Volume
        To calculate the mash water volume you will need to know your liquor to
        grist ratio.  The term liquor refers to the mash water and grist refers
        to the milled malt.  We need to calculate the appropriate amount of
        water to allow for enzyme action and starch conversion take place.

        :math:`\text{gallons H2O} = \frac{\text{Lbs malt} \times \text{L:G} \times \text{1 gallon H2O}}{\text{8.32 pounds water}}`

    Original Volume
    Start Volume
        The volume of the wort at the beginning of the process.

    Specific Gravity
        The ratio of the density of the wort against the density of water.

    Standard Reference Method (SRM)
        SRM is the standard unit of measure of the color of beer

    Strike Water
        As you know when you are mashing, your strike water has to be warmer
        than the target mash temperature because the cool malt will cool the
        temperature of the water.  To correctly calculate the temperature of
        the strike water, use the following formula.

        :math:`\text{Strike Temp} = \frac{0.4 \times \big(\text{T mash} - \text{T malt}\big)}{L:G} + \text{T mash}`

    Weight of Extract
        The weight of extract is the amount of malt extract present in the
        wort.

        :math:`\text{Lbs extract} = \text{density of water} \times \text{gal of wort} \times \text{SG} \times \frac{P}{100}`

        The weight of one gallon of water in the above formula is 8.32 lbs/gal

        To find the weight of a gallon of wort, multiply the specific gravity
        of the wort by the density of water.

        Plato is a percentage of sugars by weight.  So 10 Plato means solution
        is 10% sugars.  In this equation we convert the degrees plato to a
        decimal number between 0.0 and 1.0 by dividing it by 100.  This is
        multiplied by the  weight of a gallon of wort.

    Working Yield
        The product of the Hot Water Extract multiplied by the
        Brew House Yield.  This product will provide the percent of extract
        collected from the malt.

        :math:`WY = \text{HWE as-is} \times \text{BHY}`

    Wort Color
        The color of the wort

        :math:`\text{Color of Wort} = \text{S} \times \text{% extract} \times \text{L of malt} \times \frac{\text{P wort}}{\text{8P reference}}`

        Source:

        * http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
        * http://brewwiki.com/index.php/Estimating_Color
