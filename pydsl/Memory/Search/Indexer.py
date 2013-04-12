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
from pydsl.Abstract import InmutableDict
import re

class Indexer(object):
    """Indexes memory content. Current implementation just copy Memory iterator (Inmutabledicts) into a cache dict.
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

    def search_index(self, queryterm): #-> set:
        result = set()
        right = queryterm.right
        if isinstance(queryterm, QueryEquality):
            for element in self.index:
                if not element:
                    continue
                elementright = None
                if queryterm.left.count('.') > 0:
                    getlist = queryterm.left.split('.')
                    try:
                        elementright = element[getlist[0]]
                        for getindex in getlist[1:]:
                            elementright = elementright.__getitem__(getindex)
                    except KeyError:
                        continue
                if not elementright and not queryterm.left in element:
                    continue
                if not elementright:
                    elementright = element[queryterm.left]
                if len(right)>2 and right[-1] == "/" and right[0] == "/":
                    #Regular Expression
                    rexp = re.compile(right[1:-1])
                    if rexp.match(elementright) is None:
                        continue
                else:
                    if right != elementright:
                        continue
                if isinstance(element, dict):
                    result.add(InmutableDict(element))
                else:
                    result.add(element)
        elif isinstance(queryterm, QueryInclusion):
            for element in self.index:
                try:
                    if right[-1] == "/" and right[0] == "/":
                        #RegExp
                        rexp = re.compile(right[1:-1])
                        for item in element[queryterm.left]:
                            if rexp.match(item) is not None:
                                break
                        else:
                            continue
                    else:
                        #string
                        if right not in element[queryterm.left]:
                            continue
                except KeyError:
                    continue
                if isinstance(element, dict):
                    result.add(InmutableDict(element))
                else:
                    result.add(element)
        elif isinstance(queryterm, QueryPartial):
            for element in self.index:
                ismatch = True
                if queryterm.left not in element:
                    continue
                for key, value in right.items():
                    try:
                        if key not in element[queryterm.left]:
                            ismatch = False
                            break
                        if element[queryterm.left][key] != value:
                            ismatch = False
                    except KeyError:
                        continue
                if not ismatch:
                    continue
                if isinstance(element, dict):
                    result.add(InmutableDict(element))
                else:
                    result.add(element)
        elif isinstance(queryterm, QueryGreaterThan):
            try:
                right = int(queryterm.right)
            except ValueError:
                return set()
            for element in self.index:
                #TODO: "." operator for dict member access
                try:
                    if right != int(element[queryterm.left]):
                        continue
                except (KeyError, ValueError):
                    continue
                if isinstance(element, dict):
                    result.add(InmutableDict(element))
                else:
                    result.add(element)
        return result


