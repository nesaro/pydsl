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


class TestActor(unittest.TestCase):
    pass

class TestSense(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Abstraction.Scheme import Sense
        self.__senser = Sense() #Loads a sense that reads from a function call
        self.__sensew = Sense() #Loads a sense that writes in a buffer member

    def testMemory(self):
        """Connects to a Memory"""
        pass

    def testMemoryWrite(self):
        """Connects to a memory, writes in memory"""
        pass

    def testMemoryRead(self):
        """Connects to a memory, read from memory, store in buffer"""
        pass

class TestWorkingMemory(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Abstraction.Memory import WorkingMemory
        self.__mem = WorkingMemory()

    def testSearch(self):
        self.__mem.search("")

    def testSave(self):
        from ColonyDSL.Concept.Concept import Concept
        self.__mem.save(Concept("concept1"), None)
        self.__mem['0']

    def testDelete(self):
        pass

    def testAutoClean(self):
        #future
        pass

class TestScheme(unittest.TestCase):
    def testJoinMemory(self):
        pass


