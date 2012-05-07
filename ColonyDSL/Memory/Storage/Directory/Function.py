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

"""Functions Library"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .DirStorage import DirStorage, getFileTuple
import logging
LOG = logging.getLogger("Storage.Directory.Function")

def _readBoardFileRightSideArgs(thestring, basegtname):
    """Reads input or output definition, and splits it accordingly"""
    from .BoardSection import BoardConnectionDefinition
    finallist = []
    tmplist = thestring.split(",")
    for gt in tmplist:
        if gt.count(".") == 2:
            tmpgt = gt.split(".")
            gtcondef = BoardConnectionDefinition(basegtname, tmpgt[0], tmpgt[1], tmpgt[2])
        else:
            raise SyntaxError
        finallist.append(gtcondef)
    return finallist

def sectionToBoardDefinition(configparser, sectionname):
    """Create a Transformer definition object from file"""
    items = configparser.items(sectionname)
    LOG.debug("sectionToBoardDefinition: Item List: " + str(items))
    myinput = _readBoardFileRightSideArgs(configparser.get(sectionname, "input"), sectionname)
    output = _readBoardFileRightSideArgs(configparser.get(sectionname, "output"), sectionname)
    mytype = configparser.get(sectionname, "type")
    from .BoardSection import BoardDefinitionSection
    return BoardDefinitionSection(sectionname, mytype, myinput, output)

def parseRegularSections(configparser):
    definitionlist = []
    for section in configparser.sections():
        definitionlist.append(sectionToBoardDefinition(configparser, section))
    return definitionlist

def load_board_file(filename, server = None , name = None):
    import configparser
    config = configparser.ConfigParser()
    config.read(filename)
    if len(config.sections()) == 0:
        from ColonyDSL.Exceptions import BadFileFormat
        raise BadFileFormat(filename)
    GTDefinitionList = parseRegularSections(config)
    from ColonyDSL.Function.Transformer.Board import Board
    return Board(GTDefinitionList, ecuid = name, server = server) 

def load_python_f(modulename , name, server):
    """Load a file written in python"""
    identifier = getFileTuple(modulename)[2]
    import imp
    moduleobject = imp.load_source(identifier, modulename)
    from .DirStorage import load_python_file
    return load_python_file(moduleobject, name, server)

class TransformerDirStorage(DirStorage):
    """generate instances of Grammar Transformers"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def provided_iclasses(self) -> list:
        return ["PythonTransformer", "HostPythonTransformer"]

    def load(self, identifier, server = None, name = None):
        """guess class, guess filename from id, and then call loadTInstance"""
        import imp
        for value in self._searcher.search(identifier): 
            try:
                imp.load_source(identifier, value["filepath"])
            except (ImportError, IOError):
                LOG.exception("Exception while loading: " + identifier)
            else:
                return load_python_f(value["filepath"], name, server)

        from ColonyDSL.Exceptions import StorageException
        raise StorageException("TR", identifier)
    
    def summary_from_filename(self, modulepath):
        from ColonyDSL.Function.Transformer.Python import PythonTransformer
        (_, _, fileBaseName, _) = getFileTuple(modulepath)
        import imp
        moduleobject = imp.load_source(fileBaseName, modulepath)
        from ColonyDSL.Abstract import InmutableDict
        try:
            result = {"identifier":fileBaseName,"iclass":moduleobject.iclass, "filepath":modulepath, "ancestors":PythonTransformer.ancestors()}
            if hasattr(moduleobject, "title"):
                from ColonyDSL.Abstract import InmutableDict
                result["title"] =  InmutableDict(moduleobject.title)
            if hasattr(moduleobject, "description"):
                from ColonyDSL.Abstract import InmutableDict
                result["description"] =  InmutableDict(moduleobject.description)
            if hasattr(moduleobject, "inputdic"):
                result["input"] = InmutableDict(moduleobject.inputdic)
            if hasattr(moduleobject, "outputdic"):
                result["output"] = InmutableDict(moduleobject.outputdic)
            if hasattr(moduleobject, "inputformat"):
                result["input"] = moduleobject.inputformat
            if hasattr(moduleobject, "outputformat"):
                result["output"] = moduleobject.outputformat

            return InmutableDict(result)
        except AttributeError:
            #LOG.exception(modulepath)
            return InmutableDict()
        except ValueError:
            LOG.exception("Error: non-indexable element while loading " + modulepath)
            return InmutableDict()

class BoardDirStorage(DirStorage):
    """Loads boards from library"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".board"])


    def load(self, identifier, server = None, name = None):
        searchresult = self._searcher.search(identifier)
        if not searchresult:
            raise Exception
        for result in searchresult:
            #TODO assert(len(self._search(identifier) == 2)) 
            return load_board_file(result["filepath"], server, name)

        from ColonyDSL.Exceptions import StorageException
        raise StorageException("B", identifier)

    def summary_from_filename(self, filename):
        from ColonyDSL.Function.Transformer.Board import Board
        from ColonyDSL.Abstract import InmutableDict
        (_, _, fileBaseName, _) = getFileTuple(filename)
        return InmutableDict({"iclass":"Board", "identifier":fileBaseName, "filepath":filename, "ancestors":Board.ancestors()})

    def provided_iclasses(self) -> list:
        return ["Board"]



class ProcedureDirStorage(DirStorage):
    """Procedure Library"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def summary_from_filename(self, filename):
        (_, _, fileBaseName, _) = getFileTuple(filename)
        return {"iclass":"Procedure","identifier":fileBaseName, "filepath":filename}

    def load(self, identifier, server = None, name = None):
        """guess class, guess filename from id, and then call loadTInstance"""
        import imp
        try:
            imp.load_source(identifier, self.identifier + "/" + identifier + ".py")
        except (ImportError, IOError):
            pass
        else:
            return load_python_f(identifier, name, server)

        from ColonyDSL.Exceptions import StorageException
        raise StorageException("P", identifier)

    def provided_iclasses(self) -> list:
        return ["Procedure"]

    def all_files_generator(self):
        """Generates (inputlist, outputlist, name, description) from T list"""
        from ColonyDSL.Exceptions import StorageException
        for elementname in self.allElementStaticIdGenerator():
            try:
                instance = self.load(elementname)
            except TypeError:
                continue
            except StorageException:
                continue
            except ImportError:
                continue
            except NameError:
                continue
            exfun = lambda x:getattr(x,"name").split(".")[0]
            yield (map(exfun, elementname, instance.description))
            #instance.outputchanneldic.values()),
        

