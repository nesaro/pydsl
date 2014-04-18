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
from pydsl.Grammar import RegularExpression

class TestGuesser(unittest.TestCase):
    def testGuesser(self):
        cstring = RegularExpression('.*')
        g1234 = RegularExpression('1234')
        memorylist = [cstring, g1234 ]
        from pydsl.Guess import Guesser
        guesser = Guesser(memorylist)
        self.assertListEqual(guesser('1234'), [cstring, g1234])
        self.assertListEqual(guesser([x for x in '1234']), [cstring, g1234])
        self.assertListEqual(guesser('134'), [cstring])

