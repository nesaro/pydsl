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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"



from pydsl.contrib.bnfgrammar import *
from pydsl.parser.backtracing import BacktracingErrorRecursiveDescentParser
from pydsl.parser.LR0 import LR0Parser
from pydsl.lex import DummyLexer, lex
from pydsl.parser.LL import LL1RecursiveDescentParser
import unittest

class TestBacktracingRecursiveDescentParser(unittest.TestCase):
    def testRecursiveLeftRecursion(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionsetlr)
        self.assertRaises(RuntimeError, descentparser, dots)

    def testRightRecursion(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionsetrr)
        result = descentparser(dots)
        self.assertTrue(result)
        result = descentparser(list(dots))
        self.assertTrue(result)

    def testCenterRecursion(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionsetcr)
        result = descentparser(dots)
        self.assertTrue(result)
        result = descentparser(list(dots))
        self.assertTrue(result)

    def testRecursiveDescentParserStore(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionset1)
        result = descentparser(string1)
        self.assertTrue(result)
        result = descentparser(list(string1))
        self.assertTrue(result)

    def testRecursiveDescentParserBad(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionset1)
        result = descentparser(string2)
        self.assertFalse(result)
        result = descentparser(list(string2))
        self.assertFalse(result)


    def testRecursiveDescentParserNull(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionset2)
        result = descentparser(string3)
        self.assertTrue(result)
        result = descentparser(list(string3))
        self.assertTrue(result)

    def testRecursiveDescentParserNullBad(self):
        descentparser = BacktracingErrorRecursiveDescentParser(productionset2)
        from pydsl.encoding import ascii_encoding
        ascii_encoding = ascii_encoding
        lexed_string4 = [x.content for x in lex(productionset2.alphabet, ascii_encoding, string4)]
        result = descentparser(lexed_string4)
        self.assertFalse(result)
        result = descentparser(list(string4))
        self.assertFalse(result)


class TestLR0Parser(unittest.TestCase):
    def testLR0ParseTable(self):
        """Tests the lr0 table generation"""
        from pydsl.parser.LR0 import _slr_build_parser_table, build_states_sets
        state_sets = build_states_sets(productionset0)
        self.assertEqual(len(state_sets), 5)
        #0 . EI: : . exp $ , 
        #   exp : .SR
        #       transitions: S -> 2,
        #       goto: exp -> 1
        #1 EI:  exp . $ ,
        #       transitions: $ -> 3
        #2 exp:  S . R,
        #       transitions: R -> 4
        #3 EI: exp $ .
        #4 exp:  S R .
        #       reduce

        parsetable = _slr_build_parser_table(productionset0)
        self.assertEqual(len(parsetable), 4)


    def testLR0ParserStore(self):
        parser = LR0Parser(productionset0)
        tokelist = [x.content for x in DummyLexer()(p0good)]
        result = parser(tokelist)
        self.assertTrue(result)

    def testLR0ParserBad(self):
        parser = LR0Parser(productionset1)
        result = parser(string2)
        self.assertFalse(result)
        result = parser(list(string2))
        self.assertFalse(result)

    def testCenterRecursion(self):
        self.assertRaises(Exception, LR0Parser, productionsetcr)

    def testArithmetic(self):
        parser = LR0Parser(productionset_arithmetic)
        self.assertFalse(parser('1'))
        self.assertTrue(parser(['123']))
        self.assertTrue(parser(['123','+','123']))
        self.assertTrue(parser(['123','*','123']))
        self.assertFalse(parser(['123a','+','123']))
        self.assertFalse(parser(['123','+','+']))


class TestLL1RecursiveDescentParser(unittest.TestCase):
    @unittest.skip
    def testRecursiveLeftRecursion(self):
        descentparser = LL1RecursiveDescentParser(productionsetlr)
        result = descentparser(dots)
        self.assertTrue(result)

    def testRightRecursion(self):
        descentparser = LL1RecursiveDescentParser(productionsetrr)
        self.assertFalse(descentparser(dots)) #Ambiguous grammar

    def testCenterRecursion(self):
        descentparser = LL1RecursiveDescentParser(productionsetcr)
        self.assertFalse(descentparser(dots)) #Ambiguous grammar

    def testLL1RecursiveDescentParserStore(self):
        descentparser = LL1RecursiveDescentParser(productionset1)
        result = descentparser(string1)
        self.assertTrue(result)
        result = descentparser(list(string1))
        self.assertTrue(result)

    def testLL1RecursiveDescentParserBad(self):
        descentparser = LL1RecursiveDescentParser(productionset1)
        result = descentparser(string2)
        self.assertFalse(result)
        result = descentparser(list(string2))
        self.assertFalse(result)

@unittest.skip
class TestPEGParser(unittest.TestCase):
    def testBasicChoice(self):
        from pydsl.grammar.PEG import Choice
        from pydsl.tree import ParseTree
        from pydsl.parser.PEG import PEGParser
        gd = Choice([String('a'), String('b')])
        parser = PEGParser(gd)
        result = parser('a')
        self.assertTrue(isinstance(result, ParseTree))



class TestParse(unittest.TestCase):
    def testverb(self):
        """Tests the lr0 table generation"""
        from pydsl.parser.parser import parse, parser_factory
        tokelist = [x.content for x in DummyLexer()(p0good)]
        self.assertTrue(parse(productionset0, tokelist , "default"))
        self.assertTrue(parse(productionset0, tokelist , "lr0"))
        self.assertTrue(parse(productionset0, tokelist , "ll1"))
        tokelist = [x.content for x in DummyLexer()(p0bad)]
        self.assertFalse(parse(productionset0, tokelist , "default"))
        self.assertFalse(parse(productionset0, tokelist , "lr0"))
        self.assertFalse(parse(productionset0, tokelist , "ll1"))
