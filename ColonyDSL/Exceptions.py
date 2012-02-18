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


"""Exceptions definitions"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Exceptions")

class NameOverlap(Exception):
    pass

class TProcessingError(Exception):
    def __init__(self, source, errortype):
        Exception.__init__(self)
        self.source = source
        from .Config import ERRORLIST
        assert(errortype in ERRORLIST)
        self.errortype = errortype

class EventError(Exception):
    """Event related exception"""
    pass

class ParserError(Exception):
    pass

class LRConflictException(ParserError):
    pass

class LibraryException(Exception):
    """Error while accessing library element"""
    def __init__(self, elementtype, elementname):
        Exception.__init__(self)
        self.elementtype = elementtype
        self.elementname = elementname

    def __str__(self):
        return "LIBRARY EXCEPTION: " + str(self.elementtype) + ": " + str(self.elementname)

class BadFileFormat(Exception):
    def __init__(self, filename):
        Exception.__init__(self)
        self.filename = filename

