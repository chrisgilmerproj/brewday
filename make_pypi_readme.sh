#! /bin/bash

# PyPI requires reStructureText for the README file.  This converts the README.md
# that is primarily used on Github to a README.rst file for PyPI.

pandoc -f markdown -t rst README.md -o README.rst
