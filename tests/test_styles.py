import textwrap
import unittest

from brew.grains import GrainAddition
from brew.recipes import Recipe
from brew.styles import Style
from fixtures import american_pale_ale_style
from fixtures import crystal
from fixtures import hop_additions
from fixtures import pale
from fixtures import recipe
from fixtures import yeast


class TestStyle(unittest.TestCase):

    def setUp(self):
        # Define Style
        self.style = american_pale_ale_style

    def test_validate_input_list_empty(self):
        with self.assertRaises(Exception):
            Style._validate_input_list(None, (int, float), 'OG')

    def test_validate_input_list_type(self):
        with self.assertRaises(Exception):
            Style._validate_input_list({'a': 'b'}, (int, float), 'OG')

    def test_validate_input_list_length_short(self):
        with self.assertRaises(Exception):
            Style._validate_input_list([1], (int, float), 'OG')

    def test_validate_input_list_length_long(self):
        with self.assertRaises(Exception):
            Style._validate_input_list([1, 2, 3], (int, float), 'OG')

    def test_validate_input_list_wrong_type(self):
        with self.assertRaises(Exception):
            Style._validate_input_list([1, '2'], (int, float), 'OG')

    def test_validate_input_list_bad_order(self):
        with self.assertRaises(Exception):
            Style._validate_input_list([2, 1], (int, float), 'OG')

    def test_str(self):
        out = str(self.style)
        self.assertEquals(out, '18B American Pale Ale')

    def test_repr(self):
        out = repr(self.style)
        self.assertEquals(out, "Style('American Pale Ale', category='18', subcategory='B', og=[1.045, 1.06], fg=[1.01, 1.015], abv=[0.045, 0.062], ibu=[30, 50], color=[5, 10])")  # nopep8

    def test_eq(self):
        style1 = self.style
        style2 = self.style
        self.assertEquals(style1, style2)

    def test_ne_style(self):
        style2 = Style('English Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_category(self):
        style2 = Style('American Pale Ale',
                       category='11',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_subcategory(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='A',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_og(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.061],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_fg(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.016],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_abv(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[4.5, 6.3],
                       ibu=[30, 50],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_ibu(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 51],
                       color=[5, 10])
        self.assertTrue(self.style != style2)

    def test_ne_color(self):
        style2 = Style('American Pale Ale',
                       category='18',
                       subcategory='B',
                       og=[1.045, 1.06],
                       fg=[1.010, 1.015],
                       abv=[0.045, 0.062],
                       ibu=[30, 50],
                       color=[5, 11])
        self.assertTrue(self.style != style2)

    def test_ne_style_class(self):
        self.assertTrue(self.style != recipe)

    def test_og_matches(self):
        out = self.style.og_matches(1.050)
        self.assertTrue(out)

    def test_og_matches_low(self):
        out = self.style.og_errors(1.044)
        self.assertEquals(out, ['OG is below style'])

    def test_og_matches_high(self):
        out = self.style.og_errors(1.061)
        self.assertEquals(out, ['OG is above style'])

    def test_fg_matches(self):
        out = self.style.fg_matches(1.012)
        self.assertTrue(out)

    def test_fg_matches_low(self):
        out = self.style.fg_errors(1.009)
        self.assertEquals(out, ['FG is below style'])

    def test_fg_matches_high(self):
        out = self.style.fg_errors(1.016)
        self.assertEquals(out, ['FG is above style'])

    def test_abv_matches(self):
        out = self.style.abv_matches(0.050)
        self.assertTrue(out)

    def test_abv_matches_low(self):
        out = self.style.abv_errors(0.044)
        self.assertEquals(out, ['ABV is below style'])

    def test_abv_matches_high(self):
        out = self.style.abv_errors(0.063)
        self.assertEquals(out, ['ABV is above style'])

    def test_ibu_matches(self):
        out = self.style.ibu_matches(33.0)
        self.assertTrue(out)

    def test_ibu_matches_low(self):
        out = self.style.ibu_errors(29)
        self.assertEquals(out, ['IBU is below style'])

    def test_ibu_matches_high(self):
        out = self.style.ibu_errors(51)
        self.assertEquals(out, ['IBU is above style'])

    def test_color_matches(self):
        out = self.style.color_matches(7.5)
        self.assertTrue(out)

    def test_color_matches_low(self):
        out = self.style.color_errors(4)
        self.assertEquals(out, ['Color is below style'])

    def test_color_matches_high(self):
        out = self.style.color_errors(11)
        self.assertEquals(out, ['Color is above style'])

    def test_recipe_matches(self):
        pale_add = GrainAddition(pale,
                                 weight=8.69)
        crystal_add = GrainAddition(crystal,
                                    weight=1.02)
        pale_ale = Recipe(name='pale ale',
                          grain_additions=[
                               pale_add,
                               crystal_add,
                          ],
                          hop_additions=hop_additions,
                          yeast=yeast,
                          percent_brew_house_yield=0.70,
                          start_volume=7.0,
                          final_volume=5.0,
                          )
        out = self.style.recipe_matches(pale_ale)
        self.assertTrue(out)

    def test_recipe_matches_false(self):
        out = self.style.recipe_matches(recipe)
        self.assertFalse(out)

    def test_recipe_errors(self):
        out = self.style.recipe_errors(recipe)
        expected = ['OG is above style',
                    'FG is above style',
                    'ABV is above style']
        self.assertEquals(out, expected)

    def test_recipe_errors_none(self):
        pale_add = GrainAddition(pale,
                                 weight=8.69)
        crystal_add = GrainAddition(crystal,
                                    weight=1.02)
        pale_ale = Recipe(name='pale ale',
                          grain_additions=[
                               pale_add,
                               crystal_add,
                          ],
                          hop_additions=hop_additions,
                          yeast=yeast,
                          percent_brew_house_yield=0.70,
                          start_volume=7.0,
                          final_volume=5.0,
                          )
        out = self.style.recipe_errors(pale_ale)
        expected = []
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.style.to_json()
        expected = '{"abv": [0.045, 0.062], "category": "18", "color": [5, 10], "fg": [1.01, 1.015], "ibu": [30, 50], "og": [1.045, 1.06], "style": "American Pale Ale", "subcategory": "B"}'  # nopep8
        self.assertEquals(out, expected)

    def test_format(self):
        out = self.style.format()
        expected = textwrap.dedent("""\
            18B American Pale Ale
            ===================================

            Original Gravity:   1.045 - 1.060
            Final Gravity:      1.010 - 1.015
            ABV:                4.50% - 6.20%
            IBU:                30.0 - 50.0
            Color (SRM):        5.0 - 10.0
            """)
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.style.to_dict()
        Style.validate(data)
