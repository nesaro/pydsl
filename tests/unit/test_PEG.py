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

"""Tests PEG grammars"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Grammar.Definition import String, Grammar
from pydsl.Grammar.PEG import Many, Not, Sequence
from pydsl.Grammar.Alphabet import Choice

class TestPEG(unittest.TestCase):
    def testMany(self):
        mygrammar = Many(String("a"))
        self.assertTrue(isinstance(mygrammar, Grammar))

    def testChoice(self):
        mygrammar = Choice((String("a"), String("b")))
        from pydsl.Check import check
        self.assertTrue(check(mygrammar, "a"))
        self.assertTrue(check(mygrammar, "b"))
        self.assertFalse(check(mygrammar, "c"))
        self.assertEqual(mygrammar, mygrammar.first)

    def testNot(self):
        mygrammar = Not(String("a"))
        self.assertTrue(isinstance(mygrammar, Grammar))

    def testSequence(self):
        mygrammar = Sequence((String("a"), String("b")))
        self.assertTrue(isinstance(mygrammar, Grammar))
