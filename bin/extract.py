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
extracts input slices that are a Type 
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Memory.Loader import load
from pydsl.Extract import extract

def extractaux(grammar, expression = None, input_file = None):
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other

    grammar = load(grammar)
    if expression:
        result = extract(grammar,expression)
        print(result)
        return result
    elif input_file:
        with open(input_file) as f:
            content = f.read()
        result = extract(grammar,content)
        print(result)
        return result
    raise Exception("No input file nor expression")

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] type"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="input_file", help="input filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("grammar", metavar="grammar", help="Grammar name")
    ARGS = vars(PARSER.parse_args())
    import sys
    DEBUGLEVEL = ARGS.pop('debuglevel') or logging.WARNING
    from pydsl.Config import load_default_memory
    load_default_memory()
    logging.basicConfig(level = DEBUGLEVEL)
    try:
        result = extractaux(**ARGS)
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
