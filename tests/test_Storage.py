#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

import unittest

class TestLoader(unittest.TestCase):
    """Test loaders"""
    def setUp(self):
        from pydsl.Memory.Storage.Directory.Grammar import GrammarDirStorage
        self.glibrary = GrammarDirStorage("/usr/share/pydsl/lib_contrib/grammar")
        from pydsl.Config import GLOBALCONFIG
        GLOBALCONFIG.strictgrammar = False 
    
    def test_grammars(self):
        grammarlist = self.glibrary.all_names()
        from pydsl.Memory.Storage.Loader import load_grammar
        for grammar in grammarlist:
            load_grammar(grammar)

