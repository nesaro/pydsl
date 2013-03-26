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

"""Test global configuration"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestConfig(unittest.TestCase):
    def testInstance(self):
        from pydsl.Config import GLOBALCONFIG


class TestInmutableDict(unittest.TestCase):
    def testEqual(self):
        from pydsl.Abstract import InmutableDict
        a = InmutableDict({"a":1,"b":2})
        b = InmutableDict({"a":1,"b":2})
        c = InmutableDict({"a":1,"b":3})
        self.assertEqual(a,b)
        self.assertEqual(hash(a),hash(b))
        self.assertNotEqual(a,c)
        self.assertNotEqual(hash(a),hash(c))
