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
from pydsl.Memory.Loader import load, load_checker, load_lexer
from pydsl.Alphabet.Token import  Token
from pydsl.Alphabet.Definition import Encoding

class TestAlphabet(unittest.TestCase):
    def setUp(self):
        from pydsl.Alphabet.Definition import AlphabetDictDefinition
        self.alphabet = AlphabetDictDefinition({"integer":"integer","Date":"Date"})

    def testChecker(self):
        checker = load_checker(self.alphabet)
        self.assertTrue(checker.check(["1234","11/11/1991"]))
        self.assertFalse(checker.check(["bcdf"]))

    def testLexer(self):
        lexer = load_lexer(self.alphabet)
        self.assertListEqual(lexer("1234"), [(Token("1234",load("integer")))])
        self.assertListEqual(lexer("11/11/20011234"), ((Token("date", "11/11/2011",Token("integer", "1234"), Token("EOF_TYPE", "")))))

    def testProperties(self):
        self.alphabet.grammar_list

    def testGenerateSymbol(self):
        alphabet = Encoding('ascii')
        print(alphabet['a'])
        print(self.alphabet['integer'])

class TestLexerExamples:
    pass
    #string to ascii
