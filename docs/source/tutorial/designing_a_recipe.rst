Designing a Recipe
==================

This tutorial is going to show you how to design a beer recipe from raw
ingredients.  This will walk you through building the objects provided by
the BrewDay library, describe some methods, and end by building a complete
recipe.

The Style
---------

The first thing you'll want to do is determine the style of the beer. In this
example we're going to design a Pale Ale.  The pale ale uses two types of
grain and two types of hops.  Let's build those first:

.. code-block:: python

    from brew.grains import Grain
    from brew.hops import Hop
    pale = Grain('pale 2-row',
                 color=2.0,
                 ppg=37.0)
    crystal = Grain('crystal C20',
                    color=20.0,
                    ppg=35.0)
    grain_list = [pale, crystal]
    centennial = Hop(name='centennial',
                     percent_alpha_acids=0.14)
    cascade = Hop(name='cascade',
                  percent_alpha_acids=0.07)
    hop_list = [centennial, cascade]

The style dictates the ingredients, the expected original gravity and the
target IBU.  Here is a list of what we expect for the latter two:

* Original Gravity: 1.076
* Target IBU: 33.0

We must also describe the system we intend to brew on:

* Percent brew house yield: 70%
* Start volume: 7.0
* Final volume: 5.0

This helps us construct the :py:class:`brew.recipes.RecipeBuilder`
for building our recipe:

.. code-block:: python

    from brew.recipes import RecipeBuilder
    builder = RecipeBuilder(name='Pale Ale',
                            grain_list=grain_list,
                            hop_list=hop_list,
                            target_ibu=33.0,
                            original_gravity=1.0761348,
                            percent_brew_house_yield=0.70,
                            start_volume=7.0,
                            final_volume=5.0,
                            )

With the builder class we can now determine the amount of grains and hops that
we will use in our recipe.

The Grain Bill
--------------

Now that we have a :py:class:`brew.recipes.RecipeBuilder` to help us build a
recipe we want to determine the grain additions that we'll be using.  This is
done by providing an estimate of the percentages each grain will contribute to
the final beer.  In this case the pale 2-row will contribute 95% and the
crystal 20L will contribute 5%.

.. code-block:: python

    percent_list = [0.95, 0.05]
    grain_additions = builder.get_grain_additions(percent_list)
    for grain_add in grain_additions:
        print(grain_add.format())
        print('')

Produces the output::

	Pale Malt (2 Row) US Addition
	-----------------------------------
	Grain Type:        cereal
	Weight:            13.96 lbs

	Caramel/Crystal Malt - 20L Addition
	-----------------------------------
	Grain Type:        cereal
	Weight:            0.78 lbs

Now you have designed the grain bill for your recipe.

The Hop Bill
--------------

Next we will use the :py:class:`brew.recipes.RecipeBuilder` to determine the
hop additions that we'll be using.  This is done by providing an estimate of
the percentages each grain will contribute to the final beer.  In this case the
centennial will contribute 88.27% and the cascade will contribute 11.73%.

Additionally we need to know how long each hop will be in the boil.  For the
centennial we will boil 60 minutes and for the cascade we will boil 5 minutes.
Time is measured from the end of the boil.

.. code-block:: python

    percent_list = [0.8827, 0.1173]
    boil_time_list = [60.0, 5.0]
    hop_additions = builder.get_hop_additions(percent_list, boil_time_list)
    for hop_add in hop_additions:
        print(hop_add.format())
        print('')

Produces the output::

	Centennial Addition
	-----------------------------------
	Hop Type:     pellet
	AA %:         14.0%
	Weight:       0.57 oz
	Boil Time:    60.0 min

	Cascade (US) Addition
	-----------------------------------
	Hop Type:     pellet
	AA %:         7.0%
	Weight:       0.76 oz
	Boil Time:    5.0 min

Now you have designed the hop bill for your recipe.

The Yeast
---------

There is very little control over the yeast that you'll use.  The style typically
dictates two or three choices of yeast to get the correct flavor.  The remaining
question is how much the yeast will attenuate the wort to create alcohol.
Since attenuation is a property of the yeast the best you can do is set a target
ABV and use that to determine what range of attenuation you will need from your
yeast.

TBD code example to determine attenuation from ABV.



----

:doc:`Back to Index </index>`
