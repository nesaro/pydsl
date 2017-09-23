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
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.lex import DummyLexer, lexer_factory
from pydsl.contrib.bnfgrammar import *
from pydsl.grammar.definition import String
from pydsl.grammar.PEG import Sequence, Choice
from pydsl.file.BNF import load_bnf_file
from pydsl.token import Token, PositionToken
from pydsl.encoding import ascii_encoding


class TestEncodingLexer(unittest.TestCase):
    def testLexer(self):
        """Lexer call"""
        lexer = lexer_factory(productionset1.alphabet, ascii_encoding)
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
        lexer = lexer_factory(mydef, ascii_encoding)
        self.assertFalse(lexer(""))

    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = frozenset([integer,date])
        lexer = lexer_factory(mydef, ascii_encoding)
        self.assertListEqual(lexer("1234"), [Token("1234", integer)])
        self.assertListEqual(lexer([Token(x, ascii_encoding) for x in "1234"]), [Token("1234", integer)])

    @unittest.skip('FIXME:  Non contiguous parsing from sucessors')
    def testOverlappingLexing(self):
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = frozenset([integer,date])
        lexer = lexer_factory(mydef, ascii_encoding)
        self.assertListEqual(lexer("123411/11/2001"), [("1234", integer),("11/11/2001", date)])
        self.assertListEqual(lexer([x for x in "123411/11/2001"]), [("1234", integer),("11/11/2001", date)])

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
        from pydsl.check import checker_factory
        checker = checker_factory(second_level)
        self.assertTrue(checker([a,b]))
        second_level_alphabet = Choice([first_level, first_levelb]) 
        lexer = lexer_factory(second_level_alphabet, base=first_level+first_levelb)
        self.assertListEqual(lexer("ab"), [Token("a",first_level),Token("b",first_level)])


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
        alphabet = Choice([red, green, blue])
        lexer = lexer_factory(alphabet, ascii_encoding)

        def concept_translator_fun(inputtokens):
            result = []
            for token in inputtokens:
                x = str(token)
                if x == "red":
                    result.append("color red")
                elif x == "green":
                    result.append("color green")
                elif x == "blue":
                    result.append("color blue")
                else:
                    raise Exception("%s,%s" % (x, x.__class__.__name__))

            return result

        ct = concept_translator_fun


        self.assertListEqual(ct(lexer("red")), ["color red"])
        red_list = [PositionToken(content=character, gd=ascii_encoding, left=i, right=i+1) for i, character in enumerate("red")]
        self.assertListEqual(ct(lexer(red_list)), ["color red"])
