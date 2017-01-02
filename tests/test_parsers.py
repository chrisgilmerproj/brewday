# -*- coding: utf-8 -*-
import unittest
import warnings

import mock
from brew.parsers import DataLoader
from brew.parsers import JSONDataLoader
from brew.parsers import parse_cereals
from brew.parsers import parse_hops
from brew.parsers import parse_recipe
from brew.parsers import parse_yeast
from brew.recipes import Recipe
from fixtures import cascade_add
from fixtures import pale_add
from fixtures import yeast


class CerealsLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        grain_add = pale_add.to_dict()
        grain_add.update(grain_add.pop(u'data'))
        return grain_add


class HopsLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        hop_add = cascade_add.to_dict()
        hop_add.update(hop_add.pop(u'data'))
        return hop_add


class YeastLoader(DataLoader):
    def get_item(self, dir_suffix, item_name):
        yst = yeast.to_dict()
        yst.update(yst.pop(u'data'))
        return yst


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = DataLoader('./')
        self.loader.DATA = {}
        self.loader.EXT = 'json'

    def test_data_dir_does_not_exist(self):
        with self.assertRaises(Exception):
            DataLoader('./baddirectory')

    def test_read_data_raises(self):
        with self.assertRaises(NotImplementedError):
            self.loader.read_data('filename')

    @mock.patch('glob.glob')
    def test_get_item(self, mock_glob):
        def read_data(item_filename):
            return 'data'
        self.loader.read_data = read_data
        mock_glob.return_value = ['cereals/crystal_20.json']
        out = self.loader.get_item('/', 'crystal 20')
        expected = 'data'
        self.assertEquals(out, expected)

    @mock.patch('glob.glob')
    def test_get_item_dir_does_not_exist(self, mock_glob):
        with self.assertRaises(Exception):
            self.loader.get_item('baditemdir/', 'crystal 20')

    @mock.patch('glob.glob')
    def test_get_item_warns(self, mock_glob):
        def read_data(item_filename):
            return 'data'
        self.loader.read_data = read_data
        mock_glob.return_value = ['cereals/crystal_40.json']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.loader.get_item('/', 'crystal 20')
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, Warning))
            self.assertTrue('dir not found' in str(w[-1].message))


class TestJSONDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = JSONDataLoader('./')

    def test_format_name(self):
        name_list = [(u'pale malt 2-row us', u'pale_malt_2_row_us'),
                     (u'caramel crystal malt 20l', u'caramel_crystal_malt_20l'),  # noqa
                     (u'centennial', u'centennial'),
                     (u'cascade us', u'cascade_us'),
                     (u'Wyeast 1056', u'wyeast_1056'),
                     ]
        for name, expected in name_list:
            out = self.loader.format_name(name)
            self.assertEquals(out, expected)


class TestCerealParser(unittest.TestCase):

    def setUp(self):
        self.grain_add = pale_add.to_dict()
        self.loader = CerealsLoader('./')

    def test_parse_cereals(self):
        out = parse_cereals(self.grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_loader_returns_no_data(self):
        def get_item(dir_suffix, item_name):
            return {}
        self.loader.get_item = get_item
        out = parse_cereals(self.grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_no_color(self):
        grain_add = pale_add.to_dict()
        grain_add[u'data'].pop(u'color')
        grain_add.update(grain_add.pop(u'data'))
        out = parse_cereals(grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_no_color_data(self):
        class Loader(DataLoader):
            def get_item(self, dir_suffix, item_name):
                grain_add = pale_add.to_dict()
                grain_add[u'data'].pop(u'color')
                grain_add.update(grain_add.pop(u'data'))
                return grain_add
        grain_add = pale_add.to_dict()
        grain_add[u'data'].pop(u'color')
        grain_add.update(grain_add.pop(u'data'))
        with self.assertRaises(Exception):
            parse_cereals(grain_add, Loader('./'))

    def test_parse_cereals_no_ppg(self):
        grain_add = pale_add.to_dict()
        grain_add[u'data'].pop(u'ppg')
        grain_add.update(grain_add.pop(u'data'))
        out = parse_cereals(grain_add, self.loader)
        self.assertEquals(out, pale_add)

    def test_parse_cereals_no_ppg_data(self):
        class Loader(DataLoader):
            def get_item(self, dir_suffix, item_name):
                grain_add = pale_add.to_dict()
                grain_add[u'data'].pop(u'ppg')
                grain_add.update(grain_add.pop(u'data'))
                return grain_add
        grain_add = pale_add.to_dict()
        grain_add[u'data'].pop(u'ppg')
        grain_add.update(grain_add.pop(u'data'))
        with self.assertRaises(Exception):
            parse_cereals(grain_add, Loader('./'))


class TestHopsParser(unittest.TestCase):

    def setUp(self):
        self.hop_add = cascade_add.to_dict()
        self.loader = HopsLoader('./')

    def test_parse_hops(self):
        out = parse_hops(self.hop_add, self.loader)
        self.assertEquals(out, cascade_add)

    def test_parse_hops_loader_returns_no_data(self):
        def get_item(dir_suffix, item_name):
            return {}
        self.loader.get_item = get_item
        out = parse_hops(self.hop_add, self.loader)
        self.assertEquals(out, cascade_add)

    def test_parse_hops_no_percent_alpha_acids(self):
        hop_add = cascade_add.to_dict()
        hop_add[u'data'].pop(u'percent_alpha_acids')
        hop_add.update(hop_add.pop(u'data'))
        out = parse_hops(hop_add, self.loader)
        self.assertEquals(out, cascade_add)

    def test_parse_hops_no_percent_alpha_acids_data(self):
        class Loader(DataLoader):
            def get_item(self, dir_suffix, item_name):
                hop_add = cascade_add.to_dict()
                hop_add[u'data'].pop(u'percent_alpha_acids')
                hop_add.update(hop_add.pop(u'data'))
                return hop_add
        hop_add = cascade_add.to_dict()
        hop_add[u'data'].pop(u'percent_alpha_acids')
        hop_add.update(hop_add.pop(u'data'))
        with self.assertRaises(Exception):
            parse_hops(hop_add, Loader('./'))


class TestYeastParser(unittest.TestCase):

    def setUp(self):
        self.yeast = yeast.to_dict()
        self.loader = YeastLoader('./')

    def test_parse_yeast(self):
        out = parse_yeast(self.yeast, self.loader)
        self.assertEquals(out, yeast)

    def test_parse_yeast_loader_returns_no_data(self):
        def get_item(dir_suffix, item_name):
            return {}
        self.loader.get_item = get_item
        out = parse_yeast(self.yeast, self.loader)
        self.assertEquals(out, yeast)

    def test_parse_yeast_no_percent_attenuation(self):
        yst = yeast.to_dict()
        yst[u'data'].pop(u'percent_attenuation')
        yst.update(yst.pop(u'data'))
        out = parse_yeast(yst, self.loader)
        self.assertEquals(out, yeast)

    def test_parse_yeast_no_percent_attenuation_data(self):
        class Loader(DataLoader):
            def get_item(self, dir_suffix, item_name):
                yst = yeast.to_dict()
                yst[u'data'].pop(u'percent_attenuation')
                yst.update(yst.pop(u'data'))
                return yst
        yst = yeast.to_dict()
        yst[u'data'].pop(u'percent_attenuation')
        yst.update(yst.pop(u'data'))
        with self.assertRaises(Exception):
            parse_yeast(yst, Loader('./'))


class TestRecipeParser(unittest.TestCase):

    def setUp(self):
        # A special recipe is needed since the loaders only return
        # pre-chosen additions
        self.recipe = Recipe(name=u'pale ale',
                             grain_additions=[pale_add, pale_add],
                             hop_additions=[cascade_add, cascade_add],
                             yeast=yeast,
                             percent_brew_house_yield=0.70,  # %
                             start_volume=7.0,  # G
                             final_volume=5.0,  # G
                             )
        self.recipe_data = self.recipe.to_dict()
        self.cereals_loader = CerealsLoader('./')
        self.hops_loader = HopsLoader('./')
        self.yeast_loader = YeastLoader('./')

    def test_parse_recipe(self):
        out = parse_recipe(self.recipe_data, None,
                           cereals_loader=self.cereals_loader,
                           hops_loader=self.hops_loader,
                           yeast_loader=self.yeast_loader)
        self.assertEquals(out, self.recipe)

    def test_parse_recipe_default_loader(self):
        out = parse_recipe(self.recipe_data, DataLoader('./'),
                           cereals_dir_suffix='/',
                           hops_dir_suffix='/',
                           yeast_dir_suffix='/')
        self.assertEquals(out, self.recipe)
