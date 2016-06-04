
from brew.utilities import sg_from_dry_basis


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
    mc = 4
    bhe = 0.9

    chart = []
    for dbcg in range(5000, 7600, 100) + range(7600, 8025, 25):
        gu = sg_from_dry_basis(
                dbcg / 100.0,
                moisture_content=mc,
                brew_house_efficiency=bhe)
        sg = 1 + (gu / 1000.0)
        chart.append([round(dbcg / 100.0, 2), round(gu, 2), round(sg, 4)])
    return chart


def print_chart():
    chart = get_chart()
    print("DBCG\tGU\t1 lb./gallon")
    print("'As-Is'\t\tYields SG")
    print("-------\t-----\t------------")
    for dbcg, gu, sg in chart:
        print("{0:0.2f}\t{1:0.2f}\t{2:0.4f}".format(dbcg, gu, sg))


def main():
    print_chart()


if __name__ == "__main__":
    main()
