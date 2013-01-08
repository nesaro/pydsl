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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Interaction.Shell import parse_shell_dict, open_files_dict, StreamFileToTransformerInteraction, save_result_to_output
from pydsl.Exceptions import BadFileFormat
from pydsl.Memory.Loader import load
LOG = logging.getLogger(__name__)

#FIXME Some parts of this class should call separated functions. This code is a mess
def translate(transformer = None, expression = None, inputfiledic = None, outputfiledic = None, inputstreamdic = None, pipemode = None, **kwargs):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    #Generating and connecting output
    #listen to user, open read file, or other
    #configure output, write file, or other
    #print self._opt
    mainfunc = load(transformer) 
    if expression and  outputfiledic: #input type: expression #output: file
        inputdic = parse_shell_dict(expression)
        if not isinstance(inputdic, dict):
            raise TypeError
        outputdic = parse_shell_dict(outputfiledic)
        resultdic = mainfunc(inputdic)
        save_result_to_output(resultdic, outputdic)
        return resultdic
    elif expression and not outputfiledic:
        myexpression = parse_shell_dict(expression)
        result = mainfunc(myexpression)
        if result:
            for key in result.keys():
                result[key] = str(result[key])
        print(result)
        return result #FIXME: this is the only condition that returns a result. Because of tests
    elif inputstreamdic and outputfiledic:
        interactor = StreamFileToTransformerInteraction(mainfunc, parse_shell_dict(inputstreamdic), parse_shell_dict(outputfiledic))
        interactor.start()
    elif inputfiledic and outputfiledic:
        inputdic = parse_shell_dict(inputfiledic)
        outputdic = parse_shell_dict(outputfiledic)
        stringdic = open_files_dict(inputdic)
        resultdic = mainfunc(stringdic)
        save_result_to_output(resultdic, outputdic)
        return resultdic
    elif pipemode:
        assert(len(mainfunc.inputchanneldic) == 1)
        assert(len(mainfunc.outputchanneldic) == 1)
        inputname = list(mainfunc.inputchanneldic.keys())[0]
        outputname = list(mainfunc.outputchanneldic.keys())[0]
        interactor = StreamFileToTransformerInteraction(mainfunc, {inputname:"stdin"} , {outputname:"stdout"})
        interactor.start()
    elif not inputfiledic and not outputfiledic and not expression:
        from pydsl.Interaction.Shell import CommandLineToTransformerInteraction
        interactor = CommandLineToTransformerInteraction(mainfunc)
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
    #except KeyError as le:
    #    print("Unable to load " + str(le))
    #    sys.exit(1)
    #else:
    #    print(TUSAGE)
    #    sys.exit(0)
    try:
        result = translate(**vars(ARGS))
    except EOFError:
        sys.exit(0)
    except BadFileFormat:
        print("Error reading input file")
        sys.exit(1)
    if not result:
        sys.exit(-1)
    sys.exit(0)
