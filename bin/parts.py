#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Show input's components according to a language
"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Interaction.Program import UnixProgram


def print_errors(postnode):
    result = ""
    if not postnode.valid:
        result += "Error at production: " + str(postnode.production) + "(" + str(postnode.leftpos) + "," + str(postnode.rightpos) + ")"
        for child in postnode.childlist:
            result += print_errors(child) + "\n"
    return result

class Parts(UnixProgram):
    """Shows the differents components of data according to a Grammar"""
    def __init__(self, optionsdict):
        from pydsl.Memory.Loader import load_grammar
        #import pydsl.GlobalConfig
        #pydsl.GlobalConfig.GLOBALCONFIG.strictgrammar = True
        UnixProgram.__init__(self, optionsdict)
        self.__sgrammar = load_grammar(optionsdict.sgrammar) 
    
    def execute(self):
        import sys
        result = None
        if not self._opt["part"]:
            print("Grouplist: " + "\n".join(self.__sgrammar.groups()))
            return True
        myinput = None
        if self._opt["expression"]: 
            myinput = self._opt["expression"]
        elif self._opt["inputfile"]:
            with open(self._opt["inputfile"], "rb") as f:
                myinput = f.read()
        else:
            raise Exception #No input method
        result = self.__sgrammar.get_groups(myinput, self._opt["part"])
        dataresults = []
        for left,right in result:
            dataresults.append(myinput[left:right])

        if self._opt["outputformat"] == "str":
            for x in range(len(result)):
                print("(" + str(result[x][0]) + "," + str(result[x][1]) + ") " +  str(dataresults[x]))
            return True

        elif self._opt["outputformat"] == "json":
            mylist = []
            for x in range(len(result)):
                mylist.append((result[x][0],result[x][1],dataresults[x]))
            import json
            print(json.dumps(mylist))
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
    PARSER.add_argument("part", nargs='?', metavar="part" , help="Part name")
    ARGS = PARSER.parse_args()
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    
    logging.basicConfig(level = DEBUGLEVEL)
    manager = Parts(ARGS)
    import sys
    try:
        result = manager.execute()
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
