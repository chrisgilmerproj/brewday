from brew.grains import Grain
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe

# Define Grains
pale = Grain(name='pale 2-row',
             short_name='2-row',
             hot_water_extract=0.76,
             color=2,
             percent_extract=95)
crystal = Grain(name='crystal C20',
                short_name='C20',
                hot_water_extract=0.70,
                color=20,
                percent_extract=5.0)
grain_list = [pale, crystal]

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
                grain_list=grain_list,
                hop_additions=hop_additions,
                percent_brew_house_yield=70.0,  # %
                final_volume=5.0,  # G
                target_degrees_plato=14.0,  # P
                mash_temp=152.0,  # F
                malt_temp=60.0,  # F
                liquor_to_grist_ratio=3.0 / 1.0,
                percent_color_loss=30.0,  # %
                target_ibu=40.0)
