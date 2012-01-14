#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Abstract Classes"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

import logging
LOG = logging.getLogger("Type")
from abc import ABCMeta, abstractmethod
from ColonyDSL.Abstract import Indexable

class Type(Indexable, metaclass = ABCMeta):
    """ Ensures information follows a rule, protocol or has a shape.
    Provides only check function, for complex operations, use Grammar"""
    def __init__(self, identifier):
        Indexable.__init__(self, identifier)

    @abstractmethod
    def check(self, value):
        pass

class DummyType(Type):
    """ Calls another program to perform checking"""
    def __init__(self):
        Type.__init__(self, "DummyType")

    def check(self, word):
        return True
        
    def __eq__(self, other):
        if isinstance(other, DummyType):
            return True
        return False
        
    @property
    def summary(self):
        return {"iclass":"DummyType", "description":self.description, "ancestors":self.ancestors() }

