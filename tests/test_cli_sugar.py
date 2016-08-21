import unittest

from brew.cli.sugar import get_sugar_conversion


class TestCliSugar(unittest.TestCase):

    def setUp(self):
        self.brix = 22.0
        self.plato = 22.0
        self.sg = 1.092

    def test_get_sugar_conversion_brix_to_brix(self):
        out = get_sugar_conversion(self.brix, None, None, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_brix_to_plato(self):
        out = get_sugar_conversion(self.brix, None, None, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_brix_to_sg(self):
        out = get_sugar_conversion(self.brix, None, None, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_plato_to_brix(self):
        out = get_sugar_conversion(None, self.plato, None, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_plato_to_plato(self):
        out = get_sugar_conversion(None, self.plato, None, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_plato_to_sg(self):
        out = get_sugar_conversion(None, self.plato, None, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_sg_to_brix(self):
        out = get_sugar_conversion(None, None, self.sg, 'b')
        self.assertEquals(round(out, 1), self.brix)

    def test_get_sugar_conversion_sg_to_plato(self):
        out = get_sugar_conversion(None, None, self.sg, 'p')
        self.assertEquals(round(out, 1), self.plato)

    def test_get_sugar_conversion_sg_to_sg(self):
        out = get_sugar_conversion(None, None, self.sg, 's')
        self.assertEquals(round(out, 3), self.sg)

    def test_get_sugar_conversion_all_brix(self):
        out = get_sugar_conversion(self.brix, None, None, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_plato(self):
        out = get_sugar_conversion(None, self.plato, None, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)

    def test_get_sugar_conversion_all_sg(self):
        out = get_sugar_conversion(None, None, self.sg, None)
        expected = 'SG\tPlato\tBrix\n1.092\t22.0\t22.0'
        self.assertEquals(out, expected)
