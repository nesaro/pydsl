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

from pydsl.Abstract import Indexable

class Texto(Indexable):
    def summary(self):
        return {"iclass":"Texto"}


class TestMemory(unittest.TestCase):
    """Tests Transformers"""
    def setUp(self):
        from pydsl.Memory.Memory import LocalMemory
        self.mem = LocalMemory()
        
    def testSaveLoadAndDelete(self):
        texto1 = Texto()
        texto2 = Texto()
        self.mem.save(texto1,"id1")
        self.mem.save(texto2, "id2")
        newdg = self.mem["id1"]
        self.assertTrue(newdg == texto1)
        del self.mem["id1"]
        del self.mem["id2"]

    def testSimpleSearch(self):
        return True

class TestPersistentMemory(unittest.TestCase):
    """Tests Transformers"""
    def setUp(self):
        from pydsl.Memory.Storage.Storage import PersistentStorage
        from pydsl.Grammar.Checker import Checker
        self.mem = PersistentStorage("tmp", Checker)
        
    @unittest.skip
    def testSaveLoadAndDelete(self):
        from pydsl.Grammar.Checker import DummyChecker
        dg = DummyChecker()
        if "DummyChecker" in self.mem:
            del self.mem["DummyChecker"]
        self.mem.save(dg, "DummyChecker")
        newdg = self.mem["DummyChecker"]
        self.assertEqual(newdg,dg)
        del self.mem["DummyChecker"]
