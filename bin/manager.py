#!/usr/bin/python3

"""Gestiona las memorias
uso: manager.py [opciones] comando MemURI Identifier
   comandos: n new element
             r read element
             s save element
             a append to element
             d delete element
             l list elements

   opciones: -e input expression
             -i input URI
             -o output URI or stdout

   MemURI: La URI de la memoria
   Identifier: El identificador del elemento en cuestión. Solo si no esta incluido en la URI
   """

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging

def load_memory(identifier):
    """Intenta adivinar el tipo de memoria de la URI pasada y la carga"""
    import os
    if os.path.isdir(identifier):
        from pydsl.Memory.Directory.DirStorage import StrDirStorage
        return StrDirStorage(identifier)


if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] command URI [Identifier]"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--input", action="store", dest="inputuri", help="input filename dict")
    PARSER.add_argument("-o", "--output", action="store", dest="outputuri", help="output filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("command", metavar="command" , help="command")
    PARSER.add_argument("uri", metavar="uri" , help="command")
    PARSER.add_argument("identifier", metavar="identifier" , nargs='?', help="command")
    ARGS = PARSER.parse_args()
    import sys
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    logging.basicConfig(level = DEBUGLEVEL)
    if ARGS.command == "n":
        pass
    elif ARGS.command == "r":
        pass
    elif ARGS.command == "s":
        pass
    elif ARGS.command == "a":
        pass
    elif ARGS.command == "d":
        pass
    elif ARGS.command == "l":
        mem = load_memory(ARGS.uri)
        for element in mem:
            print(element)
    else:
        print("Unknown command")
        print(TUSAGE)
        sys.exit(-1)
