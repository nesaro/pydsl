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


"""Exceptions definitions"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)
ERRORLIST = ["Grammar", "Timeout", "Transformer"]

class ProcessingError(Exception):
    def __init__(self, errortype, source = []):
        Exception.__init__(self)
        self.source = source
        assert(errortype in ERRORLIST)
        self.errortype = errortype

    def append(self, element):
        self.source.append(element)

class LRConflictException(Exception):
    pass

class BadFileFormat(Exception):
    def __init__(self, filename):
        Exception.__init__(self)
        self.filename = filename

class ParseError(Exception):
    def __init__(self, msg, offset):
        self.msg = msg
        self.offset = offset
    def __repr__(self):
        return "ParseError(%r, %r)" % (self.msg, self.offset)
    def __str__(self):
        return "%s at position %s" % (self.msg, self.offset + 1)

