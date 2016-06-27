import unittest

from brew.utilities.abv import alcohol_by_volume_alternative
from brew.utilities.abv import alcohol_by_volume_standard


class TestABVUtilities(unittest.TestCase):

    def test_alcohol_by_volume_alternative(self):
        abv = alcohol_by_volume_alternative(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.95)

    def test_alcohol_by_volume_standard(self):
        abv = alcohol_by_volume_standard(1.057, 1.013)
        self.assertEquals(round(abv, 2), 5.78)
