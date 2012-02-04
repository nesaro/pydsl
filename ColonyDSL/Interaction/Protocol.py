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

"""Protocolos"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger("Protocol")
from ColonyDSL.Abstract import Singleton
from abc import ABCMeta, abstractmethod 

PROTOLIST = ["file","lib"]
PROTOMODES = ["direct", "connection", "session", "continuous"]

class Interaction(metaclass=ABCMeta):
    """Protocol based interaction"""
    pass

class DirectInteraction(Interaction):
    @abstractmethod
    def get(self) -> "Information":
        pass

    @abstractmethod
    def put(self, information):
        pass

class ConnectionInteraction(Interaction):
    def connect(self):
        pass

    def get(self):
        pass

    def disconnect(self):
        pass

class Protocol(metaclass=Singleton):
    """ A method for data interaction with system. http://, file:// socket://, audio://"""
    def __init__(self, protocolstr:str):
        self.protocolstr = protocolstr
        self.modes = ["direct"]

    def check(self, uri)-> bool:
        """Check if the URI is handled by this protocol"""
        return str(uri).startswith(self.protocolstr)


from ColonyDSL.Identifier import Identifier

class URI(Identifier):
    """Unified resource information"""
    def __init__(self, name):
        Identifier.__init__(self)
        self.name = name

    def __dict__(self):
        protocol, path = self.name.split("://")
        result =  {"protocol":protocol}
        if "?" in path:
            npath, identifier = rest.split("?")
            result["path"] = npath
            result["identifier"] = identifier
        else:
            result["path"] = path
        return result

