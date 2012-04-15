#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""External program Transformer"""

import logging
from .Function import Function
from .Channel import TypeChannelHost
LOG = logging.getLogger("Function.ExternalProgram")

class ExternalProgramFunction(Function, TypeChannelHost):
    """returns stdout from program call"""
    def __init__(self, inputdic, outputdic, programcall:list):
        #programlist ["program","-s","#{inputchannelname1}","-e","#{inputchannelname2}"]
        if len(outputdic) != 1:
            raise ValueError
        Function.__init__(self)
        TypeChannelHost.__init__(self, inputdic, outputdic)
        self.__programlist = programcall

    def __call__(self, wdic):
        for inputkey in self.inputchanneldic.keys():
            if inputkey not in wdic:
                LOG.error("Key not found in inputdic")
                from ColonyDSL.Function.Function import Error
                err = Error("Transformer")
                err.appendSource(self.ecuid)
                return err 
        result = self.__processWords(wdic)
        if not result:
            return Error(self.name, "transformerError")
        return result

    def __processWords(self, inputdict):
        #inputdict = {channelname:data,}
        if not inputdict:            
            raise Exception
        calllist  = list(self.__programlist)
        for channel, informationBlock in inputdict.items():
            channelfound = False
            for index in range(len(calllist)):
                element = calllist[index]
                if element.find("#{"+channel+"}") != -1:
                    channelfound = True
                calllist[index] = element.replace("#{"+channel+"}", str(informationBlock))
            if not channelfound:
                LOG.critical("No channel found")
                raise Exception
        LOG.debug("Calllist: "+ str(calllist))
        import subprocess
        proc = subprocess.Popen(calllist, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        proc.stdout.close()
        if len(lines) > 1:
            LOG.warning("program execution returned > 1 lines")
        lines = map(lambda x: x.decode('utf-8'), lines)
        lines = "\n".join(lines)
        for key in self.outputchanneldic.keys():
            return {key:lines} #FIXME: Solo un canal?
        #returns dict {outputchannelname:informationBlock,}

    @property
    def summary(self):
        inputdic = [ x.identifier for x in self.inputchanneldic.values() ]
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"ExternalProgramFunction", "description":self.description, "input":inputdic, "output":outputdic }
