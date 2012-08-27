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

"""Abstract Classes"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractproperty


class Singleton(type):
    """singleton pattern metaclass"""
    #Only problem here is that classes can't have two metaclasses
    def __init__(self, name, bases, dct):
        self.__instance = None
        type.__init__(self, name, bases, dct)

    def __call__(self, *args, **kw):
        if self.__instance is None:
            self.__instance = type.__call__(self, *args, **kw)
        return self.__instance


class InmutableDict(dict):
    """A dict with a hash method for dictionary use"""
    def __hash__(self):
        if not self:
            return 0
        items = tuple(self.items())
        res = hash(items[0])
        for item in items[1:]:
            res ^= hash(item)
        return res

    def __eq__(self, other):
        if len(self.keys()) != len(other.keys()):
            return False
        for key in self:
            if other[key] != self.__getitem__(key):
                return False
        return True


class Indexable(metaclass=ABCMeta):
    """ This class is searchable """
    @abstractproperty
    def summary(self) -> InmutableDict:
        pass

    @classmethod
    def ancestors(cls):
        result = [cls.__name__]
        for x in cls.__bases__:
            if issubclass(x, Indexable):
                if not x in result:
                    result += x.ancestors()
        return tuple(result)
