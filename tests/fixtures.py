# -*- coding: utf-8 -*-
from brew.grains import Grain
from brew.grains import GrainAddition
from brew.hops import Hop
from brew.hops import HopAddition
from brew.recipes import Recipe
from brew.recipes import RecipeBuilder
from brew.styles import Style
from brew.yeasts import Yeast

# Define Grains
pale = Grain(u'pale 2-row',
             color=2.0,
             ppg=37.0)
crystal = Grain(u'crystal C20',
                color=20.0,
                ppg=35.0)
grain_list = [pale, crystal]

pale_add = GrainAddition(pale,
                         weight=13.96)

crystal_add = GrainAddition(crystal,
                            weight=0.78)
grain_additions = [pale_add, crystal_add]

# Define Hops
centennial = Hop(name=u'centennial',
                 percent_alpha_acids=0.14)
cascade = Hop(name=u'cascade',
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
yeast = Yeast(u"Wyeast 1056")

# Define Recipes
recipe = Recipe(name=u'pale ale',
                grain_additions=grain_additions,
                hop_additions=hop_additions,
                yeast=yeast,
                percent_brew_house_yield=0.70,
                start_volume=7.0,
                final_volume=5.0,
                )

# Define Recipe Builder
builder = RecipeBuilder(name=u'pale ale',
                        grain_list=grain_list,
                        hop_list=hop_list,
                        target_ibu=33.0,
                        target_og=1.0761348,
                        percent_brew_house_yield=0.70,
                        start_volume=7.0,
                        final_volume=5.0,
                        )

# Define a Style
american_pale_ale_style = Style(u'American Pale Ale',
                                category=u'18',
                                subcategory=u'B',
                                og=[1.045, 1.06],
                                fg=[1.010, 1.015],
                                abv=[0.045, 0.062],
                                ibu=[30, 50],
                                color=[5, 10])

english_pale_ale_style = Style(u'Ordinary Bitter',
                               category=u'11',
                               subcategory=u'A',
                               og=[1.030, 1.039],
                               fg=[1.007, 1.011],
                               abv=[0.032, 0.038],
                               ibu=[25, 35],
                               color=[8, 14])
