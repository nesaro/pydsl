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
check if input data belongs to a Type 
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Exceptions import BadFileFormat
from pydsl.Interaction.Shell import parse_shell_dict, open_files_dict 

def checkfun(inputdic, auxboarddic, inputgt, outputgt):
    output = auxboarddic["checker"]({"string":inputdic["input"], "grammar":CURRENTGRAMMAR})
    if not output:
        return output
    return {"output":str(output["output"])}

def bool_dict_values(dic):
    for key in dic:
        if str(dic[key]) == "False":
            dic[key] = False
        else:
            dic[key] = bool(dic[key])
    return dic

def checker(expression = None, outputfiledic = None, inputfiledic = None, pipemode = None, **kwargs ):
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    from pydsl.Function.Python import HostPythonTransformer
    maingt = HostPythonTransformer({"input":"cstring"},{"output":"TrueFalse"},{"checker":"GrammarChecker"}, checkfun) 
    if expression and outputfiledic: #input type: expression #output: file
        myexpression = {"input":expression}
        outputdic = parse_shell_dict(outputfiledic)
        resultdic = maingt(myexpression, outputdic)
        resultdic = bool_dict_values(resultdic)
        from pydsl.Interaction.Shell import save_result_to_output
        save_result_to_output(resultdic, outputdic)
        return resultdic
    elif expression and not outputfiledic:
        myexpression = {"input":expression}
        result = maingt(myexpression)["output"]
        #result = bool_dict_values(str(result["output"]))
        print(result)
        return result #FIXME: Only expression mode expects a returned result
    elif inputfiledic:
        inputdic = parse_shell_dict(inputfiledic)
        outputdic = {"output":"stdout"}
        if outputfiledic:
            outputdic = parse_shell_dict(outputfiledic)
        stringdic = open_files_dict(inputdic)
        resultdic = maingt(stringdic)
        resultdic = bool_dict_values(resultdic)
        from pydsl.Interaction.Shell import save_result_to_output
        save_result_to_output(resultdic, outputdic)
    elif pipemode:
        from pydsl.Interaction.Shell import StreamFileToTransformerInteraction
        assert(len(maingt.inputchanneldic) == 1)
        assert(len(maingt.outputchanneldic) == 1)
        inputname = list(maingt.inputchanneldic.keys())[0]
        outputname = list(maingt.outputchanneldic.keys())[0]
        interactor = StreamFileToTransformerInteraction(maingt, {inputname:"stdin"} , {outputname:"stdout"})
        interactor.start()
    elif not inputfiledic and not outputfiledic and not expression:
        from pydsl.Interaction.Shell import CommandLineToTransformerInteraction
        interactor = CommandLineToTransformerInteraction(maingt)
        interactor.start()
    else:
        raise Exception
    return True

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options] type"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    PARSER.add_argument("-i", "--inputfile", action="store", dest="inputfiledic", help="input filename dict")
    PARSER.add_argument("-o", "--outputfile", action="store", dest="outputfiledic", help="output filename dict")
    PARSER.add_argument("-e", "--expression", action="store", dest="expression", help="input expression")
    PARSER.add_argument("-p", "--pipe", action="store_true", dest="pipemode", help="Pipe interaction mode")
    PARSER.add_argument("tname", metavar="tname", help="Type name")
    ARGS = PARSER.parse_args()
    import sys
    if (ARGS.outputfiledic and not ARGS.expression) and (ARGS.outputfiledic and not ARGS.inputfiledic):
        PARSER.error("options -o require -e or -i")
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    
    logging.basicConfig(level = DEBUGLEVEL)
    try: 
        global CURRENTGRAMMAR
        CURRENTGRAMMAR = ARGS.tname
    except BadFileFormat:
        print("Error reading input file")
        sys.exit(1)
    except KeyError as le:
        print("Unable to load " + str(le))
        sys.exit(1)
    try:
        result = checker(**vars(ARGS))
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
