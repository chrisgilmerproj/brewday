#! /usr/bin/env python

"""
PyPI requires reStructureText for the README file.  This converts the README.md
that is primarily used on Github to a README.rst file for PyPI.
"""

from pypandoc import convert


if __name__ == "__main__":
    with open('README.rst', 'w') as f:
        f.write(convert('README.md', 'rst', 'md'))
