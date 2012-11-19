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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class GrammarTools:
    """Convenience class that have members for checking, groups, tokenizing"""

    def get_groups(self, information, propertyname = None) -> list:
        """  
        returns [wordgroup1, wordgroup2] (list). A list of tokens.  provides dict like access.
        if propertyname == none: returns all input groups 
        """
        return []

    def groups(self) -> set:
        """Returns a set with all groups names"""
        return set() 

    def enumerate(self) -> set:
        """Yields a list of accepted values (if possible) else return {}"""
        return set() 

    def alphabet(self) -> set:
        """Returns the alphabet of this grammar, a list of token (if possible) else return {}"""
        return set()

    def tokenize(self, information):
        """tokenize and iterates through all tokens of the input (from left to right)"""
        raise NotImplementedError

    def distance(self, input1, input2 = None):
        """Gives a distance score between two words according to this grammar. If input2 == None, means distance from input1 to valid"""
        raise NotImplementedError

    @property
    def minsize(self):
        raise NotImplementedError

    @property
    def maxsize(self):
        raise NotImplementedError

#TODO
class NGramGrammar(GrammarTools):
    """Grammar defined by an ngram and a threshold"""
    pass
