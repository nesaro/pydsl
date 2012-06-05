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

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import unittest

class TestQuery(unittest.TestCase):
    """Test search query functions"""
    def setUp(self):
        pass
    
    def teststrToQuery(self):
        from pydsl.Memory.Search.Query import str_to_memoryquery
        str_to_memoryquery("id")
        str_to_memoryquery("identifier=id")
        str_to_memoryquery("identifier=id&&description=desc")
        str_to_memoryquery("identifier=id&&!description=desc")
        
    def testdicttoQuery(self):
        from pydsl.Memory.Search.Query import dict_to_query
        dict_to_query({"identifier":"id"})
        dict_to_query({"identifier":"id","description":"desc"})
        dict_to_query({"identifier":"id","description":{"$not":"desc"}})
        myquery = dict_to_query({"roledict":{"$part":{"subject":"human"}}})
        from pydsl.Memory.Memory import LocalMemory
        mymem = LocalMemory()
        from pydsl.Concept.Concept import Concept
        from pydsl.Concept.Relation import Relation, Rel
        concept1 = Concept("human")
        concept2 = Concept("animal")
        concept3 = Concept("dog")
        rel = Rel("ISA", ["subject","object"])
        rela = Relation(rel,{"subject":concept1,"object":concept2})
        relb = Relation(rel,{"subject":concept3,"object":concept2})
        mymem.save( concept1,"c1")
        mymem.save( concept2,"c2")
        mymem.save( concept3,"c3")
        #mymem.save(rel,"r1")
        mymem.save(rela,"r2")
        mymem.save(relb,"r3")
        mymem.search(myquery)



