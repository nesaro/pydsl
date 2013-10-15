#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

from pydsl.Grammar.Definition import StringGrammarDefinition
from pydsl.Match import match_factory

class TestStringGrammarMatch(unittest.TestCase):
    def setUp(self):
        self.grammardef = StringGrammarDefinition("abc")
        self.matcher = match_factory(self.grammardef)

    def testOkMatch(self):
        self.assertEqual(self.matcher("abcd"), ("abc","d"))

    def testNoMatch(self):
        self.assertRaises(Exception, self.matcher, "d")

