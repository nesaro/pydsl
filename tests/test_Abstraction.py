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

import unittest

def fun1(exchangedict, exchange, role):
    exchange.append("Success", role)

class TestActor(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Exchange.Actor import Actor
        from ColonyDSL.Exchange.Exchange import Exchange
        self.__mem = Exchange(["input","output"])
        self.__actor = Actor(fun1)
        self.__actor.register(self.__mem, "input")
        self.__actor.start()

    def testCall(self):
        self.__mem.append("1234", self.__actor)
        import time
        time.sleep(1)
        print("HI")
        print(self.__mem.last_element()[1])
        self.assertTrue(self.__mem.last_element()[1] == "Success")


