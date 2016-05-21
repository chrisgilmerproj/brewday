
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
