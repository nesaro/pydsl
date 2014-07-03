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
from pydsl.Alphabet import Encoding

class TestBinaryAlphabet(unittest.TestCase):
    def test_binaryAlphabet(self):
        binary_alphabet = GrammarCollection([String('0'), String('1')])
        lexed = Lexer(binary_alphabet, '010')
        self.assertListEqual(lexed, Token...)
        diff('0101', '0110')
        extract('a010', base_alphabet=ascii)
        ascii_subset = GrammarCollection([String('0000'), String('0001'), ...])
        ascii_binary = encode('000000010010', ascii_subset)
        characters = encode(ascii_binary, ascii_subset, base_alphabet = binary_alphabet)
