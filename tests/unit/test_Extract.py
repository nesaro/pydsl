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
from pydsl.Token import PositionToken


class TestGrammarExtract(unittest.TestCase):

    def testGrammarDefinition(self):
        from pydsl.Extract import extract
        from pydsl.Grammar import RegularExpression
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
        self.assertListEqual(extract(gd,[x for x in 'abc1234abc']), expected_result)
        self.assertRaises(Exception, extract, None)


class TestAlphabetExtract(unittest.TestCase):

    def testAlphabet(self):
        from pydsl.Extract import extract
        from pydsl.Grammar.Alphabet import Encoding
        ad = Encoding('ascii')
        self.assertListEqual(extract(ad,'a£'), [PositionToken('a', None, 0,1)])
        self.assertListEqual(extract(ad,['a','£']), [PositionToken(['a'], None, 0,1)])
        self.assertRaises(Exception, extract, None)

