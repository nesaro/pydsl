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


"""
Calls a transformer
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Exceptions import BadFileFormat
from pydsl.Memory.Loader import load_translator
LOG = logging.getLogger(__name__)

def escapedsplitby(inputstring, separator):
    """Splits inputstring with separator and using "\" as a escape character"""
    #TODO check alternatives (shlex and csv)
    result = []
    while inputstring[0] == separator:
        inputstring = inputstring[1:]
    lastindex = 0
    index = 0
    while index < len(inputstring):
        if inputstring[index] == "\\" and inputstring[index + 1] == separator:
            inputstring = inputstring[:index] + inputstring[index + 1:]
            index += 1
            continue
        elif inputstring[index] == "\\" and inputstring[index + 1] == "\\":
            inputstring = inputstring[:index] + inputstring[index + 1:]
            index += 1
            continue
        elif inputstring[index] == separator:
            result.append(inputstring[lastindex:index])
            while inputstring[index] == separator:
                index += 1
            lastindex = index
            continue
        else:
            index += 1
            continue
    result.append(inputstring[lastindex:])
    return result

def parse_shell_dict(inputstring): # -> dict:
    """Parses commandline input dicts. Example: a:b,c:d,e:f."""
    result = {}
    arglist = escapedsplitby(inputstring, ",")
    for arg in arglist:
        pair = escapedsplitby(arg, ":")
        result[pair[0]] = pair[1]
    return result


def translate(transformer = None, expression = None, inputfiledic = None, outputfiledic = None):
    """Read input file contents, creates grammar and transform objects, create connections,
    and afterwards reads required input/launch main loop"""
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    #print self._opt
    mainfunc = load(transformer)
    if expression and not outputfiledic:
        myexpression = parse_shell_dict(expression)
        result = mainfunc(**myexpression)
        if result:
            for key in result.keys():
                result[key] = str(result[key])
        print(result)
        return result #FIXME: this is the only condition that returns a result. Because of tests
    raise Exception("Invalid arguments")

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] transformername"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfiledic", help="input filename dict")
    PARSER.add_argument("-o", "--outputfile", action="store", dest="outputfiledic", help="output filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("transformer", help="Transformer name")
    ARGS = PARSER.parse_args()
    import sys
    if (ARGS.outputfiledic and not ARGS.expression) and (ARGS.outputfiledic and not ARGS.inputfiledic):
        PARSER.error("options -o and -e or -i must be together")
    ARGS = vars(ARGS)
    DEBUGLEVEL = ARGS.pop('debuglevel',logging.WARNING)
    logging.basicConfig(level = DEBUGLEVEL)
    from pydsl.Config import load_default_memory, GLOBALCONFIG
    load_default_memory()
    try:
        result = translate(**ARGS)
    except EOFError:
        sys.exit(0)
    except BadFileFormat:
        print("Error reading input file")
        sys.exit(1)
    if not result:
        sys.exit(-1)
    sys.exit(0)
