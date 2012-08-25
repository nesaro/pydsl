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

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import unittest

class TestMongoChecker(unittest.TestCase):
    def testCheck(self):
        spec = {"a":1,"b":2}
        bad = {"a":1,"b":3}
        letter = {"a":1,"b":"asd"}
        fullspec = {"a":{"$type":"integer"},"b":{"$type":"integer"}}
        from pydsl.Grammar.Checker import MongoChecker
        checker = MongoChecker(spec)
        self.assertTrue(checker.check(spec))
        self.assertFalse(checker.check(bad))
        fullchecker = MongoChecker(fullspec)
        self.assertTrue(fullchecker.check(spec))
        self.assertTrue(fullchecker.check(bad))
        self.assertFalse(fullchecker.check(letter))
