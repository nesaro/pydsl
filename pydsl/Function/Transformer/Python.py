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

"""Python Transformers"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Transformer import Transformer
from .Network import HostFunctionNetwork
import logging
from pydsl.Function.Function import Error
LOG = logging.getLogger("PythonTransformer")

class PythonTransformer(Transformer):
    """ Python function based transformer """
    def __init__(self, inputdic, outputdic, function, ecuid = None, server = None, handleeventfunction = None):
        Transformer.__init__(self, inputdic, outputdic, ecuid = ecuid, server = server)
        self._function = function
        self._evfunctiondic = {"client":self.emit, "server":self.emitToServer} #arg passed to wrapper
        if handleeventfunction == None:
            handleeventfunction = lambda x: None
        self.__receiveEvent = handleeventfunction

    def _onReceiveEvent(self, event):
        return self.__receiveEvent(event)
    
    def __call__(self, ibdic):
        for inputkey in self.inputchanneldic.keys():
            if inputkey not in ibdic:
                LOG.error("Key not found in inputdic")
                newerror = Error("Transformer")
                newerror.appendSource(self.ecuid)
                return newerror
        for dickey in ibdic.keys():
            if not self.inputchanneldic[dickey].check(ibdic[dickey]):
                newerror = Error("Grammar") #FIXME: Should be Type error
                newerror.appendSource(self.ecuid)
                return newerror
        from pydsl.Exceptions import TProcessingError
        try:
            result = self._functionwrapper(ibdic)
        except TProcessingError: #TODO: Extract exception source
            newerror = Error("Transformer", [self.ecuid])
            return newerror
        if isinstance(result, Error):
            result.appendSource(self.ecuid)
            return result
        if not result:
            newerror = Error("Transformer", [self.ecuid])
            return newerror
        return result

    def _functionwrapper(self, wdict):
        """Wraps function call, to add parammeters if required"""
        LOG.debug("PythonTransformer._functionwrapper: begin")
        result = self._function(wdict, self.inputchanneldic, self.outputchanneldic, self._evfunctiondic)
        from pydsl.Exceptions import TProcessingError
        if not result or isinstance(result, Error):
            raise TProcessingError(self.ecuid,"Transformer")
        for outputgrammarname in self.outputchanneldic.keys():
            LOG.debug("Verifying Grammar name: " + outputgrammarname)
            if not outputgrammarname in result:
                LOG.error("Error while verifying Grammar name:" + outputgrammarname)
                raise TProcessingError(self.ecuid,"Transformer")

        #Converting to words
        #TODO Process errors like HostPythonTransformer
        return result

    
    def _processsequences(self, sequencestoprocess):
        for sequence in sequencestoprocess:
            from pydsl.Exceptions import TProcessingError
            try:
                result = self.__process(sequence)
            except TProcessingError:
                LOG.exception("run: Error while processing input")
                self.emitToServer(sequence, Error("transformerError"))
                self._dropSequences(sequence)
            else:
                self._dropSequences(sequence)
                if not isinstance(result, dict):
                    LOG.error("run: __process returned bad type")
                    raise TypeError
                if result == {}:
                    self.emitToServer(sequence, Error("transformerError"))
                else:
                    self.emitToServer(sequence, result)
                    for outputchannel in self._connections.keys():
                        self.send(outputchannel, sequence, result[outputchannel])


    def __process(self, sequence):
        """Processing function. Calls to function wrapper. Error case returns {} """
        LOG.info("__process: Begin")
        if not self._function:
            LOG.error("__process: No function defined")
            return {}
        else: 
            datadict = {}
            for entry in self._seq_cache:
                if entry["msgid"] == sequence:
                    datadict[entry["channel"]] =  entry["data"]
            try:
                #TODO: check if datadict has all the required keys
                LOG.debug("__process: grammar dict: " + str(datadict))
                result = self._functionwrapper(datadict)
                return result
            except IndexError: 
                LOG.exception("__process: Index Error Exception calling function")
                #self.emitMsgToServer({"type":"transformerError"}) #FIXME. Should emit an event, but no from this function
                return {}
            
    @property
    def summary(self):
        from pydsl.Abstract import InmutableDict
        inputdic = tuple(self.inputdefinition.values())
        outputdic = tuple(self.outputdefinition.values())
        result = {"iclass":"PythonTransformer", "input":inputdic,"output":outputdic}
        return InmutableDict(result)

class HostPythonTransformer(PythonTransformer, HostFunctionNetwork):
    """Python Function Transformer which can call to other functions"""
    def __init__(self, inputdic, outputdic, auxdic:dict, function, ecuid = None, server = None, handleeventfunction = None):
        HostFunctionNetwork.__init__(self)
        PythonTransformer.__init__(self, inputdic, outputdic, function, ecuid = ecuid, server = server, handleeventfunction = handleeventfunction)
        self._initHostT(auxdic)
        self._server.start()

    def handleEvent(self, event):
        """Handle message As a server"""
        if event.destination == self._server.ecuid:
            msg = event.msg
            if isinstance(msg, Error):
                msg.appendSource(self.name)
                self.emitToServer(msg.msgid, msg)
            else:
                from pydsl.Exceptions import EventError
                LOG.error("HostPythonTransformer: unknown message type: " + str(msg))
                raise EventError
        else:
            self._server.handleEvent(event) 

    def registerInstance(self, name, clientinstance):
        clientinstance.changeParent(self._server)
        self._hostT[name] = clientinstance


    def _functionwrapper(self, worddic):
        """Wraps function call, to add parammeters if required"""
        LOG.info("HostPythonTransformer._functionwrapper: begin")
        from pydsl.Exceptions import TProcessingError
        try:
            result = self._function(worddic, self._hostT, self.inputchanneldic, self.outputchanneldic, self._evfunctiondic)
        except TProcessingError:            
            LOG.exception("__process: Index Error Exception calling function")
            newerror = Error("Tranformer")
            newerror.appendSource(self.ecuid.name)
            return newerror
        if isinstance(result, Error):
            result.appendSource(self.ecuid.name)
            return result
        for channel in result.keys():
            if not result[channel]: #FIXME: > 1 channel receives an error
                newerror = result[channel]
                return newerror
        return result
