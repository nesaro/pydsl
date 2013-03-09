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

class TestLexer(unittest.TestCase):
    """Mongo checker"""
    def testSimpleLexing(self):
        """Test checker instantiation and call"""
        from pydsl.Alphabet.Lexer import Lexer
        from pydsl.Alphabet.Definition import AlphabetDictDefinition
        mydef = AlphabetDictDefinition({'1':'integer','2':'Date'})
        mylexer = Lexer(mydef)
        self.assertTrue(lexer.lexer('123411/23/32'),['integer','date']) 
        self.assertTrue([x for x in lexer.lexer_generator('123411/23/32')],['integer','date']) 

