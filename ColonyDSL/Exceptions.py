#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Exceptions definitions"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"


import logging
LOG = logging.getLogger("Exceptions")

class ColonyException(Exception):
    """ColonyDSL Exception Base Class"""
    pass

class NameOverlap(ColonyException):
    pass

class TProcessingError(ColonyException):
    def __init__(self, source, errortype):
        ColonyException.__init__(self)
        self.source = source
        from .GlobalConfig import ERRORLIST
        assert(errortype in ERRORLIST)
        self.errortype = errortype

class EventError(ColonyException):
    """Event related exception"""
    pass

class ParserError(ColonyException):
    pass

class LRConflictException(ParserError):
    pass

class LibraryException(ColonyException):
    """Error while accessing library element"""
    def __init__(self, elementtype, elementname):
        ColonyException.__init__(self)
        self.elementtype = elementtype
        self.elementname = elementname

    def __str__(self):
        return "LIBRARY EXCEPTION: " + str(self.elementtype) + ": " + str(self.elementname)

class BadFileFormat(ColonyException):
    def __init__(self, filename):
        ColonyException.__init__(self)
        self.filename = filename

