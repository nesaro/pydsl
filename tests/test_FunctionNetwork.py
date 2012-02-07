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


#Events between transformer (E/S)
#Aux call to tranformer

import unittest

def parentfunction(inputdic, auxgt, inputgt, outputgt, evfuncs):
    result = auxgt["client"].call({"input":"HI"})
    return {"output":inputdic["input"]}

def childfunction(inputdic, inputgt, outputgt, evfuncs):
    #Send events to parent
    #from ColonyDSL.Message import ContextRequestMsg
    import random
    intrandom = random.randint(0,10000)

class TestServer(unittest.TestCase):
    """Tests Server"""
    def setUp(self):
        from ColonyDSL.Function.Transformer.Network import FunctionNetworkServer
        self._server = FunctionNetworkServer()
        #Create a child Manager
        from ColonyDSL.Function.Transformer.Python import PythonTransformer, HostPythonTransformer
        self._child = PythonTransformer({"input":"cstring"}, {"output":"cstring"}, childfunction)
        self._parentManager = HostPythonTransformer({"input":"cstring"}, {"output":"cstring"}, {}, parentfunction, server = self._server)
        self._parentManager.registerInstance("client", self._child)
        #load special Transformer that generates client messages
        #load special Transformer that listen client messages

    def testProperty(self):
        result = self._parentManager.call({"input":"1+1"})
        self.assertTrue(str(result["output"]) == "1+1")

        #test messages to a server
        #test  server.environmentlookup 
        #test  parent server.environmentlookup 
