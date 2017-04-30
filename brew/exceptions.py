# -*- coding: utf-8 -*-

__all__ = [
    u'BrewdayException',
    u'ColorException',
    u'DataLoaderException',
    u'GrainException',
    u'HopException',
    u'RecipeException',
    u'StyleException',
    u'SugarException',
    u'ValidatorException',
    u'YeastException',
]


class BrewdayException(Exception):
    pass


class ColorException(BrewdayException):
    pass


class DataLoaderException(BrewdayException):
    pass


class GrainException(BrewdayException):
    pass


class HopException(BrewdayException):
    pass


class RecipeException(BrewdayException):
    pass


class StyleException(BrewdayException):
    pass


class SugarException(BrewdayException):
    pass


class ValidatorException(BrewdayException):
    pass


class YeastException(BrewdayException):
    pass
