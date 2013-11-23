#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

"""Test BNF file loading"""

import unittest

class TestFileLoader(unittest.TestCase):
    """Loading a bnf instance from a .bnf file"""
    def testFileLoader(self):
        from pydsl.File.BNF import load_bnf_file
        self.assertTrue(load_bnf_file("pydsl/contrib/grammar/Date.bnf"))
