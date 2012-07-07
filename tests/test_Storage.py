#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

import unittest

class TestLoader(unittest.TestCase):
    #TODO
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

class TestConceptListStorage(unittest.TestCase):
    """Requires test_concept_library"""
    def setUp(self):
        from pydsl.Memory.Storage.List import ConceptListStorage
        self._cll = ConceptListStorage("tests/conceptlibrary.list")

    def test_load(self):
        self.assertTrue(self._cll.load("person"))
        with self.assertRaises(KeyError):
            self._cll.load("person2")
    
    def test_generate_all_summaries(self):
        self._cll.generate_all_summaries()

class TestRelListStorage(unittest.TestCase):
    def setUp(self):
        from pydsl.Memory.Storage.List import RelListStorage
        self._cll = RelListStorage("tests/rellibrary.list")

    def test_load(self):
        self.assertTrue(self._cll.load("ISA"))
        with self.assertRaises(KeyError):
            self._cll.load("WHAT")
    
    def test_generate_all_summaries(self):
        self._cll.generate_all_summaries()

class TestRelationListStorage(unittest.TestCase):
    def setUp(self):
        from pydsl.Memory.Storage.List import RelationListStorage
        self._cll = RelationListStorage("tests/relationlibrary.list")

    @unittest.skip
    def test_load(self):
        self.assertTrue(self._cll.load("{'object': 'concept2', 'subject': 'concept1'}ISA"))
        with self.assertRaises(KeyError):
            self._cll.load("WHAT")
    
    def test_generate_all_summaries(self):
        self._cll.generate_all_summaries()

