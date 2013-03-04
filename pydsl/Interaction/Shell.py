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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import sys
import logging
LOG = logging.getLogger(__name__)

promptstr = "Insert data (Control-d to exit)"
try: input = raw_input #Python2 workaround http://stackoverflow.com/questions/954834/how-do-i-use-raw-input-in-python-3-1
except: pass


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


def parse_shell_dict(inputstring): # -> dict:
    """Parses commandline input dicts. Example: a:b,c:d,e:f."""
    result = {}
    arglist = escapedsplitby(inputstring, ",")
    for arg in arglist:
        pair = escapedsplitby(arg, ":")
        result[pair[0]] = pair[1]
    return result


def open_files_dict(inputdic): # -> dict:
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
                currentfile.write(str(resultdic[key]))

def getInput(tinstance):
    if not sys.stdin.isatty():
        if len(tinstance.inputchanneldic) != 1:
            raise Exception("More than one channel required and no tty detected")
    else:
        print(promptstr)
    while True:
        inputdic = {}
        try:
            for channel in tinstance.inputchanneldic.keys():
                inputstr = ""
                if sys.stdin.isatty():
                    inputstr = channel + ":\n"
                var = input(inputstr)
                inputdic[channel] = var
        except (SyntaxError, NameError, TypeError):
            pass
        return inputdic

def command_line_to_transformer(tinstance, inputfunc = getInput):
    """Shell interaction for functions"""
    if sys.stdin.isatty():
        print("Input: " + ",".join(tinstance.inputchanneldic.keys()))
    value = inputfunc(tinstance)
    while value is not None:
        resultdic = tinstance(value)
        if not resultdic:
            print(str(resultdic) + "\n")
        else:
            for key in resultdic.keys():
                try:
                    resultdic[key] = str(resultdic[key])
                except UnicodeDecodeError:
                    resultdic[key] = "Unprintable"
            if len(resultdic) == 1:
                print(str(list(resultdic.values())[0]) + "\n")
            else:
                print(str(resultdic) + "\n")
        value = inputfunc(tinstance)
    print("Bye Bye")

