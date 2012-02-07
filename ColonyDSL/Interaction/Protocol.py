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


def protocol_split(content):
    """Splits a protocol string"""
    try:
        protocol, path = content.split("://")
    except ValueError:
        return {"protocol":""}
    result =  {"protocol":protocol}
    if "?" in path:
        npath, identifier = rest.split("?")
        result["path"] = npath
        result["identifier"] = identifier
    else:
        result["path"] = path
    return result

