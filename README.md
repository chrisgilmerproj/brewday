[![PyPI](https://img.shields.io/pypi/v/brewday.svg)](https://pypi.python.org/pypi/brewday/0.0.2)
[![Versions](https://img.shields.io/pypi/pyversions/brewday.svg)](https://img.shields.io/pypi/pyversions/brewday.svg)
[![Build Status](https://travis-ci.org/chrisgilmerproj/brewday.svg?branch=master)](https://travis-ci.org/chrisgilmerproj/brewday) 
[![License](https://img.shields.io/pypi/l/brewday.svg)](https://opensource.org/licenses/MIT)

# Brew Day

This repositiory is a set of utilities for the homebrewer.  It should help in
constructing and analyzing recipes.  There are also command line utilities for
brew day.

The hope is to help improve your planning and execution when making beer.

# Recipe Examples

To see examples of this library in action check out the `examples/` directory or
read the [Example README.md](./examples/README.md) for more information.

# Tools

To be helpful a few tools have been included.  Run them thusly:

```sh
$ PYTHONPATH=$PYTHONPATH: python bin/abv -h
$ PYTHONPATH=$PYTHONPATH: python bin/sugar -h
$ PYTHONPATH=$PYTHONPATH: python bin/temp -h
$ PYTHONPATH=$PYTHONPATH: python bin/yeast -h
```

# Charts

In an attempt to understand the data as it is presented in various brewing
books and websites the `charts/` directory attempts to reproduce them using
the tools of this library.  Credit is given as best as possible to the
original author.  Corrections are made where possible to make the charts as
accurate as possible.

## A note on Graphs

Importantly these charts are generally lists of numbers and NOT graphs.
To limit the required dependencies of this library any graphs are kept
in the [BrewSci](https://github.com/chrisgilmerproj/brewsci) repo.

# Data

The `data/` directory holds data used by parsers in the repo to build recipes.
The data was gathered using Scrapy to gather info from different brewing
websites.  The scraping code exists there along with the following data dirs:

- `cereals/`
- `hops/`
- `water/`
- `yeast/`

All the data is formatted in `*.json` files.  The files are guaranteed to work
with the parsers in this library.

# Units

The standard for this repository at the moment is to use Imperial Units.  This
is because most of the equations used as reference use Imperial Units.  As
tests are updated units may change to SI Units (metric).  Not all methods
work with SI Units yet.

# Percentages

A fair number of methods require input values as a percentage.  To avoid confusion
all percentages are expected to be in decimal form between the number 0.0
and 1.0.

There still remain some methods that return percentages not in decimal form,
notably the ABV utilities.
