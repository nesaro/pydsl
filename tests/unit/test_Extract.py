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


class TestGrammarExtract(unittest.TestCase):

    def testGrammarDefinition(self):
        from pydsl.Extract import extract
        from pydsl.Config import load
        gd = load('integer')
        expected_result = [(3, 4, '1'), (3, 5, '12'), (3, 6, '123'), (3, 7, '1234'), (4, 5, '2'), (4, 6, '23'), (4, 7, '234'), (5, 6, '3'), (5, 7, '34'), (6, 7, '4')]
        self.assertListEqual(extract(gd,'abc1234abc'), expected_result)
        self.assertRaises(Exception, extract, None)

    def testListInput(self):
        pass

    def testEmptyInput(self):
        pass


class TestAlphabetExtract(unittest.TestCase):

    def testAlphabet(self):
        from pydsl.Extract import extract
        from pydsl.Config import load
        ad = load('ascii')
        self.assertListEqual(extract(ad,'a£'), [(0,1,'a')])
        self.assertRaises(Exception, extract, None)

    def testListInput(self):
        pass

    def testEmptyInput(self):
        pass


