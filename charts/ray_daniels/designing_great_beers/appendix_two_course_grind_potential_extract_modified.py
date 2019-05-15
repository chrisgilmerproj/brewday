#! /usr/bin/env python

from brew.utilities.malt import sg_from_dry_basis
from brew.utilities.sugar import sg_to_gu


"""
Ray Daniels
Designing Great Beers

Appendix 2: Course Grind Potential Extract (modified)

Notes:
    The chart appears to have been developed with the moisture content set
    to zero (0.0) and the Brew House Efficiency set to 100% (1.0).  This
    is not typical and the book even states that you should expect moisture
    content at around 4.0% and Brew House Efficiency at arount 90.0%.

This version has been modified with more typical values.
"""


def get_chart():
    mc = 0.04
    bhe = 0.9

    chart = []
    for dbcg in range(5000, 7600, 100) + range(7600, 8025, 25):
        sg = sg_from_dry_basis(
            dbcg / 10000.0, moisture_content=mc, brew_house_efficiency=bhe
        )
        gu = sg_to_gu(sg)
        chart.append([round(dbcg / 100.0, 2), round(gu, 2), round(sg, 4)])
    return chart


def print_chart():
    chart = get_chart()
    print(u"DBCG\tGU\t1 lb./gallon")
    print(u"'As-Is'\t\tYields SG")
    print(u"-------\t-----\t------------")
    for dbcg, gu, sg in chart:
        print(u"{0:0.2f}\t{1:0.2f}\t{2:0.4f}".format(dbcg, gu, sg))


def main():
    print_chart()


if __name__ == "__main__":
    main()
