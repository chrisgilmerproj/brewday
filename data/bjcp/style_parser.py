#! /usr/bin/env python

import csv
import pprint
import string

"""
Parse the BJCP 2015 Styles CSV file
"""


def main():
    categories = {}
    styles = {}

    filename = '2015_Styles.csv'
    with open(filename, 'rb') as fileobj:
        reader = csv.reader(fileobj)
        for row in reader:
            if row[0] and row[1]:
                if not row[3] and row[2] and 'Specialty' not in row[2]:
                    cat_num, cat_name = row[2].split('. ')
                    if cat_name == 'IPA':
                        cat_name = 'India Pale Ale'
                    if cat_num not in categories:
                        categories[cat_num] = string.capwords(cat_name)

                if row[3]:
                    category = row[1]
                    subcategory = ''
                    if subcategory == '':
                        if category[-2].isalpha():
                            subcategory = category[-2:]
                            category = category[:-2]
                        elif category[-1].isalpha():
                            subcategory = category[-1:]
                            category = category[:-1]
                    category = int(category)

                    # Create the dictionary
                    if category not in styles:
                        styles[category] = {}

                    style = row[2]
                    if '.' in style:
                        subcategory, style = style.split('. ')
                        if not subcategory and subcategory == category[-1]:
                            category = category[:-1]

                    og = row[3].split('-')
                    fg = row[4].split('-')
                    abv = row[5].split('-')
                    ibu = row[6].split('-')
                    color = row[7].split('-')
                    if og[0] == 'Varies':
                        og = []
                        fg = []
                        abv = []
                        ibu = []
                        color = []
                    else:
                        og[1] = str(1.0 + float(og[1]) / 1000.)
                        if float(fg[1]) > 1.015:
                            fg[1] = str(1.0 + float(fg[1]) / 1000.)
                    styles[category][subcategory] = {
                        'category': category,
                        'subcategory': subcategory.strip(),
                        'style': style.strip(),
                        'og': [float(o) for o in og],
                        'fg': [float(f) for f in fg],
                        'abv': [round(float(a) / 100.0, 3) for a in abv],
                        'ibu': [float(i) for i in ibu],
                        'color': [float(c) for c in color],
                    }
    pprint.pprint(categories)
    pprint.pprint(styles)


if __name__ == "__main__":
    main()
