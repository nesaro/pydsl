#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha

import unittest
from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
from pydsl.Memory.Storage.File.BNF import load_bnf_file

class TestLogicGrammars(unittest.TestCase):
    def setUp(self):
        #tokenlist definition
        self.tokelist5 = "True"

    def testLogicalExp(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf")
        #import pdb
        #pdb.set_trace()
        parser = RecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testTrueFalse(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")
        parser = RecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testLogicalExpression(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf")
        parser = RecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees("True&&False")
        self.assertTrue(result)
        result = parser.get_trees("True&|False")
        self.assertFalse(result)



class TestHTMLGrammars(unittest.TestCase):
    def testHTMLTable(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueHTMLTable.bnf")
        parser = RecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees("<table><tr><td>1</td></tr></table>")
        self.assertTrue(result)
        result = parser.get_trees("<trble><tr><td>1</td></tr></table>")
        self.assertFalse(result)

    def testSTTToTransformer(self):
        pass
