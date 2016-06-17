import unittest

from brew.validators import validate_percentage
from brew.validators import validate_units


class TestValidators(unittest.TestCase):

    def test_validate_percentage_pass(self):
        out = validate_percentage(0.97)
        self.assertEquals(out, 0.97)

    def test_validate_percentage_raises(self):
        with self.assertRaises(Exception):
            validate_percentage(1.01)

        with self.assertRaises(Exception):
            validate_percentage(-0.01)

    def test_validate_units(self):
        out = validate_units('metric')
        self.assertEquals(out, 'metric')

    def test_validate_units_raises(self):
        with self.assertRaises(Exception):
            validate_units('bad')
