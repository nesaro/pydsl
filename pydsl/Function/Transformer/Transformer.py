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

"""Transformers"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from .Network import FunctionNetworkClient
from ..Channel import NetworkedHostChannel 
LOG = logging.getLogger(__name__)
from abc import ABCMeta

class Transformer(NetworkedHostChannel, FunctionNetworkClient, metaclass = ABCMeta):
    """Channel and Network enabled Function"""
    def __init__(self, inputgrammars, outputgrammars, ecuid, server = None):
        NetworkedHostChannel.__init__(self, inputgrammars, outputgrammars)
        FunctionNetworkClient.__init__(self, ecuid, server)


