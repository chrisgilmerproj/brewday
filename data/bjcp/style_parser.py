#! /usr/bin/env python

import csv
import pprint
import string

"""
Parse the BJCP 2015 Styles CSV file
"""

# TODO:
# - numbers as floats not strings
# - abv as decimal percent
# - category without subcategory


def main():
    styles = {}

    filename = '2015_Styles.csv'
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        stylename = ''
        for row in reader:
            if row[0] and row[1]:
                if row[3]:
                    category = row[1]
                    subcategory = ''
                    style = row[2]
                    if '.' in style:
                        subcategory, style = style.split('.')

                    og = row[3].split('-')
                    fg = row[4].split('-')
                    abv = row[5].split('-')
                    ibu = row[6].split('-')
                    color = row[7].split('-')
                    if og[0] == 'Varies':
                        og = ''
                        fg = ''
                        abv = ''
                        ibu = ''
                        color = ''
                    else:
                        og[1] = str(1.0 + float(og[1]) / 1000.)
                        if float(fg[1]) > 1.015:
                            fg[1] = str(1.0 + float(fg[1]) / 1000.)
                    styles[stylename].append({
                        'category': category,
                        'subcategory': subcategory.strip(),
                        'style': style.strip(),
                        'og': og,
                        'fg': fg,
                        'abv': abv,
                        'ibu': ibu,
                        'color': color,
                    })
                else:
                    stylename = string.capwords(row[2])
                    styles[stylename] = []
    pprint.pprint(styles)


if __name__ == "__main__":
    main()
