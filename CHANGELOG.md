# CHANGELOG

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
