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


class TestBNF(unittest.TestCase):
    def setUp(self):
        from pydsl.contrib.bnfgrammar import productionset0
        self.grammardef = productionset0

    @unittest.skip
    def testEnumerate(self):
        self.assertListEqual([x for x in self.grammardef.enum()], ["SR"])

    def testFirst(self):
        from pydsl.Grammar.Definition import String
        self.assertEqual(self.grammardef.first, String("S"))

    @unittest.skip
    def testMin(self):
        self.assertEqual(self.grammardef.minsize,2)

    @unittest.skip
    def testMax(self):
        self.assertEqual(self.grammardef.maxsize,2)

    def testFirstLookup(self):
        from pydsl.Grammar.Symbol import NonTerminalSymbol, TerminalSymbol
        from pydsl.Alphabet import AlphabetListDefinition
        from pydsl.Grammar.Definition import String
        self.grammardef.first_lookup(NonTerminalSymbol("exp"))[0]
        self.assertEqual(self.grammardef.first_lookup(NonTerminalSymbol("exp")).to_list,AlphabetListDefinition([String("S")]).to_list)

    def testNextLookup(self):
        from pydsl.Grammar.Symbol import NonTerminalSymbol, EndSymbol
        self.grammardef.next_lookup(NonTerminalSymbol("exp"))[0]
        self.assertListEqual(self.grammardef.next_lookup(NonTerminalSymbol("exp")),[EndSymbol()])

    def testAlphabet(self):
        from pydsl.Grammar.Definition import String
        self.assertListEqual(self.grammardef.alphabet().to_list, [String(x) for x in ["S","R"]])
