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
Calls a transformer
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Exceptions import BadFileFormat

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] transformername"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-is", "--inputstreams", action="store", dest="inputstreamdic", help="input streams filename dict")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfiledic", help="input filename dict")
    PARSER.add_argument("-o", "--outputfile", action="store", dest="outputfiledic", help="output filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("-p", "--pipe", action="store_true", dest="pipemode", help="Pipe interaction mode")
    PARSER.add_argument("transformer", help="Transformer name")
    ARGS = PARSER.parse_args()
    import sys
    if ((ARGS.outputfiledic and not ARGS.expression) and (ARGS.outputfiledic and not ARGS.inputfiledic)):
        PARSER.error("options -o and -e or -i must be together")
    DEBUGLEVEL = logging.WARNING
    if ARGS.debuglevel:
        DEBUGLEVEL = ARGS.debuglevel
    logging.basicConfig(level = DEBUGLEVEL)
    from pydsl.Interaction.Translate import Translate
    MANAGER = Translate(ARGS)
    try: 
        MANAGER.readTR(ARGS.transformer)
    except BadFileFormat:
        print("Error reading input file")
        sys.exit(1)
    #except KeyError as le:
    #    print("Unable to load " + str(le))
    #    sys.exit(1)
    #else:
    #    print(TUSAGE)
    #    sys.exit(0)
    try:
        result = MANAGER.execute()
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
