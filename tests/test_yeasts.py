import textwrap
import unittest

from fixtures import yeast


class TestYeasts(unittest.TestCase):

    def setUp(self):

        # Define Yeasts
        self.yeast = yeast

    def test_str(self):
        out = str(self.yeast)
        self.assertEquals(out, 'Danstar, attenuation 0.75%')

    def test_repr(self):
        out = repr(self.yeast)
        self.assertEquals(out, "Yeast('Danstar', percent_attenuation=0.75)")

    def test_to_dict(self):
        out = self.yeast.to_dict()
        expected = {'name': 'Danstar',
                    'percent_attenuation': 0.75,
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.yeast.to_json()
        expected = '{"name": "Danstar", "percent_attenuation": 0.75}'
        self.assertEquals(out, expected)

    def test_format(self):
        out = self.yeast.format()
        msg = textwrap.dedent("""\
                Danstar Yeast
                -----------------------------------
                Attenuation:  0.75 %""")
        self.assertEquals(out, msg)
