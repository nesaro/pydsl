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

import unittest
from pydsl.Translator import translator_factory
from pydsl.Check import checker_factory
from pydsl.File.Python import load_python_file
import sys

__author__ = "Ptolom"
__copyright__ = "Copyright 2014, Ptolom"
__email__ = "ptolom@hexifact.co.uk"

class TestParsley(unittest.TestCase):
    def testDate(self):
        import parsley
        from pydsl.File.Parsley import load_parsley_grammar_file
        repository = {'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')} #DayOfMonth loaded as checker
        G=load_parsley_grammar_file("pydsl/contrib/grammar/Date.parsley", "expr", repository)
        C=checker_factory(G)
        T=translator_factory(G)
        self.assertTrue(C("2/4/12"))
        self.assertEqual(T("2/4/12"),(2,4,12))
        self.assertRaises(parsley.ParseError,T, "40/4/12")
        
    def testCalculator(self):
        import parsley
        G=load_python_file("pydsl/contrib/translator/calculator.py")
        T=translator_factory(G)
        self.assertEqual(T("1+1"),2)
        

if __name__ == '__main__':
        unittest.main()
