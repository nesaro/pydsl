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

from ColonyDSL.Abstract import Indexable

class Texto(Indexable):
    def summary(self):
        return {"iclass":"Texto"}


class TestMemory(unittest.TestCase):
    """Tests Transformers"""
    def setUp(self):
        from ColonyDSL.Memory.Memory import LocalMemory
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
        from ColonyDSL.Memory.External.Library import PersistentLibrary
        from ColonyDSL.Type.Type import Type
        self.mem = PersistentLibrary("tmp", Type)
        
    def testSaveLoadAndDelete(self):
        from ColonyDSL.Type.Type import DummyType
        dg = DummyType()
        if "DummyType" in self.mem:
            del self.mem["DummyType"]
        self.mem.save(dg, "DummyType")
        newdg = self.mem["DummyType"]
        self.assertTrue(newdg == dg)
        del self.mem["DummyType"]
