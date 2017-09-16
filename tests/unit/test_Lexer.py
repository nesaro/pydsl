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

import unittest
from pydsl.lex import DummyLexer, lexer_factory
from pydsl.contrib.bnfgrammar import *
from pydsl.grammar.definition import String
from pydsl.grammar.PEG import Sequence, Choice
from pydsl.file.BNF import load_bnf_file


class TestEncodingLexer(unittest.TestCase):
    def testLexer(self):
        """Lexer call"""
        lexer = lexer_factory(productionset1.alphabet)
        result = list(lexer(string1))
        self.assertTrue(result)

    def testencodingLexer(self):
        lexer = DummyLexer()
        result = list(lexer("abcde"))
        self.assertTrue([str(x) for x in result])
        result = list(lexer([x for x in "abcde"]))
        self.assertTrue([str(x) for x in result])

class TestChoiceBruteForceLexer(unittest.TestCase):
    def testEmptyInput(self):
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = frozenset([integer,date])
        lexer = lexer_factory(mydef)
        self.assertFalse(lexer(""))

    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = frozenset([integer,date])
        lexer = lexer_factory(mydef)
        self.assertListEqual(lexer("1234"), [(["1","2","3","4"], integer)])
        self.assertListEqual(lexer([x for x in "1234"]), [(["1","2","3","4"], integer)])

    @unittest.skip('FIXME:  Non contiguous parsing from sucessors')
    def testOverlappingLexing(self):
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = frozenset([integer,date])
        lexer = lexer_factory(mydef)
        self.assertListEqual(lexer("123411/11/2001"), [("1234", integer),("11/11/2001", date)])
        self.assertListEqual(lexer([x for x in "123411/11/2001"]), [("1234", integer),("11/11/2001", date)])

    @unittest.skip('GeneralLexer doesn\'t know how to get from the base to the target')
    def testSecondLevelGrammar(self):
        a = String("a")
        b = String("b")
        c = String("c")
        x = String("x")
        y = String("y")
        z = String("z")
        first_level = Choice([a,b,c])
        first_levelb = Choice([x,y,z])
        second_level = Sequence([a,b], base_alphabet=first_level)
        from pydsl.Check import checker_factory
        checker = checker_factory(second_level)
        self.assertTrue(checker([a,b]))
        second_level_alphabet = Choice([first_level, first_levelb]) 
        lexer = lexer_factory(second_level_alphabet, base=first_level+first_levelb)
        self.assertListEqual(lexer("ab"), [("a",first_level),("b",first_level)])


class TestChoiceLexer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testSimpleChoiceLexer(self):
        a1 = Choice([String('a'), String('b'), String('c')])
        from pydsl.lex import ChoiceLexer
        lexer = ChoiceLexer(a1)
        self.assertListEqual(lexer("abc"), [("a", String('a'))])

class TestPythonLexer(unittest.TestCase):
    def test_Concept(self):
        red = Sequence.from_string("red")
        green = Sequence.from_string("green")
        blue = Sequence.from_string("blue")
        alphabet = Choice([red,green,blue])
        lexer = lexer_factory(alphabet)

        def concept_translator_fun(inputtokens):
            result = []
            for x,_ in inputtokens:
                if x == "red" or x == ["r","e","d"]:
                    result.append("color red")
                elif x == "green" or x == ["g","r","e","e","n"]:
                    result.append("color green")
                elif x == "blue" or x == ["b","l","u","e"]:
                    result.append("color blue")
                else:
                    raise Exception("%s,%s" % (x, x.__class__.__name__))

            return result

        ct = concept_translator_fun

        self.assertListEqual(ct(lexer("red")), ["color red"])
        self.assertListEqual(ct(lexer([x for x in "red"])), ["color red"])
