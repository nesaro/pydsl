
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


class TestExtract(unittest.TestCase):
    def testGrammarDefinition(self):
        from pydsl.Extract import extract
        from pydsl.Memory.Loader import load
        gd = load('integer')
        self.assertListEqual(extract(gd,'abc1234abc'), ['1234'])
        self.assertRaises(Exception, extract, None)

    def testAlphabet(self):
        from pydsl.Extract import extract
        from pydsl.Memory.Loader import load
        ad = load('ascii')
        self.assertListEqual(extract(ad,'a£'), ['a'])
        self.assertRaises(extract.extract(None))
