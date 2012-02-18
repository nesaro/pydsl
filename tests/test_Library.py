#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

import unittest

class TestLoader(unittest.TestCase):
    #TODO
    """Test loaders"""
    def setUp(self):
        from ColonyDSL.Memory.External.DirLibrary.Type import GrammarFileLibrary
        self.glibrary = GrammarFileLibrary("/usr/share/ColonyDSL/lib_contrib/grammar")
        from ColonyDSL.Config import GLOBALCONFIG
        GLOBALCONFIG.strictgrammar = False 
    
    def test_grammars(self):
        grammarlist = self.glibrary.all_names()
        from ColonyDSL.Memory.External.Loader import load_grammar
        for grammar in grammarlist:
            load_grammar(grammar)

class TestConceptListLibrary(unittest.TestCase):
    """Requires test_concept_library"""
    def setUp(self):
        from ColonyDSL.Memory.External.ListLibrary import ConceptListLibrary
        self._cll = ConceptListLibrary("tests/conceptlibrary.list")

    def test_load(self):
        self.assertTrue(self._cll.load("person"))
        with self.assertRaises(KeyError):
            self._cll.load("person2")
    
    def test_generate_all_summaries(self):
        self._cll.generate_all_summaries()
