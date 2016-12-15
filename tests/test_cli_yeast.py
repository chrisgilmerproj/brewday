# -*- coding: utf-8 -*-
import unittest

from brew.cli.yeast import get_parser


class TestCliArgparserTemp(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()
        self.default_args = {
            'cells': 100,
            'days': 0,
            'fv': 5.0,
            'method': 'stir plate',
            'model': 'white',
            'num': 1,
            'og': 1.05,
            'sg': 1.036,
            'sv': 0.5283443537159779,
            'target_pitch_rate': 1.42,
            'type': 'liquid',
            'units': 'imperial'}

    def test_get_parser_(self):
        args = []
        out = self.parser.parse_args(args)
        expected = {}
        self.default_args.update(expected)
        self.assertEquals(out.__dict__, self.default_args)
