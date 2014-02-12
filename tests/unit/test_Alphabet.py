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
from pydsl.Check import checker_factory
from pydsl.Lex import lexer_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Grammar import String
from pydsl.Grammar.PEG import Sequence
from pydsl.Grammar.Alphabet import Choice, Encoding, GrammarCollection
from pydsl.Grammar import RegularExpression
from pydsl.File.BNF import load_bnf_file
from pydsl.File.Python import load_python_file


class TestAlphabet(unittest.TestCase):
    def setUp(self):
        self.integer = RegularExpression("^[0123456789]*$")
        self.date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':self.integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})

    def testChecker(self):
        alphabet = GrammarCollection([self.integer,self.date])
        checker = checker_factory(alphabet)
        self.assertTrue(checker.check("1234"))
        self.assertTrue(checker.check([x for x in "1234"]))
        self.assertFalse(checker.check("11/11/1991")) #Non tokenized input
        self.assertFalse(checker.check([x for x in "11/11/1991"])) #Non tokenized input
        self.assertTrue(checker.check(["11","/","11","/","1991"])) #tokenized input
        self.assertFalse(checker.check("bcdf"))
        self.assertFalse(checker.check([x for x in "bcdf"]))

    def testEncoding(self):
        alphabet = Encoding('ascii')
        self.assertTrue(alphabet[0])
        self.assertEqual(len(alphabet.enum()), 128)
        alphabet = Encoding('unicode')
        self.assertTrue(alphabet[0])
        self.assertEqual(len(alphabet.enum()), 9635)
        self.assertRaises(KeyError, alphabet.__getitem__, 'a')
        self.assertRaises(KeyError, alphabet.__getitem__, 5.5)
        self.assertTrue(alphabet[100])
