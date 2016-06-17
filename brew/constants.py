# Unit Types
IMPERIAL_UNITS = 'imperial'
SI_UNITS = 'metric'

IMPERIAL_TYPES = {
    'volume': 'gallon',
    'weight_large': 'lbs',
    'weight_small': 'oz',
    'temperature': 'degF',
}

SI_TYPES = {
    'volume': 'liter',
    'weight_large': 'kg',
    'weight_small': 'mg',
    'temperature': 'degC',
}

# Conversions
# Try to define SI to US units instead of US to SI.
MG_PER_OZ = 28349.5
OZ_PER_MG = 1.0 / MG_PER_OZ

LITER_PER_GAL = 3.78541
GAL_PER_LITER = 1.0 / LITER_PER_GAL

# 1 oz/gallon = 7489.15 mg/l
# Use this when calculating IBUS
HOPS_CONSTANT_IMPERIAL = MG_PER_OZ * GAL_PER_LITER
HOPS_CONSTANT_SI = 1000

# Elevation
SEA_LEVEL = 0     # feet or meters
MILE_HIGH = 5280  # feet
KM_HIGH = 1000    # meters

# Grind Constants
# fine/coarse difference percentage for different grain in decimal format
FC_DIFF_TWO_ROW = 0.017
FC_DIFF_SIX_ROW = 0.015

# Moisture in finished malt as percentage in decimal form (ie 4% is 0.04)
MOISTURE_FINISHED_MALT = 0.04
# I've seen this correction but haven't found a source, set to zero instead
# MOISTURE_CORRECTION = 0.002
MOISTURE_CORRECTION = 0.0

# Sucrose is considered 100% extractable in water, so the maximum PPG and
# Plato are listed here
SUCROSE_PLATO = 11.486
SUCROSE_PPG = 46.214

# Hot Water Extract is a measure of how many liters of wort are required at a
# Specific Gravity of 1.001
LITERS_OF_WORT_AT_SG = 386.0

# Most hydrometers are calibrated to 59 degF
HYDROMETER_ADJUSTMENT_TEMP = 59.0

# Weight of Water
WATER_WEIGHT_IMPERIAL = 8.32  # lbs / gallon
WATER_WEIGHT_SI = 1.0  # kg / liter
