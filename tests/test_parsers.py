import unittest

from brew.parsers import DataLoader
from brew.parsers import JSONDataLoader
from brew.parsers import parse_cereals
from brew.parsers import parse_hops
from brew.parsers import parse_yeast

from fixtures import cascade_add
from fixtures import pale_add
from fixtures import yeast


class CerealLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        grain_add = pale_add.to_dict()
        grain_add.update(grain_add.pop('data'))
        return grain_add


class HopsLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        hop_add = cascade_add.to_dict()
        hop_add.update(hop_add.pop('data'))
        return hop_add


class YeastLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        yst = yeast.to_dict()
        yst.update(yst.pop('data'))
        return yst


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
        self.grain_add = pale_add.to_dict()
        self.loader = CerealLoader('./')

    def test_parse_cereals(self):
        out = parse_cereals(self.grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_loader_raises(self):
        def get_item(self, dir_suffix, item_name):
            raise Exception
        self.loader.get_item = get_item
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


class TestHopsParser(unittest.TestCase):

    def setUp(self):
        self.hop_add = cascade_add.to_dict()
        self.loader = HopsLoader('./')

    def test_parse_hops(self):
        out = parse_hops(self.hop_add, self.loader)
        self.assertEquals(out, cascade_add)

    def test_parse_hops_loader_raises(self):
        def get_item(self, dir_suffix, item_name):
            raise Exception
        self.loader.get_item = get_item
        out = parse_hops(self.hop_add, self.loader)
        self.assertEquals(out, cascade_add)

    def test_parse_hops_no_percent_alpha_acids(self):
        hop_add = cascade_add.to_dict()
        hop_add['data'].pop('percent_alpha_acids')
        hop_add.update(hop_add.pop('data'))
        out = parse_hops(hop_add, self.loader)
        self.assertEquals(out, cascade_add)


class TestYeastParser(unittest.TestCase):

    def setUp(self):
        self.yeast = yeast.to_dict()
        self.loader = YeastLoader('./')

    def test_parse_yeast(self):
        out = parse_yeast(self.yeast, self.loader)
        self.assertEquals(out, yeast)

    def test_parse_yeast_loader_raises(self):
        def get_item(self, dir_suffix, item_name):
            raise Exception
        self.loader.get_item = get_item
        out = parse_yeast(self.yeast, self.loader)
        self.assertEquals(out, yeast)

    def test_parse_yeast_no_percent_attenuation(self):
        yst = yeast.to_dict()
        yst['data'].pop('percent_attenuation')
        yst.update(yst.pop('data'))
        out = parse_yeast(yst, self.loader)
        self.assertEquals(out, yeast)
