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
from threading import Thread

class Actor(Indexable, Thread, FunctionInterface):
    """Exchange Actor Actors writes and read an exchange """
    def __init__(self, exchange, rolaname, workingfunction):
        Thread.__init__(self)
        Indexable.__init__(self)
        exchange.register(self, rolename)
        self.workingfunction = workingfunction
        self.setDaemon(True)

    def run(self):
        while True:
            self.workingfunction(self.exchange, self.rolename)

