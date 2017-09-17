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
from pydsl.extract import extract, extract_alphabet, match, search
from pydsl.grammar import RegularExpression, String
from pydsl.grammar.PEG import Choice
from pydsl.encoding import ascii_encoding
from pydsl.token import PositionToken, Token
import sys


class TestGrammarExtract(unittest.TestCase):

    def testRegularExpressionExtract(self):
        gd = RegularExpression('^[0123456789]*$')
        expected_result = [
                PositionToken(content='1', gd=None, left=3, right=4), 
                PositionToken(content='12', gd=None, left=3, right=5), 
                PositionToken(content='123', gd=None, left=3, right=6), 
                PositionToken(content='1234', gd=None, left=3, right=7), 
                PositionToken(content='2', gd=None, left=4, right=5), 
                PositionToken(content='23', gd=None, left=4, right=6), 
                PositionToken(content='234', gd=None, left=4, right=7), 
                PositionToken(content='3', gd=None, left=5, right=6), 
                PositionToken(content='34', gd=None, left=5, right=7), 
                PositionToken(content='4', gd=None, left=6, right=7)]
        self.assertListEqual(extract(gd,'abc1234abc'), expected_result)
        expected_result = [
                PositionToken(content=['1'], gd=None, left=3, right=4), 
                PositionToken(content=['1','2'], gd=None, left=3, right=5), 
                PositionToken(content=['1','2','3'], gd=None, left=3, right=6), 
                PositionToken(content=['1','2','3','4'], gd=None, left=3, right=7), 
                PositionToken(content=['2'], gd=None, left=4, right=5), 
                PositionToken(content=['2','3'], gd=None, left=4, right=6), 
                PositionToken(content=['2','3','4'], gd=None, left=4, right=7), 
                PositionToken(content=['3'], gd=None, left=5, right=6), 
                PositionToken(content=['3','4'], gd=None, left=5, right=7), 
                PositionToken(content=['4'], gd=None, left=6, right=7)]
        self.assertListEqual(extract(gd,[Token(x, None) for x in 'abc1234abc']), expected_result)
        self.assertListEqual(extract(gd,[x for x in 'abc1234abc']), expected_result)
        self.assertRaises(Exception, extract, None)
        self.assertListEqual(extract(gd,''), []) #Empty input

    def testRegularExpressionSearch(self):
        gd = RegularExpression('^[0123456789]*$')
        expected_result = PositionToken(content='1', gd=None, left=3, right=4)
        self.assertEqual(search(gd,'abc1234abc'), expected_result)
        expected_result = PositionToken(content=['1'], gd=None, left=3, right=4)
        self.assertEqual(search(gd,[Token(x, None) for x in 'abc1234abc']), expected_result)
        self.assertEqual(search(gd,[x for x in 'abc1234abc']), expected_result)
        self.assertRaises(Exception, search, None)
        self.assertListEqual(search(gd,''), []) #Empty input

    def testRegularExpressionMatch(self):
        gd = RegularExpression('^[0123456789]*$')
        expected_result = []
        self.assertEqual(match(gd,'abc1234abc'), expected_result)
        self.assertEqual(match(gd,[Token(x, None) for x in 'abc1234abc']), expected_result)
        self.assertEqual(match(gd,[x for x in 'abc1234abc']), expected_result)
        self.assertRaises(Exception, match, None)
        self.assertListEqual(match(gd,''), []) #Empty input



class TestAlphabetExtract(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3,0), "Full encoding support not available for python 2")
    def testEncoding(self):
        ad = ascii_encoding
        self.assertListEqual(extract(ad,''), [])
        self.assertListEqual(extract(ad,'a£'), [PositionToken('a', None, 0,1)])
        self.assertListEqual(extract(ad,['a','£']), [PositionToken(['a'], None, 0,1)])
        self.assertRaises(Exception, extract, None)

    def testChoices(self):
        gd = Choice([String('a'), String('b'), String('c')])
        self.assertListEqual(extract_alphabet(gd,'axbycz'), [PositionToken('a', None,0,1), PositionToken('b', None, 2,3), PositionToken('c', None, 4,5)])
        self.assertListEqual(extract_alphabet(gd,'xyzabcxyz'), [PositionToken('abc', None, 3,6)])
        self.assertListEqual(extract_alphabet(gd,'abcxyz'), [PositionToken('abc', None, 0,3)])
        self.assertListEqual(extract_alphabet(gd,[Token(x, None) for x in 'abcxyz']), [PositionToken(['a','b','c'], None, 0,3)])
        self.assertListEqual(extract_alphabet(gd,'abc'), [PositionToken('abc', None, 0,3)])
        self.assertListEqual(extract_alphabet(gd,''), [])
