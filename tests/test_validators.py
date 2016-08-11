import unittest

from brew.constants import GRAIN_TYPE_CEREAL
from brew.constants import HOP_TYPE_PELLET
from brew.validators import validate_grain_type
from brew.validators import validate_hop_type
from brew.validators import validate_percentage
from brew.validators import validate_units


class TestValidators(unittest.TestCase):

    def test_validate_grain_type(self):
        out = validate_grain_type(GRAIN_TYPE_CEREAL)
        self.assertEqual(out, GRAIN_TYPE_CEREAL)

    def test_validate_grain_type_raises(self):
        with self.assertRaises(Exception):
            validate_grain_type('bad grain type')

    def test_validate_hop_type(self):
        out = validate_hop_type(HOP_TYPE_PELLET)
        self.assertEqual(out, HOP_TYPE_PELLET)

    def test_validate_hop_type_raises(self):
        with self.assertRaises(Exception):
            validate_hop_type('bad hop type')

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
