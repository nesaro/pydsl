#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

"""Test BNF file loading"""

import unittest

class TestAntlr(unittest.TestCase):
    """Loading a bnf instance from a .g file"""
    def testFileLoader(self):
        from pydsl.Memory.File.Antlr import  load_anltr_file
        self.assertTrue(load_anltr_file("tests/FOL.g"))

class TestPydsl(unittest.TestCase):
    """Loading a bnf instance from a .bnf file"""
    def testFileLoader(self):
        from pydsl.Memory.File.BNF import load_bnf_file
        self.assertTrue(load_bnf_file("tests/Date.bnf"))
