#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Memory import Actor
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

    def receive(self, connection, slot, element = None):
        self.queue.put((connection, slot, element))

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
