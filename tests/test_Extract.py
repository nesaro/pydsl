
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
        from pydsl.Extract import Extract
        guesser = Extract('integer')
        self.assertListEqual(extract.extract('abc1234abc'), ['1234'])
        self.assertRaises(extract.extract(None))

    def testAlphabet(self):
        from pydsl.Extract import Extract
        guesser = Extract('ascii')
        self.assertListEqual(extract.extract('a£'), ['a'])
        self.assertRaises(extract.extract(None))


    def testLoad(self):
        gd = None
        from pydsl.Memory.Loader import load_extractor
        extractor = load_extractor(gd)
        self.assertTrue(extractor("input"))
