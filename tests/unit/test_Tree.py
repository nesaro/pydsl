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

class TestTrees(unittest.TestCase):
    def setUp(self):
        from pydsl.Tree import ParseTree
        a = ParseTree(0,6, None, "abcdef")
        self.firstleaf1 = ParseTree(0,1, None, "a")
        a.append(self.firstleaf1)
        b = ParseTree(1,3,None, "bc")
        a.append(b)
        b.append(ParseTree(1,2,None, "b"))
        b.append(ParseTree(2,3,None, "c"))
        a.append(ParseTree(3,4,None, "d"))
        a.append(ParseTree(4,5,None, "e"))
        a.append(ParseTree(5,6,None, "f"))
        self.tree1 = a
        c = ParseTree(0,6, None, "abcdef")
        self.firstleaf2 = ParseTree(0,1, None, "a")
        c.append(self.firstleaf2)
        b = ParseTree(1,3, None, "bc")
        c.append(b)
        b.append(ParseTree(1,2, None, "b"))
        b.append(ParseTree(2,3, None, "j"))
        c.append(ParseTree(3,4, None, "d"))
        c.append(ParseTree(4,5, None, "e"))
        c.append(ParseTree(5,6, None, "f"))
        self.tree2 = c

    def testBasics(self):
        self.assertTrue(len(self.tree1) == 6)


class TestPositionResultList(unittest.TestCase):
    def testMain(self):
        from pydsl.Tree import PositionResultList
        seq = PositionResultList()
        seq.append(0,1,".")
        seq.append(1,2,".")
        seq.append(2,3,".")
        seq.append(3,4,".")
        seq.append(4,5,".")
        self.assertEqual(len(seq.valid_sequences()[-1]), 5)

