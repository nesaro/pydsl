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

"""Board Definition classes"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

class BoardConnectionDefinition:
    """Transformer connection definition"""
    def __init__(self, basename, source, gtname, destination):
        self.source = basename
        self.sourcechannel = source
        self.destination = gtname
        self.destinationchannel = destination

    def __str__(self):
        result = "<BoardConnectionDefinition: " + self.source + " " + self.sourcechannel
        result += " -> " + self.externalgtname + ":" + self.destinationchannel
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

