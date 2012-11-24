#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha

import unittest

class TestLoader(unittest.TestCase):
    """Test loaders"""
    def setUp(self):
        from pydsl.Memory.Storage.Directory import DirStorage
        self.glibrary = DirStorage("/usr/share/pydsl/lib_contrib/grammar")
        from pydsl.Config import GLOBALCONFIG
        GLOBALCONFIG.strictgrammar = False 
    
    def test_grammars(self):
        grammarlist = self.glibrary.all_names()
        from pydsl.Memory.Loader import load
        for grammar in grammarlist:
            load(grammar)

