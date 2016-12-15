import textwrap
import unittest

from brew.yeasts import Yeast
from fixtures import cascade_add
from fixtures import yeast


class TestYeasts(unittest.TestCase):

    def setUp(self):

        # Define Yeasts
        self.yeast = yeast

    def test_str(self):
        out = str(self.yeast)
        self.assertEquals(out, u'Wyeast 1056, attenuation 75.0%')

    def test_repr(self):
        out = repr(self.yeast)
        self.assertEquals(out, u"Yeast('Wyeast 1056', percent_attenuation=0.75)")  # noqa

    def test_eq(self):
        yeast1 = Yeast(u'Wyeast 1056',
                       percent_attenuation=0.75)
        yeast2 = Yeast(u'Wyeast 1056',
                       percent_attenuation=0.75)
        self.assertEquals(yeast1, yeast2)

    def test_ne_name(self):
        yeast1 = Yeast(u'Wyeast 1056',
                       percent_attenuation=0.75)
        yeast2 = Yeast(u'Wyeast 1057',
                       percent_attenuation=0.75)
        self.assertTrue(yeast1 != yeast2)

    def test_ne_percent_attenuation(self):
        yeast1 = Yeast(u'Wyeast 1056',
                       percent_attenuation=0.75)
        yeast2 = Yeast(u'Wyeast 1056',
                       percent_attenuation=0.70)
        self.assertTrue(yeast1 != yeast2)

    def test_ne_yeast_add_class(self):
        self.assertTrue(yeast != cascade_add)

    def test_to_dict(self):
        out = self.yeast.to_dict()
        expected = {u'name': u'Wyeast 1056',
                    u'data': {
                        u'percent_attenuation': 0.75,
                    },
                    }
        self.assertEquals(out, expected)

    def test_to_json(self):
        out = self.yeast.to_json()
        expected = u'{"data": {"percent_attenuation": 0.75}, "name": "Wyeast 1056"}'  # noqa
        self.assertEquals(out, expected)

    def test_validate(self):
        data = self.yeast.to_dict()
        Yeast.validate(data)

    def test_format(self):
        out = self.yeast.format()
        msg = textwrap.dedent(u"""\
                Wyeast 1056 Yeast
                -----------------------------------
                Attenuation:  75.0%""")
        self.assertEquals(out, msg)
