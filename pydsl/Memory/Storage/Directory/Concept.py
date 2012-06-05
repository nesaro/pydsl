#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Concepts DirLibrary Module"""

from .DirStorage import DirStorage 
import logging
LOG = logging.getLogger("DirLibrary.Concept")

class ConceptFileStorage(DirStorage):
    """Concept DirLibrary"""
    def __init__(self):
        DirStorage.__init__(self, "concept/", [".py"])
    
class ConceptToValueFileStorage(DirStorage):
    def __init__(self):
        DirStorage.__init__(self, "concepttovalue/", [".py"])
    
