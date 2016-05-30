

def fahrenheit_to_celsius(temp):
    """
    Convert degrees Fahrenheit  to degrees Celsius
    """
    return (temp - 32.0) / 1.8


def celsius_to_fahrenheit(temp):
    """
    Convert degrees Celsius to degrees Fahrenheit
    """
    return(temp * 1.8) + 32.0


def plato_to_sg(deg_plato):
    """
    Specific Gravity (S.G.)
    S.G. is the density of a liquid or solid compared to that of water.
    The simple formula for S.G. is:

    S.G. = 1 + 0.004 x Plato

    The more precise calculation of S.G. is:

    S.G. = [(Plato) / (258.6 - (Plato/258.2 x 227.1))] + 1

    Source:
    http://www.learntobrew.com/page/1mdhe/Shopping/Beer_Calculations.html
    """
    return (deg_plato / (258.6 - ((deg_plato / 258.2) * 227.1))) + 1


def sg_to_plato(sg):
    """
    Plato
    Degrees Plato is the weight of the extract in a 100gram solution at
    64 degrees Fahrenheit.

    Plato = [(S.G. - 1) x 1000] / 4

    The more precise calculation of Plato is:

    Plato = -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3

    Source:
    http://www.brewersfriend.com/2012/10/31/on-the-relationship-between-plato-and-specific-gravity/
    """
    # return (sg - 1.0) * 1000 / 4
    return -616.868 + 1111.14 * sg - 630.272 * sg ** 2 + 135.997 * sg ** 3


def hydrometer_adjustment(sg, temp):
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
    return sg + (correction * 0.001)


def alcohol_by_volume_standard(og, fg):
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


def alcohol_by_volume_alternative(og, fg):
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
