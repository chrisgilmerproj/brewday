# Unit Types
IMPERIAL_UNITS = 'imperial'
SI_UNITS = 'metric'

IMPERIAL_TYPES = {
    'volume': 'gallon',
    'weight_large': 'lbs',
    'weight_small': 'oz',
}

SI_TYPES = {
    'volume': 'liter',
    'weight_large': 'kg',
    'weight_small': 'mg',
}

# Conversions
# Try to define SI to US units instead of US to SI.
MG_PER_OZ = 28349.5
OZ_PER_MG = 1.0 / MG_PER_OZ

LITER_PER_GAL = 3.78541
GAL_PER_LITER = 1.0 / LITER_PER_GAL

# 1 oz/gallon = 7489.15 mg/l
# Use this when calculating IBUS
HOPS_CONSTANT_US = MG_PER_OZ * GAL_PER_LITER
HOPS_CONSTANT_SI = 1000

# Elevation
SEA_LEVEL = 0     # feet or meters
MILE_HIGH = 5280  # feet
KM_HIGH = 1000    # meters
