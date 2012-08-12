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

""" Channels: Where words are sent and received """

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"


from abc import ABCMeta, abstractmethod, abstractproperty
from .Function import FunctionInterface
import logging
LOG = logging.getLogger(__name__)

def _loadGrammarTools(originaldic):
    """Converts {"channelname","type"} into {"channelname",instance}"""
    from pydsl.Memory.Storage.Loader import load_grammar_tool
    result = {}
    for key in originaldic:
        result[key] = load_grammar_tool(str(originaldic[key]))
    return result

class HostChannel(FunctionInterface):
    """A class that contains input and output string-named channels. Each channel must contain a Type object
    Any class which inherites from this must also inherit from HostChannel
    """
    def __init__(self, inputtypedict:dict, outputtypedict:dict):
        FunctionInterface.__init__(self)
        for key in inputtypedict:
            if not isinstance(key, str):
                raise TypeError
        for key in outputtypedict:
            if not isinstance(key, str):
                raise TypeError
        self.inputdefinition = inputtypedict
        self.outputdefinition = outputtypedict
        self.__inputchanneldic = _loadGrammarTools(inputtypedict)
        self.__outputchanneldic = _loadGrammarTools(outputtypedict)
        self._connections = {}

    def connect(self, extGT, extChannel):
        self._connections[intchannel] = Channel(extGT, extChannel)

    def send(self, outputchannel, msgid, content):
        """ Sends a data block"""
        self._connections[outputchannel].send(msgid, content)

    @property
    def inputchanneldic(self):
        return self.__inputchanneldic

    @property
    def outputchanneldic(self):
        return self.__outputchanneldic

class Channel(metaclass = ABCMeta):
    def __init__(self, host2:HostChannel, channel2Name):
        self._host2 = host2
        self.channel2Name = channel2Name

    def send(self, msgid, content):
        self._host2.receive(self.channel2Name, msgid, content)

