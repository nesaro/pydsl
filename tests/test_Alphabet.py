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
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

@unittest.skip
class TestAlphabet(unittest.TestCase):
    def setUp(self):
        pass

    def testAlphabetChecker(self):
        x = load_alphabet("xyz")
        checker = load_checker(x)
        self.assertTrue(checker("abc"))
        self.assertTrue(checker("bcdf"))

    def testLexer(self):
        x = load_alphabet("xyz")
        lexer = load_lexer(x)
        self.assertListEqual(lexer("abc"), TokenList("A:type1","B:type2","C:type3"))

    def testAlphabetTranslator(self):
        x = load_alphabet("xyz")
        translator = load_translator("bcy")
        y = translator(x)
        self.assertListEqual(y, TokenList("A:type1","B:type2","C:type3"))

    def testAlphabetProperties(self):
        x = load_alphabet("xyz")
        x.symbols() #list allowed symbols


@unittest.skip
class TestTokenList(unittest.TestCase):
    def setUp(self):
        pass

    def testInstance(self):
        from pydsl.Alphabet.Token import Token
        a = Token()
        b = Token()
        c = Token()
        tl = TokenList(a,b,c)


class TestLexerExamples:
    pass
    #string to ascii
