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

"""loader class"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

def load(identifier, repositories):
    results = search(identifier, repositories)
    if not results:
        raise KeyError(identifier)
    if len(results) > 1:
        raise ValueError("Multiple results")
    identifier = list(results)[0]["identifier"]
    for repository in repositories:
        if identifier in repository:
            return repository.load(identifier)
    raise KeyError(identifier)

def search(query, repositories):
    from pypository.search.Searcher import Searcher
    from pypository.search.Indexer import Indexer
    searcher = Searcher([Indexer(x) for x in repositories])
    return searcher.search(query)
