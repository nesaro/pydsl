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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Néstor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Exceptions import BadFileFormat
from pydsl.Interaction.Shell import parse_shell_dict, open_files_dict 

#CURRENTGRAMMAR = ""

def checkfun(inputdic, auxboarddic, inputgt, outputgt):
    output = auxboarddic["checker"]({"string":inputdic["input"], "grammar":CURRENTGRAMMAR})
    if not output:
        return output
    return {"output":str(output["output"])}

def extract(expression = None, outputfiledic = None, pipemode = None, inputfiledic = None, **kwargs):
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    from pydsl.Function.Python import HostPythonTransformer
    maingt = HostPythonTransformer({"input":"cstring"},{"output":"TrueFalse"},{"checker":"GrammarChecker"}, checkfun) 
    if expression and outputfiledic: #input type: expression #output: file
        myexpression = {"input":expression}
        outputdic = parse_shell_dict(outputfiledic)
        resultdic = maingt(myexpression, outputdic)
        from .Shell import save_result_to_output
        save_result_to_output(resultdic, outputdic)
        return resultdic
    elif expression and not outputfiledic:
        result = _slice(maingt,expression)
        print(result)
        return result #FIXME: Solo en el modo expresion se espera de resultado para test 
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
    else:
        raise Exception
    return True

def _slice(maingt, inputdata):
    totallen = len(inputdata)
    from pydsl.Memory.Loader import load_grammar_tool
    currenttype = load_grammar_tool(CURRENTGRAMMAR)
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
            check = maingt({"input":inputdata[i:j]})["output"]
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
        result = extract(**vars(ARGS))
    except EOFError:
        sys.exit(0)
    if not result:
        sys.exit(-1)
    sys.exit(0)
