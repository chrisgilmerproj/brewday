import unittest

from brew.parsers import JSONDataLoader


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
