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

"""
External Program Type
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Type import Type 
#TODO: Use URI and fileprotocols

class ExternalProgramType(Type):
    """Calls another program to perform checking. Args are always filenames"""
    def __init__(self, checkprogramcommandlinelist, checkpropertycommandlinelist = None):
        Type.__init__(self)
        self.checkpropertycommandlinelist = checkpropertycommandlinelist
        self.checkprogramcommandlinelist = checkprogramcommandlinelist

    def check(self, information):
        calllist = list(self.checkprogramcommandlinelist)
        for index in range(len(calllist)):
            element = self.checkprogramcommandlinelist[index]
            if element.find("#{block}") != -1:
                try:
                    calllist[index] = element.replace("#{block}", str(information))
                except UnicodeDecodeError:
                    return False
        import subprocess
        try:
            value = subprocess.call(calllist)
        except OSError:
            return False
        return value == 0
        
    @property
    def summary(self):
        return {"iclass":"ExternalProgramGrammar", "identifier":self.identifier, "description":self.description}
