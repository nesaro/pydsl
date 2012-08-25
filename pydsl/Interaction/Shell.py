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

"""pydsl element Interaction"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import sys
import logging
LOG = logging.getLogger(__name__)

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
        if inputstring[index] == "\\" and inputstring[index + 1] == separator:
            inputstring = inputstring[:index] + inputstring[index + 1:]
            index += 1
            continue
        elif inputstring[index] == "\\" and inputstring[index + 1] == "\\":
            inputstring = inputstring[:index] + inputstring[index + 1:]
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


def open_files_dict(inputdic) -> dict:
    """Converts a all str filename values into file objects"""
    result = {}
    for channel, filename in inputdic.items():
        with open(filename, 'rb') as f:
            result[channel] = f.read()
    return result


def save_result_to_output(resultdic, outputdic):
    """Saves results dict to files in output values.
    Both dicts must have the same keys"""
    if not resultdic:
        raise Exception("Error: " + str(resultdic))
    for key in outputdic:
        if not key in resultdic:
            raise KeyError("No output channel detected")
    for key in outputdic:
        if outputdic[key] == "stdout":  # print to screen
            print(resultdic[key])
        else:
            with open(outputdic[key], 'w') as currentfile:  # print to file
                currentfile.write(resultdic[key].string)


class CommandLineToTransformerInteraction:
    """Shell interaction for functions"""
    def __init__(self, gt):
        self._tinstance = gt

    def start(self):
        print("Input: " + ",".join(self._tinstance.inputchanneldic.keys()))
        value = self._getInput()
        while value is not None:
            resultdic = self._tinstance(value)
            if not resultdic:
                print(str(resultdic) + "\n")
            else:
                for key in resultdic.keys():
                    try:
                        resultdic[key] = str(resultdic[key])
                    except UnicodeDecodeError:
                        resultdic[key] = "Unprintable"
                print(str(resultdic) + "\n")
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
            except (SyntaxError, NameError, TypeError):
                pass
            for channel in self._tinstance.inputchanneldic.keys():
                if channel not in inputdic:
                    print('Invalid python dict. Example: {"key":"value1",...}')
                    var = input(promptstr)  # TODO use AST
                continue
            return inputdic


class StreamFileToTransformerInteraction:
    """Write to file n times"""
    def __init__(self, gt, inputfiledic: dict, outputfiledic: dict={}):
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
                    line = sys.stdin.readline()
                    if not line:
                        endofstdin = True
                    else:
                        stringdic[channel] = line.rstrip('\n')
                    break
            if endofstdin:
                break  # No new line received
            resultdic = self._tinstance(stringdic)
            self.__showOutput(resultdic)
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

    def __showOutput(self, resultdic):
        #TODO: check if is an error. if stdout is used, use stderr
        if not resultdic:
            sys.stderr.write(str(resultdic) + "\n")
        elif not self._outputfiledic:
            #No output information, stdout assumed
            for key in resultdic:
                print(resultdic[key].string.strip())
        else:
            for key in self._outputfiledic:
                if not key in resultdic:
                    raise Exception("No output channel detected")
            for key in self._outputfiledic:
                if self._outputfiledic[key] == "stdout":  # print to screen
                    print(resultdic[key].string.strip())
                else:  # print to file
                    with open(self._outputfiledic[key], 'a') as currentfile:
                        currentfile.write(resultdic[key].string + "\n")
