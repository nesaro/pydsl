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

"""loader class"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"
from pkg_resources import Requirement, resource_filename
from ColonyDSL.Exceptions import StorageException

def load_type(name:str, memorylist = []):
    if name == "dummy":
        from ColonyDSL.Type.Type import DummyType
        return DummyType()
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    import os
    from ColonyDSL.Memory.Storage.Directory.DirStorage import load_python_file
    dirname = resource_filename(Requirement.parse("colony_archive"),"")
    if os.path.exists(dirname + "/grammar/protocol.py"):
        pginstance = load_python_file(dirname + "/grammar/protocol.py")
    else:
        pginstance = load_python_file("lib_contrib/grammar/protocol.py")
    if not pginstance.check(name):
        for memory in memorylist:
            if name in memory:
                return memory.load(name)
    else:
        protocol = pginstance.get_groups(name, "protocol")
        path = pginstance.get_groups(name, "path")
        if protocol == "file":
            return load_python_file(path) #FIXME: there are types that aren't  python files
        elif protocol == "memory":
            identifier = pginstance.get_groups(name, "options")
            for memory in memorylist:
                if memory.identifier == path:
                    return memory.load(identifier)
            raise Exception("Memory not found")

    raise StorageException("Type", name)

def load_function(name, memorylist = []):
    raise NotImplementedError

def load_grammar(name, memorylist = []):
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        #if memory.provided_iclasses() and "Grammar" not in memory.provided_iclasses():
        #    continue
        if name in memory:
            return memory.load(name)
    raise StorageException("Grammar", name)

def load_procedure(identifier, eventmanager = None , name = "", memorylist = []):
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier, eventmanager, name)
    raise StorageException("Procedure", identifier)

def load_transformer(identifier, eventmanager = None, name = None, memorylist = []):
    #FIXME: Can return any type of element
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist

    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier, eventmanager, name)
    raise StorageException("Transformer", identifier)

def load_board(identifier, eventmanager = None, name = None, memorylist = []):
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if "Board" not in memory.provided_iclasses():
            continue
        if name in memory:
            return memory.load(name)
    raise StorageException("Grammar", name)

def load_concept(identifier, memorylist = []):
    pass

def load_scheme(identifier, memorylist = []):
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if "Scheme" not in memory.provided_iclasses():
            continue
        if identifier in memory:
            return memory.load(identifier)
    raise StorageException("Scheme", identifier)

def load_information(name:str, memorylist = []):
    if not memorylist:
        from ColonyDSL.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    import os
    from ColonyDSL.Memory.Storage.Directory.DirStorage import load_python_file
    dirname = resource_filename(Requirement.parse("colony_archive"),"")
    if os.path.exists(dirname + "/grammar/protocol.py"):
        pginstance = load_python_file(dirname + "/grammar/protocol.py")
    else:
        pginstance = load_python_file("lib_contrib/grammar/protocol.py")
    if not pginstance.check(name):
        for memory in memorylist:
            if name in memory:
                return memory.load(name)
    else:
        protocol = pginstance.get_groups(name, "protocol")[0]
        path = pginstance.get_groups(name, "path")[0]
        if protocol == "file":
            from ColonyDSL.Memory.Storage.Directory.Value import load_information as lin
            return lin(path)
        elif protocol == "memory":
            identifier = pginstance.get_groups(name, "options")
            for memory in memorylist:
                if memory.identifier == path:
                    return memory.load(identifier)
            raise Exception("Memory not found")

    raise StorageException("Information", name)

