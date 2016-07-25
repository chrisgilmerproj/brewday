import textwrap
import unittest

from brew.yeasts import Yeast

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
                    'yeast_data': {
                        'percent_attenuation': 0.75,
                    },
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.yeast.to_json()
        expected = '{"name": "Danstar", "yeast_data": {"percent_attenuation": 0.75}}'  # nopep8
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.yeast.to_dict()
        Yeast.validate(data)

    def test_format(self):
        out = self.yeast.format()
        msg = textwrap.dedent("""\
                Danstar Yeast
                -----------------------------------
                Attenuation:  0.75 %""")
        self.assertEquals(out, msg)
