

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
