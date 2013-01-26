#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestLoader(unittest.TestCase):
    """Test loaders"""
    def setUp(self):
        from pydsl.Memory.Directory import DirStorage
        self.glibrary = DirStorage("/usr/share/pydsl/lib_contrib/grammar")
        from pydsl.Config import GLOBALCONFIG
        GLOBALCONFIG.strictgrammar = False 
    
    def test_grammars(self):
        grammarlist = self.glibrary.all_names()
        from pydsl.Memory.Loader import load
        for grammar in grammarlist:
            load(grammar)

