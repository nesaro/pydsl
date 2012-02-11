#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from ColonyDSL.Abstract import Indexable
from abc import abstractmethod, ABCMeta


class WorkingMemoryElement(Indexable):
    def __init__(self, rep, source:str, content, taglist = []):
        Indexable.__init__(self, rep.request_id())
        self.source = source
        self.content = content
        self.taglist = taglist

    @property
    def summary(self):
        mydict = {"iclass":"WorkingMemoryElement", "identifier":str(self.identifier), "source":str(self.source), "content":str(self.content)}
        from ColonyDSL.Abstract import InmutableDict
        return InmutableDict(mydict)

from ColonyDSL.Memory.Memory import LocalMemory
class WorkingMemory(LocalMemory): 
    def __init__(self):
        LocalMemory.__init__(self)
        self.connections = {} 
        self.totalseq = 0
    
    def register(self, connection, slot, identifier):
        if not identifier in self.connections:
            self.connections[identifier] = []
        self.connections[identifier].append((connection, slot))
        connection.actor.register(connection, slot)

    def save(self, content, source) -> int:
        element = WorkingMemoryElement(self, source, content)
        LocalMemory.save(self, element)
        for conn, slot in self.connections[source]:
            conn.actor.receive(conn, slot, element)
        return element.identifier
    
    def request_id(self):
        self.totalseq += 1
        return self.totalseq - 1

    def last_element(self):
        i = -1 
        element = None
        for key, value in self.content.items():
            if int(key) > i:
                element = value
                i = int(key)
        return element
