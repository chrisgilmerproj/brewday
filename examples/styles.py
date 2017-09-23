#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A utility for visualizing beer styles
"""

import os

from brew.styles import StyleFactory


def main():

    data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data/'))
    factory = StyleFactory(os.path.join(data_dir, 'bjcp', 'styles.json'))
    print(factory.format())


if __name__ == "__main__":
    main()
