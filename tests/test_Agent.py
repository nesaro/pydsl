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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Agent import AgentNetwork

def fun1(parent, obj):
    print("FUN !")
    parent.emit_message('output',obj['message'])


class TestAgentNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def testNetwork(self):
        initlist = [("agent1", {'input':fun1})]
        #initlist = [("agent1", {'input':lambda parent,obj:'OK'})]
        mynetwork = AgentNetwork("ExampleExchange", initlist)
        result = mynetwork.call("1234")
        print(result)
