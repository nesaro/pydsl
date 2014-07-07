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


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Grammar.Definition import RegularExpression
import re

class TestRegularExpression(unittest.TestCase):
    """Regular expression method tests"""
    def testInstantiation(self):
        re1 = RegularExpression('^a$')
        re2 = RegularExpression(re.compile('^a$'))
        self.assertEqual(str(re1), str(re2)) #FIXME python3 default flag value is 32

    def testEnumerate(self):
        re1 = RegularExpression(re.compile('^a$'))
        self.assertRaises(NotImplementedError, re1.enum)

    def testFirst(self):
        re1 = RegularExpression(re.compile('^a$'))
        self.assertEqual(len(re1.first()),1)
        from pydsl.Grammar.Definition import String
        self.assertEqual(re1.first()[0],String('a'))

    def testMin(self):
        re1 = RegularExpression(re.compile('^a$'))
        re1.minsize

    def testMax(self):
        re1 = RegularExpression(re.compile('^a$'))
        re1.maxsize

    def testAlphabet(self):
        from pydsl.Encoding import ascii_encoding
        re1 = RegularExpression(re.compile('^a$'))
        self.assertEqual(re1.alphabet, ascii_encoding)

