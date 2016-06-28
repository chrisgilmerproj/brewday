import unittest

from brew.utilities.yeast import yeast_pitch_rate


class TestYeastUtilities(unittest.TestCase):

    def test_yeast_pitch_rate(self):
        out = yeast_pitch_rate()
        expected = {'pitch_rate': 355.0,
                    'viability': 0.8,
                    'cells': 80.0,
                    'growth_rate': 4.44,
                    }
        self.assertEquals(out, expected)
