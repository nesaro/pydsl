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

import unittest
from pydsl.Grammar.Definition import String
from pydsl.Alphabet import GrammarCollection


class TestBNF(unittest.TestCase):
    def setUp(self):
        from pydsl.contrib.bnfgrammar import productionset0
        self.grammardef = productionset0

    @unittest.skip("Not implemented")
    def testEnumerate(self):
        self.assertListEqual([x for x in self.grammardef.enum()], ["SR"])

    def testFirst(self):
        self.assertEqual(self.grammardef.first(), GrammarCollection([String("S")]))

    @unittest.skip("Not implemented")
    def testMin(self):
        self.assertEqual(self.grammardef.minsize,2)

    @unittest.skip("Not implemented")
    def testMax(self):
        self.assertEqual(self.grammardef.maxsize,2)

    def testFirstLookup(self):
        from pydsl.Grammar.Symbol import NonTerminalSymbol, TerminalSymbol
        from pydsl.Grammar.PEG import Choice
        self.grammardef.first_lookup(NonTerminalSymbol("exp"))[0]
        self.assertEqual(self.grammardef.first_lookup(NonTerminalSymbol("exp")),Choice([String("S")]))

    def testNextLookup(self):
        from pydsl.Grammar.Symbol import NonTerminalSymbol, EndSymbol
        self.grammardef.next_lookup(NonTerminalSymbol("exp"))[0]
        self.assertListEqual(self.grammardef.next_lookup(NonTerminalSymbol("exp")),[EndSymbol()])

    def testAlphabet(self):
        self.assertListEqual(list(self.grammardef.alphabet), [String(x) for x in ["S","R"]])
