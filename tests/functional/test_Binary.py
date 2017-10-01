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
from pydsl.grammar import String
from pydsl.grammar.parsley import ParsleyGrammar
from pydsl.grammar.PEG import OneOrMore, Choice
from pydsl.translator import ParsleyTranslator


class TestBinaryAlphabet(unittest.TestCase):
    def test_binaryAlphabet(self):
        binary_alphabet = Choice([String('0'), String('1')])
        binary_number = OneOrMore(binary_alphabet)
        parsley_grammar = ParsleyGrammar("""digit = anything:x ?(x in '01')
number = <digit+>:ds -> int(ds)
expr = number:left ( '+' number:right -> left + right 
                   | -> left)""", "expr")
        binary_addition = ParsleyTranslator(parsley_grammar)
        self.assertEqual(binary_addition('01+10'), 11)

