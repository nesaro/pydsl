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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Interaction.Shell import parse_shell_dict, open_files_dict
from pydsl.Interaction.Program import UnixProgram
from pydsl.Exceptions import BadFileFormat
LOG = logging.getLogger(__name__)

#FIXME Some parts of this class should call separated functions. This code is a mess
class Translate(UnixProgram):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    def __init__(self, optionsdict):
        self.__mainfunc = None
        UnixProgram.__init__(self, optionsdict)
        
    def readTR(self, gtname):
        from pydsl.Memory.Loader import load
        self.__mainfunc = load(gtname) 
    
    def execute(self):
        #Generating and connecting output
        #listen to user, open read file, or other
        #configure output, write file, or other
        #print self._opt
        LOG.debug(self._opt)
        if self._opt["expression"] and  self._opt["outputfiledic"]: #input type: expression #output: file
            inputdic = parse_shell_dict(self._opt["expression"])
            if not isinstance(inputdic, dict):
                raise TypeError
            outputdic = parse_shell_dict(self._opt["outputfiledic"])
            resultdic = self.__mainfunc(inputdic)
            from .Shell import file_output
            file_output(resultdic, outputdic)
            return resultdic
        elif self._opt["expression"] and not self._opt["outputfiledic"]:
            myexpression = parse_shell_dict(self._opt["expression"])
            result = self.__mainfunc(myexpression)
            from pydsl.Function.Function import Error
            if result:
                for key in result.keys():
                    result[key] = str(result[key])
            print(result)
            return result #FIXME: this is the only condition that returns a result. Because of tests
        elif self._opt["inputstreamdic"] and self._opt["outputfiledic"]:
            from pydsl.Interaction.Shell import StreamFileToTransformerInteraction
            interactor = StreamFileToTransformerInteraction(self.__mainfunc, parse_shell_dict(self._opt["inputstreamdic"]), parse_shell_dict(self._opt["outputfiledic"]))
            interactor.start()
        elif self._opt["inputfiledic"] and self._opt["outputfiledic"]:
            inputdic = parse_shell_dict(self._opt["inputfiledic"])
            outputdic = parse_shell_dict(self._opt["outputfiledic"])
            stringdic = open_files_dict(inputdic)
            resultdic = self.__mainfunc(stringdic)
            from .Shell import file_output
            file_output(resultdic, outputdic)
            close_input_dic(stringdic)
            return resultdic
        elif self._opt["pipemode"]:
            from pydsl.Interaction.Shell import StreamFileToTransformerInteraction
            assert(len(self.__mainfunc.inputchanneldic) == 1)
            assert(len(self.__mainfunc.outputchanneldic) == 1)
            inputname = list(self.__mainfunc.inputchanneldic.keys())[0]
            outputname = list(self.__mainfunc.outputchanneldic.keys())[0]
            interactor = StreamFileToTransformerInteraction(self.__mainfunc, {inputname:"stdin"} , {outputname:"stdout"})
            interactor.start()
        elif not self._opt["inputfiledic"] and not self._opt["outputfiledic"] \
                and not self._opt["expression"]:
            from pydsl.Interaction.Shell import CommandLineToTransformerInteraction
            interactor = CommandLineToTransformerInteraction(self.__mainfunc)
            interactor.start()
        else:
            raise Exception
        return True
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
