#!/usr/bin/python
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
Runs a program developed with ColonyDSL language
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2011, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

from ColonyDSL.Interaction.Shell import parse_shell_dict, open_files_dict
from ColonyDSL.Interaction.Program import UnixProgram
import logging
LOG = logging.getLogger("Translate")

#FIXME Some parts of this class should call separated functions. This code is a mess
class Translate(UnixProgram):
    """Read input file contents, creates grammar and transform objects, create connections, 
    and afterwards reads required input/launch main loop"""
    def __init__(self, optionsdict):
        self.__mainfunc = None
        self.__mode = None
        UnixProgram.__init__(self, optionsdict)
        
    def readTR(self, gtname):
        self.__mode = "Transformer"
        from ColonyDSL.Memory.External.Loader import load_transformer
        self.__mainfunc = load_transformer(gtname) 
    
    def readP(self, pname):
        self.__mode = "Procedure"
        from ColonyDSL.Memory.External.Loader import load_procedure
        self.__mainfunc = load_procedure(pname)

    def execute(self):
        #Generating and connecting output
        #listen to user, open read file, or other
        #configure output, write file, or other
        #print self._opt
        if self.__mode == "Transformer":
            LOG.debug(self._opt)
            if self._opt["expression"] and  self._opt["outputfiledic"]: #input type: expression #output: file
                inputdic = parse_shell_dict(self._opt["expression"])
                if not isinstance(inputdic, dict):
                    raise TypeError
                outputdic = parse_shell_dict(self._opt["outputfiledic"])
                resultdic = self.__mainfunc.call(inputdic)
                from .Shell import file_output
                file_output(resultdic, outputdic)
                return resultdic
            elif self._opt["expression"] and not self._opt["outputfiledic"]:
                myexpression = parse_shell_dict(self._opt["expression"])
                result = self.__mainfunc.call(myexpression)
                from ColonyDSL.Function.Function import Error
                if result:
                    for key in result.keys():
                        result[key] = str(result[key])
                print(result)
                return result #FIXME: this is the only condition that returns a result. Because of tests
            elif self._opt["inputstreamdic"] and self._opt["outputfiledic"]:
                from ColonyDSL.Interaction.Shell import StreamFileToTransformerInteraction
                interactor = StreamFileToTransformerInteraction(self.__mainfunc, parse_shell_dict(self._opt["inputstreamdic"]), parse_shell_dict(self._opt["outputfiledic"]))
                interactor.start()
            elif self._opt["inputfiledic"] and self._opt["outputfiledic"]:
                inputdic = parse_shell_dict(self._opt["inputfiledic"])
                outputdic = parse_shell_dict(self._opt["outputfiledic"])
                stringdic = open_files_dict(inputdic)
                resultdic = self.__mainfunc.call(stringdic)
                from .Shell import file_output
                file_output(resultdic, outputdic)
                close_input_dic(stringdic)
                return resultdic
            elif self._opt["pipemode"]:
                from ColonyDSL.Interaction.Shell import StreamFileToTransformerInteraction
                assert(len(self.__mainfunc.inputchanneldic) == 1)
                assert(len(self.__mainfunc.outputchanneldic) == 1)
                inputname = list(self.__mainfunc.inputchanneldic.keys())[0]
                outputname = list(self.__mainfunc.outputchanneldic.keys())[0]
                interactor = StreamFileToTransformerInteraction(self.__mainfunc, {inputname:"stdin"} , {outputname:"stdout"})
                interactor.start()
            elif not self._opt["inputfiledic"] and not self._opt["outputfiledic"] \
                    and not self._opt["expression"]:
                from ColonyDSL.Interaction.Shell import CommandLineToTransformerInteraction
                interactor = CommandLineToTransformerInteraction(self.__mainfunc)
                interactor.start()
            else:
                raise Exception
        elif self.__mode == "Procedure":
            if self._opt["pipemode"]:
                assert(len(self.__mainfunc.outputchanneldic) == 1)
                result = self.__mainfunc.call()
                print(result[list(self.__mainfunc.outputchanneldic.keys())[0]])
            else:
                result = self.__mainfunc.call()
                print(result)
                return result 
        return True
