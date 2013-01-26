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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)

def _loadGrammarTools(originaldic):
    """Converts {"channelname","type"} into {"channelname",instance}"""
    from pydsl.Memory.Loader import load_grammar_tool
    result = {}
    for key in originaldic:
        result[key] = load_grammar_tool(str(originaldic[key]))
    return result

class HostChannel(object):
    """A class that contains input and output string-named channels. Each channel must contain a Type object
    Any class which inherites from this must also inherit from HostChannel
    """
    def __init__(self, inputtypedict, outputtypedict):
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

    @property
    def inputchanneldic(self):
        return self.__inputchanneldic

    @property
    def outputchanneldic(self):
        return self.__outputchanneldic
