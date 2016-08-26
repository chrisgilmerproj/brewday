import unittest

from brew.parsers import DataLoader
from brew.parsers import JSONDataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.parser = DataLoader('./')

    def test_read_data_raises(self):
        with self.assertRaises(NotImplementedError):
            self.parser.read_data('filename')


class TestJSONDataLoader(unittest.TestCase):

    def setUp(self):
        self.parser = JSONDataLoader('./')

    def test_format_name(self):
        name_list = [('pale malt 2-row us', 'pale_malt_2_row_us'),
                     ('caramel crystal malt 20l', 'caramel_crystal_malt_20l'),
                     ('centennial', 'centennial'),
                     ('cascade us', 'cascade_us'),
                     ('Wyeast 1056', 'wyeast_1056'),
                     ]
        for name, expected in name_list:
            out = self.parser.format_name(name)
            self.assertEquals(out, expected)
