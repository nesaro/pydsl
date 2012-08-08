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

"""Protocols"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Abstract import Singleton
from abc import ABCMeta, abstractmethod 

PROTOLIST = ["file","lib"]
PROTOMODES = ["direct", "connection", "session", "continuous"]

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

