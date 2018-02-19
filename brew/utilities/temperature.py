# -*- coding: utf-8 -*-

import math

__all__ = [
    u'fahrenheit_to_celsius',
    u'celsius_to_fahrenheit',
    u'strike_temp',
    u'mash_infusion',
    u'boiling_point',
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


def strike_temp(target_temp, initial_temp, liquor_to_grist_ratio=1.5):
    """
    Get Strike Water Temperature

    All temperatures in F.

    http://howtobrew.com/book/section-3/the-methods-of-mashing/calculations-for-boiling-water-additions

    :param float target_temp: Mash Temperature to Achieve
    :param float initial_temp: Malt Temperature
    :param float liquor_to_grist_ratio: The Liquor to Grist Ratio (qt:lbs)
    :return: The strike water temperature
    :rtype: float
    """  # noqa
    return (0.2 / liquor_to_grist_ratio) \
        * (target_temp - initial_temp) + target_temp


def mash_infusion(target_temp, initial_temp,
                  grain_weight, water_volume, infusion_temp=212):
    """
    Get Volume of water to infuse into mash to reach scheduled temperature

    All temperatures in F.

    http://howtobrew.com/book/section-3/the-methods-of-mashing/calculations-for-boiling-water-additions

    :param float target_temp: Mash Temperature to Achieve
    :param float inital_temp: Mash Temperature
    :param float grain_weight: Total weight of grain in mash (lbs)
    :param float water_volume: Total volume of water in mash (qt)
    :param float infusion_temp: Temperature of water to infuse
    :return: The volume of water to add to the mash (qt)
    :rtype: float
    """
    return (target_temp - initial_temp) \
        * (0.2 * grain_weight + water_volume) \
        / (infusion_temp - target_temp)


def boiling_point(altitude):
    """
    Get the boiling point at a specific altitude

    https://www.omnicalculator.com/chemistry/boiling-point-altitude

    :param float altitude: Altitude in feet (ft)
    :return: The boiling point in degF
    :rtype: float
    """

    pressure = 29.921 * pow((1 - 0.0000068753 * altitude), 5.2559)
    boiling_point = 49.161 * math.log(pressure) + 44.932
    return boiling_point
