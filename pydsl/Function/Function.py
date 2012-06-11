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

"""Function base classes"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod, abstractproperty
from pydsl.Abstract import Indexable 

class FunctionInterface(metaclass = ABCMeta):
    """A method applied to a function to comunicate with other functions"""
    pass

class Function(Indexable, metaclass = ABCMeta):
    """ data transformation or translation performed
    default interface: call -> data -> data
    """
    @abstractmethod
    def __call__(self, data):
        """ Non threaded, all input as parameter ibdic contains ("channel",data) pairs. Returns a TransformResult """
        pass

class FileFunction(Function):
    """Function restricted to work with file://* URI"""
    pass

class Error:
    """Error Transformation result"""
    def __init__(self, errortype, bt = []):
        from pydsl.Config import ERRORLIST
        self.__bt = bt
        assert(errortype in ERRORLIST)
        self.errortype = errortype

    def appendSource(self, name):
        self.__bt.append(name)

    @property
    def bt(self):
        return self.__bt

    def __str__(self):
        result = "<Error- source: " 
        result += str(self.__bt)
        result += " type: "
        result += str(self.errortype)
        result += " >"
        return result

    def __bool__(self):
        return False