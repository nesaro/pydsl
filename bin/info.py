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
Shows information about an element retrieved from Memory
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] identifier"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument('--lang', dest='lang',nargs='?', choices=["es","en"], default="en", help="Languages")
    PARSER.add_argument('-o', dest='outputformat',nargs='?', choices=["str","json","raw"], default="str", help="output formats")
    PARSER.add_argument("identifier", metavar="identifier" , help="Element identifier")
    ARGS = PARSER.parse_args()
    import sys
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    logging.basicConfig(level = DEBUGLEVEL)
    from pydsl.Config import GLOBALCONFIG
    memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if ARGS.identifier in memory:
            instance = memory.load(ARGS.identifier)
            break
    else:
        print("Not found")
        sys.exit(-1)
    if instance:
        if hasattr(instance, "summary"):
            resultdic = instance.summary
        else:
            resultdic = {"instance":instance}
        if ARGS.outputformat == "str":
            for key in resultdic:
                print(key + ": " + str(resultdic[key]))
        elif ARGS.outputformat == "json":
            import json
            print(json.dumps(resultdic))
        else:
            print("Raw format not supported")
            sys.exit(-1)
    else:
        if ARGS.outputformat == "str":
            print(str(instance))
        elif ARGS.outputformat == "raw":
            import sys
            sys.stdout.write(str(instance))
        else:
            print("JSON format not supported")
            sys.exit(-1)
    sys.exit(0)
