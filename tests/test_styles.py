import textwrap
import unittest

from brew.styles import Style
from fixtures import american_pale_ale_style
from fixtures import recipe


class TestStyle(unittest.TestCase):

    def setUp(self):
        # Define Style
        self.style = american_pale_ale_style

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
