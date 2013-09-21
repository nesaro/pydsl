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

class TestTrees(unittest.TestCase):
    def setUp(self):
        from pydsl.Tree import PositionTree
        a = PositionTree(0,6,"abcdef")
        self.firstleaf1 = PositionTree(0,1,"a")
        a.append_child(self.firstleaf1)
        b = PositionTree(1,3,"bc")
        a.append_child(b)
        b.append_child(PositionTree(1,2,"b"))
        b.append_child(PositionTree(2,3,"c"))
        a.append_child(PositionTree(3,4,"d"))
        a.append_child(PositionTree(4,5,"e"))
        a.append_child(PositionTree(5,6,"f"))
        self.tree1 = a
        c = PositionTree(0,6,"abcdef")
        self.firstleaf2 = PositionTree(0,1,"a")
        c.append_child(self.firstleaf2)
        b = PositionTree(1,3,"bc")
        c.append_child(b)
        b.append_child(PositionTree(1,2,"b"))
        b.append_child(PositionTree(2,3,"j"))
        c.append_child(PositionTree(3,4,"d"))
        c.append_child(PositionTree(4,5,"e"))
        c.append_child(PositionTree(5,6,"f"))
        self.tree2 = c

    def testBasics(self):
        self.assertTrue(len(self.tree1) == 6)
        self.assertTrue(self.tree1.first_leaf() == self.firstleaf1)

    def testTreeDistance(self):
        from pydsl.Tree import zss_distance
        self.assertTrue(zss_distance(self.tree1,self.tree2) == 1)

