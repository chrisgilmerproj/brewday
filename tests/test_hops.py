import textwrap
import unittest

from brew.hops import HopAddition
from brew.hops import HopsUtilizationGlennTinseth
from brew.hops import HopsUtilizationJackieRager
from brew.utilities import plato_to_sg

from fixtures import hop_list


class TestHops(unittest.TestCase):

    def setUp(self):

        # Define Hops
        self.hop_list = hop_list
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)

    def test_str(self):
        out = str(self.hop_list[0])
        self.assertEquals(out, 'Centennial, alpha 14.0%')

    def test_repr(self):
        out = repr(self.hop_list[0])
        self.assertEquals(out, "Hop('centennial', percent_alpha_acids=14.0)")

    def test_format(self):
        out = self.hop_list[0].format()
        msg = textwrap.dedent("""
                              """)
        self.assertEquals(out, msg)


class TestHopAdditions(unittest.TestCase):

    def setUp(self):
        self.addition_kwargs = [
            {
                'boil_time': 60.0,
                'weight': 0.57,
                'percent_contribution': 95.0,
            },
            {
                'boil_time': 5.0,
                'weight': 0.76,
                'percent_contribution': 5.0,
            },
        ]

        # Define Hops
        self.plato = 14.0
        self.sg = plato_to_sg(self.plato)
        self.target_ibu = 40.0
        self.final_volume = 5.0

    def test_get_ibus_jackie_rager(self):
        self.addition_kwargs[0]['utilization_cls'] = HopsUtilizationJackieRager
        hop_addition = HopAddition(hop_list[0],
                                   **self.addition_kwargs[0])
        ibu = hop_addition.get_ibus(self.sg,
                                    self.final_volume)
        self.assertEquals(round(ibu, 2), 35.62)

        self.addition_kwargs[1]['utilization_cls'] = HopsUtilizationJackieRager
        hop_addition = HopAddition(hop_list[1],
                                   **self.addition_kwargs[1])
        ibu = hop_addition.get_ibus(self.sg,
                                    self.final_volume)
        self.assertEquals(round(ibu, 2), 4.41)

    def test_get_ibu_glenn_tinseth(self):
        self.addition_kwargs[0]['utilization_cls'] = \
            HopsUtilizationGlennTinseth
        hop_addition = HopAddition(hop_list[0],
                                   **self.addition_kwargs[0])
        ibu = hop_addition.get_ibus(self.sg,
                                    self.final_volume)
        self.assertEquals(round(ibu, 2), 25.93)

        self.addition_kwargs[1]['utilization_cls'] = \
            HopsUtilizationGlennTinseth
        hop_addition = HopAddition(hop_list[1],
                                   **self.addition_kwargs[1])
        ibu = hop_addition.get_ibus(self.sg,
                                    self.final_volume)
        self.assertEquals(round(ibu, 2), 3.45)

    # def test_get_percent_utilization(self):
    #     utilization = self.hop_additions[0].get_percent_utilization(
    #             self.sg, self.hop_additions[0].boil_time)
    #     self.assertEquals(round(utilization * 100, 2), 21.69)
    #     utilization = self.hop_additions[1].get_percent_utilization(
    #             self.sg, self.hop_additions[1].boil_time)
    #     self.assertEquals(round(utilization * 100, 2), 4.32)

    def test_get_hops_weight(self):
        self.addition_kwargs[0]['utilization_cls'] = HopsUtilizationJackieRager
        hop_addition = HopAddition(hop_list[0],
                                   **self.addition_kwargs[0])
        hops_weight = hop_addition.get_hops_weight(
                        self.sg,
                        self.target_ibu,
                        self.final_volume)
        self.assertEquals(round(hops_weight, 2), 0.61)

        self.addition_kwargs[0]['utilization_cls'] = HopsUtilizationJackieRager
        hop_addition = HopAddition(hop_list[0],
                                   **self.addition_kwargs[0])
        hops_weight = hop_addition.get_hops_weight(
                        self.sg,
                        self.target_ibu,
                        self.final_volume)
        self.assertEquals(round(hops_weight, 2), 0.61)
