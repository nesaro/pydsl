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
from pydsl.Lexer import EncodingTranslator
from pydsl.contrib.bnfgrammar import *


class TestLexer2(unittest.TestCase):
    def testLexer(self):
        """Lexer call"""
        from pydsl.Memory.Loader import lexer_factory
        lexer = lexer_factory(productionset1.alphabet())
        result = list(lexer(string1))
        self.assertTrue(result)

    def testencodingLexer(self):
        lexer = EncodingTranslator('utf8')
        result = list(lexer("abcde"))
        print([str(x) for x in result])

class TestLexer(unittest.TestCase):
    def setUp(self):
        from pydsl.Config import load_default_memory
        load_default_memory()

    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        from pydsl.Memory.Loader import lexer_factory, load
        from pydsl.Alphabet.Definition import AlphabetListDefinition
        from pydsl.Alphabet.Token import Token
        integer = load('integer')
        date = load('Date')
        mydef = AlphabetListDefinition([integer,date])
        lexer = lexer_factory(mydef)
        self.assertListEqual(lexer("1234"), [(Token("1234",integer))])
        self.assertListEqual(lexer("123411/11/2001"), [Token("1", load("integer")),Token("2", load("integer")),Token("3", load("integer")),Token("4", load("integer")), Token("11/11/2001",date)])

    def testLexerGenerator(self):
        from pydsl.Memory.Loader import lexer_factory
        from pydsl.Grammar.Definition import StringGrammarDefinition
        from pydsl.Alphabet.Definition import AlphabetListDefinition
        abc = StringGrammarDefinition("abc")
        numbers = StringGrammarDefinition("123")
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
        from pydsl.Alphabet.Token import Token
        self.assertListEqual(result, [Token("123", numbers), Token("abc",abc),Token("abc",abc), Token("123", numbers)])

class TestConceptTranslator(unittest.TestCase):
    def test_Concept(self):
        from pydsl.Memory.Loader import lexer_factory
        from pydsl.Grammar.Definition import StringGrammarDefinition
        from pydsl.Alphabet.Definition import AlphabetListDefinition
        from pydsl.Alphabet.Token import Token
        from pydsl.Lexer import ConceptTranslator
        red = StringGrammarDefinition("red")
        green = StringGrammarDefinition("green")
        blue = StringGrammarDefinition("blue")
        alphabet = AlphabetListDefinition([red,green,blue])
        lexer = lexer_factory(alphabet)

        def concept_translator_fun(inputtokens):
            result = []
            for x in inputtokens:
                if x == Token("red"):
                    result.append("color red")
                elif x == Token("green"):
                    result.append("color green")
                elif x == Token("blue"):
                    result.append("color blue")
                else:
                    raise Exception(x.__class__.__name__)

            return result

        ct = ConceptTranslator(concept_translator_fun)

        self.assertListEqual(ct(lexer("red")), ["color red"])
