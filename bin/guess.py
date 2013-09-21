#!/usr/bin/env python

# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""
guess to which type can belong an input. It works like the unix file command
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging


if __name__ == "__main__":
    import argparse
    USAGE = "usage: %(prog)s [options]"
    PARSER = argparse.ArgumentParser(usage=USAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store",
                        type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store",
                        dest="inputfile", help="input filename dict")
    PARSER.add_argument(
        "-e", "--expression", action="store", dest="expression", help="input expression")
    ARGS = PARSER.parse_args()
    import sys
    if not ARGS.inputfile and not ARGS.expression:
        PARSER.error("options -i, -u or -e are required")
    if ARGS.inputfile and ARGS.expression:
        PARSER.error("options -i and -e can't be together")
    from pydsl.Config import load_default_memory
    load_default_memory()
    DEBUGLEVEL = 39
    if ARGS.debuglevel:
        DEBUGLEVEL = ARGS.debuglevel
    logging.basicConfig(level=DEBUGLEVEL)
    from pydsl.Guess import Guesser
    guess = Guesser()
    if ARGS.inputfile:
        with open(ARGS.inputfile, "rb") as f:
            inputstr = f.read()
        result = guess(inputstr)
    elif ARGS.expression:
        result = guess(ARGS.expression)
    else:
        print(USAGE)
        sys.exit(0)
    print(result)
    sys.exit(0)
