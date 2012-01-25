#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

import unittest

class TestRegExpGrammars(unittest.TestCase):
    """Funcionamiento basico de las gramaticas"""
    def setUp(self):
        from ColonyDSL.Type.Grammar.Regular import RegularExpressionGrammar
        self.g1 = RegularExpressionGrammar("test", "(?P<tone>1)23")

    def testCheck(self):
        self.assertTrue(self.g1.check("123"))

    def testBadCheck(self):
        self.assertTrue(not self.g1.check("124"))

    def testAlphabet(self):
        self.assertTrue(self.g1.alphabet() == {'1','2','3'}) 

    def testEnumerate(self):
        pass

    def testAskGroup(self):
        result = self.g1.get_groups("123", "tone")
        self.assertTrue((0,1) in result)

    def testGroup(self):
        result = self.g1.groups()
        self.assertTrue(result == ["tone"])

class TestPythonGrammars(unittest.TestCase):
    """Funcionamiento basico de las gramaticas"""
    def setUp(self):
        from ColonyDSL.Type.Grammar.Python import PythonGrammar
        self.g1 = PythonGrammar("test", lambda x:int(str(x))>6)

    def testCheck(self):
        self.assertTrue(self.g1.check("7"))

    def testBadCheck(self):
        self.assertTrue(not self.g1.check("3"))

    def testsenumerateWords(self):
        pass

    def testAskGroup(self):
        pass

    def testCheckWordStatus(self):
        pass
    
    def testSerialize(self):
        pass

    def testIterate(self):
        pass

class TestHostPythonGrammars(unittest.TestCase):
    """HostPythonGrammar test"""
    def setUp(self):
        from ColonyDSL.Type.Grammar.Python import HostPythonGrammar
        self.g1 = HostPythonGrammar("test2",lambda x,aux: aux["ext"].check(x), {"ext":"email"})

    def testCheck(self):
        self.assertTrue(self.g1.check("NESARO@COLONYMBUS.COM"))

    def testBadCheck(self):
        self.assertTrue(not self.g1.check("777"))

    def testsenumerateWords(self):
        pass

    def testAskGroup(self):
        pass

    def testCheckWordStatus(self):
        pass
    
    def testSerialize(self):
        pass

    def testloadgrammar(self):
        #Load a grammar that uses a package (integerOPGrammar), call check
        from ColonyDSL.Memory.External.Loader import load_grammar
        grammar = load_grammar("integerop")
        self.assertTrue(grammar.check("123+3"))

class TestSymbolGrammars(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Type.Grammar.Symbol import SymbolGrammar
        from ColonyDSL.Memory.External.DirLibrary.BNF import strlist_to_production_set
        productionset, macrodic  = strlist_to_production_set(["#parser=descent","S ::= dayofmonth separator number separator number", "separator := Char,/","number := Word,integer,max,1","dayofmonth := Word,DayOfMonth,max,1"])
        if "parser" in macrodic:
            self.g1 = SymbolGrammar("test3",productionset, macrodic["parser"])
        else:
            self.g1 = SymbolGrammar("test3",productionset)

    def testCheck(self):
        result = self.g1.check("1/1/2001")
        self.assertTrue(result)

    def testBadCheck(self):
        self.assertTrue(not self.g1.check("777"))

    def testsenumerateWords(self):
        pass

    def testAskGroup(self):
        result = self.g1.get_groups("11/1/1", "DayOfMonth")
        self.assertTrue((0,2) in result)

    def testCheckWordStatus(self):
        pass
    
    def testSerialize(self):
        pass

class ExternalProgramType(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Type.ExternalProgram import ExternalProgramType
        self.g1 = ExternalProgramType("externalExample", ["echo"," "])

    def testCheck(self):
        self.assertTrue(self.g1.check("123"))

