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

#Objeto teorico a realizar:
##Scheme MatchConcept: Intentar cuadrar el contenido de la representacion con un concepto conocido. 
### Pepe y Sus podria ser un concepto "Conjunto de Personas"

class Exchange: 
    def __init__(self, rolelist):
        self.totalseq = 0
        self.content = []
        self.rolelist = rolelist
        self.roledict = {}

    def register(self, instance, role):
        assert(role in  self.rolelist)
        self.roledict[instance] = role

    def append(self, content, source) -> None:
        self.content.append((self.roledict[source], content))
        self.notify_all()
    
    def notify_all(self):
        for key in self.roledict:
            key.notify()

    def last_element(self):
        """Returns last element"""
        return self.content[-1]
