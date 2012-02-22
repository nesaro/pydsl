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

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from ColonyDSL.Abstract import Indexable
from abc import abstractmethod, ABCMeta

class Actor(Indexable, metaclass = ABCMeta):
    """WorkingMemory Actor"""
    def __init__(self, inputslotdefinitions:list, outputslotdefinitions:list):
        Indexable.__init__(self)
        self.inputs = {}
        self.outputs = {}
        for ins in inputslotdefinitions::
            self.inputs[ins] = []
        for outs in outputslotdefinitions::
            self.outputs[outs] = []

    def register_input(self, slot, wm:"WorkingMemory"):
        """Registers a working memory as concept feeder"""
        self.inputs[slot].append(wm) 

    def register_output(self, slot, wm:"WorkingMemory"):
        """Registers a working memory as concept destination"""
        self.outputs[slot].append(wm) 

    @abstractmethod
    def run(self):
        pass
        
