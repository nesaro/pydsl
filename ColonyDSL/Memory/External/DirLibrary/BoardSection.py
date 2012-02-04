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

"""Board Definition classes"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

class BoardConnectionDefinition:
    """Transformer connection definition"""
    def __init__(self, basename, internalname, gtname, externalname):
        self.basename = basename
        self.internalchannelname = internalname
        self.externalgtname = gtname
        self.externalchannelname = externalname

    def __str__(self):
        result = "<BoardConnectionDefinition: " + self.basename + " " + self.internalchannelname
        result += " -> " + self.externalgtname + ":" + self.externalchannelname
        return result

class BoardDefinitionSection:
    """Board and its connections definition"""
    def __init__(self, name, gttype, inputconnections: list, outputconnections: list):
        self.name = name
        self.type = gttype
        self.inputConnectionDefinitions = inputconnections #each element is a BoardConnectionDefinition
        self.outputConnectionDefinitions = outputconnections #each element is a BoardConnectionDefinition

    def __str__(self):
        result = "<BoardDefinitionSection "
        result += self.name + ", " + self.type 
        for con in self.inputConnectionDefinitions:
            result += str(con) 
        result += " - "
        for con in self.outputConnectionDefinitions:
            result += str(con) 
        result += ">"
        return result

