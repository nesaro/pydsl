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
validates input against the Grammar
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from ColonyDSL.Interaction.Program import UnixProgram


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

class Validate(UnixProgram):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    def __init__(self, optionsdict):
        from ColonyDSL.Memory.External.Loader import load_grammar
        UnixProgram.__init__(self, optionsdict)
        self.__sgrammar = load_grammar(optionsdict.sgrammar) 
    
    def execute(self):
        resulttrees = None
        if self._opt["expression"]: 
            resulttrees = self.__sgrammar.get_trees(self._opt["expression"], True)
        elif self._opt["inputfile"]:
            with open(self._opt["inputfile"], "rb") as f:
                resulttrees = self.__sgrammar.get_trees(f.read(), True)
        else:
            raise Exception #No input method
        jsonlist = []
        for index, tree in enumerate(resulttrees):
            if self._opt["outputformat"] == "str":
                print("Tree: " + str(index) + "\n")
            from ColonyDSL.Type.Grammar.Tree import parser_to_post_node
            posttree = parser_to_post_node(tree)
            if self._opt["outputformat"] == "str":
                if posttree.valid:
                    print("Result OK")
                else:
                    print("Errors:")
                    print(print_errors(posttree))
            elif self._opt["outputformat"] == "json":
                jsonlist.append(errors_to_list(posttree))
        if self._opt["outputformat"] == "json":
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
    ARGS = PARSER.parse_args()
    import sys
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    
    logging.basicConfig(level = DEBUGLEVEL)
    manager = Validate(ARGS)
    try:
        result = manager.execute()
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
