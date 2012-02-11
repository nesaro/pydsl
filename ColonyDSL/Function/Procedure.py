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

"""Procedure class"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Function import Function

class Procedure(Function):
    """Function restricted to work with no input """
    pass

class PythonProcedure(Procedure):
    """ Python function implementation of procedure.
    As a procedure it doesn't have input. Output is a Word dictionary that follows output type definition 
    """
    def __init__(self, outputdic, function):
        Procedure.__init__(self)
        self.__function = function
        self.outputchanneldic = outputdic

    def call(self):
        return self.__function()

    def _onReceiveEvent(self, source, msg):
        pass

    @property
    def summary(self):
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"PythonProcedure", "identifier":self.identifier, "output":outputdic }
