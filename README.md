[![Build Status](https://travis-ci.org/chrisgilmerproj/brewday.svg?branch=master)](https://travis-ci.org/chrisgilmerproj/brewday) 
[![Github Issues](http://githubbadges.herokuapp.com/chrisgilmerproj/brewday/issues.svg?style=plastic)](https://github.com/chrisgilmerproj/brewday/issues)
[![Pending Pull-Requests](http://githubbadges.herokuapp.com/chrisgilmerproj/brewday/pulls.svg?style=plastic)](https://github.com/chrisgilmerproj/brewday/pulls)

# Brew Day

This repositiory is a set of utilities for the homebrewer.  It should help in
constructing and analyzing recipes.  There are also command line utilities for
brew day.

The hope is to help improve your planning and execution when making beer.

# Examples

To be helpful a few tools have been included.  Run them thusly:

```sh
$ PYTHONPATH=$PYTHONPATH: python bin/abv -h
$ PYTHONPATH=$PYTHONPATH: python bin/sugar -h
$ PYTHONPATH=$PYTHONPATH: python bin/temp -h
$ PYTHONPATH=$PYTHONPATH: python bin/yeast -h
```

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
