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

from ColonyDSL.Abstract import Indexable
from abc import abstractmethod, ABCMeta

class WorkingMemoryElement(Indexable):
    def __init__(self, wm, source:str, content, taglist = []):
        Indexable.__init__(self)
        self.source = source
        self.content = content #concept or relation
        self.taglist = taglist
        self.identifier = wm.request_id()

    @property
    def summary(self):
        mydict = {"iclass":"WorkingMemoryElement", "identifier":str(self.identifier), "source":str(self.source), "content":str(self.content)}
        from ColonyDSL.Abstract import InmutableDict
        return InmutableDict(mydict)

#Objeto teorico a realizar:
##Scheme MatchConcept: Intentar cuadrar el contenido de la representacion con un concepto conocido. 
### Pepe y Sus podria ser un concepto "Conjunto de Personas"

from ColonyDSL.Memory.Memory import LocalMemory
class WorkingMemory(LocalMemory): 
    """
    Holds concepts (and maybe relations)
    It holds a DOM like struct where all concepts are linked with known concepts or new ones
    It kepts timestamps for allelements
    Only Accepts WorkingMemoryElement
    """
    def __init__(self):
        LocalMemory.__init__(self)
        self.totalseq = 0
    
    def save(self, content, source) -> int:
        """adds a new element. Returns sequence number"""
        element = WorkingMemoryElement(self, source, content)
        LocalMemory.save(self, element, element.identifier)
        return element.identifier
    
    def request_id(self):
        self.totalseq += 1
        return self.totalseq - 1

    def last_element(self):
        """Returns last element"""
        i = -1 
        element = None
        for key, value in self.content.items():
            if int(key) > i:
                element = value
                i = int(key)
        return element
