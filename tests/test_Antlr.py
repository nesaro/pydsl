#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Test Antlr file handling"""

import unittest

class TestAntlr(unittest.TestCase):
    def setUp(self):
        pass

    def testFileLoader(self):
        from pydsl.Memory.Storage.File.Antlr import load_anltr_from_text, load_anltr_file
        print(load_anltr_file("tests/FOL.g"))
