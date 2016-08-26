import unittest

from brew.parsers import DataLoader
from brew.parsers import JSONDataLoader
from brew.parsers import parse_cereals

from fixtures import pale_add


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = DataLoader('./')

    def test_read_data_raises(self):
        with self.assertRaises(NotImplementedError):
            self.loader.read_data('filename')


class TestJSONDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = JSONDataLoader('./')

    def test_format_name(self):
        name_list = [('pale malt 2-row us', 'pale_malt_2_row_us'),
                     ('caramel crystal malt 20l', 'caramel_crystal_malt_20l'),
                     ('centennial', 'centennial'),
                     ('cascade us', 'cascade_us'),
                     ('Wyeast 1056', 'wyeast_1056'),
                     ]
        for name, expected in name_list:
            out = self.loader.format_name(name)
            self.assertEquals(out, expected)


class TestCerealParser(unittest.TestCase):

    def setUp(self):

        class CerealLoader(DataLoader):
            def get_item(self, dir_suffix, item_name):
                grain_add = pale_add.to_dict()
                grain_add.update(grain_add.pop('data'))
                return grain_add
        self.grain_add = pale_add.to_dict()
        self.loader = CerealLoader('./')

    def test_parse_cereals(self):
        out = parse_cereals(self.grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_no_color(self):
        grain_add = pale_add.to_dict()
        grain_add['data'].pop('color')
        grain_add.update(grain_add.pop('data'))
        out = parse_cereals(grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_no_ppg(self):
        grain_add = pale_add.to_dict()
        grain_add['data'].pop('ppg')
        grain_add.update(grain_add.pop('data'))
        out = parse_cereals(grain_add, self.loader)
        self.assertEquals(out, pale_add)
