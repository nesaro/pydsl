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


"""Tests the Grammar definition instances"""


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.grammar.definition import String
from pydsl.encoding import ascii_encoding


@unittest.skip
class TestGrammarDefinitionPLY(unittest.TestCase):
    def setUp(self):
        import plye
        from pydsl.grammar.definition import PLYGrammar
        self.grammardef = PLYGrammar(plye)

    @unittest.skip
    def testEnumerate(self):
        self.grammardef.enum()

    @unittest.skip
    def testFirst(self):
        self.grammardef.first

    @unittest.skip
    def testMin(self):
        self.grammardef.minsize

    @unittest.skip
    def testMax(self):
        self.grammardef.maxsize

    def testAlphabet(self):
        self.assertListEqual(self.grammardef.alphabet, frozenset)

class TestGrammarDefinitionString(unittest.TestCase):
    def setUp(self):
        self.grammardef = String('abc')

    def testEnumerate(self):
        self.assertListEqual(['abc'], [x for x in self.grammardef.enum()])

    def testFirst(self):
        self.assertEqual(self.grammardef.first, String('a'))

    def testMin(self):
        self.assertEqual(self.grammardef.minsize, 3)

    def testMax(self):
        self.assertEqual(self.grammardef.maxsize, 3)

    def testAlphabet(self):
        self.assertSetEqual(self.grammardef.alphabet, ascii_encoding)


class TestGrammarDefinitionJson(unittest.TestCase):
    def setUp(self):
        from pydsl.grammar.definition import JsonSchema
        self.grammardef = JsonSchema({})

    def testEnumerate(self):
        self.assertRaises(NotImplementedError, self.grammardef.enum)

    def testFirst(self):
        self.assertSetEqual(self.grammardef.first, ascii_encoding)

    def testMin(self):
        self.grammardef.minsize

    def testMax(self):
        self.grammardef.maxsize

    def testAlphabet(self):
        self.assertSetEqual(self.grammardef.alphabet, ascii_encoding)

