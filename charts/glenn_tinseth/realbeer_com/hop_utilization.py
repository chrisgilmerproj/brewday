#! /usr/bin/env python

from brew.hops import HopsUtilizationGlennTinseth


"""
This recreates Glenn Tinseth's Hop Utilization table from
http://realbeer.com/hops/research.html
"""


def main():
    HopsUtilizationGlennTinseth.print_utilization_table()


if __name__ == "__main__":
    main()
