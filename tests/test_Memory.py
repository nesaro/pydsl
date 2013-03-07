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


class Texto(object):
    def summary(self):
        return {"iclass":"Texto"}


class TestMemory(unittest.TestCase):
    """Tests Local MEmory"""
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
    """Tests ShelveMemory"""
    def setUp(self):
        from pydsl.Memory.Shelve import ShelveStorage
        self.mem = ShelveStorage("tmp")
        
    def testSaveLoadAndDelete(self):
        from pydsl.Memory.Loader import load
        dg = load("cstring")
        if "cstring" in self.mem:
            del self.mem["cstring"]
        self.mem.save(dg, "cstring")
        newdg = self.mem["cstring"]
        self.assertEqual(newdg,dg)
        del self.mem["cstring"]

class TestLoader(unittest.TestCase):
    """Test loaders"""
    def setUp(self):
        from pydsl.Memory.Directory import DirStorage
        self.glibrary = DirStorage("/usr/share/pydsl/lib_contrib/grammar")
        from pydsl.Config import GLOBALCONFIG
        GLOBALCONFIG.strictgrammar = False

    def test_grammars(self):
        grammarlist = self.glibrary.all_names()
        from pydsl.Memory.Loader import load
        for grammar in grammarlist:
            load(grammar)
