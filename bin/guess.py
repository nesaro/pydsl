#!/usr/bin/python3
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

"""
guess to which type can belong an input. It works like the unix file command
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"


import logging


if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] [filename]"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfile", help="input filename dict")
    PARSER.add_argument("-u", "--url", action="store", dest="inputurl", help="input filename url") #TODO inputfile and urlfile can follow protocol specs
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    ARGS = PARSER.parse_args()
    import sys
    if not ARGS.inputfile and not ARGS.expression and not ARGS.inputurl:
        PARSER.error("options -i, -u or -e are required")
    if ARGS.inputfile and ARGS.expression:
        PARSER.error("options -i and -e can't be together")
    DEBUGLEVEL = 39
    if ARGS.debuglevel:
        DEBUGLEVEL = ARGS.debuglevel
    logging.basicConfig(level = DEBUGLEVEL)    
    inputstr = ""
    if (ARGS.inputfile):
        with open(ARGS.inputfile, "rb") as f:
            inputstr = f.read() #FIXME: Protocol support
    elif (ARGS.expression):
        inputstr = ARGS.expression
    elif (ARGS.inputurl):
        import urllib.request
        f = urllib.request.urlopen(ARGS.inputurl);
        inputstr = f.read()
        f.close()
    else:
        print(TUSAGE)
        sys.exit(0)
    from ColonyDSL.Interaction.Guess import guess
    result = guess(inputstr)
    print(result)
    sys.exit(0)
