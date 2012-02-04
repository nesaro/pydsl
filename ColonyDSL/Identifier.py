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

"""
Identifiers.
Class that identifies an element but doesn't hold information about it
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from abc import ABCMeta 
import logging
LOG = logging.getLogger("Identifier")

class Identifier(metaclass = ABCMeta):
    """Abstract identifier"""
    pass

class FunctionNetworkClientId(Identifier):
    """Unique identifier for FunctionNetworkClients Hierarchy"""
    def __init__(self, name, path = None):
        Identifier.__init__(self)
        self.name = name
        self.path = path 
        
    @property
    def absname(self):
        if self.path:
            return self.path + "." + self.name
        return self.name

    def reparent(self, newpath):
        self.path = newpath

    def __hash__(self):
        return self.absname.__hash__()

    def __eq__(self, other):
        if not isinstance(other, FunctionNetworkClientId):
            LOG.warning('comparing an eventclientid with ' + str(other))
            return False
        return other.path == self.path and other.name == self.name

    def __str__(self):
        return self.absname

    def __contains__(self, element):
        if self.path == None:
            return True
        return self.path in element.path

