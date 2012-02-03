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

"""External program FileType"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from .Function import FileFunction
from ColonyDSL.TypeCheck import typecheck
LOG = logging.getLogger("Function.File")

class ExternalProgramFileFunction(FileFunction):
    """FileFunction which calls an external program"""
    @typecheck
    def __init__(self, identifier, inputformat, outputformat, programcall:list):
        #programlist ["program","-s","#{inputchannelname1}","-e","#{inputchannelname2}"]
        FileFunction.__init__(self, identifier)
        self.__programlist = programcall
        self.inputformat = inputformat #TODO
        self.outputformat = outputformat #TODO

    def call(self, wdic):
        #fileinput, fileoutput
        #TODO: check if follows inputformat. 
        from ColonyDSL.Interaction.Protocol import FileProtocol, URI
        fp = FileProtocol()
        for dickey in wdic.keys():
            val = wdic[dickey]
            if isinstance(val, URI):
                wdic[dickey] = val.split()[1]
            elif fp.check(val):
                wdic[dickey] = URI(val).split()[1]
            else:
                wdic[dickey] = val #file object assumed
        result = self.__processWords(wdic["inputfile"],wdic["outputfile"])
        if not result:
            return Error(self.name, "transformerError")
        return result

    def __processWords(self, inputfile, outputfile):
        if not inputfile:            
            raise Exception
        calllist  = list(self.__programlist)
        for index in range(len(calllist)):
            element = calllist[index]
            if element.find("#{inputfile}") != -1:
                calllist[index] = element.replace("#{inputfile}", inputfile.string)
            if element.find("#{outputfile}") != -1:
                calllist[index] = element.replace("#{outputfile}", outputfile.string)
        LOG.debug("Calllist: "+ str(calllist))
        import subprocess
        proc = subprocess.Popen(calllist, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        proc.stdout.close()
        if len(lines) > 1:
            LOG.warning("program execution returned > 1 lines")
        lines = map(lambda x: x.decode('utf-8'), lines)
        lines = "\n".join(lines)
        return {"output":lines}

    def _onReceiveEvent(self, source, msg):
        pass

    @property
    def summary(self):
        return {"iclass":"ExternalProgramFileFunction", "input":self.inputformat, "output":self.outputformat, "identifier":self.identifier}
