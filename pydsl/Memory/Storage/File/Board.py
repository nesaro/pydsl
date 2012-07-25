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

"""Functions Library"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

from .Python import getFileTuple
import logging
LOG = logging.getLogger("Storage.Directory.Function")

def _readBoardFileRightSideArgs(thestring, basegtname):
    """Reads input or output definition, and splits it accordingly"""
    from .BoardSection import BoardConnectionDefinition
    finallist = []
    tmplist = thestring.split(",")
    for gt in tmplist:
        if gt.count(".") == 2:
            tmpgt = gt.split(".")
            gtcondef = BoardConnectionDefinition(basegtname, tmpgt[0], tmpgt[1], tmpgt[2])
        else:
            raise SyntaxError
        finallist.append(gtcondef)
    return finallist

def sectionToBoardDefinition(configparser, sectionname):
    """Create a Transformer definition object from file"""
    items = configparser.items(sectionname)
    LOG.debug("sectionToBoardDefinition: Item List: " + str(items))
    myinput = _readBoardFileRightSideArgs(configparser.get(sectionname, "input"), sectionname)
    output = _readBoardFileRightSideArgs(configparser.get(sectionname, "output"), sectionname)
    mytype = configparser.get(sectionname, "type")
    from .BoardSection import BoardDefinitionSection
    return BoardDefinitionSection(sectionname, mytype, myinput, output)

def parseRegularSections(configparser):
    definitionlist = []
    for section in configparser.sections():
        definitionlist.append(sectionToBoardDefinition(configparser, section))
    return definitionlist

def load_board_file(filename, server = None , ecuid = None):
    import configparser
    config = configparser.ConfigParser()
    config.read(filename)
    if len(config.sections()) == 0:
        from pydsl.Exceptions import BadFileFormat
        raise BadFileFormat(filename)
    GTDefinitionList = parseRegularSections(config)
    from pydsl.Function.Transformer.Board import Board
    return Board(GTDefinitionList, ecuid = ecuid, server = server) 

def load_python_f(modulename , server):
    """Load a file written in python"""
    identifier = getFileTuple(modulename)[2]
    import imp
    print(identifier, modulename)
    moduleobject = imp.load_source(identifier, modulename)
    from .DirStorage import load_python_file
    return load_python_file(moduleobject, server = server)


