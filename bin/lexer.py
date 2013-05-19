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
check if input data belongs to a Type
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Memory.Loader import load_lexer

def bool_dict_values(dic):
    for key in dic:
        if str(dic[key]) == "False":
            dic[key] = False
        else:
            dic[key] = bool(dic[key])
    return dic

def lexer(alphabet, expression = None, inputfile = None):
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    lexer = load_lexer(alphabet)
    if expression:
        result = [str(x) for x in lexer(expression)]
        print(result)
    elif inputfile:
        with open(inputfile, 'rb') as f:
            expression = f.read()
        result = [str(x) for x in lexer(expression)]
        print(result)
    else:
        raise Exception
    return True

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] alphabet"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfile", help="input filename")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("alphabet", metavar="alphabet", help="Alphabet name")
    ARGS = PARSER.parse_args()
    if not ARGS.expression and not ARGS.inputfile:
        PARSER.error("expression or inputfile required")
    ARGS = vars(ARGS)
    import sys
    DEBUGLEVEL = ARGS.pop("debuglevel") or logging.WARNING
    logging.basicConfig(level = DEBUGLEVEL)
    from pydsl.Config import load_default_memory
    load_default_memory()
    try:
        result = lexer(**ARGS)
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
