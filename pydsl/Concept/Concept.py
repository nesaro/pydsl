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


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import ABCMeta
from pydsl.Abstract import Indexable

class Concept(Indexable, metaclass = ABCMeta):
    def __init__(self, identifier):
        self.identifier = identifier

    def __eq__(self, other):
        if isinstance(other, Concept) and other.identifier == self.identifier:
            return True
        return False
    
    @property
    def summary(self):
        return {"iclass":"Concept", "identifier":str(self.identifier)}

    def __str__(self):
        return str(self.identifier)

    def __hash__(self):
        return hash(self.identifier)
