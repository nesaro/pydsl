#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Show input's components according to a language
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging


def print_errors(postnode):
    result = ""
    if not postnode.valid:
        result += "Error at production: " + str(postnode.production) + "(" + str(postnode.leftpos) + "," + str(postnode.rightpos) + ")"
        for child in postnode.childlist:
            result += print_errors(child) + "\n"
    return result

def parts(grammar, part, outputformat = None, expression = None, inputfile = None):
    from pydsl.Memory.Loader import load
    sgrammar = load(grammar) 
    if not part:
        print("Grouplist: " + "\n".join(sgrammar.groups()))
        return True
    myinput = None
    if expression: 
        myinput = expression
    elif inputfile:
        with open(inputfile, "rb") as f:
            myinput = f.read()
    else:
        raise Exception("No input method")
    result = sgrammar.get_groups(myinput, part)
    dataresults = []
    for left,right in result:
        dataresults.append(myinput[left:right])

    if outputformat == "str":
        for x in range(len(result)):
            print("(" + str(result[x][0]) + "," + str(result[x][1]) + ") " +  str(dataresults[x]))
        return True

    elif outputformat == "json":
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
    import sys
    try:
        result = parts(vars(**ARGS))
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
