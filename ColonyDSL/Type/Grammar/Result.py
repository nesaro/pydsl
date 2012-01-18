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
Grammar result object
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"


import logging
LOG = logging.getLogger("Grammar.Result")
from abc import ABCMeta


class GrammarResult(metaclass = ABCMeta):
    """When a grammar checks an Information, it returns an instance of this class"""
    def __init__(self, isvalid):
        self._isvalid = bool(isvalid)

    def __bool__(self):
        """True or false"""
        return self._isvalid

    def __str__(self):
        return str(bool(self))

class DiscreteGrammarResult(GrammarResult):
    def __init__(self, isvalid, flagdic = {}):
        GrammarResult.__init__(self, isvalid)
        self.__flagdic = flagdic

    @property
    def flags(self) -> dict:
        #SUBSTRING (left or right or both)
        #AMBIGUOUS
        return self.__flagdic

    def error_locations(self) -> list:
        """returns the most accurate error locations available"""
        #a list of (begin, end, group=None) 
        return {}

class ProbabilityGrammarResult(GrammarResult):
    """Returns an ordered list with most probable status"""
    def __init__(self, isvalid, threshold = 0.5):
        GrammarResult.__init__(self, isvalid)
        self.__threshold = threshold

    def validResults(self) -> list:
        """Return all valid results (list) """
        pass

