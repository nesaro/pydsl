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

"""Transformers"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

import logging
from ColonyDSL.Function.Function import Function 
from .Network import FunctionNetworkClient
from .Channel import TypeChannelHost 
LOG = logging.getLogger("Transformer")
from abc import ABCMeta

class Transformer(TypeChannelHost, FunctionNetworkClient, Function, metaclass = ABCMeta):
    """Channel and Network enabled Function"""
    def __init__(self, inputgrammars, outputgrammars, ecuid, server = None):
        TypeChannelHost.__init__(self, inputgrammars, outputgrammars)
        Function.__init__(self)
        FunctionNetworkClient.__init__(self, ecuid, server)

    def receive(self, channel, msgid, content):
        TypeChannelHost.receive(self, channel, msgid, content)

    

