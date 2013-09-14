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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest

class TestValidate(unittest.TestCase):
    def setUp(self):
        from pydsl.Config import load_default_memory
        load_default_memory()

    def testBasic(self):
        from pydsl.Memory.Loader import load_parser
        parser = load_parser('Date', 'descent')
        self.assertFalse(parser.get_trees("11/11/ab", True)[0].valid)
        self.assertTrue(parser.get_trees("11/11/2011", True)[0].valid)

    def testValidateLoad(self):
        from pydsl.contrib.bnfgrammar import productionset0
        from pydsl.Memory.Loader import load_validator
        validator = load_validator(productionset0)
        self.assertTrue(validator("input"))

    def testTokenInput(self):
        pass

    def testListInput(self):
        pass

    def testEmptyInput(self):
        pass
