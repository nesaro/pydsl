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
Query and related classes
"""

#Current query class only works for indexable elements
#for concepts ands relations, other operators are required: ELEMENT HASA CONCEPT1 OR ELEMENT ISA CONCEPT4 OR ELEMENT PROPERTY CONCEPT5

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

class QueryElement:
    pass

class QueryTerm(QueryElement):
    """Any query Term"""
    def __init__(self, left, right):
        self.left = left
        self.right = right


class QueryEquality(QueryTerm):
    """ a = b. It can use a string or a regexp"""
    def __hash__(self):
        return hash(self.left) ^ hash(self.right)
    def __str__(self):
        return "<" + str(self.left) + "=" + str(self.right) + ">"

class QueryPartial(QueryTerm):
    """ a = b. It can use a string or a regexp"""
    def __hash__(self):
        return hash(self.left) ^ hash(self.right)
    def __str__(self):
        return "<" + str(self.left) + "=~" + str(self.right) + ">"


class QueryInclusion(QueryTerm):
    """ looks for an element within a list """
    def __hash__(self):
        return hash(self.left) ^ hash(self.right)

class QueryGreaterThan(QueryTerm):
    """associated with > symbol """
    def __hash__(self):
        return hash(self.left) ^ hash(self.right)

class BinaryOperator(QueryElement):
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

class AndQueryOperator(BinaryOperator):
    def __str__(self):
        return "<" + str(self.element1) + "&&" + str(self.element2) + ">"

class OrQueryOperator(BinaryOperator):
    pass

class NotQueryOperator(QueryElement):
    def __init__(self, element):
        self.element = element
    def __str__(self):
        return "<!" + str(self.element) + ">"

class Query:
    """A generic query"""
    def __init__(self, content:QueryElement):
        self.content = content 

    def qand(self, element:QueryElement):
        self.content = AndQueryOperator(self.content, element)

    def qor(self, element:QueryElement):
        self.content = OrQueryOperator(self.content, element)

    def __str__(self):
        return("<Query:"+str(self.content)+">")

