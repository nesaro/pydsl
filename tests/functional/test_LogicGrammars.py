#!/usr/bin/python
# -*- coding: utf-8 -*-
from pydsl.Check import checker_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
from pydsl.File.BNF import load_bnf_file
from pydsl.Grammar import RegularExpression


class TestLogicGrammars(unittest.TestCase):
    def setUp(self):
        #tokenlist definition
        self.tokelist5 = "True"

    def testLogicalExp(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testTrueFalse(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testLogicalExpression(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees("True&&False")
        self.assertTrue(result)
        result = parser.get_trees("True&|False")
        self.assertFalse(result)



class TestHTMLGrammars(unittest.TestCase):
    def testHTMLTable(self):
        repository = {'integer':RegularExpression("^[0123456789]*$")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueHTMLTable.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees("<table><tr><td>1</td></tr></table>")
        self.assertTrue(result)
        result = parser.get_trees("<trble><tr><td>1</td></tr></table>")
        self.assertFalse(result)


class TestLogGrammar(unittest.TestCase):
    def testLogLine(self):
        repository = {'space':RegularExpression("^ $"), 
                'integer':RegularExpression("^[0123456789]*$"),
                'ipv4':RegularExpression("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"),
                'characters':RegularExpression("^[A-z]+$")}
        grammar = load_bnf_file("pydsl/contrib/grammar/logline.bnf", repository)
        checker = checker_factory(grammar)
        self.assertTrue(checker.check("1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GET\" 1 1 \"referer\" \"useragent\""))
        self.assertFalse(checker.check("1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GOT\" 1 1 \"referer\" \"useragent\""))
