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
General diff implementation
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging

def diff2(elem1, elem2):
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    #print self._opt
    from Diff import diff
    result = diff(elem1, elem2)
    #result = bool_dict_values(str(result["output"]))
    print(result)
    return result

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] type"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-g", "--gramarlist", action="store", dest="grammarlist", help="Grammar list")
    PARSER.add_argument("-o", "--alphabetlist", action="store", dest="alphabetlist", help="Alphabet list")
    PARSER.add_argument("elem1", metavar="elem1", help="First Element")
    PARSER.add_argument("elem2", metavar="elem2", help="Second Element")
    ARGS = PARSER.parse_args()
    import sys
    if ((ARGS.outputfiledic and not ARGS.expression) and (ARGS.outputfiledic and not ARGS.inputfiledic)):
        PARSER.error("options -o require -e or -i")
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    
    logging.basicConfig(level = DEBUGLEVEL)
    try:
        result = diff2(**vars(ARGS))
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
