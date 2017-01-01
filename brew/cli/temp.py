# -*- coding: utf-8 -*-
import argparse
import sys

from brew.utilities.temperature import celsius_to_fahrenheit
from brew.utilities.temperature import fahrenheit_to_celsius


def get_temp_conversion(fahrenheit, celsius):
    """
    Convert temperature between fahrenheit and celsius
    """
    if fahrenheit:
        return round(fahrenheit_to_celsius(fahrenheit), 1)
    elif celsius:
        return round(celsius_to_fahrenheit(celsius), 1)


def get_parser():
    parser = argparse.ArgumentParser(description=u'Temperature Conversion')
    parser.add_argument(u'-c', u'--celsius', metavar=u'C', type=float,
                        help=u'Temperature in Celsius')
    parser.add_argument(u'-f', u'--fahrenheit', metavar=u'F', type=float,
                        help=u'Temperature in Fahrenheit')
    return parser


def main(parser_fn=get_parser, parser_kwargs=None):
    parser = None
    if not parser_kwargs:
        parser = parser_fn()
    else:
        parser = parser_fn(**parser_kwargs)
    args = parser.parse_args()
    if args.fahrenheit and args.celsius:
        print(u"Must provide only one of Fahrenheit or Celsius")
        sys.exit(1)
    elif not (args.fahrenheit or args.celsius):
        print(u"Must provide one of Fahrenheit or Celsius")
        sys.exit(1)
    out = get_temp_conversion(args.fahrenheit, args.celsius)
    print(out)


if __name__ == "__main__":
    main()
