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

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import unittest


from bnfgrammar import *

class TestParsers(unittest.TestCase):

    #def testLeftRecursion(self):
    #    from pydsl.Type.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
    #    descentparser = RecursiveDescentParser(self.productionsetlr)
    #    result = descentparser.check(self.dots)
    #    self.assertTrue(result)

    def testRightRecursion(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionsetrr)
        result = descentparser(dots)
        self.assertTrue(result)

    def testCenterRecursion(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionsetcr)
        result = descentparser(dots)
        self.assertTrue(result)

    def testRecursiveDescentParserStore(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionset1)
        result = descentparser(string1)
        self.assertTrue(result)

    def testRecursiveDescentParserBad(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionset1)
        result = descentparser(string2)
        self.assertFalse(result)
       
    def testRecursiveDescentParserNull(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionset2)
        result = descentparser(string3)
        self.assertTrue(result)
        
    def testRecursiveDescentParserNullBad(self):
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        descentparser = RecursiveDescentParser(productionset2)
        result = descentparser(string4)
        self.assertTrue(not result)
       
    #def testLR0ParserStore(self):
    #    from pydsl.Grammar.Parser.LR0Parser import LR0Parser
    #    parser = LR0Parser(self.productionset1)
    #    result = parser.check_word(self.tokelist1)
    #    self.assertTrue(result)

    #def testLR0ParserBad(self):
    #    from pydsl.Grammar.Parser.LR0Parser import LR0Parser
    #    parser = LR0Parser(self.productionset1)
    #    result = parser.check_word(self.tokelist2)
    #    self.assertTrue(not result)

    #def testWeightedRightRecursion(self):
    #    from pydsl.Type.Grammar.Parser.Weighted import WeightedParser
    #    parser = WeightedParser(self.productionsetrr)
    #    result = parser.check(self.dots)
    #    self.assertTrue(result)

    #def testWeightedCenterRecursion(self):
    #    from pydsl.Type.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
    #    descentparser = RecursiveDescentParser(self.productionsetcr)
    #    result = descentparser.check(self.dots)
    #    self.assertTrue(result)

    #def testWeightedParserStore(self):
    #    from pydsl.Type.Grammar.Parser.Weighted import WeightedParser
    #    parser = WeightedParser(self.productionset1)
    #    result = parser.check(self.tokelist1)
    #    self.assertTrue(result)

    #def testWeightedParserBad(self):
    #    from pydsl.Type.Grammar.Parser.Weighted import WeightedParser
    #    parser = WeightedParser(self.productionset1)
    #    result = parser.check(self.tokelist2)
    #    self.assertTrue(not result)
    #    
    #def testWeightedParserNull(self):
    #    from pydsl.Type.Grammar.Parser.Weighted import WeightedParser
    #    parser = WeightedParser(self.productionset2)
    #    result = parser.check(self.tokelist3)
    #    self.assertTrue(result)

    #def testWeightedParserNullBad(self):
    #    from pydsl.Type.Grammar.Parser.Weighted import WeightedParser
    #    parser = WeightedParser(self.productionset2)
    #    result = parser.check(self.tokelist4)
    #    self.assertTrue(not result)

#class TestWeightedParser(unittest.TestCase):
#    def setUp(self):
#        from pydsl.Value.Information import Information
#        self.dots = Information("..................................")
#        from pydsl.Memory.External.FileLibrary.BNF import strlist_to_production_set
#        self.productionsetlr,_ = strlist_to_production_set(leftrecursive)
#        self.productionsetrr,_ = strlist_to_production_set(rightrecursive)
#        self.productionsetcr,_ = strlist_to_production_set(centerrecursive)

    #def testLeftRecursion(self):
    #    from pydsl.Type.Grammar.Parser.WeightedParser import WeightedParser
    #    parser = WeightedParser(self.productionsetlr)
    #    result = parser.check_word(self.dots)
    #    self.assertTrue(result)

    #def testMixResults(self):
    #    from pydsl.Type.Grammar.Parser.Parser import mix_results 
    #    from pydsl.Type.Grammar.Tree import ParserTreeNode
    #    from pydsl.Abstract import TypeCheckList
    #    from pydsl.Type.Grammar.Symbol import NullSymbol
    #    result1 = ParserTreeNode(0, 3, [NullSymbol()], "", None)
    #    result2 = ParserTreeNode(0, 5, [NullSymbol()], "", None)
    #    result3 = ParserTreeNode(3, 6, [NullSymbol()], "", None)
    #    result4 = ParserTreeNode(6, 8, [NullSymbol()], "", None)
    #    result5 = ParserTreeNode(7, 8, [NullSymbol()], "", None)
    #    set1 = [result1, result2]
    #    set1b = TypeCheckList(ParserTreeNode, set1)
    #    set2 = [result3]
    #    set2b = TypeCheckList(ParserTreeNode, set2)
    #    set3 = [result4, result5]
    #    set3b = TypeCheckList(ParserTreeNode, set3)
    #    result = mix_results([set1b, set2b, set3b], None)
    #    #TODO: check result
    #    self.assertTrue(len(result) == 1)

