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
FileType
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"


from .Type import Type 

class FileType(Type):
    """subclass of type used for fast filetype recognition"""
    def __init__(self, regexp):
        import re
        self.regexp = re.compile(regexp)
        Type.__init__(self)

    def check(self, data, synonymgrammar = None):
        from ColonyDSL.Interaction.Protocol import URI, Protocol
        fp = Protocol("file")
        filename = None
        if isinstance(data, URI) :
            filename = vars(data)()["path"]
        elif fp.check(data):
            filename = vars(URI(data))()["path"]
        else:
            import tempfile
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write(data.encode())
            filename = tmpfile.name
        import subprocess
        proc = subprocess.Popen(["file", "-b",  filename], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        proc.stdout.close()
        line = lines[0].decode()
        return self.regexp.match(line) != None

    @property
    def summary(self):
        return {"iclass":"FileType"}
