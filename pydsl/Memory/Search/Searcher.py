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

"""
Searcher class
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

#En esta implementacion, el searcher se enlaza con un indexer. El usuario introduce un Query, y se utiliza el indexer para averiguar que documentos cumplen cada una de las condiciones. El uso de operadores and y or se realizara despues de obtener los resultados con operaciones de conjuntos

#A searcher is linked with an indexer. Users creates a query, and then searcher iterates the indexer to find matches

from .Indexer import Indexer

class Searcher(object):
    def search(self, query):
        raise NotImplementedError

class MemorySearcher(Searcher):
    def __init__(self, indexerlist):
        from pydsl.Memory.Memory import Memory
        if isinstance(indexerlist, Indexer):
            indexerlist = [indexerlist]
        elif isinstance(indexerlist, Memory):
            indexerlist = [Indexer(indexerlist)]
        assert(isinstance(indexerlist, list))
        self.indexerlist = indexerlist

    def search(self, query = None): # -> set:
        if isinstance(query, str):
            from .Query import str_to_memoryquery
            query = str_to_memoryquery(query)
        elif isinstance(query, dict):
            from .Query import dict_to_query
            query = dict_to_query(query)
        if not query:
            result = set()
            for indexer in self.indexerlist:
                result = result.union(indexer.show_all())
            return result
        return self.__recursive_search(query.content)

    def __recursive_search(self, queryelement): # -> set:
        from pydsl.Query import NotQueryOperator, AndQueryOperator, OrQueryOperator, QueryTerm
        if isinstance(queryelement, AndQueryOperator):
            r1 = self.__recursive_search(queryelement.element1)
            r2 = self.__recursive_search(queryelement.element2)
            return r1.intersection(r2)
        elif isinstance(queryelement, OrQueryOperator):
            r1 = self.__recursive_search(queryelement.element1)
            r2 = self.__recursive_search(queryelement.element2)
            return r1.union(r2)
        elif isinstance(queryelement, NotQueryOperator):
            total = set()
            for indexer in self.indexerlist:
                total = total.union(indexer.show_all())
            s1 = self.__recursive_search(queryelement.element)
            return total.difference(s1)
        elif isinstance(queryelement, QueryTerm):
            result = set()
            for indexer in self.indexerlist:
                result = result.union(indexer.search_index(queryelement))
            return result
        else:
            raise TypeError


