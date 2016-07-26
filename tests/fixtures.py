from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.yeasts import Yeast

# Define Grains
pale = Grain('pale 2-row',
             short_name='2-row',
             color=2.0,
             ppg=37.0)
crystal = Grain('crystal C20',
                short_name='C20',
                color=20.0,
                ppg=35.0)
grain_list = [pale, crystal]

pale_add = GrainAddition(pale,
                         weight=13.96)

crystal_add = GrainAddition(crystal,
                            weight=0.78)
grain_additions = [pale_add, crystal_add]

# Define Hops
centennial = Hop(name='centennial',
                 percent_alpha_acids=0.14)
cascade = Hop(name='cascade',
              percent_alpha_acids=0.07)
hop_list = [centennial, cascade]

centennial_add = HopAddition(centennial,
                             boil_time=60.0,
                             weight=0.57)
cascade_add = HopAddition(cascade,
                          boil_time=5.0,
                          weight=0.76)
hop_additions = [centennial_add, cascade_add]

# Define Yeast
yeast = Yeast("Wyeast 1056")

# Define Recipes
recipe = Recipe(name='pale ale',
                grain_additions=grain_additions,
                hop_additions=hop_additions,
                yeast=yeast,
                percent_brew_house_yield=0.70,  # %
                start_volume=7.0,  # G
                final_volume=5.0,  # G
                )
