#!/usr/bin/env python

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
Generic validator for BNF Grammars. 
Displays the part of the tree that doesn't conform the grammar definition
"""
from pydsl.Validate import validator_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging

def print_errors(postnode):
    result = ""
    if not postnode.valid:
        result += "Error at production: " + str(postnode.production) + "(" + str(postnode.leftpos) + "," + str(postnode.rightpos) + ")"
        for child in postnode.childlist:
            result += print_errors(child) + "\n"
    return result

def errors_to_list(postnode):
    result = []
    if not postnode.valid:
        result.append((postnode.leftpos, postnode.rightpos, str(postnode.production)))
        for child in postnode.childlist:
            result += errors_to_list(child)
    return result

def validate(sgrammar, expression = None, inputfile = None, outputformat = None):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    validator = validator_factory(sgrammar)
    if expression:
        resulttrees = validator(expression)
    elif inputfile:
        with open(inputfile, "rb") as f:
            resulttrees = validator(f.read())
    else:
        raise Exception("No input method")
    jsonlist = []
    for index, posttree in enumerate(resulttrees):
        if outputformat == "str":
            print("Tree: " + str(index) + "\n")
        if outputformat == "str":
            if posttree.valid:
                print("Result OK")
            else:
                print("Errors:")
                print(print_errors(posttree))
        elif outputformat == "json":
            jsonlist.append(errors_to_list(posttree))
    if outputformat == "json":
        import json
        print(json.dumps(jsonlist))
    return True

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] [filename]"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfile", help="input filename ")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument('-o', dest='outputformat',nargs='?', choices=["str","json"], default="str", help="output formats")
    PARSER.add_argument("sgrammar", metavar="sgrammar" , help="Grammar")
    ARGS = vars(PARSER.parse_args())
    import sys
    DEBUGLEVEL = ARGS.pop('debuglevel') or logging.WARNING
    from pydsl.Config import load_default_memory
    load_default_memory()
    logging.basicConfig(level = DEBUGLEVEL)
    try:
        result = validate(**ARGS)
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
