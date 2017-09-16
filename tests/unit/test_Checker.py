#!/usr/bin/env python
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

import unittest
from pydsl.check import checker_factory
from pydsl.grammar.definition import String
from pydsl.grammar.PEG import Sequence
import sys

class TestBNFChecker(unittest.TestCase):
    """BNF Checker"""
    def testStringInput(self):
        """Test checker instantiation and call"""
        from pydsl.contrib.bnfgrammar import productionset0
        from pydsl.check import BNFChecker
        grammardef = productionset0
        checker = BNFChecker(grammardef)
        self.assertTrue(checker.check("SR"))
        self.assertTrue(checker.check("SR"))
        self.assertTrue(checker.check(("S","R")))
        self.assertFalse(checker.check("SL"))
        self.assertFalse(checker.check(("S","L")))
        self.assertFalse(checker.check(""))

class TestRegularExpressionChecker(unittest.TestCase):
    """BNF Checker"""
    def testCheck(self):
        """Test checker instantiation and call"""
        from pydsl.check import RegularExpressionChecker
        input_str = "abc"
        checker = RegularExpressionChecker(input_str)
        self.assertTrue(checker.check(input_str))
        self.assertTrue(checker.check([x for x in input_str]))
        self.assertTrue(checker.check([x for x in input_str]))
        self.assertTrue(checker.check(input_str))
        self.assertFalse(checker.check("abd"))
        self.assertFalse(checker.check(""))

class TestPLYChecker(unittest.TestCase):
    def testCheck(self):
        """Test checker instantiation and call"""
        from pydsl.check import PLYChecker
        from pydsl.contrib.grammar import example_ply
        from pydsl.grammar.definition import PLYGrammar
        grammardef = PLYGrammar(example_ply)
        checker = PLYChecker(grammardef)
        self.assertTrue(checker.check("O"))
        self.assertTrue(checker.check(["O"]))
        self.assertFalse(checker.check("FALSE"))
        #self.assertFalse(checker.check("")) #FIXME



class TestJsonSchemaChecker(unittest.TestCase):
    def testCheck(self):
        """Test checker instantiation and call"""
        from pydsl.grammar.definition import JsonSchema
        from pydsl.check import JsonSchemaChecker
        schema = {
                "type" : "object",
                "required":["foo"],
                "properties" : {
                    "foo" : {"enum" : [1, 3]},
                    "bar" : {"format": "number_three"} #Ignored by jsonschema
                }
        }
        grammardef = JsonSchema(schema)
        checker = JsonSchemaChecker(grammardef)
        self.assertFalse(checker.check("a"))
        self.assertTrue(checker.check({"foo":1}))
        self.assertFalse(checker.check({"foo":2}))
        self.assertTrue(checker.check({"foo":3}))
        self.assertFalse(checker.check([1, {"foo" : 2, "bar" : {"baz" : [1]}}, "quux"]))
        self.assertRaises(Exception, checker.check, [1, {"foo" : 2, "bar" : {"baz" : [1]}}, "quux"], raise_exceptions=True)
        number_three = checker_factory(String("3"))
        fc = {"number_three":number_three}
        grammardef = JsonSchema(schema)
        checker = JsonSchemaChecker(grammardef, fc) # Adds a format checker
        self.assertFalse(checker.check({"foo" : 1, "bar" : "123456"}))
        self.assertTrue(checker.check({"foo" : 1, "bar" : "3"}))





class TestChoiceChecker(unittest.TestCase):
    def testCheck(self):
        from pydsl.check import ChoiceChecker
        from pydsl.grammar.PEG import Choice
        from pydsl.grammar import RegularExpression
        a = Choice([RegularExpression('^[0123456789]*$')])
        checker = ChoiceChecker(a)
        self.assertTrue(checker.check([x for x in '1234']))
        self.assertTrue(checker.check('1234'))
        self.assertFalse(checker.check('abc'))
        self.assertFalse(checker.check(''))

class TestStringChecker(unittest.TestCase):
    def testCheck(self):
        """Test checker instantiation and call"""
        from pydsl.check import StringChecker
        grammarchecker = StringChecker(String("3"))
        self.assertTrue(grammarchecker("3"))
        self.assertTrue(grammarchecker(["3"]))
        self.assertTrue(grammarchecker(("3",)))
        self.assertFalse(grammarchecker(''))

class TestSequenceChecker(unittest.TestCase):
    def testCheck(self):
        from pydsl.grammar.PEG import Sequence
        from pydsl.check import SequenceChecker
        sequence = Sequence((String("a"), String("b"), String("c")))
        checker = SequenceChecker(sequence)
        self.assertTrue(checker.check("abc"))
        self.assertTrue(checker.check([x for x in "abc"]))
        self.assertFalse(checker.check("abd"))
        self.assertFalse(checker.check(""))
