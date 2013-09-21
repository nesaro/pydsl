#!/usr/bin/env python

""" Memory management binary """

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl import VERSION
from pydsl.Config import GLOBALCONFIG


def search_pp(inputset: set, filterlist=None):  # -> str:
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


def filterset(inputset: set, filterlist=None):  # -> set:
    if filterlist is None:
        return inputset  # Don't filter at all
    from pypository.utils import ImmutableDict
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
            resultdic = {"instance": instance}
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
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-d", "--debuglevel", action="store",
                        type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument('-o', dest='outputformat', nargs='?', choices=[
                        "str", "json", "raw"], default="str", help="output format")
    PARSER.add_argument('--version', action='version', version=VERSION)
    PARSER.add_argument('--filter', dest='myfilter',
                        nargs='?', default=None, help="comma separated field list")
    PARSER.add_argument(
        "verb", choices=("info", "search", "list", "grammars", "alphabets", "functions"), help="action to execute")
    PARSER.add_argument(
        "identifier", metavar="identifier", nargs='?', help="command")
    from pydsl.Config import load_default_memory
    load_default_memory()
    ARGS = PARSER.parse_args()
    import sys
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    logging.basicConfig(level=DEBUGLEVEL)
    if ARGS.verb == "info":
        if not ARGS.identifier:
            print("Please specify an identifier")
            sys.exit(-1)
        info(ARGS.identifier, ARGS. outputformat)
    elif ARGS.verb in ("search", "list", "grammars", "alphabets", "functions"):
        from pydsl.Memory.Loader import search
        myfilter = None
        if ARGS.myfilter:
            myfilter = ARGS.myfilter.split(',')
        if ARGS.verb == "grammars":
            identifier = "iclass=SymbolGrammar||iclass=PythonGrammar||iclass=PLY"
        elif ARGS.verb == "alphabets":
            identifier = "iclass=Encoding||iclass=AlphabetListDefinition"
        elif ARGS.verb == "functions":
            identifier = "iclass=PythonTransformer"
        else:
            identifier = ARGS.identifier
        if ARGS.outputformat == "str":
            print(search_pp(search(identifier), myfilter))
        elif ARGS.outputformat == "json":
            import json
            print(json.dumps(list(filterset(search(identifier), myfilter))))
        else:
            print("Unsupported output for action")
            sys.exit(-1)
    else:
        print("Unknown verb")
        sys.exit(-1)
