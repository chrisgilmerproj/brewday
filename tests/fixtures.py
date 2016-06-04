from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe

# Define Grains
pale = Grain(name='pale 2-row',
             short_name='2-row',
             color=2)
crystal = Grain(name='crystal C20',
                short_name='C20',
                color=20)
grain_list = [pale, crystal]

pale_add = GrainAddition(pale,
                         hot_water_extract=0.76,
                         percent_extract=95)

crystal_add = GrainAddition(crystal,
                            hot_water_extract=0.70,
                            percent_extract=5.0)
grain_additions = [pale_add, crystal_add]

# Define Hops
centennial = Hop(name='centennial',
                 percent_alpha_acids=14.0)
cascade = Hop(name='cascade',
              percent_alpha_acids=7.0)
hop_list = [centennial, cascade]

centennial_add = HopAddition(centennial,
                             boil_time=60.0,
                             weight=0.57,
                             percent_contribution=95.0)
cascade_add = HopAddition(cascade,
                          boil_time=5.0,
                          weight=0.76,
                          percent_contribution=5.0)
hop_additions = [centennial_add, cascade_add]

# Define Recipes
recipe = Recipe(name='pale ale',
                grain_additions=grain_additions,
                hop_additions=hop_additions,
                percent_brew_house_yield=70.0,  # %
                start_volume=7.0,  # G
                final_volume=5.0,  # G
                target_sg=1.057,  # SG
                target_ibu=40.0)
