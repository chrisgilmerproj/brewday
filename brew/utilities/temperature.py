# -*- coding: utf-8 -*-

__all__ = [
    u'fahrenheit_to_celsius',
    u'celsius_to_fahrenheit',
]


def fahrenheit_to_celsius(temp):
    """
    Convert degrees Fahrenheit to degrees Celsius

    :param float temp: The temperature in Fahrenheit
    :return: The temperature in Celsius
    :rtype: float
    """
    return (temp - 32.0) / 1.8


def celsius_to_fahrenheit(temp):
    """
    Convert degrees Celsius to degrees Fahrenheit

    :param float temp: The temperature in Celsius
    :return: The temperature in Fahrenheit
    :rtype: float
    """
    return(temp * 1.8) + 32.0
