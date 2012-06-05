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


"""
FileType
"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"


from .Checker import Checker 
from pydsl.Abstract import Indexable

class FileType(Checker, Indexable):
    """subclass of type used for fast filetype recognition"""
    def __init__(self, regexp):
        import re
        self.regexp = re.compile(regexp)
        Checker.__init__(self)

    def check(self, data):
        from pydsl.Interaction.Protocol import protocol_split
        filename = None
        if protocol_split(data)["protocol"] == "file":
            filename = protocol_split(data)["path"]
        else:
            import tempfile
            tmpfile = tempfile.NamedTemporaryFile(delete=False)
            tmpfile.write(data)
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
