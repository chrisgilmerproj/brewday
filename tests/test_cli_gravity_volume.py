# -*- coding: utf-8 -*-
import unittest

from brew.cli.gravity_volume import get_parser
from brew.cli.gravity_volume import get_gravity
from brew.cli.gravity_volume import main


class TestCliTemp(unittest.TestCase):

    def setUp(self):
        self.ov = 3
        self.fv = 10
        self.gravity = 1.050

    def test_get_gravity(self):
        out = get_gravity(self.ov, self.fv, self.gravity)
        self.assertEquals(out, 1.015)


class TestCliArgparserTemp(unittest.TestCase):

    def setUp(self):
        self.parser = get_parser()

    def test_get_parser(self):
        args = [u'-o', u'3.0', u'-f', u'10.0', u'-g', u'1.050']
        out = self.parser.parse_args(args)
        expected = {
            u'original_volume': 3.0,
            u'final_volume': 10.0,
            u'gravity': 1.050,
        }
        self.assertEquals(out.__dict__, expected)


class TestCliMainTemp(unittest.TestCase):

    def setUp(self):
        class Parser(object):
            def __init__(self, output):
                self.output = output

            def parse_args(self):
                class Args(object):
                    pass
                args = Args()
                if self.output:
                    for k, v in self.output.items():
                        setattr(args, k, v)
                return args

        def g_parser(output=None):
            return Parser(output)
        self.parser_fn = g_parser
        self.main = main

    def test_main_no_args(self):
        args = {u'output': {u'original_volume': None,
                            u'final_volume': None,
                            u'gravity': None}}
        with self.assertRaises(SystemExit):
            self.main(parser_fn=self.parser_fn,
                      parser_kwargs=args)

    def test_main_no_kwargs(self):
        with self.assertRaises(AttributeError):
            self.main(parser_fn=self.parser_fn)

    def test_main_all_args(self):
        args = {u'output': {u'original_volume': 3.0,
                            u'final_volume': 10.0,
                            u'gravity': 1.050}}
        self.main(parser_fn=self.parser_fn,
                  parser_kwargs=args)
