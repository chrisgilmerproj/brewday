# Recipes

Provided here are example recipes for using the BrewDay library.  Recipes are
given attribution where necessary and are used with permission of the
copyright owner.  If this is in error please let the maintainer know and the
recipe will be updated or removed.

## Types of Recipes

There are two types of recipes, those that end in `_objects.py` and those that
end in `_dict.py`.   Let's look at the differences with the Pale Ale recipe
examples:

### `pale_ale_objects.py`

Building a recipe using python objects.  This gives you full control over
making each and every element of a recipe.

### `pale_config_dict.py`

Building a recipe with a python dict.  This dict is parsed and any missing data
is pulled from a directory named `data/`.  You have full control over the
required elements but leaving out many of them will still cause the recipe to
work.

# Recipes

## Standard Example

- [Pale Ale](./pale_ale_dict.py) (Dictionary Version)
- [Pale Ale](./pale_ale_object.py) (Python Object Version)

## Brewing Classic Styles: 80 Winning Recipes Anyone Can Brew

Authors: Jamil Zainasheff and John J. Palmer

Used by permission of Brewers Publications (2007). All rights reserved.
You can purchase the book here: [Brewing Classig Styles](http://www.brewerspublications.com/books/brewing-classic-styles-80-winning-recipes-anyone-can-brew/).

- [Biere de l'Inde (English IPA)](./biere_de_linde_dict.py) (Extract Version)
- [Munich Madness](./munich_madness_dict.py) (All Grain Version)
- [Raison de Saison](./raison_de_saison_dict.py) (Extract Version)
