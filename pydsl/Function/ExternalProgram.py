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

"""External program Transformer"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging
import subprocess
from pydsl.Exceptions import ProcessingError
from .Channel import HostChannel
LOG = logging.getLogger("Function.ExternalProgram")

class ExternalProgramFunction(HostChannel):
    """returns stdout from program call"""
    def __init__(self, inputdic, outputdic, programcall:list):
        #programlist ["program","-s","#{inputchannelname1}","-e","#{inputchannelname2}"]
        if len(outputdic) != 1:
            raise ValueError
        HostChannel.__init__(self, inputdic, outputdic)
        self.__programlist = programcall

    def __call__(self, wdic):
        for inputkey in self.inputchanneldic.keys():
            if inputkey not in wdic:
                LOG.error("Key not found in inputdic")
                raise ProcessingError("Transformer", self)
        result = self.__processWords(wdic)
        if not result:
            raise ProcessingError("Transformer")
        return result

    def __processWords(self, inputdict):
        #inputdict = {channelname:data,}
        if not inputdict:            
            raise Exception
        calllist  = list(self.__programlist)
        for channel, data in inputdict.items():
            channelfound = False
            for index in range(len(calllist)):
                element = calllist[index]
                if element.find("#{"+channel+"}") != -1:
                    channelfound = True
                    calllist[index] = element.replace("#{"+channel+"}", str(data))
            if not channelfound:
                raise Exception("No channel found")
        proc = subprocess.Popen(calllist, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        proc.stdout.close()
        if len(lines) > 1:
            LOG.warning("program execution returned > 1 lines")
        lines = map(lambda x: x.decode('utf-8'), lines)
        lines = "\n".join(lines)
        for key in self.outputchanneldic.keys():
            return {key:lines} #FIXME: only one channel!?
        #returns dict {outputchannelname:informationBlock,}

    @property
    def summary(self):
        inputdic = [ x.identifier for x in self.inputchanneldic.values() ]
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"ExternalProgramFunction", "description":self.description, "input":inputdic, "output":outputdic }
