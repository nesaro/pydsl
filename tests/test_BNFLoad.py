#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha

"""Test BNF file loading"""

import unittest

class TestAntlr(unittest.TestCase):
    """Loading a bnf instancew from a .g file"""
    def testFileLoader(self):
        from pydsl.Memory.Storage.File.Antlr import load_anltr_from_text, load_anltr_file
        self.assertTrue(load_anltr_file("tests/FOL.g"))

class TestPydsl(unittest.TestCase):
    """Loading a bnf instancew from a .bnf file"""
    def testFileLoader(self):
        from pydsl.Memory.Storage.File.BNF import load_bnf_file
        self.assertTrue(load_bnf_file("tests/Date.bnf"))
