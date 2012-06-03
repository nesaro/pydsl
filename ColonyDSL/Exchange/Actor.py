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

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

from ColonyDSL.Abstract import Indexable
from abc import abstractmethod, ABCMeta
from ColonyDSL.Function.Function import FunctionInterface
from threading import Thread, Event

class Actor(Indexable, Thread, FunctionInterface):
    """Exchange Actor Actors writes and read an exchange """
    def __init__(self, workingfunction):
        Thread.__init__(self)
        Indexable.__init__(self)
        self.exchange = exchange
        self.rolename = rolename
        self.exchangedict = {}
        self.workingfunction = workingfunction
        self.setDaemon(True)
        self.event = Event()
        self.lastcaller = None

    def register(self, exchange, rolename):
        if not rolename in exchangedict:
            self.exchangedict[rolename] = []
        self.exchangedict[rolename].append(exchange)
        exchange.register(self, rolename)

    def notify(self, caller):
        self.lastcaller = caller
        self.event.set()

    def run(self):
        while self.event.wait():
            self.workingfunction(self.exchangedict, self.lastcaller, self.rolename)
            self.event.clear()

    def summary(self):
        raise NotImplementedError
