#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Tests GrammarTool instances"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestRegExpGrammars(unittest.TestCase):
    """Regular expression method tests"""
    def setUp(self):
        from pydsl.Grammar.Tool.Regular import RegularExpressionGrammarTools
        self.g1 = RegularExpressionGrammarTools("(?P<tone>1)23")

    def testCheck(self):
        self.assertTrue(self.g1.check("123"))

    def testBadCheck(self):
        self.assertFalse(self.g1.check("124"))

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
    """Python Grammar Tool"""
    def setUp(self):
        from pydsl.Grammar.Tool.Python import PythonGrammarTools
        self.g1 = PythonGrammarTools({"matchFun":lambda x:int(str(x))>6})

    def testCheck(self):
        self.assertTrue(self.g1.check("7"))

    def testBadCheck(self):
        self.assertFalse(self.g1.check("3"))

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
    """Python Grammar tool with auxiliary grammars"""
    def setUp(self):
        from pydsl.Grammar.Tool.Python import PythonGrammarTools
        self.g1 = PythonGrammarTools({"matchFun":lambda x,aux: aux["ext"].check(x),"auxdic":{"ext":"email"}})

    def testCheck(self):
        self.assertTrue(self.g1.check("NESARO@GMAIL.COM"))

    def testBadCheck(self):
        self.assertFalse(self.g1.check("777"))

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
        from pydsl.Memory.Loader import load_checker # FIXME: is load_grammar_tool
        grammar = load_checker("integerop")
        self.assertTrue(grammar.check("123+3"))

class TestSymbolGrammars(unittest.TestCase):
    def setUp(self):
        from pydsl.Grammar.Tool.Symbol import SymbolGrammarTools
        from pydsl.Memory.File.BNF import strlist_to_production_set
        productionset = strlist_to_production_set(["#parser=descent","S ::= dayofmonth separator number separator number", "separator := String,/","number := Word,integer,max,1","dayofmonth := Word,DayOfMonth,max,1"])
        self.g1 = SymbolGrammarTools(productionset)

    def testCheck(self):
        result = self.g1.check("1/1/2001")
        self.assertTrue(result)

    def testBadCheck(self):
        self.assertFalse(self.g1.check("777"))

    def testsenumerateWords(self):
        pass

    def testAskGroup(self):
        result = self.g1.get_groups("11/1/1", "DayOfMonth")
        self.assertTrue((0,2) in result)

    def testCheckWordStatus(self):
        pass
    
    def testSerialize(self):
        pass
