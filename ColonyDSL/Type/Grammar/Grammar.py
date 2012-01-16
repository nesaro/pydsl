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


"""Grammar Class"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

import logging
from ColonyDSL.Type.Type import Type
from abc import ABCMeta, abstractmethod, abstractproperty
LOG = logging.getLogger("Grammar")

class Grammar(Type, metaclass = ABCMeta):
    """Checks if an  belongs to a language. 
    It can also have functions to extract elements or guess information about the sentence or production rule """
    def get_groups(self, information, propertyname = None) -> list:
        """  
        returns [wordgroup1, wordgroup2] (list). A list of tokens
        dict like access
        if propertyname == none: returns all input groups 
        """
        return []

    def groups(self) -> set:
        """Returns a set with all groups names"""
        pass

    def enumerate(self) -> set:
        """Returns a set of accepted values (if possible) else return {}"""
        return set() 

    @abstractproperty
    def alphabet(self) -> set:
        """Returns the alphabet of this grammar, a list of values (if possible) else return {}"""
        return set()

    def genealogy(self, information, index) -> list:
        """Given a word(token) index, will tell all parent symbols  until root node"""
        pass

    #@abstractmethod
    def iterate(self, information):
        """Iterates through all tokens of the input (from left to right)"""
        pass

#TODO
class NGramGrammar(Grammar):
    """Grammar defined by an ngram and a threshold"""
    pass
