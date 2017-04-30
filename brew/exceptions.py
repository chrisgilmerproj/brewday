# -*- coding: utf-8 -*-

__all__ = [
    u'BrewdayException',
    u'DataLoaderException',
    u'GrainException',
    u'HopException',
    u'StyleException',
    u'ValidatorException',
    u'YeastException',
]


class BrewdayException(Exception):
    pass


class DataLoaderException(BrewdayException):
    pass


class GrainException(BrewdayException):
    pass


class HopException(BrewdayException):
    pass


class StyleException(BrewdayException):
    pass


class ValidatorException(BrewdayException):
    pass


class YeastException(BrewdayException):
    pass
