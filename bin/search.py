#!/usr/bin/python3
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


"""This program perform searchs across library"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


def search_pp(inputset: set, filterlist = None) -> str:
    """Search pretty print"""
    result = ""
    for element in inputset:
        for key in element:
            if filterlist == None or key in filterlist:
                if isinstance(element[key], tuple):
                    result += key + "-> " + str(element[key]) + " "
                else:
                    result += key + ": " + str(element[key]) + " "
        result += '\n'
    return result

def filterset(inputset: set, filterlist = None) -> set:
    if filterlist == None:
        return inputset #Don't filter at all
    from pydsl.Abstract import InmutableDict
    result = set()
    for element in inputset:
        telement = {}
        for key in element:
            if key in filterlist:
                telement[key] = element[key]
        result.add(InmutableDict(telement))
    return result


if __name__ == "__main__":
    import argparse
    from pydsl.Config import VERSION, GLOBALCONFIG
    TUSAGE = "usage: %(prog)s [options] query"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("query", nargs="?", default="/.*/", metavar="query", help="Query to search")
    PARSER.add_argument('--version', action='version', version = VERSION)
    PARSER.add_argument('--filter', dest='myfilter',nargs='?', default=None, help="comma separated field list")
    PARSER.add_argument('-o', dest='outputformat',nargs='?', choices=["str","json"], default="str", help="output formats")
    ARGS = PARSER.parse_args()
    import sys
    from pydsl.Memory.Search.Searcher import MemorySearcher
    from pydsl.Memory.Search.Indexer import Indexer
    if ARGS.query:
        searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
        myfilter = None
        if ARGS.myfilter:
            myfilter = ARGS.myfilter.split(',')
        if ARGS.outputformat == "str":
            print(search_pp(searcher.search(ARGS.query), myfilter))
        elif ARGS.outputformat == "json":
            import json
            print(json.dumps(list(filterset(searcher.search(ARGS.query), myfilter))))
        sys.exit(0)
    else:
        print(TUSAGE)
        sys.exit(0)
    sys.exit(0)
