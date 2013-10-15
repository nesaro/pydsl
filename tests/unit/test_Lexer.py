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


class TestLexer2(unittest.TestCase):
    def testLexer(self):
        """Lexer call"""
        lexer = lexer_factory(productionset1.alphabet())
        result = list(lexer(string1))
        self.assertTrue(result)

    def testencodingLexer(self):
        lexer = EncodingLexer('utf8')
        result = list(lexer("abcde"))
        print([str(x) for x in result])

class TestLexer(unittest.TestCase):
    def setUp(self):
        from pydsl.Config import load_default_memory
        load_default_memory()

    def testListInput(self):
        pass

    def testEmptyInput(self):
        pass

    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        from pydsl.Config import load
        from pydsl.Alphabet import AlphabetListDefinition
        integer = load('integer')
        date = load('Date')
        mydef = AlphabetListDefinition([integer,date])
        lexer = lexer_factory(mydef)
        self.assertListEqual(lexer("1234"), ["1234"])
        self.assertListEqual(lexer("123411/11/2001"), ["1234","11/11/2001"])

    def testLexerGenerator(self):
        from pydsl.Grammar.Definition import String
        from pydsl.Alphabet import AlphabetListDefinition
        abc = String("abc")
        numbers = String("123")
        mydef = AlphabetListDefinition([abc, numbers])
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

class TestConceptLexer(unittest.TestCase):
    def test_Concept(self):
        from pydsl.Grammar.Definition import String
        from pydsl.Alphabet import AlphabetListDefinition
        from pydsl.Lex import ConceptLexer
        red = String("red")
        green = String("green")
        blue = String("blue")
        alphabet = AlphabetListDefinition([red,green,blue])
        lexer = lexer_factory(alphabet)

        def concept_translator_fun(inputtokens):
            result = []
            for x in inputtokens:
                if x == "red":
                    result.append("color red")
                elif x == "green":
                    result.append("color green")
                elif x == "blue":
                    result.append("color blue")
                else:
                    raise Exception(x.__class__.__name__)

            return result

        ct = ConceptLexer(concept_translator_fun)

        self.assertListEqual(ct(lexer("red")), ["color red"])
