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

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)

class TProcessingError(Exception):
    def __init__(self, source, errortype):
        Exception.__init__(self)
        self.source = source
        from .Config import ERRORLIST
        assert(errortype in ERRORLIST)
        self.errortype = errortype


class LRConflictException(Exception):
    pass

class BadFileFormat(Exception):
    def __init__(self, filename):
        Exception.__init__(self)
        self.filename = filename

