Designing the Grain Bill
========================

This tutorial is going to show you how to design a grain bill for your beer.
Once the style is known you will want to decide how much of each grain to add
to get the Original Gravity you desire.  This can be done in a few easy steps.

If we build a Pale Ale we might first want to pick an original gravity.  This
would be the driven primarily by the style of the beer and for a Pale Ale we
will pick 1.076.  This is the gravity you desire after you have steeped your
grains and added your malt extract.  This is largely driven by your Brew House
Efficiency, the final volume, and the types of grain you use
(cereals, malt extracts, etc).

In this example the final volume is 5.0 Gallons and the target OG in Gravity
Units (GU) is 76 GU. Let's use a Brew House Efficiency of 70% for our example.
That means that we expect to only extract 70% of the total points from the grain
bill's potential points.  So let's look at what the total points are if we could
fully extract all the sugars from the malts:

.. code-block:: python

    from brew.grains import Grain
    from brew.recipes import RecipeBuilder
    pale = Grain('pale 2-row',
                 color=2.0,
                 ppg=37.0)
    crystal = Grain('crystal C20',
                    color=20.0,
                    ppg=35.0)
    grain_list = [pale, crystal]
    builder = RecipeBuilder(name='pale ale',
                            grain_list=grain_list,
                            original_gravity=1.0761348,
                            percent_brew_house_yield=0.70,
                            start_volume=7.0,
                            final_volume=5.0,
                            )

Now that we have an object to help us build a recipe we want to determine the
grain additions that we'll be using.  This is done by providing an estimate of
the percentages each grain will contribute to the final beer.  In this case the
pale 2-row will contribute 95% and the crystal 20L will contribute 5%.

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

----

:doc:`Back to Index </index>`
