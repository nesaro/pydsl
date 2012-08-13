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


"""Storage class"""


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import abstractmethod, ABCMeta

import contextlib
import shelve
import logging
LOG = logging.getLogger(__name__)
from pydsl.Memory.Memory import Memory

class Storage(Memory, metaclass = ABCMeta):
    """External Memory. A Memory type which stores on physical files"""
    @abstractmethod
    def load(self, name, **kwargs):
        pass

    #Salvo que se implemente, no soporta guardado de elemento
    def save(self, element):
        raise Exception

    @abstractmethod
    def provided_iclasses(self) -> list:
        pass

class PersistentStorage(Storage):
    def __init__(self, dbname, allowedclass = None):
        Storage.__init__(self)
        self.identifier = dbname
        #store shelve path list
        #load/create each shelve path
        from pydsl.Config import GLOBALCONFIG
        if GLOBALCONFIG.persistent_dir:
            self.filename = GLOBALCONFIG.persistent_dir + "/" + dbname
        import threading
        self.lock = threading.Lock()
        self.allowedclass = allowedclass
    
    def load(self, name):
        return self.__getitem__(name)
    
    def __getitem__(self, name):
        with self.lock:
            a = shelve.open(self.filename)
            with contextlib.closing(a):
                result = a[name]
                return result
        
    def __iter__(self):
        self.index = 0
        with self.lock:
            a = shelve.open(self.filename)
            with contextlib.closing(a):
                self.cache = a.keys() #TODO: should return full dict, not only names
        return self

    def __next__(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
    
    def save(self, instance, identifier):
        if self.allowedclass and not isinstance(instance, self.allowedclass):
            raise TypeError
        with self.lock:
            a = shelve.open(self.filename)
            with contextlib.closing(a):
                a[str(identifier)] = instance
        
    def __delitem__(self, element):
        with self.lock:
            a = shelve.open(self.filename)
            with contextlib.closing(a):
                del a[element]
        
    def __contains__(self, element):
        with self.lock:
            a = shelve.open(self.filename)
            with contextlib.closing(a):
                return element in a
        
    def provided_iclasses(self):
        if self.allowedclass:
            return [self.allowedclass.__class__.__name__]
        return [] #FIXME: Default implementation should include all classes


