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
from pydsl.Check import checker_factory
from pydsl.Lex import lexer_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Alphabet import Encoding
from pydsl.Config import load, load_default_memory

class TestAlphabet(unittest.TestCase):
    def setUp(self):
        load_default_memory()
        from pydsl.Alphabet import AlphabetListDefinition
        self.integer = load("integer")
        self.date = load("Date")
        self.alphabet = AlphabetListDefinition([self.integer,self.date])

    def testChecker(self):
        checker = checker_factory(self.alphabet)
        self.assertTrue(checker.check(["1234","11/11/1991"]))
        self.assertFalse(checker.check(["bcdf"]))

    def testLexer(self):
        lexer = lexer_factory(self.alphabet)
        self.assertListEqual(lexer("1234"), ["1234"])
        self.assertListEqual(lexer("123411/11/2001"), ["1234","11/11/2001"])

    def testProperties(self):
        self.alphabet.grammarlist

    def testGenerateSymbol(self):
        alphabet = Encoding('ascii')
        print(alphabet['a'])
        print(self.alphabet[0])

class TestLexerExamples:
    pass
    #string to ascii
