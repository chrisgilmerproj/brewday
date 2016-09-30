Building a Recipe
=================

This tutorial is going to show you how to build a recipe using the objects
provided by the BrewDay library.  This will walk you through putting together
each object, describe them and some methods, and then finally build a complete
recipe.

The Grain Bill
--------------

To build a beer recipe you will want to first describe the grains to be used.
This is done by describing each grain with a :py:class:`brew.grains.Grain` object.

.. code-block:: python

    from brew.grains import Grain
    pale = Grain('Pale Malt (2 Row) US',
                 color=1.8,
                 ppg=37)

This object is really only descriptive.  It tells you the characteristics of
the Grain that you will later add to your beer.  What you want to construct
is a :py:class:`brew.grains.GrainAddition` object, which describes how
much of the grain is added to the recipe:

.. code-block:: python

    from brew.grains import GrainAddition
    pale_add = GrainAddition(pale, weight=13.96)

This object now decribes what will be added to the beer.  You can further
customize the grain by describing the type of grain being added:

.. code-block:: python

    from brew.constants import GRAIN_TYPE_LME
    from brew.grains import GrainAddition
    pale_add = GrainAddition(pale, weight=13.96, grain_type=GRAIN_TYPE_LME)

By describing the type of grain you change how it is utilized in the recipe
equations.

The Hops Bill
-------------

The next piece to describe is the :py:class:`brew.hops.Hop` object.

.. code-block:: python

    from brew.hops import Hop
    centennial = Hop('Centennial',
                     percent_alpha_acids=0.14)

Again, this object is really only descriptive.  It tells you the characteristics
of the Hop that you will later add to your beer.  What you want to construct
is a :py:class:`brew.hops.HopAddition` object, which describes how many hops
are added to the recipe and how long they are boiled for.

.. code-block:: python

    from brew.hops import HopAddition
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0)

This object now decribes what will be added to the beer.  You can further
customize the hop by describing the type of hop being added:

.. code-block:: python

    from brew.constants import HOP_TYPE_WHOLE
    from brew.hops import HopAddition
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0,
                                 hop_type=HOP_TYPE_WHOLE)

By describing the type of hop you change how it is utilized in the recipe
equations.

Yeast
-----

Yeast describes how much alcohol is expected to be produced by the recipe. This
is done with a :py:class:`brew.yeasts.Yeast` object.

.. code-block:: python

    from brew.yeasts import Yeast
    yeast = Yeast('Wyeast 1056',
                  percent_attenuation=0.70)

By changing the percentage of attenuation you can estimate different final ABV
amounts for the recipe.  By default the yeast expects 75% attenuation.

Building the Recipe
-------------------

Let's take what we've learned so far and prepare a Pale Ale recipe:

.. code-block:: python

    from brew.grains import Grain
    from brew.grains import GrainAddition
    from brew.hops import Hop
    from brew.hops import HopAddition
    from brew.yeasts import Yeast

    # Define Grains
    pale = Grain('Pale Malt (2 Row) US',
                 color=1.8,
                 ppg=37)
    pale_add = GrainAddition(pale,
                             weight=13.96)

    crystal = Grain('Caramel/Crystal Malt - 20L',
                    color=20.0,
                    ppg=35)
    crystal_add = GrainAddition(crystal,
                                weight=0.78)
    grain_additions = [pale_add, crystal_add]

    # Define Hops
    centennial = Hop('Centennial',
                     percent_alpha_acids=0.14)
    centennial_add = HopAddition(centennial,
                                 weight=0.57,
                                 boil_time=60.0)

    cascade = Hop('Cascade (US)',
                  percent_alpha_acids=0.07)
    cascade_add = HopAddition(cascade,
                              weight=0.76,
                              boil_time=5.0)
    hop_additions = [centennial_add, cascade_add]

    # Define Yeast
    yeast = Yeast('Wyeast 1056')

Now we want to put them together into a :py:class:`brew.recipes.Recipe`.

.. code-block:: python

    from brew.recipes import Recipe
    beer = Recipe('Pale Ale',
                  grain_additions=grain_additions,
                  hop_additions=hop_additions,
                  yeast=yeast,
                  percent_brew_house_yield=0.70,
                  start_volume=7.0,
                  final_volume=5.0)

In any recipe you will want to define a few more pieces about the brew that
will be done.  The first is the Brew House Yield, or how efficient your system
is.  Typically this is set at 70% efficiency but can be anywhere from 60%-80%
for a typical homebrewer.

You also need to describe the start and ending volume of your system.  Here
the recipe expects to start at 7 Gallons and end at 5 Gallons.  The units
are expected to be in Imperial Units unless otherwise specified.

Now you'll want to see what this recipe produces.  Just format the recipe
to see what you've constructed!

.. code-block:: python

    print(beer.format())

Produces the output::

	Pale Ale
	===================================

	Brew House Yield:   70.0%
	Start Volume:       7.0
	Final Volume:       5.0

	Original Gravity:   1.076
	Boil Gravity:       1.054
	Final Gravity:      1.019

	ABV / ABW Standard: 7.49% / 5.95%
	ABV / ABW Alt:      7.98% / 6.33%

	IBU:                33.0 ibu
	BU/GU:              0.6

	Morey   (SRM/EBC):  6.3 degL / 12.4
	Daniels (SRM/EBC):  N/A degL / N/A
	Mosher  (SRM/EBC):  7.1 degL / 14.1

	Grains
	===================================

	Pale Malt (2 Row) US Addition
	-----------------------------------
	Grain Type:        cereal
	Weight:            13.96 lbs
	Percent Malt Bill: 95.0%
	Working Yield:     56.0%
	SRM/EBC:           4.5 degL / 8.9

	Caramel/Crystal Malt - 20L Addition
	-----------------------------------
	Grain Type:        cereal
	Weight:            0.78 lbs
	Percent Malt Bill: 5.0%
	Working Yield:     53.0%
	SRM/EBC:           3.3 degL / 6.4

	Hops
	===================================

	Centennial Addition
	-----------------------------------
	Hop Type:     pellet
	AA %:         14.0%
	Weight:       0.57 oz
	Boil Time:    60.0 min
	IBUs:         29.2
	Utilization:  24.0%

	Cascade (US) Addition
	-----------------------------------
	Hop Type:     pellet
	AA %:         7.0%
	Weight:       0.76 oz
	Boil Time:    5.0 min
	IBUs:         3.9
	Utilization:  5.0%

	Yeast
	===================================

	Wyeast 1056 Yeast
	-----------------------------------
	Attenuation:  75.0%

Congratulations, you've now constructed your first recipe.

----

:doc:`Back to Index </index>`
