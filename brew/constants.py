# -*- coding: utf-8 -*-

# Unit Types
#: Imperial Units
IMPERIAL_UNITS = u'imperial'
#: SI or Metric Units
SI_UNITS = u'metric'

#: Imperial unit types
IMPERIAL_TYPES = {
    u'volume': u'gallon',
    u'weight_large': u'lbs',
    u'weight_small': u'oz',
    u'temperature': u'degF',
}

#: SI unit types
SI_TYPES = {
    u'volume': u'liter',
    u'weight_large': u'kg',
    u'weight_small': u'mg',
    u'temperature': u'degC',
}

# Grains

#: Grain type cereal
GRAIN_TYPE_CEREAL = u'cereal'
#: Grain type specialty
GRAIN_TYPE_SPECIALTY = u'specialty'
#: Grain type DME
GRAIN_TYPE_DME = u'dme'
#: Grain type LME
GRAIN_TYPE_LME = u'lme'
#: Grain type list
GRAIN_TYPE_LIST = [
    GRAIN_TYPE_CEREAL,
    GRAIN_TYPE_SPECIALTY,
    GRAIN_TYPE_DME,
    GRAIN_TYPE_LME,
]

# Hops

#: Hop type pellet
HOP_TYPE_PELLET = u'pellet'
#: Hop type whole leaf
HOP_TYPE_WHOLE = u'whole'
#: Hop type plug
HOP_TYPE_PLUG = u'plug'
#: Hop type list
HOP_TYPE_LIST = [
    HOP_TYPE_PELLET,
    HOP_TYPE_WHOLE,
    HOP_TYPE_PLUG,
]

# Hop utilization scale factors
#: Hop utilization scale factor for pellets
HOP_UTILIZATION_SCALE_PELLET = 1.1  # 110%

# Conversions
# Try to define SI to US units instead of US to SI.
#: Milligrams per Oz
MG_PER_OZ = 28349.5
#: Oz per Milligram
OZ_PER_MG = 1.0 / MG_PER_OZ

#: Gram per Oz
G_PER_OZ = 28.3495
#: Oz per Gram
OZ_PER_G = 1.0 / G_PER_OZ

#: Killogram per Pound
KG_PER_POUND = 0.453592
#: Pound per Killogram
POUND_PER_KG = 1.0 / KG_PER_POUND

#: Liter per Gallon
LITER_PER_GAL = 3.78541
#: Gallon per Liter
GAL_PER_LITER = 1.0 / LITER_PER_GAL

# 1 oz/gallon = 7489.15 mg/l
# Use this when calculating IBUS
#: Hops Constant Imperial Units
HOPS_CONSTANT_IMPERIAL = MG_PER_OZ * GAL_PER_LITER
#: Hops Constant SI Units
HOPS_CONSTANT_SI = 1.0

# Elevation
#: Elevation at Sea Level in feet or meters
ELEVATION_SEA_LEVEL = 0     # feet or meters
#: Elevation at one mile high in feet
ELEVATION_MILE_HIGH = 5280  # feet
#: Elevation at one kilometer high in meters
ELEVATION_KM_HIGH = 1000    # meters

# Grind Constants
# fine/coarse difference percentage for different grain in decimal format
#: Fine/Coarse difference for two row grain
FC_DIFF_TWO_ROW = 0.017
#: Fine/Coarse difference for six row grain
FC_DIFF_SIX_ROW = 0.015

#: Moisture in finished malt as percentage in decimal form (ie 4% is 0.04)
MOISTURE_FINISHED_MALT = 0.04
# I've seen this correction but haven't found a source, set to zero instead
# MOISTURE_CORRECTION = 0.002
#: Moisture correction factor
MOISTURE_CORRECTION = 0.0

# Sucrose is considered 100% extractable in water, so the maximum PPG and
# Plato are listed here
#: Maximum Plato for 100% sugar dissolved in water
SUCROSE_PLATO = 11.486
#: Maximum PPG for 100% sugar dissolved in water
SUCROSE_PPG = 46.214

# Hot Water Extract is a measure of how many liters of wort are required at a
# Specific Gravity of 1.001
#: Liters of Wort at SG 1.001 for HWE
LITERS_OF_WORT_AT_SG = 386.0
#: PPG to HWE Conversion Factor
PPG_TO_HWE_CONVERSION = LITER_PER_GAL * POUND_PER_KG

# Most hydrometers are calibrated to 59 degF
#: Standard hydrometer adjustment temperature
HYDROMETER_ADJUSTMENT_TEMP = 59.0

# Weight of Water
#: Weight of water Imperial Units
WATER_WEIGHT_IMPERIAL = 8.32  # lbs / gallon
#: Weight of water SI Units
WATER_WEIGHT_SI = 1.0  # kg / liter

# Alcohol
#: Specific gravity of alcohol
ALCOHOL_SPECIFIC_GRAVITY = 0.7936

#: Molecular mass of Ethanol (C2H6O)
MASS_C2H6O = 46.07  # g/mol
#: Molecular mass of Carbon Dioxide (CO2)
MASS_CO2 = 44.0095  # g/mol
#: Ratio of molecular mass of Ethanol to Carbon Dioxide
RATIO_C2H6O_TO_CO2 = MASS_C2H6O / MASS_CO2
#: Density of Ethanol at 20C
DENSITY_ETHANOL = 0.78945  # g/ml  @ 20C
#: Alcohol by Volume Constant
ABV_CONST = 131.25  # RATIO_C2H6O_TO_CO2 / ALCOHOL_SPECIFIC_GRAVITY * 100.0

#: Weight Tolerance, considered equal within this range
WEIGHT_TOLERANCE = 0.005

#: Percent of water evaporated during boil, usually 8% or between 8%-10%
BOIL_EVAPORATION = 0.00
