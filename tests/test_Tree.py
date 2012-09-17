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
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestTrees(unittest.TestCase):
    def setUp(self):
        from pydsl.Grammar.Tree import AST
        a = AST(0,6,"abcdef", None)
        self.firstleaf1 = AST(0,1,"a", None)
        a.append_child(self.firstleaf1)
        b = AST(1,3,"bc", None)
        a.append_child(b)
        b.append_child(AST(1,2,"b",None))
        b.append_child(AST(2,3,"c",None))
        a.append_child(AST(3,4,"d",None))
        a.append_child(AST(4,5,"e",None))
        a.append_child(AST(5,6,"f",None))
        self.tree1 = a
        c = AST(0,6,"abcdef", None)
        self.firstleaf2 = AST(0,1,"a", None)
        c.append_child(self.firstleaf2)
        b = AST(1,3,"bc", None)
        c.append_child(b)
        b.append_child(AST(1,2,"b",None))
        b.append_child(AST(2,3,"j",None))
        c.append_child(AST(3,4,"d",None))
        c.append_child(AST(4,5,"e",None))
        c.append_child(AST(5,6,"f",None))
        self.tree2 = c

    def testBasics(self):
        self.assertTrue(len(self.tree1) == 6)
        self.assertTrue(self.tree1.first_leaf() == self.firstleaf1)

    def testTreeDistance(self):
        from pydsl.Grammar.Tree import zss_distance
        self.assertTrue(zss_distance(self.tree1,self.tree2) == 1)

