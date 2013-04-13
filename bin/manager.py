#!/usr/bin/python3

""" Memory management
   verbs:    i info
             s search
             l list elements
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl import VERSION
from pydsl.Config import GLOBALCONFIG

def search_pp(inputset: set, filterlist = None) -> str:
    """Search pretty print"""
    result = ""
    for element in inputset:
        for key in element:
            if filterlist is None or key in filterlist:
                if isinstance(element[key], tuple):
                    result += key + "-> " + str(element[key]) + " "
                else:
                    result += key + ": " + str(element[key]) + " "
        result += '\n'
    return result

def filterset(inputset: set, filterlist = None) -> set:
    if filterlist is None:
        return inputset #Don't filter at all
    from pydsl.Abstract import ImmutableDict
    result = set()
    for element in inputset:
        telement = {}
        for key in element:
            if key in filterlist:
                telement[key] = element[key]
        result.add(ImmutableDict(telement))
    return result


def info(identifier, outputformat):
    memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if identifier in memory:
            instance = memory.load(identifier)
            break
    else:
        print("Not found")
        return False
    if instance:
        if hasattr(instance, "summary"):
            resultdic = instance.summary
        else:
            resultdic = {"instance":instance}
        if outputformat == "str":
            for key in resultdic:
                print(key + ": " + str(resultdic[key]))
        elif outputformat == "json":
            import json
            print(json.dumps(resultdic))
        else:
            print("Raw format not supported")
            return False
    else:
        if outputformat == "str":
            print(str(instance))
        elif outputformat == "raw":
            import sys
            sys.stdout.write(str(instance))
        else:
            print("JSON format not supported")
            return False
    return True

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] verb [identifier]"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument('-o', dest='outputformat',nargs='?', choices=["str","json","raw"], default="str", help="output format")
    PARSER.add_argument('--version', action='version', version = VERSION)
    PARSER.add_argument('--filter', dest='myfilter',nargs='?', default=None, help="comma separated field list")
    PARSER.add_argument("verb", metavar="verb" , help="verb")
    PARSER.add_argument("identifier", metavar="identifier" , nargs='?', help="command")
    from pydsl.Config import load_default_memory
    load_default_memory()
    ARGS = PARSER.parse_args()
    import sys
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    logging.basicConfig(level = DEBUGLEVEL)
    if ARGS.verb == "i":
        info(ARGS.identifier, ARGS. outputformat)
    elif ARGS.verb in ("s","l"):
        if ARGS.verb == "s":
            query = ARGS.identifier
        else:
            query = ""
        from pydsl.Memory.Search.Searcher import MemorySearcher
        from pydsl.Memory.Search.Indexer import Indexer
        searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
        myfilter = None
        if ARGS.myfilter:
            myfilter = ARGS.myfilter.split(',')
        if ARGS.outputformat == "str":
            print(search_pp(searcher.search(ARGS.identifier), myfilter))
        elif ARGS.outputformat == "json":
            import json
            print(json.dumps(list(filterset(searcher.search(ARGS.identifier), myfilter))))
    else:
        print("Unknown verb")
        print(TUSAGE)
        sys.exit(-1)
