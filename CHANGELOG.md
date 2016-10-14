# CHANGELOG

## Version 0.0.6

- Correctly capture exceptions for color equations
- Use same format for all documentation
- Give RecipeBuilder ability to determine needed yeast attenuation
- Add Style object for checking recipes

## Version 0.0.5

- Add __repr__, __eq__ and __ne__ to all classes
- Allow using multiple loaders in recipe parsing
- Remove short_name from grain since it doesn't give us any extra functionality
- Add tests for recipe parsers
- Update hops scraper to work with new website and parse alpha acids
- Update hops data
- Update readme since all methods work with SI units
- Make abv and abw methods return decimal percentage numbers
- All percentages now print in percentage, not decimal, format
- Add attenuation equations and a test for abw
- Add utility to calculate apparent extract to real extract
- Start to clarify the abv constant
- Add statements to all cli's so they can be run directly
- Add tests for cli's abv, sugar, and temp
- Add docs to project

## Version 0.0.4

- Add tests for cli utilities
- Use console_scripts instead of scripts in setup.py.
- Add docstrings to all classes and methods
- Add __all__ to all modules
- Fix classifiers
- Add README.rst version of readme for PyPI and a conversion utility

## Version 0.0.3

- Add tests for validators
- Add test for yeast pitch rate with no viable cells
- Change print_utilization_table() to format_utilization_table() and add a test
- Add tests for grain addition weights
- Update coarse grind potential extract charts to return correct values
- Clean up Recipe.format() to be more succinct
- Round all calculations in to_dict() and format()
- Improve test coverage for Recipe to_json() and to_dict()
- Remove malt weight and total grain weight from Recipe
- Use boil gravity for calculating IBU contributions of hop additions in Recipe
- Add caching to Recipe for easy lookup of grains and hops
- Add ABW to recipe and utilities
- Fix malt weight and color in recipe calculations
- examples to package: biere de l'inde, munich madness, and raison de saison from BCS
- Update setup.py classifiers and license
- Add setup.cfg MANIFEST.in, LICENCE.txt, CHANGELOG.md, CONTRIBUTING.md
- Remove list of grain weight from Recipe.format()
- Introduce different grain types: cereal, dme, lme, specialty

## Version 0.0.2

- Fix import path for abv binary for sugar utilities

## Version 0.0.1

- Released to PyPI
