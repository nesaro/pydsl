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
extracts input slices that are a Type 
"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Exceptions import BadFileFormat
from pydsl.Interaction.Shell import parse_shell_dict, open_files_dict 
from pydsl.Interaction.Program import UnixProgram

CURRENTGRAMMAR = ""

def checkfun(inputdic, auxboarddic, inputgt, outputgt, evfunctions):
    output = auxboarddic["checker"]({"string":inputdic["input"], "grammar":CURRENTGRAMMAR})
    if not output:
        return output
    return {"output":str(output["output"])}

class Extract(UnixProgram):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    def __init__(self, optionsdict):
        from pydsl.Function.Python import HostPythonTransformer
        #import pydsl.GlobalConfig
        #pydsl.GlobalConfig.GLOBALCONFIG.strictgrammar = True
        self.__maingt = HostPythonTransformer({"input":"cstring"},{"output":"TrueFalse"},{"checker":"GrammarChecker"}, checkfun) 
        UnixProgram.__init__(self, optionsdict)
    
    def execute(self):
        #Generating and connecting output
        #listen to user, open read file, or other
        #configure output, write file, or other
        #print self._opt
        if self._opt["expression"] and self._opt["outputfiledic"]: #input type: expression #output: file
            myexpression = {"input":self._opt["expression"]}
            outputdic = parse_shell_dict(self._opt["outputfiledic"])
            resultdic = self.__maingt(myexpression, outputdic)
            from .Shell import save_result_to_output
            save_result_to_output(resultdic, outputdic)
            return resultdic
        elif self._opt["expression"] and not self._opt["outputfiledic"]:
            result = self.__slice(self._opt["expression"])
            print(result)
            return result #FIXME: Solo en el modo expresion se espera de resultado para test 
        elif self._opt["inputfiledic"]:
            inputdic = parse_shell_dict(self._opt["inputfiledic"])
            outputdic = {"output":"stdout"}
            if self._opt["outputfiledic"]:
                outputdic = parse_shell_dict(self._opt["outputfiledic"])
            stringdic = open_files_dict(inputdic)
            resultdic = self.__maingt(stringdic)
            resultdic = bool_dict_values(resultdic)
            from pydsl.Interaction.Shell import save_result_to_output
            save_result_to_output(resultdic, outputdic)
        elif self._opt["pipemode"]:
            from pydsl.Interaction.Shell import StreamFileToTransformerInteraction
            assert(len(self.__maingt.inputchanneldic) == 1)
            assert(len(self.__maingt.outputchanneldic) == 1)
            inputname = list(self.__maingt.inputchanneldic.keys())[0]
            outputname = list(self.__maingt.outputchanneldic.keys())[0]
            interactor = StreamFileToTransformerInteraction(self.__maingt, {inputname:"stdin"} , {outputname:"stdout"})
            interactor.start()
        elif not self._opt["inputfiledic"] and not self._opt["outputfiledic"] and not self._opt["expression"]:
            from pydsl.Interaction.Shell import CommandLineToTransformerInteraction
            interactor = CommandLineToTransformerInteraction(self.__maingt)
            interactor.start()
        else:
            raise Exception
        return True

    def readT(self, newtype):
        global CURRENTGRAMMAR
        CURRENTGRAMMAR = newtype

    def __slice(self, inputdata):
        totallen = len(inputdata)
        from pydsl.Memory.Storage.Loader import load_grammartools
        currenttype = load_grammartools(CURRENTGRAMMAR)
        try:
            maxl = currenttype.maxsize
        except NotImplementedError:
            maxl = totallen
        try:
            minl = currenttype.minsize
        except NotImplementedError:
            minl = 1
        maxwsize = maxl - minl + 1
        result = []
        for i in range(totallen):
            for j in range(i+minl, min(i+maxwsize+1, totallen+1)):
                check = self.__maingt({"input":inputdata[i:j]})["output"]
                if check == "True":
                    result.append((i,j, inputdata[i:j]))
        return result

                #TODO check alphabet

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] type"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfiledic", help="input filename dict")
    PARSER.add_argument("-o", "--outputfile", action="store", dest="outputfiledic", help="output filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("tname", metavar="tname", help="Type name")
    ARGS = PARSER.parse_args()
    import sys
    if ((ARGS.outputfiledic and not ARGS.expression) and (ARGS.outputfiledic and not ARGS.inputfiledic)):
        PARSER.error("options -o require -e or -i")
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    
    logging.basicConfig(level = DEBUGLEVEL)
    program = Extract(ARGS)
    try: 
        program.readT(ARGS.tname)
    except BadFileFormat:
        print("Error reading input file")
        sys.exit(1)
    except KeyError as le:
        print("Unable to load " + str(le))
        sys.exit(1)
    try:
        result = program.execute()
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
