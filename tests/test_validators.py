# -*- coding: utf-8 -*-
import unittest

from brew.constants import GRAIN_TYPE_CEREAL
from brew.constants import HOP_TYPE_PELLET
from brew.validators import validate_grain_type
from brew.validators import validate_hop_type
from brew.validators import validate_optional_fields
from brew.validators import validate_percentage
from brew.validators import validate_required_fields
from brew.validators import validate_units


class TestValidators(unittest.TestCase):

    def test_validate_grain_type(self):
        out = validate_grain_type(GRAIN_TYPE_CEREAL)
        self.assertEqual(out, GRAIN_TYPE_CEREAL)

    def test_validate_grain_type_raises(self):
        with self.assertRaises(Exception):
            validate_grain_type(u'bad grain type')

    def test_validate_hop_type(self):
        out = validate_hop_type(HOP_TYPE_PELLET)
        self.assertEqual(out, HOP_TYPE_PELLET)

    def test_validate_hop_type_raises(self):
        with self.assertRaises(Exception):
            validate_hop_type(u'bad hop type')

    def test_validate_percentage_pass(self):
        out = validate_percentage(0.97)
        self.assertEquals(out, 0.97)

    def test_validate_percentage_raises(self):
        with self.assertRaises(Exception):
            validate_percentage(1.01)

        with self.assertRaises(Exception):
            validate_percentage(-0.01)

    def test_validate_units(self):
        out = validate_units(u'metric')
        self.assertEquals(out, u'metric')

    def test_validate_units_raises(self):
        with self.assertRaises(Exception):
            validate_units(u'bad')

    def test_validate_required_fields(self):
        data = {u'required': u'data'}
        required_fields = [(u'required', str)]
        validate_required_fields(data, required_fields)

    def test_validate_required_fields_missing_field_raises(self):
        data = {u'missing': u'data'}
        required_fields = [(u'required', str)]
        with self.assertRaises(Exception):
            validate_required_fields(data, required_fields)

    def test_validate_required_fields_wrong_field_type_raises(self):
        data = {u'required': u'data'}
        required_fields = [(u'required', int)]
        with self.assertRaises(Exception):
            validate_required_fields(data, required_fields)

    def test_validate_optional_fields(self):
        data = {u'data': {u'optional': u'data'}}
        optional_fields = [(u'optional', str)]
        validate_optional_fields(data, optional_fields)

    def test_validate_optional_fields_extra_data(self):
        data = {u'data': {u'extra': u'data'}}
        optional_fields = [(u'optional', str)]
        validate_optional_fields(data, optional_fields)

    def test_validate_optional_fields_missing_data_field(self):
        data = {u'missing': {u'optional': u'data'}}
        optional_fields = [(u'optional', str)]
        validate_optional_fields(data, optional_fields)

    def test_validate_optional_fields_wrong_field_type_raises(self):
        data = {u'data': {u'optional': u'data'}}
        optional_fields = [(u'optional', int)]
        with self.assertRaises(Exception):
            validate_optional_fields(data, optional_fields)
