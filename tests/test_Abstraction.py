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
from ColonyDSL.Concept.Concept import Concept

def funr(inputstr):
    if inputstr == "yellow":
        #TODO: Load Yellow Concept from Memory
        return Concept("yellow")
    elif inputstr == "black":
        #TODO: Load Black Concept from Memory
        return Concept("black")

def funw(inputconcept):
    if inputconcept == Concept("yellow"):
        return "#CDCD00"
    elif inputconcept == Concept("black"):
        return "#000000"

def funrecogcolor(inputconcept):
    if inputconcept == Concept("yellow") or inputconcept == Concept("black"):
        return True

class TestActor(unittest.TestCase):
    pass

class TestSense(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Abstraction.Scheme import Sense
        self.__senser = Sense(funr) #Loads a sense that reads from a function call and outputs concepts
        self.__sensew = Sense(funw) #Loads a sense that reads concepts and  writes in a buffer member

    def testCall(self):
        myconcept = self.__senser("yellow")
        mystr = self.__sensew(myconcept)
        self.assertEqual(mystr, "#CDCD00")

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

    def testMemoryWrite(self):
        """Connects to a memory, writes in memory"""
        pass

    def testMemoryRead(self):
        """Connects to a memory, read from memory, store in buffer"""
        pass

class TestScheme(unittest.TestCase):
    def testCall(self):
        from ColonyDSL.Abstraction.Scheme import Scheme
        myscheme = Scheme(funrecogcolor)
        result = myscheme(Concept("yellow"))
        self.assertTrue(result)
        result = myscheme(Concept("dog"))
        self.assertFalse(result)


