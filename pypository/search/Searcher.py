#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pypository.
#
#pypository is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pypository is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pypository.  If not, see <http://www.gnu.org/licenses/>.

"""
Searcher class
A searcher is linked with an indexer. Users creates a query, and then searcher iterates the indexer to find matches
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


from .Indexer import Indexer

class Searcher(object):
    def __init__(self, indexerlist):
        from pypository.Repository import Repository
        if isinstance(indexerlist, Indexer):
            indexerlist = [indexerlist]
        elif isinstance(indexerlist, Repository):
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
        from .Query import NotQueryOperator, AndQueryOperator, OrQueryOperator, QueryTerm
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
            raise TypeError("got %s" % (queryelement.__class__.__name__,))


