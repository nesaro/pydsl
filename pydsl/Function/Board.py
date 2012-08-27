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

"""Boards"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class Board:
    """A Transformer where you can call other Transformer. Doesn't perform any computation"""

    def __init__(self, gtenvdefinitionslist:list, timeout = 10):
        self._hostT = {}
        self.__GTDefinitionlist = gtenvdefinitionslist #list to put every gt envdefinition
        self.__loadTfromDefinitionList()
        self.__inputGTDict = {} #{"channelname":GTinstance,} #Inner GT that receives input
        self.__outputGTDict = {} #{"channelname":GTinstance,}
        self.connectionsdict = {}
        self.__connectAllGTs()
        self.__extractExternalChannelGrammarsFromDefinitions()

    @property
    def inputchanneldic(self):
        return self.__inputGTDict

    @property
    def summary(self):
        from pydsl.Abstract import InmutableDict
        #TODO: inputs and outputs
        result = {"iclass":"Board", "ancestors":self.ancestors()}
        return InmutableDict(result)

    def __call__(self, inputdict:dict):
        LOG.debug(" received dic:" + str(inputdict))
        resultdict = {}
        calldict = {}
        if not inputdict:
            LOG.error("No input")
            return None
        for channel, strcontent in inputdict.items():
            LOG.debug("Board Receiving: " + channel + " " + str(strcontent))
            #self.__sendToChannel(channel, rand, strcontent)
            gtname, keyname = self.__inputGTDict[channel]
            if not gtname in calldict:
                calldict[gtname] = {}
            calldict[gtname][keyname] = strcontent
        for gtname, functinput in calldict.items():
            resultdict[gtname] = self._hostT[gtname](functinput)
        #prepare extendedtuplelist

        extendedtuplelist = []
        for gtname, results in self.connectionsdict.items():
            for chan1, duple in results.items():
                #gtname, outputchannel, inputchannel, gtinstance
                extendedtuplelist.append((gtname, chan1, duple[0], duple[1], duple[2]))
        change = True
        while change:
            change = False
            thisroundgt = set()
            for gtname, extkey, intkey, gtinstance, extgtname in extendedtuplelist:
                if gtinstance:
                    thisroundgt.add((gtinstance, extgtname))
            for curgt, curgtname in thisroundgt:
                curinputs = {}
                for gtname, extkey, intkey, gtinstance, extgtname in extendedtuplelist:
                    if not gtinstance:
                        continue
                    if not gtname in curinputs:
                        curinputs[gtname] = {}
                    if gtname in resultdict:
                        curinputs[gtname][extkey] = resultdict[gtname][intkey]
                if sum([len(x) for x in curinputs.values()]) == len(curgt.inputchanneldic):
                    change = True
                    curinputdict = {}
                    for gtname, value in curinputs.items():
                        curinputdict.update(value)
                        for key in value:
                            del resultdict[gtname][key]
                        if not resultdict[gtname]:
                            del resultdict[gtname]
                    resultdict[curgtname] = self._hostT[curgtname](curinputdict)
                    
            finaldict = {}
            for key, value in self.__outputGTDict.items():
                gtname, channelname = value
                finaldict[key] = resultdict[gtname][channelname]
            return finaldict
                

    def __extractExternalChannelGrammarsFromDefinitions(self):
        """Extracts grammars from definition.
        generated channel must be connected to outside elements"""
        #TODO: Store connections in a dictionary
        #{"part1":["part2","part3"],
        # "part2":....
        # "partn":...}

        #Store initials and ends in lists
        #initials: ["part1"]
        #ends: ["partn"]

        for definition in self.__GTDefinitionlist:
            for gtcondef in definition.inputConnectionDefinitions:
                if gtcondef.externalgtname == "Main":
                    self.__inputGTDict[gtcondef.externalchannelname] = (gtcondef.basename, gtcondef.internalchannelname) #Prepares self.__inputGTDict
            for gtcondef in definition.outputConnectionDefinitions:
                if gtcondef.externalgtname == "Main":
                    self.__outputGTDict[gtcondef.externalchannelname] = (gtcondef.basename, gtcondef.internalchannelname) #Prepares self.__outputGTDict

    def __loadTfromDefinitionList(self):
        """GTDefinitions -> Instances"""
        from pydsl.Memory.Storage.File.BoardSection import BoardDefinitionSection
        auxnametype = {}
        for definition in self.__GTDefinitionlist:
            if not isinstance(definition, BoardDefinitionSection):
                raise TypeError
            gtname = definition.name
            gttype = definition.type
            auxnametype[gtname] = gttype
        self._initHostT(auxnametype)
        LOG.debug("__loadTfromDefinitionList: loaded __GTs: " + str(self._hostT.keys()))

    def __connectAllGTs(self):
        """Connect all instances"""
        from pydsl.Memory.Storage.File.BoardSection import BoardConnectionDefinition
        for definition in self.__GTDefinitionlist:
            gtname = definition.name
            outputgrammarlist = definition.outputConnectionDefinitions
            gtinstance = self._hostT[gtname]
            self.connectionsdict[gtname] = {}
            for gtcondef in outputgrammarlist:
                hostt = None     
                if gtcondef.externalgtname != "Main":
                    hostt = self._hostT[gtcondef.externalgtname]
                self.connectionsdict[gtname][gtcondef.internalchannelname] = (gtcondef.externalchannelname, hostt, gtcondef.externalgtname)

    def __str__(self):
        result = "<B " + str(self.identifier) + " "
        result += "input: " + str(self.inputchanneldic)
        result += "output: " + str(self.outputchanneldic)
        result += "inputGT: " + str(self.__inputGTDict)
        result += "outputGT: " + str(self.__outputGTDict)
        result += "connections: " + str(self._connections)
        result += ">"
        return result

    def _initHostT(self, namedic):
        """Inits aux GTs. if a requested aux GT isn't connected, This function will create them"""
        from pydsl.Memory.Loader import load_transformer
        for title, gttype in namedic.items():
            self._hostT[title] = load_transformer(gttype) 
            LOG.debug("loaded " + str(title) + "auxT")

