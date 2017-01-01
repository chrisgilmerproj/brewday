# -*- coding: utf-8 -*-
import unittest

from brew.constants import IMPERIAL_UNITS
from brew.constants import SI_UNITS
from brew.utilities.yeast import KaiserYeastModel
from brew.utilities.yeast import pitch_rate_conversion
from brew.utilities.yeast import WhiteYeastModel
from brew.utilities.yeast import YeastModel


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
        self.yeast_model = YeastModel(u'stir plate')

    def test_yeast_model_raises(self):
        with self.assertRaises(Exception):
            YeastModel(u'not an allowed method')

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
        self.yeast_model_cls = WhiteYeastModel
        self.yeast_model = self.yeast_model_cls()

    def test_get_growth_rate(self):
        inoculation_rate = 6.17
        out = self.yeast_model.get_growth_rate(inoculation_rate)
        self.assertEquals(round(out, 2), 4.44)

    def test_get_inoculation_rate(self):
        growth_rate = 4.44
        out = self.yeast_model.get_inoculation_rate(growth_rate)
        self.assertEquals(round(out, 2), 6.17)

    def test_get_viability(self):
        out = self.yeast_model.get_viability(0)
        self.assertEqual(out, 1.0)
        out = self.yeast_model.get_viability(30)
        self.assertEqual(out, 0.79)
        out = self.yeast_model.get_viability(143)
        self.assertEqual(out, 0.0)

    def test_get_yeast_pitch_rate(self):
        out = self.yeast_model.get_yeast_pitch_rate()
        expected = {u'original_gravity': 1.050,
                    u'final_volume': 5.0,
                    u'viability': 0.79,
                    u'cells': 79.0,
                    u'target_pitch_rate': 1.42,
                    u'pitch_rate_as_is': 0.32,
                    u'pitch_rate_cells': 355.0,
                    u'cells_needed': 276.0,
                    u'required_growth_rate': 4.49,
                    u'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_get_yeast_pitch_rate_two_packs(self):
        out = self.yeast_model.get_yeast_pitch_rate(num_packs=2)
        expected = {u'original_gravity': 1.05,
                    u'final_volume': 5.0,
                    u'viability': 0.79,
                    u'cells': 158.0,
                    u'target_pitch_rate': 1.42,
                    u'pitch_rate_as_is': 0.63,
                    u'pitch_rate_cells': 355.0,
                    u'cells_needed': 197.0,
                    u'required_growth_rate': 2.25,
                    u'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_get_yeast_pitch_rate_cells_le_zero(self):
        out = self.yeast_model.get_yeast_pitch_rate(days_since_manufacture=365)
        expected = {u'original_gravity': 1.050,
                    u'final_volume': 5.0,
                    u'viability': 0.0,
                    u'cells': 0.0,
                    u'target_pitch_rate': 1.42,
                    u'pitch_rate_as_is': 0.0,
                    u'pitch_rate_cells': 355.0,
                    u'cells_needed': 355.0,
                    u'required_growth_rate': 0.0,
                    u'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_get_yeast_pitch_rate_metric(self):
        self.yeast_model.set_units(SI_UNITS)
        out = self.yeast_model.get_yeast_pitch_rate(
            final_volume=21.0,
            target_pitch_rate=1.5,
            num_packs=2)
        expected = {u'original_gravity': 1.050,
                    u'final_volume': 21.0,
                    u'viability': 0.79,
                    u'cells': 158.0,
                    u'target_pitch_rate': 1.5,
                    u'pitch_rate_as_is': 0.61,
                    u'pitch_rate_cells': 390.21,
                    u'cells_needed': 232.21,
                    u'required_growth_rate': 2.47,
                    u'units': 'metric',
                    }
        self.assertEquals(out, expected)

    def test_get_starter_volume(self):
        available_cells = 160.0
        out = self.yeast_model.get_starter_volume(available_cells)
        expected = {u'available_cells': 160.0,
                    u'starter_volume': 0.53,
                    u'original_gravity': 1.036,
                    u'dme': 7.23,
                    u'inoculation_rate': 80.0,
                    u'growth_rate': 0.68,
                    u'end_cell_count': 268.15,
                    u'units': 'imperial',
                    }
        self.assertEquals(out, expected)

    def test_get_starter_volume_metric_no_agitation(self):
        available_cells = 160.0
        self.yeast_model.set_units(SI_UNITS)
        out = self.yeast_model.get_starter_volume(available_cells,
                                                  starter_volume=2.0)
        expected = {u'available_cells': 160.0,
                    u'starter_volume': 2.0,
                    u'original_gravity': 1.036,
                    u'dme': 204.9,
                    u'inoculation_rate': 80.0,
                    u'growth_rate': 0.68,
                    u'end_cell_count': 268.15,
                    u'units': 'metric',
                    }
        self.assertEquals(out, expected)

    def test_get_starter_volume_metric_shaking(self):
        available_cells = 160.0
        yeast_model = self.yeast_model_cls(u'shaking')
        yeast_model.set_units(SI_UNITS)
        out = yeast_model.get_starter_volume(available_cells,
                                             starter_volume=2.0)
        expected = {u'available_cells': 160.0,
                    u'starter_volume': 2.0,
                    u'original_gravity': 1.036,
                    u'dme': 204.9,
                    u'inoculation_rate': 80.0,
                    u'growth_rate': 1.18,
                    u'end_cell_count': 348.15,
                    u'units': 'metric',
                    }
        self.assertEquals(out, expected)

    def test_get_starter_volume_metric_stir_plate(self):
        available_cells = 160.0
        yeast_model = self.yeast_model_cls(u'stir plate')
        yeast_model.set_units(SI_UNITS)
        out = yeast_model.get_starter_volume(available_cells,
                                             starter_volume=2.0)
        expected = {u'available_cells': 160.0,
                    u'starter_volume': 2.0,
                    u'original_gravity': 1.036,
                    u'dme': 204.9,
                    u'inoculation_rate': 80.0,
                    u'growth_rate': 1.68,
                    u'end_cell_count': 428.15,
                    u'units': 'metric',
                    }
        self.assertEquals(out, expected)

    def test_get_resulting_pitch_rate_imperial(self):
        out = self.yeast_model.get_resulting_pitch_rate(268.15)
        self.assertEquals(round(out, 2), 1.49)

    def test_get_resulting_pitch_rate_metric(self):
        self.yeast_model.set_units(SI_UNITS)
        out = self.yeast_model.get_resulting_pitch_rate(268.15,
                                                        final_volume=21.0)
        self.assertEquals(round(out, 2), 1.41)
