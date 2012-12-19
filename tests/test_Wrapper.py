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

"""Test wrapper"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestWrapper(unittest.TestCase):
    def testBasic(self):
        from pydsl.Wrapper import Content, FunctionPool
        a = Content("abcde")
        #a.available_alphabet()
        #a.select_alphabet("unicode") #Autodetected as encoding
        a.available_grammars()
        a.select_grammar("cstring")
        transformlist = FunctionPool.available_transforms(a)
        result = FunctionPool.lowerCase(a.content) #Result should be a content with the right alphabet/grammar

