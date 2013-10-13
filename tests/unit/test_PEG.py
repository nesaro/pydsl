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

"""Tests spark integration"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Grammar.Definition import StringGrammarDefinition, GrammarDefinition
from pydsl.Grammar.PEG import Many, Choice, Not, Sequence

class TestPEG(unittest.TestCase):
    def testMany(self):
        mygrammar = Many(StringGrammarDefinition("a"))
        self.assertTrue(isinstance(mygrammar, GrammarDefinition))

    def testChoice(self):
        mygrammar = Choice((StringGrammarDefinition("a"), StringGrammarDefinition("b")))
        self.assertTrue(isinstance(mygrammar, GrammarDefinition))

    def testNot(self):
        mygrammar = Not(StringGrammarDefinition("a"))
        self.assertTrue(isinstance(mygrammar, GrammarDefinition))

    def testSequence(self):
        mygrammar = Sequence((StringGrammarDefinition("a"), StringGrammarDefinition("b")))
        self.assertTrue(isinstance(mygrammar, GrammarDefinition))
