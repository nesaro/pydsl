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

class TestConcept(unittest.TestCase):
    """Tests Main Class"""
    def setUp(self):
        pass

    def testInstance(self):
        from ColonyDSL.Concept.Concept import Concept
        myconcept = Concept("concept1")

    def teststr(self):
        from ColonyDSL.Concept.Concept import Concept
        myconcept = Concept("concept1")
        self.assertTrue(isinstance(str(myconcept), str))

class TestRel(unittest.TestCase):
    def setUp(self):
        pass

    def testInstance(self):
        from ColonyDSL.Concept.Relation import Rel
        myrel = Rel("rel1", ["part1","part2"])


class TestRelation(unittest.TestCase):
    """Tests Main Class"""
    def setUp(self):
        pass

    def testInstance(self):
        from ColonyDSL.Concept.Relation import Rel
        myrel = Rel("rel1", ["left","right"])
        from ColonyDSL.Concept.Relation import Relation
        myconcept = Relation(myrel, {"left":"concept2", "right":"concept3"})


class TestConceptMemory(unittest.TestCase):
    def setUp(self):
        pass

    def testMemoryLoadAndQuery(self):
        #create a memory
        #load concepts
        #load a rel
        #load a relationship
        #query for concept
        #query for rel
        #query for relationships between concept1 and concept2
        pass
