#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Abstraction: Conversion between values and concepts
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from ColonyDSL.Function.Concept import ConceptFunction
from .Memory import Actor
from threading import Thread

class Abstractor(Actor, Thread):
    def __init__(self, identifier, cclist = [], crlist = []):
        Thread.__init__(self)
        Actor.__init__(self, ["input","output"])
        self.conceptconcretizerlist = cclist
        self.conceptrecognizerlist = crlist
        self.identifier = identifier
        self.setDaemon(True)
        import queue
        self.queue = queue.Queue()
        self.start()

    def receive(self, connection, slot, data):
        self.queue.put((connection, slot, data))

    def run(self):
        pass
    
    @property
    def concrete(self):
        pass

    @property
    def abstract(self):
        pass

