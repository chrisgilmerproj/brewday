Matching Beer Styles
====================

This tutorial is going to show you how to match your beer against a beer
style.

The Style
---------

To begin we'll want to create an object that represents the style of the beer
we wish to brew.  To do this we'll need to make a :py:class:`brew.recipes.Style`
object.

.. code-block:: python

    from brew.styles import Style
    style = Style('American Pale Ale',
                  category='18',
                  subcategory='B',
                  og=[1.045, 1.060],
                  fg=[1.010, 1.015],
                  abv=[0.045, 0.062],
                  ibu=[30, 50],
                  color=[5, 10])

This represents an American Pale Ale from the BJCP 2015 Style Guidelines. The
beer recipe will match the style if it falls within the range of values given
here.  For example, the original gravity must fall between 1.045 and 1.060 to
be considered "in the style" of an American Pale Ale.  Similarly the final
gravity, alcohol by volume, IBUs, and color must all fall within the range.

Matching a Recipe
-----------------

In previous tutorials we have created an American Pale Ale recipe. It looked
something like this:

.. code-block:: python

    from brew.recipes import Recipe
    beer = Recipe('Pale Ale',
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  yeast=yeast,
                  percent_brew_house_yield=0.70,
                  start_volume=7.0,
                  final_volume=5.0)

In order to match the recipe we use a method on the class:

.. code-block:: python

    >>> style.recipe_matches(recipe)
    False
    >>> recipe_og = recipe.get_original_gravity()
    >>> style.og_matches(recipe_og)
    False
    >>> recipe_fg = recipe.get_final_gravity()
    >>> style._matches(recipe_fg)
    False
    >>> recipe_abv = alcohol_by_volume_standard(recipe_og, recipe_fg)
    >>> style.abv_matches(recipe_abv)
    False
    >>> recipe_ibu = recipe.get_total_ibu()
    >>> style.ibu_matches(recipe_ibu)
    True
    >>> recipe_color = recipe.get_total_wort_color()
    >>> style.color_matches(recipe_color)
    True

Interestingly the recipe used in the examples does not match the BJCP style!
The only feature that matches the style is the IBUs, but the remaining values
for og, fg, abv, and color are all too high.  That means its time to correct
our recipe.

As a short hand you can also get this information in a more friendly way:

.. code-block:: python

    >>> style.recipe_matches(recipe)
    ['OG is above style', 'FG is above style', 'ABV is above style']

This will help you quickly discover the problems with your recipe.

Correcting a Recipe
-------------------

The recipe we started with has the right ingredients but it appears the grain
bill may contain too much grain.  Let's repeat the builder example but this
time change the original gravity to 1.050  and keep everything else the same.

.. code-block:: python

    # Define Builder
    builder = RecipeBuilder(name='Pale Ale',
                            grain_list=grain_list,
                            hop_list=hop_list,
                            target_ibu=33.0,
                            original_gravity=1.050,
                            percent_brew_house_yield=0.70,
                            start_volume=7.0,
                            final_volume=5.0,
                            )

    # Get Grain Bill
    percent_list = [0.95, 0.05]
    grain_additions = builder.get_grain_additions(percent_list)
    for grain_add in grain_additions:
        print(grain_add.format())
        print('')

When we print out the grain bill with the new parameters we get::

    pale 2-row Addition
    -----------------------------------
    Grain Type:        cereal
    Weight:            9.17 lbs

    crystal C20 Addition
    -----------------------------------
    Grain Type:        cereal
    Weight:            0.51 lbs

Notice that the pale 2-row addition came down from 13.86 lbs to 9.17 lbs.  The
crystal 20L has come down from 0.78 lbs to 0.51 lbs.  Let's try this again.

.. code-block:: python

    >>> style.recipe_matches(recipe)
    False
    >>> recipe_og = recipe.get_original_gravity()
    >>> style.og_matches(recipe_og)
    True
    >>> recipe_fg = recipe.get_final_gravity()
    >>> style._matches(recipe_fg)
    True
    >>> recipe_abv = alcohol_by_volume_standard(recipe_og, recipe_fg)
    >>> style.abv_matches(recipe_abv)
    True
    >>> recipe_ibu = recipe.get_total_ibu()
    >>> style.ibu_matches(recipe_ibu)
    True
    >>> recipe_color = recipe.get_total_wort_color()
    >>> style.color_matches(recipe_color)
    False

It turns out the recipe still doesn't match.  Why? It appears that our color
is now off after our adjustments.

Correcting for Color
--------------------

Correcting color is difficult because it requires an understanding of the grains
being used.  In this case the pale ale should remain primarily pale 2-row grains.
However, we can reduce the pale 2-row and increase the crystal 20L and get a
different color.

.. code-block:: python

    # Get Grain Bill
    percent_list = [0.90, 0.10]
    grain_additions = builder.get_grain_additions(percent_list)
    for grain_add in grain_additions:
        print(grain_add.format())
        print('')

Gives us::

    pale 2-row Addition
    -----------------------------------
    Grain Type:        cereal
    Weight:            8.69 lbs

    crystal C20 Addition
    -----------------------------------
    Grain Type:        cereal
    Weight:            1.02 lbs

Notice that the weight of the pale 2-row went down from 9.17 lbs to 8.69 lbs and
the crystal 20L went up from 0.51 lbs to 1.02 lbs.  Now we can recreate the
recipe and check the style:

.. code-block:: python

    >>> style.recipe_matches(recipe)
    True
    >>> recipe_og = recipe.get_original_gravity()
    >>> style.og_matches(recipe_og)
    True
    >>> recipe_fg = recipe.get_final_gravity()
    >>> style._matches(recipe_fg)
    True
    >>> recipe_abv = alcohol_by_volume_standard(recipe_og, recipe_fg)
    >>> style.abv_matches(recipe_abv)
    True
    >>> recipe_ibu = recipe.get_total_ibu()
    >>> style.ibu_matches(recipe_ibu)
    True
    >>> recipe_color = recipe.get_total_wort_color()
    >>> style.color_matches(recipe_color)
    True

Nice job, now your have a beer recipe that matches the style of an American
Pale Ale.

----

:doc:`Back to Index </index>`
