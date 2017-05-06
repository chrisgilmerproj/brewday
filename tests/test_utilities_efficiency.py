# -*- coding: utf-8 -*-
import unittest

from brew.utilities.efficiency import calculate_brew_house_yield
from fixtures import recipe


class TestEfficiencyUtilities(unittest.TestCase):

    def setUp(self):
        self.recipe = recipe

    def test_calculate_brew_house_yield(self):
        out = calculate_brew_house_yield(recipe.start_volume,
                                         recipe.og,
                                         recipe.grain_additions)
        expected = 0.98
        self.assertEquals(round(out, 3), expected)
