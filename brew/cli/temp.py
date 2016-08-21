
from brew.utilities.temperature import fahrenheit_to_celsius
from brew.utilities.temperature import celsius_to_fahrenheit


def get_temp_conversion(fahrenheit, celsius):
    """
    Convert temperature between fahrenheit and celsius
    """
    if fahrenheit:
        out = fahrenheit_to_celsius(fahrenheit)
    elif celsius:
        out = celsius_to_fahrenheit(celsius)
    return round(out, 1)
