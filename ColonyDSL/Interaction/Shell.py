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

"""ColonyDSL element Interaction"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

from abc import ABCMeta, abstractmethod
import logging
LOG = logging.getLogger("Shell")

promptstr = "Insert data (q to exit)"

def escapedsplitby(inputstring, separator):
    """Splits inputstring with separator and using "\" as a escape character"""
    #TODO check alternatives (shlex and csv)
    result = []
    while inputstring[0] == separator:
        inputstring = inputstring[1:]
    lastindex = 0
    index = 0
    while index < len(inputstring):
        if inputstring[index] == "\\" and inputstring[index+1] == separator:
            inputstring = inputstring[:index] + inputstring[index+1:]
            index += 1
            continue
        elif inputstring[index] == "\\" and   inputstring[index+1] == "\\":
            inputstring = inputstring[:index] + inputstring[index+1:]
            index += 1
            continue
        elif inputstring[index] == separator:
            result.append(inputstring[lastindex:index])
            while inputstring[index] == separator:
                index += 1
            lastindex = index 
            continue
        else:
            index += 1
            continue
    result.append(inputstring[lastindex:])
    return result

def parse_shell_dict(inputstring) -> dict:
    """Parses commandline input dicts. Example: a:b,c:d,e:f."""
    result = {}
    arglist = escapedsplitby(inputstring, ",")
    for arg in arglist:
        pair = escapedsplitby(arg, ":")
        result[pair[0]] = pair[1]
    return result

class ContinuousInteraction(metaclass = ABCMeta):
    """Opened until the end of the interaction"""
    @abstractmethod
    def start(self):
        pass

from ColonyDSL.Cognition.Memory import Actor
class SchemeMixin(Actor, metaclass = ABCMeta):
    from ColonyDSL.Cognition.Scheme import Scheme
    def __init__(self, schemeinstance:Scheme):
        Actor.__init__(self, "main")
        self.scheme = schemeinstance
        from ColonyDSL.Cognition.Memory import WorkingMemory, Connection
        self.rep = WorkingMemory()
        self.inputcon = Connection(self.rep, self)
        self.maincon = Connection(self.rep, self.scheme)

def open_files_dict(inputdic) -> dict:
    """Converts a all str filename values into file objects"""
    result = {}
    for channel, filename in inputdic.items():
        with open(filename, 'rb') as f:
            result[channel] = f.read()
    return result

def close_files_dict(filedic) -> dict:
    """Closes all files"""
    for x in filedic.values():
        x.close()

def save_result_to_output(resultdic, outputdic):
    """Saves results dict to files in output values. Both dicts must have the same keys"""
    if not resultdic:
        LOG.error("Error: " + str(resultdic))
        raise Exception
    for key in outputdic:
        if not key in resultdic:
            LOG.error("No output channel detected")
            raise Exception
    for key in outputdic:
        if outputdic[key] == "stdout": #print to screen
            print(resultdic[key])
        else:
            with open(outputdic[key], 'w') as currentfile: #print to file
                currentfile.write(resultdic[key].string)    

def command_line_output(resultdic):
    """Muestra el resultado en command line"""
    print(str(resultdic) + "\n")

#FIXME: Implement Protocol 
def fetchURLs(inputdic:dict) -> dict:
    import urllib.request;
    for key in inputdic:
        f = urllib.request.urlopen(inputdic[key]);
        inputdic[key] = f.read();
        f.close()
    return inputdic
            
class CommandLineToTransformerInteraction(ContinuousInteraction):
    """Shell interaction for functions"""
    def __init__(self, gt):
        self._tinstance = gt
    
    def start(self):
        print("Input: " + ",".join(self._tinstance.inputchanneldic.keys()))
        value = self._getInput()
        while value != None:
            resultdic = self._tinstance.call(value)
            if not resultdic:
                command_line_output(str(resultdic))
            else:
                for key in resultdic.keys():
                    try:
                        resultdic[key] = str(resultdic[key])
                    except UnicodeDecodeError:
                        resultdic[key] = "Unprintable"
                command_line_output(resultdic)
            value = self._getInput()
        print("Bye Bye")
        
    def _getInput(self):
        print(promptstr)
        var = "Anything"
        while True:
            inputdic = {}
            try:
                for channel in self._tinstance.inputchanneldic.keys():
                    var = input(channel + ":\n")
                    if var == "q":
                        return None
                    inputdic[channel] = var
            except SyntaxError:
                pass
            except NameError:
                pass
            except TypeError:
                pass
            for channel in self._tinstance.inputchanneldic.keys():
                if channel not in inputdic:
                    print("Invalid python dict. Example: {\"key\":\"value1\",...}")
                    var = input(promptstr)
                continue
            return inputdic

class StreamFileToTransformerInteraction(ContinuousInteraction):
    """Write to file n times"""
    def __init__(self, gt, inputfiledic:dict, outputfiledic:dict = {}):
        self._tinstance = gt
        self._inputfiledic = inputfiledic
        self._outputfiledic = outputfiledic

    def start(self):
        inputdic = {}
        stringdic = {}
        for channel, filename in self._inputfiledic.items():
            if filename == "stdin":
                inputdic[channel] = "stdin"
                stringdic[channel] = "stdin"
            else:
                inputdic[channel] = open(filename, 'r')
                stringdic[channel] = inputdic[channel].readline()
        myand = lambda a, b: a and b
        from functools import reduce
        while reduce(myand, stringdic.values()):
            stringdiccopy = dict(stringdic)
            endofstdin = False
            for channel, content in stringdiccopy.items():
                if content == "stdin":
                    import sys
                    line = sys.stdin.readline()
                    if not line:
                        endofstdin = True 
                    else:
                        stringdic[channel] = line.rstrip('\n')
                    break
            if endofstdin:
                break #No se ha recibido nueva linea
            resultdic = self._tinstance.call(stringdic)
            self._showOutput(resultdic)
            for channel, filename in self._inputfiledic.items():
                if filename == "stdin":
                    stringdic[channel] = "stdin"
                else:
                    stringdic[channel] = inputdic[channel].readline()
                    if not stringdic[channel]:
                        break
        for key, filehandler in inputdic.items():
            if key != "input" and filehandler != "stdin":
                filehandler.close()
    
    def _showOutput(self, resultdic):
        #TODO: check if is an error. if stdout is used, use stderr
        if not resultdic:
            import sys
            sys.stderr.write(str(resultdic) + "\n" )
        elif not self._outputfiledic:
            #No output information, stdout assumed
            for key in resultdic:
                print(resultdic[key].string.strip())
        else:
            for key in self._outputfiledic:
                if not key in resultdic:
                    LOG.warning("No output channel detected")
                    raise Exception
            for key in self._outputfiledic:
                if self._outputfiledic[key] == "stdout": #print to screen
                    print(resultdic[key].string.strip())
                else:
                    with open(self._outputfiledic[key], 'a') as currentfile: #print to file
                        currentfile.write(resultdic[key].string + "\n")


class CommandLineToSchemeInteraction(ContinuousInteraction, SchemeMixin):
    """Command Line, for humans"""
    def __init__(self, sc):
        SchemeMixin.__init__(self, sc)
        import queue
        self.tmpbuffer = queue.Queue(1)

    #Threadsafe
    def receive(self, connection, element):
        self.tmpbuffer.put(element)
    
    def start(self):
        value = self._getInput()
        while value != None:
            seqid = self.inputcon.rep.save(value, "main", str(self.scheme.identifier)) #TODO: What if > 1 destination or >1 value?
            try:
                element = self.tmpbuffer.get(timeout = 3)
            except queue.Empty:
                LOG.debug("No response: memory content: "+str(self.inputcon.rep.searcher().search()))
                print("Nothing")
            else:
                try:
                    print(element.content)
                except UnicodeDecodeError:
                    print("Unprintable")
            value = self._getInput()
        print("Bye Bye")
        
    def _getInput(self):
        print(promptstr)
        var = "Anything"
        while True:
            var = input("What?:\n")
            if var == "q":
                return None
            return var
