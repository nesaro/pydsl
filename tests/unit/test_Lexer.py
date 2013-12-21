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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Lex import EncodingLexer, lexer_factory
from pydsl.contrib.bnfgrammar import *
from pydsl.Grammar.Definition import String
from pydsl.Grammar.Alphabet import Choice
from pydsl.Grammar.PEG import Sequence
from pydsl.File.BNF import load_bnf_file


class TestEncodingLexer(unittest.TestCase):
    def testLexer(self):
        """Lexer call"""
        lexer = lexer_factory(productionset1.alphabet)
        result = list(lexer(string1))
        self.assertTrue(result)

    def testencodingLexer(self):
        lexer = EncodingLexer('utf8')
        result = list(lexer("abcde"))
        print([str(x) for x in result])

class TestChoiceLexer(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("Raises an exception")
    def testEmptyInput(self):
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':self.integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = Choice([integer,date])
        lexer = lexer_factory(mydef)
        self.assertFalse(lexer(""))

    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        mydef = Choice([integer,date])
        lexer = lexer_factory(mydef)
        self.assertListEqual(lexer("1234"), [("1234", integer)])
        self.assertListEqual(lexer("123411/11/2001"), [("1234", integer),("11/11/2001", date)])

    def testLexerGenerator(self):
        abc = String("abc")
        numbers = String("123")
        mydef = Choice([abc, numbers])
        mylexer = lexer_factory(mydef)
        def text_generator(receiver):
            next(receiver)
            receiver.send("123")
            receiver.send("abc")
            receiver.send("abc")
            receiver.send("123")
            receiver.close()

        result = []
        def collector():
            try:
                while True:
                    result.append((yield))
            except GeneratorExit:
                pass

        text_generator(mylexer.lexer_generator(collector()))
        self.assertListEqual(result, ["123", "abc","abc", "123"])

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
        second_level_alphabet = Choice([first_level, first_levelb], base_alphabet=first_level+first_levelb)
        lexer = lexer_factory(second_level_alphabet)
        self.assertListEqual(lexer([a,b]), [(a,first_level),(b,first_level)])

class TestPythonLexer(unittest.TestCase):
    def test_Concept(self):
        from pydsl.Lex import PythonLexer
        red = String("red")
        green = String("green")
        blue = String("blue")
        alphabet = Choice([red,green,blue])
        lexer = lexer_factory(alphabet)

        def concept_translator_fun(inputtokens):
            result = []
            for x,_ in inputtokens:
                if x == "red":
                    result.append("color red")
                elif x == "green":
                    result.append("color green")
                elif x == "blue":
                    result.append("color blue")
                else:
                    raise Exception(x.__class__.__name__)

            return result

        ct = PythonLexer(concept_translator_fun)

        self.assertListEqual(ct(lexer("red")), ["color red"])
