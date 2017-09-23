#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.parser.backtracing import BacktracingErrorRecursiveDescentParser
from pydsl.file.BNF import load_bnf_file
from pydsl.lex import lex
from pydsl.grammar import RegularExpression, String
from pydsl.encoding import ascii_encoding
from pydsl.check import checker_factory
from pydsl.token import Token


class TestLogicGrammars(unittest.TestCase):
    def setUp(self):
        self.tokelist5 = "True"

    def testLogicalExp(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x for x in lex(repository['TrueFalse'].alphabet, ascii_encoding, self.tokelist5)]
        self.assertEqual(len(tokens), 1)
        #tokens = [x[0] for x in lex(productionrulesetlogical.alphabet, Encoding('ascii'), tokens)] #FIXME
        tokens = [Token('True', repository['TrueFalse'])]
        result = parser.get_trees(tokens)
        self.assertTrue(result)

    def testTrueFalse(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x for x in lex(productionrulesetlogical.alphabet, ascii_encoding, self.tokelist5)]
        result = parser.get_trees(tokens)
        self.assertTrue(result)

    @unittest.skip('overlapping input')
    def testLogicalExpression(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x[0] for x in lex(productionrulesetlogical.alphabet, ascii_encoding, "True&&False")]
        result = parser.get_trees(tokens)
        self.assertTrue(result)
        result = parser.get_trees("True&|False")
        self.assertFalse(result)



class TestHTMLGrammars(unittest.TestCase):
    def testHTMLTable(self):
        repository = {'integer':RegularExpression("^[0123456789]*$")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueHTMLTable.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        lexed = lex(productionrulesetlogical.alphabet, ascii_encoding, "<table><tr><td>1</td></tr></table>")
        self.assertTrue(lexed)
        result = parser.get_trees(lexed)
        self.assertTrue(result)
        lexed = [x for x in lex(productionrulesetlogical.alphabet, ascii_encoding, "<table><td>1</td></tr></table>")]
        result = parser.get_trees(lexed)
        self.assertFalse(result)


#class TestLogGrammar(unittest.TestCase):
    #def testLogLine(self):
    #    repository = {'space':String(' '), 
    #                  'integer':RegularExpression("^[0123456789]*$"),
    #                  'ipv4':RegularExpression("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"),
    #                  'characters':RegularExpression("^[A-z]+$")}
    #    grammar = load_bnf_file("pydsl/contrib/grammar/logline.bnf", repository)
    #    checker = checker_factory(grammar)
    #    original_string = "1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GET\" 1 1 \"referer\" \"useragent\""
    #    tokenized = lex(grammar.alphabet, ascii_encoding, original_string)
    #    self.assertTrue(checker.check(tokenized))
    #    self.assertFalse(checker.check("1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GOT\" 1 1 \"referer\" \"useragent\""))
