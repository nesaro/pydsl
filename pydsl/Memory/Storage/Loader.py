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

"""loader class"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"
from pkg_resources import Requirement, resource_filename
from pydsl.Grammar.BNF import BNFGrammar

def load_checker(grammar):
    if grammar == "dummy":
        from pydsl.Grammar.Checker import DummyChecker
        return DummyChecker()
    import re
    tmp = re.compile("a")
    if isinstance(grammar, str):
        grammar = load_grammar(grammar)
    if isinstance(grammar, BNFGrammar):
        raise NotImplementedError
        #return BNFChecker(grammar)
    elif isinstance(grammar, type(tmp)):
        from pydsl.Grammar.Checker import RegularExpressionChecker
        return RegularExpressionChecker(grammar)
    else:
        raise ValueError(grammar)

def load_function(identifier, memorylist = []):
    try:
        return load_board(identifier, memorylist)
    except KeyError:
        pass
    try:
        return load_transformer(identifier, memorylist)
    except KeyError:
        pass
    raise KeyError("Function" + identifier)

def load_grammar(identifier, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        #if memory.provided_iclasses() and "Grammar" not in memory.provided_iclasses():
        #    continue
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError("Grammar" + identifier)

def load_procedure(identifier, eventmanager = None , ecuid = "", memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier, eventmanager, ecuid)
    raise KeyError("Procedure" + identifier)

def load_transformer(identifier, eventmanager = None, ecuid = None, memorylist = []):
    #FIXME: Can return any type of element
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist

    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier, server=eventmanager, ecuid=ecuid)
    raise KeyError("Transformer" + identifier)

def load_board(identifier, eventmanager = None, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if "Board" not in memory.provided_iclasses():
            continue
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError("Board" + identifier)

def load_actor(identifier, exchange, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if "Actor" not in memory.provided_iclasses():
            continue
        if identifier in memory:
            return memory.load(identifier, exchange=exchange) #FIXME Pass as kwarg
    raise KeyError("Actor" + identifier)

def load_information(name:str, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    import os
    from pydsl.Memory.Storage.Directory.DirStorage import load_python_file
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
            from pydsl.Memory.Storage.Directory.Value import load_information as lin
            return lin(path)
        elif protocol == "memory":
            identifier = pginstance.get_groups(name, "options")
            for memory in memorylist:
                if memory.identifier == path:
                    return memory.load(identifier)
            raise Exception("Memory not found")

    raise KeyError("Information" + name)

