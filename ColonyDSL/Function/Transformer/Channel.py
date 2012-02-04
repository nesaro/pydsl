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

""" Channels: Where words are sent and received """

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import ABCMeta, abstractmethod, abstractproperty
import logging
LOG = logging.getLogger("Channel")

def _loadTypeInstances(originaldic):
    """Converts {"channelname","type"} into {"channelname",instance}"""
    from ColonyDSL.Memory.External.Loader import load_type
    result = {}
    for key in originaldic:
        result[key] = load_type(str(originaldic[key]))
    return result

class HostChannel(metaclass = ABCMeta):
    """Channel Host base class"""
    def __init__(self):
        self._seq_cache = [] #stores words received by channels but unprocessed
        import threading
        self._worklock = threading.Condition()
        self._appendlock = threading.Lock()

    @abstractmethod
    def connect(self, intchannel, ext, extChannel):
        pass

    @abstractproperty
    def inputchanneldic(self):
        pass

    @abstractproperty
    def outputchanneldic(self):
        pass

    def receive(self, channel, msgid, content):
        """Receives an content through channel"""
        LOG.debug("Received:" + str(channel) + " : " + str(content))
        if not channel in self.inputchanneldic.keys():
            LOG.critical(str(self.identifier) + ":Channel not found: " + str(channel)) 
            raise IndexError
        with self._appendlock:
            self._seq_cache.append({"channel":channel, "msgid":msgid, "data":content})
        with self._worklock:
            sequencestoprocess, sequencestodrop = self._checkSequences()
            if sequencestoprocess:
                LOG.debug("run: " + str(self.identifier) + " after finished: sequence list" + str(sequencestoprocess))
                self._processsequences(sequencestoprocess)
            self._dropSequences(sequencestodrop) #FIXME find the right place to clean sequences

    def _processsequences(self, sequencestoprocess) -> bool:
        for sequence in sequencestoprocess:
            from ColonyDSL.Exceptions import TProcessingError
            try:
                mylist = list(filter(lambda x:x["msgid"] == sequence, self._seq_cache))
                mydic = {}
                for x in mylist:
                    mydic[x["channel"]] = x["data"]
                result = self.call(mydic)
            except TProcessingError:
                LOG.exception("run: Error while processing input")
                self.emitToServer({"type":"transformerError"}, sequence)
                self._dropSequences(sequence)
            else:
                self._dropSequences(sequence)
                from ColonyDSL.Function.Function import Error
                if isinstance(result, Error):
                    result.appendSource(str(self.ecuid.name))
                    self.emitToServer(sequence, result) #FIXME: this sequence number must be checked
                    return False
                if not isinstance(result, dict):
                    LOG.error("run: __process returned bad type")
                    raise TypeError                
                if result == {}:
                    self.emitToServer(sequence, Error("transformerError"))
                else:
                    self.emitToServer(sequence, result)
                    for outputchannel in self._connections.keys():
                        self.send(outputchannel, sequence, result[outputchannel])
                    self.emitToSelf(sequence, result) #TODO: Only Boards requires it
        return True


    def _dropSequences(self, sequencestodrop):
        """Drops every sequence in self._sequencestodrop """
        if not isinstance(sequencestodrop, list):
            sequencestodrop = [sequencestodrop]
        LOG.debug("_dropSequences: sequences to drop:" + str(sequencestodrop))
        with self._appendlock:
            i = 0
            while i < len(self._seq_cache):
                if self._seq_cache[i]["msgid"] in sequencestodrop:
                    del self._seq_cache[i]
                else:
                    i += 1

    def _checkSequences(self):
        """Checks if there is at least one valid sequence. Fills self._sequencestoprocess and self._sequencestodrop"""
        #Iterate through self._seq_cache
        seqlist = [] #Stores every known sequence
        sequencestodrop = []
        for entry in self._seq_cache: #Grab every sequence
            if not entry["msgid"] in seqlist:
                seqlist.append(entry["msgid"])
        LOG.debug("__checkSequences: " + str(self.identifier) + " inputCommunications text list:" + str([x["data"] for x in self._seq_cache])) 
        checkdic = {} #To check valid sequences
        for sequence in seqlist:
            checkdic[sequence] = {}
            for grammarname in self.inputchanneldic.keys():
                checkdic[sequence][grammarname] = False

        for sequence in seqlist:
            for inputgrammarname, inputgrammar in self.inputchanneldic.items():
                for communication in self._seq_cache:
                    if communication["channel"] == inputgrammarname and communication["msgid"] == sequence:
                        if not inputgrammar.check(communication["data"]):
                            LOG.warning("__checkSequences: " + str(self.identifier) + " Grammar " + str(inputgrammar.identifier) + " check failed:" + inputgrammarname + " communication: " + str(communication["data"])) 
                            from ColonyDSL.Function.Function import Error
                            self.emitToServer(sequence,Error("Grammar",[self.ecuid.name])) #FIXME: which id should use?
                            if not sequence in sequencestodrop:
                                sequencestodrop.append(sequence)
                        else:
                            LOG.debug("__checkSequences: " + str(self.identifier) + "sequence :" + str(sequence) + " ok in channel: " +communication["channel"]) 
                            checkdic[sequence][communication["channel"]] = True
                    else:
                        LOG.debug("__checkSequences: " + str(self.identifier) + " communication[channel]: " + str(communication["channel"]) + " inputgrammarname: " + inputgrammarname) 
                        LOG.debug("__checkSequences: " + str(self.identifier) + "sequence  from data:" + str(communication["msgid"]) + " and from list:" + str(sequence) )


        for sequence in sequencestodrop:
            seqlist.remove(sequence)

        sequencestoprocess = []
        for sequence in seqlist:
            validsequence = True
            for value in checkdic[sequence].values():
                if not value:
                    validsequence = False
                    LOG.debug("__checkSequences: " + str(self.identifier) + " not valid sequence:" + str(sequence))
                    break
            if validsequence:
                with self._appendlock:
                    sequencestoprocess.append(sequence)
        LOG.debug("__checkSequences: valid sequences:" + str(sequencestoprocess) + " ; dropped sequences: " + str(sequencestodrop))
        return sequencestoprocess, sequencestodrop


class Channel(metaclass = ABCMeta):
    """ Channel base class"""
    def __init__(self, host1:HostChannel, channel1Name, host2:HostChannel, channel2Name):
        assert(channel1Name != channel2Name)
        self._host1 = host1
        self.channel1Name = channel1Name
        self._host2 = host2
        self.channel2Name = channel2Name

    def _sendTo(self, destination, msgid, content):
        if destination == self.channel1Name:
            self._host1.receive(self.channel1Name, msgid, content)
        elif destination == self.channel2Name:
            self._host2.receive(self.channel2Name, msgid, content)
        else:
            raise KeyError

    @abstractmethod
    def send(self):
        pass

class DirectedChannel(Channel):
    """ One way channel"""
    def __init__(self, GT, extGT, extChannelName):
        Channel.__init__(self, GT, None, extGT, extChannelName)

    def send(self, msgid, content):
        self._sendTo(self.channel2Name, msgid, content)

    def __str__(self):
        return "<DC " + str(self._host1.identifier) + " -> " + str(self._host2.identifier) + ":" + str(self.channel2Name) + ">"


MODELIST = ["fixed", "first", "free" , "copy" ] 

#first: Use the first input grammar 
#fixed: Always use the same grammar 
#free: Any grammar at any time
#copy: channel2 uses the same grammar that channel1

class TypeChannelHost(HostChannel):
    """A class that contains input and output string-named channels. Each channel must contain a Grammar object
    Any class which inherites from this must also inherit from HostChannel
    """
    def __init__(self, inputtypedict:dict, outputtypedict:dict):
        HostChannel.__init__(self)
        for key in inputtypedict:
            if not isinstance(key, str):
                raise TypeError
        for key in outputtypedict:
            if not isinstance(key, str):
                raise TypeError
        self.__inputchanneldic = _loadTypeInstances(inputtypedict)
        self.__outputchanneldic = _loadTypeInstances(outputtypedict)
        self._connections = {}

    def connect(self, intchannel, extGT, extChannel):
        self._connections[intchannel] = DirectedChannel(self, extGT, extChannel)

    def send(self, outputchannel, msgid, content):
        """ Sends a data block"""
        self._connections[outputchannel].send(msgid, content)

    @property
    def inputchanneldic(self):
        return self.__inputchanneldic

    @property
    def outputchanneldic(self):
        return self.__outputchanneldic

