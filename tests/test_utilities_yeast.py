import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.utilities.yeast import KaiserYeastModel
from brew.utilities.yeast import WhiteYeastModel
from brew.utilities.yeast import YeastModel
from brew.utilities.yeast import pitch_rate_conversion


class TestYeastUtilities(unittest.TestCase):

    def test_pitch_rate_conversion_si(self):
        out = pitch_rate_conversion(0.75, units=SI_UNITS)
        self.assertEquals(round(out, 2), 0.73)
        out = pitch_rate_conversion(1.5, units=SI_UNITS)
        self.assertEquals(round(out, 2), 1.46)
        out = pitch_rate_conversion(1.0, units=SI_UNITS)
        self.assertEquals(round(out, 3), 0.976)

    def test_pitch_rate_conversion_imperial(self):
        out = pitch_rate_conversion(0.73, units=IMPERIAL_UNITS)
        self.assertEquals(round(out, 2), 0.75)
        out = pitch_rate_conversion(1.46, units=IMPERIAL_UNITS)
        self.assertEquals(round(out, 2), 1.5)
        out = pitch_rate_conversion(0.976, units=IMPERIAL_UNITS)
        self.assertEquals(round(out, 3), 1.0)


class TestYeastModel(unittest.TestCase):

    def setUp(self):
        self.yeast_model = YeastModel('stir plate')

    def test_yeast_model_raises(self):
        with self.assertRaises(Exception):
            YeastModel('not an allowed method')

    def test_get_growth_rate(self):
        inoculation_rate = 6.17
        with self.assertRaises(NotImplementedError):
            self.yeast_model.get_growth_rate(inoculation_rate)

    def test_get_inoculation_rate(self):
        growth_rate = 4.44
        with self.assertRaises(NotImplementedError):
            self.yeast_model.get_inoculation_rate(growth_rate)


class TestKaiserYeastModel(unittest.TestCase):

    def setUp(self):
        self.yeast_model = KaiserYeastModel()

    def test_get_growth_rate(self):
        inoculation_rate = 1.0
        out = self.yeast_model.get_growth_rate(inoculation_rate)
        self.assertEquals(round(out, 2), 1.4)
        inoculation_rate = 2.5
        out = self.yeast_model.get_growth_rate(inoculation_rate)
        self.assertEquals(round(out, 2), 0.66)
        inoculation_rate = 6.17
        out = self.yeast_model.get_growth_rate(inoculation_rate)
        self.assertEquals(round(out, 2), 0)

    def test_get_inoculation_rate(self):
        growth_rate = 4.44
        out = self.yeast_model.get_inoculation_rate(growth_rate)
        self.assertEquals(round(out, 2), 1.4)
        growth_rate = 1.0
        out = self.yeast_model.get_inoculation_rate(growth_rate)
        self.assertEquals(round(out, 2), 1.99)


class TestWhiteYeastModel(unittest.TestCase):

    def setUp(self):
        self.yeast_model = WhiteYeastModel()

    def test_get_growth_rate(self):
        inoculation_rate = 6.17
        out = self.yeast_model.get_growth_rate(inoculation_rate)
        self.assertEquals(round(out, 2), 4.44)

    def test_get_inoculation_rate(self):
        growth_rate = 4.44
        out = self.yeast_model.get_inoculation_rate(growth_rate)
        self.assertEquals(round(out, 2), 6.17)

    def test_get_yeast_pitch_rate(self):
        out = self.yeast_model.get_yeast_pitch_rate()
        expected = {'original_gravity': 1.050,
                    'final_volume': 5.0,
                    'target_pitch_rate': 1.42,
                    'pitch_rate': 355.0,
                    'viability': 0.8,
                    'cells': 80.0,
                    }
        self.assertEquals(out, expected)

    def test_get_yeast_pitch_rate_two_packs(self):
        out = self.yeast_model.get_yeast_pitch_rate(num_packs=2)
        expected = {'original_gravity': 1.050,
                    'final_volume': 5.0,
                    'target_pitch_rate': 1.42,
                    'pitch_rate': 355.0,
                    'viability': 0.8,
                    'cells': 160.0,
                    }
        self.assertEquals(out, expected)

    def test_get_starter_volume_two_packs(self):
        pitch_rate = 355.0
        available_cells = 160.0
        out = self.yeast_model.get_starter_volume(pitch_rate,
                                                  available_cells)
        expected = {'growth_rate': 2.22,
                    'inoculation_rate': 19.32,
                    'starter_volume': 8.28,
                    }
        self.assertEquals(out, expected)
