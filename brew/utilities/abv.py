from ..constants import ALCOHOL_SPECIFIC_GRAVITY


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
    - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    """  # nopep8
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
    - http://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    """  # nopep8
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)


def alcohol_by_weight(abv):
    return abv * ALCOHOL_SPECIFIC_GRAVITY
