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


"""Abstract Classes"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger("Type")
from abc import ABCMeta, abstractmethod
from ColonyDSL.Abstract import Indexable

class Type(Indexable, metaclass = ABCMeta):
    """ Ensures information follows a rule, protocol or has a shape.
    Provides only check function, for complex operations, use Grammar"""
    @abstractmethod
    def check(self, value):
        pass

class DummyType(Type):
    """ Calls another program to perform checking"""
    def check(self, word):
        return True
        
    def __eq__(self, other):
        if isinstance(other, DummyType):
            return True
        return False
        
    @property
    def summary(self):
        return {"iclass":"DummyType", "description":self.description, "ancestors":self.ancestors() }

