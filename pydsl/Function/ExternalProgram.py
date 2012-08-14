#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""External program Transformer"""

import logging
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
            return {key:lines} #FIXME: only one channel!?
        #returns dict {outputchannelname:informationBlock,}

    @property
    def summary(self):
        inputdic = [ x.identifier for x in self.inputchanneldic.values() ]
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"ExternalProgramFunction", "description":self.description, "input":inputdic, "output":outputdic }

class ExternalProgramFileFunction:
    """FileFunction which calls an external program"""
    def __init__(self, identifier, inputformat, outputformat, programcall:list):
        #programlist ["program","-s","#{inputchannelname1}","-e","#{inputchannelname2}"]
        self.__programlist = programcall
        self.inputformat = inputformat #TODO
        self.outputformat = outputformat #TODO

    def __call__(self, wdic):
        #fileinput, fileoutput
        #TODO: check if follows inputformat. 
        from ColonyDSL.Interaction.Protocol import protocol_split
        for dickey in wdic.keys():
            val = wdic[dickey]
            if val.startswith("file://"):
                wdic[dickey] = protocol_split(val)[path]
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

    @property
    def summary(self):
        return {"iclass":"ExternalProgramFileFunction", "input":self.inputformat, "output":self.outputformat, "identifier":self.identifier}
