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


#TODO: Methods to connect schemes for syncronization and inhibition

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Actor import Actor
from threading import Thread

class Scheme(Actor, Thread):
    """A machine that receives representations from Interactors, sends representations to them, can ask for internal vars, concepts an relations
    and which goal is perform actions. An scheme can inhibit another scheme.
    It works with threshold like ANNs
    """
    def __init__(self, identifier, slots, activation_func, call_func):
        Thread.__init__(self)
        Actor.__init__(self, slots)
        self.activation_func = activation_func #signature: connection
        self.call_func = call_func #signature: connection
        self.setDaemon(True)
        import queue
        self.queue = queue.Queue()
        self.start()
    
    def __test_activation(self, connection) -> bool:
        """Should this scheme start working with current available data?"""
        return self.activation_func(connection, callerid)

    def summary(self):
        return {"iclass":"Scheme"}

    def run(self):
        while True:
            element = self.queue.get()
            if not self.__test_activation(connection):
                continue
            #do something. Call to other schemes to fill the input representation
            #generate new elements for the representation
            result = self.call_func(connection)
            for slot, content in result.items():
                for identifier, conn in self.slots[slot]:
                    conn.mem.save(result, self.identifier, identifier)
                for connection in self.connections():
                    if self.__test_activation(connection):
                        self.call_func(connection)
                        wait = False

class Sense(Actor, Thread):
    def __init__(self):
        Thread.__init__(self)

    def summary(self):
        pass

    def run(self):
        pass
