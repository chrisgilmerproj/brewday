
import argparse
import sys

from brew.utilities.temperature import fahrenheit_to_celsius
from brew.utilities.temperature import celsius_to_fahrenheit


def get_temp_conversion(fahrenheit, celsius):
    """
    Convert temperature between fahrenheit and celsius
    """
    if fahrenheit:
        return round(fahrenheit_to_celsius(fahrenheit), 1)
    elif celsius:
        return round(celsius_to_fahrenheit(celsius), 1)


def get_parser():
    parser = argparse.ArgumentParser(description='Temperature Conversion')
    parser.add_argument('-c', '--celsius', metavar='C', type=float,
                        help='Temperature in Celsius')
    parser.add_argument('-f', '--fahrenheit', metavar='F', type=float,
                        help='Temperature in Fahrenheit')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.fahrenheit and args.celsius:
        print("Must provide only one of Fahrenheit or Celsius")
        sys.exit(1)
    elif not (args.fahrenheit or args.celsius):
        print("Must provide one of Fahrenheit or Celsius")
        sys.exit(1)
    out = get_temp_conversion(args.fahrenheit, args.celsius)
    print(out)
