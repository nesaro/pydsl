#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import unittest

class TestTrees(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Type.Grammar.Tree import PostTree
        a = PostTree("abcdef",0,6, None)
        self.firstleaf1 = PostTree("a",0,1, None)
        a.append_child(self.firstleaf1)
        b = PostTree("bc",1,3, None)
        a.append_child(b)
        b.append_child(PostTree("b",1,2,None))
        b.append_child(PostTree("c",2,3,None))
        a.append_child(PostTree("d",3,4,None))
        a.append_child(PostTree("e",4,5,None))
        a.append_child(PostTree("f",5,6,None))
        self.tree1 = a
        c = PostTree("abcdef",0,6, None)
        self.firstleaf2 = PostTree("a",0,1, None)
        c.append_child(self.firstleaf2)
        b = PostTree("bc",1,3, None)
        c.append_child(b)
        b.append_child(PostTree("b",1,2,None))
        b.append_child(PostTree("j",2,3,None))
        c.append_child(PostTree("d",3,4,None))
        c.append_child(PostTree("e",4,5,None))
        c.append_child(PostTree("f",5,6,None))
        self.tree2 = c

    def testBasics(self):
        self.assertTrue(len(self.tree1) == 6)
        self.assertTrue(self.tree1.ancestors() == [])
        self.assertTrue(self.tree1.first_leaf() == self.firstleaf1)

    def testTreeDistance(self):
        from ColonyDSL.Type.Grammar.Tree import zss_distance
        self.assertTrue(zss_distance(self.tree1,self.tree2) == 1)

