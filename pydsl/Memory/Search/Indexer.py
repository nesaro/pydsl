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


from pydsl.Query import QueryEquality, QueryInclusion, QueryGreaterThan, QueryPartial
import collections
from pydsl.Abstract import ImmutableDict
import re

class Indexer(object):
    """Indexes memory content. Current implementation just copy Memory iterator (Immutabledicts) into a cache dict.
    This is possible because Memory iterator format is suitable for search, but it might change in the future"""
    def __init__(self, memory):
        self.memory = memory #One memory per indexer
        self.index = []
        self.__init_index()

    def __init_index(self):
        """Stores all data in the index"""
        for element in self.memory:
            if not isinstance(element, collections.Hashable):
                raise TypeError("Adding non hashable element %s to index" % str(element))
            self.index.append(element)

    def show_all(self):# -> list:
        """All elements inside index"""
        return list(self.index)

    def __update_index(self):
        """Updates index content"""
        for element in self.memory:
            if element not in self.index:
                self.index.append(element)

    @staticmethod
    def __get_left_value(left, element):
        if not '.' in left:
            return element[left]
        getlist = left.split('.')
        leftvalue = element[getlist[0]]
        for getindex in getlist[1:]:
            leftvalue = leftvalue.__getitem__(getindex)
        return leftvalue

    @staticmethod
    def __to_immutable(element):
        if isinstance(element, dict):
            return ImmutableDict(element)
        return element

    def search_index(self, queryterm): #-> set:
        result = set()
        right = queryterm.right
        left = queryterm.left
        for element in self.index:
            if not element:
                continue
            if isinstance(queryterm, QueryEquality):
                leftvalue = self.__get_left_value(left, element)
                if len(right)>2 and right[-1] == "/" and right[0] == "/":
                    #Regular Expression
                    rexp = re.compile(right[1:-1])
                    if rexp.match(leftvalue) is None:
                        continue
                elif right != leftvalue:
                    continue
            elif isinstance(queryterm, QueryInclusion):
                #a in b
                try:
                    if right[-1] == "/" and right[0] == "/":
                        #RegExp
                        rexp = re.compile(right[1:-1])
                        for item in element[left]:
                            if rexp.match(item) is not None:
                                break
                        else:
                            continue
                    else:
                        #string
                        if right not in element[left]:
                            continue
                except KeyError:
                    continue
            elif isinstance(queryterm, QueryPartial):
                if left not in element:
                    continue
                ismatch = True
                for key, value in right.items():
                    try:
                        if key not in element[left]:
                            ismatch = False
                            break
                        if element[left][key] != value:
                            ismatch = False
                    except KeyError:
                        continue
                if not ismatch:
                    continue
            elif isinstance(queryterm, QueryGreaterThan):
                try:
                    if int(queryterm.right) != int(element[left]):
                        continue
                except (KeyError, ValueError):
                    continue
            result.add(self.__to_immutable(element))
        return result


