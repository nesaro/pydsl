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
Shows information about an element retrieved from Memory
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
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
    if ARGS.lang:
        from ColonyDSL.Config import GLOBALCONFIG
        GLOBALCONFIG.lang = ARGS.lang
    if ARGS.identifier:
        from ColonyDSL.Memory.External.Loader import load_information
        instance = load_information(ARGS.identifier)
        if "summary" in dir(instance):
            resultdic = instance.summary
            descmem = None
            from ColonyDSL.Memory.External.DictLibrary import StrDictLibrary 
            if ARGS.lang == "en":
                descmem = StrDictLibrary("/usr/share/ColonyDSL/lib_contrib/dict/description_en.dict")
            else:
                descmem = StrDictLibrary("/usr/share/ColonyDSL/lib_contrib/dict/description_es.dict")
            if ARGS.identifier in descmem:
                resultdic["description"] = str(descmem[ARGS.identifier])
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
    else:
        print(TUSAGE)
        sys.exit(0)
    sys.exit(0)
